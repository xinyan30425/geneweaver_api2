"""Service code for interacting with the PubMed API.
这个模块包含与PubMed API交互的服务代码。

主要的入口点是 `get_publication` 函数，它接受一个PubMed ID并返回一个 `PublicationInfo` 对象。

顶级函数:
    - get_publication: 从PubMed API获取出版物信息

PubMed API函数:
    - get_xml_for_pubmed_id: 从PubMed API获取一个PubMed ID的XML

XML解析函数:
    - extract_fields: 从PubMed XML中提取初始化PublicationInfo对象所需的所有必要字段到一个字典中，这个过程结合了以下几个函数:
        - extract_top_level_fields: 从PubMed XML中提取顶级字段
        - extract_date: 从PubMed XML中提取日期字段
        - extract_authors: 从PubMed XML中提取作者字段

XML实用函数:
    - format_author_node: 格式化PubMed XML中的作者节点
    - authors_are_complete: 检查PubMed XML中的作者是否齐全

- `get_publication`: 这个函数使用PubMed ID从PubMed API获取出版物信息，并返回PublicationInfo对象。
- `get_xml_for_pubmed_id`: 此函数使用PubMed ID从PubMed API获取XML信息。
- `extract_fields`: 此函数从PubMed XML中提取字段，用于创建PublicationInfo对象。
- `extract_top_level_fields`: 从PubMed XML中提取顶级字段，如标题、摘要、期刊名称、卷号和页面。
- `extract_date`: 从PubMed XML中提取出版日期，包括年、月、日。
- `extract_authors`: 从PubMed XML中提取作者信息，并检查作者列表是否完整。
- `format_author_node`: 将PubMed XML中的作者节点格式化为字符串。
- `authors_are_complete`: 检查PubMed XML中的作者列表是否标记为完整，以确定是否所有作者都已列出。

这些功能在GeneWeaver程序中用于处理和分析从PubMed数据库获取的科研出版物信息。例如，`get_publication` 可以用来获取特定论文的详细信息，`extract_fields`、`extract_date` 和 `extract_authors` 等函数用于从PubMed提供的XML数据中提取有用的出版物信息，以便在GeneWeaver程序中使用。


The main entrypoint is the `get_publication` function, which takes a PubMed ID
and returns a `PublicationInfo` object.

Top-level functions:
    get_publication: Get publication info from PubMed API

PubMed API Function:
    get_xml_for_pubmed_id: Get XML for a PubMed ID from the PubMed API

XML Parsing Functions:
    extract_fields: Extract all the required fields from PubMed XML needed to initialize
    a PublicationInfo object into a dictionary, combination of the following functions:
        - extract_top_level_fields: Extract top-level fields from PubMed XML
        - extract_date: Extract date field from PubMed XML
        - extract_authors: Extract authors field from PubMed XML

XML Utility Functions:
    format_author_node: Format an author node from PubMed XML
    authors_are_complete: Check if authors are complete according PubMed XML
"""
from xml.etree import ElementTree

import requests
from geneweaver.core.config import settings
from geneweaver.core.exc import ExternalAPIError
from geneweaver.core.schema.publication import PublicationInfo
from geneweaver.core.utils import add_to_dict_if_not_none

PUBMED_SVC_URL = settings.SERVICE_URLS.PUBMED_XLM_SVC_URL


def get_publication(pubmed_id: str) -> PublicationInfo:
    """Get publication info from PubMed API.

    :param pubmed_id: The PubMed ID

    :returns: The publication info
    """
    publication_xml = get_xml_for_pubmed_id(pubmed_id)

    publication_fields = extract_fields(publication_xml)

    return PublicationInfo(**publication_fields)


