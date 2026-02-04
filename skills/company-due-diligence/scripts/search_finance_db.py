import asyncio
import json
import os
import re
from datetime import datetime, timedelta
from time import time
from typing import Annotated, List, Literal, Optional, TypedDict, Union

import aiohttp
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState
from loguru import logger



class FileIdProvider:
    """Provider for generating unique file IDs."""

    def __init__(self, start_id: int = 1):
        self._current_id = start_id

    def next_id(self) -> int:
        """Get the next available file ID."""
        current = self._current_id
        self._current_id += 1
        return current


class SearchFile(TypedDict):
    file_id: int
    file_type: str
    file_original_id: str
    file_format_name: str
    file_title: str
    file_ext: str
    
class SearchFileType:
    FINANCEDB = "finance"
    STOCKDB = "stock"
    USERDB = "box"
    WEB = "web"

    @classmethod
    def choices(cls):
        """Return a list of available SearchFILE types."""
        return [cls.FINANCEDB, cls.STOCKDB, cls.USERDB, cls.WEB]
class SearchFilesBuilder:
    def __init__(
        self,
        file_id: int,
        file_type: str,
        file_original_id: str = "",
        file_title: str = "",
        file_ext: str = "",
    ):
        self.file_id = file_id
        self.file_type = file_type
        self.file_original_id = file_original_id
        self.file_title = file_title
        self.file_ext = file_ext

    def _generate_file_format_name(self):
        """Dynamically generated according to type"""
        # if self.file_type==SearchFileType.FINANCEDB:
        #     return "finance"
        return f"[doc{self.file_id}]"

    def build(self) -> SearchFile:
        return SearchFile(
            file_id=self.file_id,
            file_type=self.file_type,
            file_original_id=self.file_original_id,
            file_format_name=self._generate_file_format_name(),
            file_ext=self.file_ext,
            file_title=self.file_title,
        )


class InfoSearchFiles(TypedDict):
    files_count: Optional[int]
    search_files: Optional[list[SearchFile]]


class InfoSearchFilesBuilder:
    @classmethod
    def add_search_file(
        cls,
        info: InfoSearchFiles,
        search_file: SearchFile,
        file_id_provider: FileIdProvider = None,
    ) -> InfoSearchFiles:
        search_files = info.get("search_files", [])
        files_count = info.get("files_count", len(search_files))
        search_file_original_id = search_file.get("file_original_id", "")
        # 判断是否已存在相同 file_original_id
        for existing in search_files:
            existing_original_id = existing.get("file_original_id", "")
            if existing_original_id == search_file_original_id:
                return info

        # 不存在则新增
        file_id = file_id_provider.next_id() if file_id_provider else files_count + 1
        new_file = SearchFilesBuilder(
            file_id=file_id,
            file_type=search_file.get("file_type", "unknown"),
            file_original_id=search_file_original_id,
            file_ext=search_file.get("file_ext", "unknown"),
            file_title=search_file.get("file_title", "unknown"),
        ).build()

        search_files.append(new_file)
        info["search_files"] = search_files
        info["files_count"] = files_count + 1
        return info

    @classmethod
    def search_format_name_from_original_id(
        self, info: InfoSearchFiles, file_original_id: str
    ) -> str:

        for file in info.get("search_files", []):
            if file.get("file_original_id", "") == file_original_id:
                return file.get("file_format_name", "")
        return ""

    @classmethod
    def search_file_id_from_original_id(
        self, info: InfoSearchFiles, file_original_id: int
    ) -> int:
        for file in info.get("search_files", []):
            if file.get("file_original_id", "") == file_original_id:
                return file.get("file_id", None)
        return 0

    @classmethod
    def search_original_id_from_file_id(
        self, info: InfoSearchFiles, file_id: int
    ) -> int:
        for file in info.get("search_files", []):
            if file.get("file_id", None) == file_id:
                return file.get("file_original_id", "")
        return 0

    @classmethod
    def search_format_name_from_file_id(
        self, info: InfoSearchFiles, file_id: int
    ) -> str:
        for file in info.get("search_files", []):
            if file.get("file_id", None) == file_id:
                return file.get("file_format_name", "")
        return ""

    @classmethod
    def remove_all_reference_id_from_content(cls, content):
        reg = r"\[doc\d+\]"
        # Use re.sub() to replace all occurrences of the pattern with empty string
        return re.sub(reg, "", content)

    @classmethod
    def search_file_title_from_file_id(self, info: InfoSearchFiles, file_id: int):
        for file in info.get("search_files", []):
            if file.get("file_id", None) == file_id:
                return file.get("file_title", "")
        return ""

    @classmethod
    def search_file_from_file_id(self, info: InfoSearchFiles, file_id: int):
        for file in info.get("search_files", []):
            if file.get("file_id", None) == file_id:
                return file
        return None

