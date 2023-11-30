"""
Test that the Eutils API rate limits don't break our usage.
这段代码是用来测试GeneWeaver项目中的Eutils API的调用频率限制是否会影响到我们的使用。这是一段集成测试代码，通常用于确保外部服务的交互在实际应用中不会出现问题。

- 首先，这段代码使用了 `pytest` 测试框架，这是一个广泛使用的Python测试库，能够让开发者编写简洁明了的测试代码。

- `N_RATE_TEST_ARGS` 是一个包含多个元组的列表，每个元组表示测试用例，其中包含调用次数（`num_times`）和速率（`rate`），用来测试不同的频率限制条件下API的响应。

- `test_rate_for_eutils_publication_endpoint` 函数是一个测试函数，它检查调用PubMed API的特定URL是否会因为超出调用频率限制而失败。它使用 `requests.get` 方法来发送HTTP请求，并断言响应是成功的。

- `test_rate_for_get_xml_for_pubmed_id` 函数测试 `get_xml_for_pubmed_id` 函数，该函数是项目中用于获取PubMed ID对应的XML数据的函数。测试确保即使在不同的调用频率下，这个函数也能够正常工作并返回非空的结果。

- `@pytest.mark.parametrize` 是pytest的一个功能，它允许开发者定义参数化测试，即对一系列参数运行相同的测试代码，检查不同条件下的函数行为。

总体而言，这段测试代码的目的是确保GeneWeaver系统能够在Eutils API的频率限制下正常运行，即使在高频率调用的情况下也不会因为超过限制而导致服务中断。这对于维护系统的稳定性和用户体验至关重要。
"""
import pytest
import requests
from geneweaver.core.publication.pubmed import PUBMED_SVC_URL, get_xml_for_pubmed_id

from tests.integration.const import PUBMED_IDS
from tests.integration.utils import call_function

N_RATE_TEST_ARGS = [
    (1, 1),
    (2, 1),
    (3, 1),
    (5, 1),
    (5, 3),
    (8, 3),
    (13, 3),
    (5, 5),
    (8, 10),
    (13, 10),
    (21, 10),
    (20, 20),
]


@pytest.mark.parametrize(("num_times", "rate"), N_RATE_TEST_ARGS)
def test_rate_for_eutils_publication_endpoint(num_times, rate):
    """Test rate for eutils API endpoint used by get_xml_for_pubmed_id."""
    urls = [PUBMED_SVC_URL.format(pubmed_id) for pubmed_id in PUBMED_IDS]
    results = call_function(requests.get, num_times, rate, iterate_args=urls)
    for response in results:
        assert response.ok, response.text


@pytest.mark.parametrize(("num_times", "rate"), N_RATE_TEST_ARGS)
def test_rate_for_get_xml_for_pubmed_id(num_times, rate):
    """Test rate for get_xml_for_pubmed_id."""
    results = call_function(
        get_xml_for_pubmed_id, num_times, rate, iterate_args=PUBMED_IDS
    )
    for response in results:
        assert response is not None, response
