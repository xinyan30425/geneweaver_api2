"""
Python Package main config file.
这是GeneWeaver程序的Python包主配置文件。

- ExternalServiceSettings：这是外部服务配置和设置的类。它定义了GeneWeaver程序可能会使用到的外部服务的URL。比如：
  - PUBMED_XLM_SVC_URL：这是PubMed API的URL模板，用于获取PubMed数据库中指定ID的XML数据。

- CoreSettings：这是核心配置和设置的类。它定义了项目的一些基本信息以及如何读取这些配置信息。例如：
  - PROJECT_NAME：项目的名称，这里是 "jax-geneweaver-core"。
  - VERSION：项目的版本号，当前是 "0.0.2"。
  - LOG_LEVEL：日志级别，默认是 "INFO"。
  - SERVICE_URLS：一个ExternalServiceSettings实例，用于存储所有外部服务的URL配置。

- Config：这是一个内部类，用于pydantic库的配置。这里定义了环境变量前缀 "GW_"，这意味着所有使用这个前缀的环境变量都会被自动识别并用于设置CoreSettings的属性值。

在GeneWeaver系统中，这些配置文件用于设置和调整项目的基本信息，日志级别，以及外部服务链接。例如，当系统需要从PubMed数据库获取文献信息时，它会使用PUBMED_XLM_SVC_URL配置的URL来发送请求并接收数据。


For more options refer to pydantic base-settings docs:
https://pydantic-docs.helpmanual.io/usage/settings/
"""
from pydantic import BaseSettings


class ExternalServiceSettings(BaseSettings):
    """External Service Config and Settings Configuration."""

    PUBMED_XLM_SVC_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={0}&retmode=xml"


class CoreSettings(BaseSettings):
    """Root Config and Settings Configuration."""

    PROJECT_NAME = "jax-geneweaver-core"
    VERSION = "0.0.2"
    LOG_LEVEL: str = "INFO"
    SERVICE_URLS: ExternalServiceSettings = ExternalServiceSettings()

    class Config:
        """Pydantic Config class."""

        env_prefix = "GW_"