def get_time_range(time_range_enum):
    now = datetime.now()
    if time_range_enum == "all":
        # 返回一个极早的时间作为起始时间
        start_time = now - timedelta(days=365 * 5)
    elif time_range_enum == "past_day":
        start_time = now - timedelta(days=1)
    elif time_range_enum == "past_week":
        start_time = now - timedelta(weeks=1)
    elif time_range_enum == "past_month":
        start_time = now - timedelta(days=30)  # 近似一个月
    elif time_range_enum == "past_quarter":
        start_time = now - timedelta(days=90)  # 一个季度约90天
    elif time_range_enum == "past_half_year":
        start_time = now - timedelta(days=180)  # 半年约180天
    elif time_range_enum == "past_year":
        start_time = now - timedelta(days=365)  # 近似一年
    else:
        raise ValueError("Invalid time range enum")
    end_time = now
    return start_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d")


@tool
async def info_search_finance_db(
    query: Annotated[
        str,
        "Ask questions in natural language with clear semantics. If the user's question contains specific time information such as the year, the generated query should also have specific time information. Only in this way can the retrieved data meet the user's needs",
    ],
    date_range: Annotated[
        Optional[
            Literal[
                "all",
                "past_week",
                "past_day",
                "past_month",
                "past_year",
                "past_quarter",
                "past_half_year",
            ]
        ],
        "(Optional) Time range filter for search results. Use all if the time range is more than 1 year.",
    ] = None,
    recall_num: Annotated[
        Optional[int], "(Optional) Number of search results to return."
    ] = 20,
    doc_type: Annotated[
        Optional[
            Union[
                List[
                    Literal[
                        "report",
                        "summary",
                        "company_all_announcement",
                        "comments",
                        "news",
                    ]
                ],
                Literal["all", "report"],
            ]
        ],
        "(Optional) Select the type of content you are looking for based on the task requirements. Supports single type or multiple types as a list. all:综合,report:研报,summary:会议纪要, company_all_announcement: 年报及公司公告,comments: 点评, news: 资讯",
    ] = None,
    state: Annotated[dict, InjectedState] = None,
):
    """
    Search finance_db. Use for obtaining latest information or finding references.Article information and content fragments with relevant information are returned
    参数说明：
    对你不熟悉的信息，检索时`date_range`参数设置为`all`且`doc_type`参数设置为`all`
    - `date_range`参数：
        默认的参数值设置为`past_half`
        关于公司财报时间：最新财报对应的时间是`past_quarter`，最近两个财报对应的时间是`past_half`
    - `doc_type`参数：
        可选: all（研报+会议纪要+公告+点评+资讯）、report（研报）、summary（会议纪要）、company_all_announcement（公告）、comments（点评）、news（资讯）
        支持单个类型或多个类型的组合，如：'report' 或 ['report', 'summary']。尽量选择`report`,`summary`,`company_all_announcement`,`comments`,`news`中的2个或多个（每一次都必须是`report`和其他的组合），完全无法确定要检索哪几个资料类型时最后才考虑用`all`。查找你不熟悉的信息，要把资料类型参数设置为`all`。
            研报（这是每次检索时最核心的资料类型）：权威金融机构发布的策略研究、晨会资讯、公司研究、行业研究、宏观经济、基金研究、债券研究、金融工程、期货研究；研报包括中国国内研报和海外投行研报。
            会议纪要：业绩会、公司交流、专家交流、分析师纪要、买方纪要
            公告：涵盖财务经营报告、首次发行（IPO）、公司债 / 可转债等融资与股本类事项，以及一般公告、重大事项、交易提示、增发 / 配股事项、基金公告等信息披露与资本操作类内容。
            点评：券商投行发布的最新观点或评论。
            资讯：第三方咨询机构提供的几百字简讯。
    - `query`参数：
        不要同时出现多个公司主体，多实体对比的问题应该要拆分成多次查询。
            正确示例：微软 资本开支 2023-2026年。正确原因是：一个公司主体。
            错误示例：全球AI巨头资本开支 微软 谷歌 Meta 亚马逊 2023-2026年。错误原因是：多个公司主体同时出现。
            正确示例: 格力电器 2024年报。正确原因是：一个公司主体。
            错误示例：格力电器 海尔智家 24年年报。错误原因是：多个公司主体同时出现。
    """
    DR_SEARCH_API_KEY = os.getenv("DR_SEARCH_API_KEY", "Shangjian@123")
    DR_SEARCH_BASE_URL_SEARCH = os.getenv(
    "DR_SEARCH_BASE_URL_SEARCH",
    "http://172.28.24.85:30648/api/fin/search_sync_for_agent",
)
    start_time = None
    end_time = None
    enum = [
        "past_week",
        "past_day",
        "past_month",
        "past_year",
        "past_quarter",
        "past_half_year",
    ]
    if date_range and date_range in enum:
        start_time, end_time = get_time_range(date_range)
        time_filter = {
            "default": False,
            "value": {"end_date": end_time, "start_date": start_time},
        }
    else:
        date_range = "all"
        start_time, end_time = get_time_range(date_range)
        time_filter = {
            "default": True,
            "value": {"end_date": end_time, "start_date": start_time},
        }
    if doc_type:
        enum = [
            "all",
            "report",
            "summary",
            "company_all_announcement",
            "comments",
            "news",
        ]

        # 处理单个类型或类型列表
        doc_types = []
        if isinstance(doc_type, str):
            doc_types = [doc_type]
        elif isinstance(doc_type, list):
            doc_types = doc_type
        else:
            doc_types = []

        if "all" in doc_types or (isinstance(doc_type, str) and doc_type == "all"):
            doc_type = {"default": False, "value": []}
        else:
            doc_type_values = []
            for dt in doc_types:
                if dt == "summary":
                    doc_type_values.extend(
                        [
                            {"document_type": "summary_sse"},
                            {"document_type": "summary_sse_finance"},
                            {"document_type": "foreign_announcement"},
                        ]
                    )
                elif dt == "report":
                    doc_type_values.extend(
                        [
                            {"document_type": "report"},
                            {"document_type": "foreign_report"},
                        ]
                    )
                elif dt in ["company_all_announcement", "comments", "news"]:
                    doc_type_values.append({"document_type": dt})

            doc_type = {"default": False, "value": doc_type_values}
    else:
        doc_type = {"default": True, "value": []}
    guess_custom_filter = {
        "company": {"default": True, "value": []},
        "document_type": doc_type,
        "institution": {"default": True, "value": []},
        "time": time_filter,
    }
    flag = True
    if state is None or "custom_filter" not in state or not state.get("custom_filter"):
        flag = False
    if flag:
        custom_filter = state.get("custom_filter", {})
        for k, v in custom_filter.items():
            if v.get("default"):
                continue
            else:
                guess_custom_filter[k] = v

    custom_input_es_filter = state.get("es_filter", None)
    es_filter_must_part = []
    if custom_input_es_filter:
        es_filter_must_part.append(custom_input_es_filter)

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{DR_SEARCH_BASE_URL_SEARCH}",
            json={
                "question": query,
                "recall_num": recall_num,
                "custom_filter": guess_custom_filter,
                "es_filter": (
                    None
                    if not es_filter_must_part
                    else {"bool": {"must": es_filter_must_part}}
                ),
                # {"bool": {"must": [es_filter, doc_type_filter]}}
            },
            headers={
                "Content-Type": "application/json",
                "X-API-Key": DR_SEARCH_API_KEY,
            },
        ) as res:
            res.raise_for_status()
            response_data = await res.json()

    ret = []
    for i in response_data:
        sections = i["sections"]
        sections = sorted(sections, key=lambda d: d["reranker_score"], reverse=True)
        section = ""
        doc_section = sections[0]
        section_document = doc_section.get("section_document", None)
        if section_document:
            section = section_document.get("text", "")
            # 发布时间、资料类型、发布机构、关联公司、内容片段
            doc_map = {
                "title": i["title"],
                "file_id": i["file_id"],
                "publish_date": i["publish_date"],
                "type_full_name": i["type_full_name"],
                "institution_name": i["institution_name"],
                "company_name": i["company_name"],
                "file_ext": i["file_format"],
                "section": section,
            }

            ret.append(doc_map)
    info_search_files = state.get("info_search_files", {})
    for i in range(len(ret)):
        file = SearchFile(
            file_original_id=ret[i]["file_id"],
            file_type=SearchFileType.FINANCEDB,
            file_title=ret[i]["title"],
            file_ext=ret[i]["file_ext"],
        )
        info_search_files = InfoSearchFilesBuilder.add_search_file(
            info_search_files, file
        )
        file_id = InfoSearchFilesBuilder.search_file_id_from_original_id(
            info_search_files, ret[i]["file_id"]
        )
        ret[i]["file_id"] = file_id
        ret[i].pop("file_ext")
    fs = state.get("fs", {})
    punctuation = (
        r'!"#$%&\'()*+,-./:;<=>?@[\$$^_`{|}~，。、；：？！（）《》【】“”‘’…—－'
    )
    for char in punctuation:
        query = query.replace(char, "")
    fs[f"/finance_db_summary/{query}.json"] = json.dumps(ret, ensure_ascii=False)
    return ret, {"tracking": info_search_files, "fs": fs}