def get_xml_for_pubmed_id(pubmed_id: str) -> ElementTree.XML:
    """Get XML for a PubMed ID from the PubMed API.

    :param pubmed_id: The PubMed ID

    :returns: The XML for the PubMed ID
    """
    response = requests.get(PUBMED_SVC_URL.format(pubmed_id))

    if not response.ok:
        raise ExternalAPIError(
            f"Error retrieving publication info from PubMed API: {response.status_code}"
        )

    return ElementTree.fromstring(response.text.encode("utf-8"))


def extract_fields(publication_xml: ElementTree.XML) -> dict:
    """Extract publication fields from XML.

    :param publication_xml: The XML to extract fields from

    :returns: The extracted fields
    """
    publication_fields = extract_top_level_fields(publication_xml)

    publication_fields.update(extract_date(publication_xml))

    publication_fields.update(extract_authors(publication_xml))

    return publication_fields


TOP_LEVEL_XML_FIELD_MAPS = {
    "title": ".//ArticleTitle",
    "abstract": ".//AbstractText",
    "journal": ".//Journal/Title",
    "volume": ".//Volume",
    "pages": ".//MedlinePgn",
}


def extract_top_level_fields(publication_xml: ElementTree.XML) -> dict:
    """Extract publication top level fields from XML.

    :param publication_xml: The XML to extract top level fields from

    :returns: The extracted top level fields
    """
    publication_fields = dict()

    for field, xpath in TOP_LEVEL_XML_FIELD_MAPS.items():
        value = publication_xml.findtext(xpath)
        add_to_dict_if_not_none(publication_fields, field, value)

    return publication_fields


def extract_date(publication_xml: ElementTree.XML) -> dict:
    """Extract publication date from XML.

    :param publication_xml: The XML to extract the date from

    :returns: The extracted date
    """
    publication_date = dict()

    pub_date_node = publication_xml.find(".//PubDate")

    if pub_date_node is not None:
        pub_date = pub_date_node.findtext("Year")
        add_to_dict_if_not_none(publication_date, "year", pub_date)

        pub_date = pub_date_node.findtext("Month")
        add_to_dict_if_not_none(publication_date, "month", pub_date)

        pub_date = pub_date_node.findtext("Day")
        add_to_dict_if_not_none(publication_date, "day", pub_date)

    return publication_date


def format_author_node(author_node: ElementTree.XML) -> str:
    """Format author node to string.

    :param author_node: The author node to format

    :returns: The formatted author node as a string.
    """
    name_parts = []

    fore_name = author_node.findtext("ForeName")

    if fore_name:
        name_parts.append(fore_name)
    else:
        initials = author_node.findtext("Initials")

        if initials:
            name_parts.append(initials)

    last_name = author_node.findtext("LastName")

    if last_name:
        name_parts.append(last_name)

    return " ".join(name_parts)


def extract_authors(publication_xml: ElementTree.XML) -> dict:
    """Extract publication authors from XML.

    :param publication_xml: The XML to extract authors from

    :returns: The extracted authors
    """
    publication_authors = dict()

    author_list_node = publication_xml.find(".//AuthorList")

    if author_list_node:
        author_nodes = author_list_node.findall(".//Author")
        authors = [format_author_node(author_node) for author_node in author_nodes]

        if not authors_are_complete(author_list_node):
            authors.append("et al.")

        add_to_dict_if_not_none(publication_authors, "authors", authors)

    return publication_authors


def authors_are_complete(author_list_node: ElementTree.XML) -> bool:
    """Check if authors are complete.

    Authors are considered completed unless the CompleteYN attribute is present and set
    to 'N'.

    :param author_list_node: The author list node to check

    :returns: Whether the authors are complete
    """
    complete = True

    try:
        # If the CompleteYN attribute is present and set to 'N', the author list is not
        # complete. Documentation recommends taking action when this is the case, but
        # does not specify taking action in any other case.
        # https://www.nlm.nih.gov/bsd/licensee/elements_descriptions.html
        if author_list_node.attrib["CompleteYN"] == "N":
            complete = False
    except KeyError:
        pass

    return complete
