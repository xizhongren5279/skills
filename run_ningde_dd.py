#!/usr/bin/env python3
"""
宁德时代尽职调查脚本 - 直接调用 API
"""
import asyncio
import json
import os
import aiohttp
from datetime import datetime, timedelta


def get_time_range(time_range_enum):
    """获取时间范围"""
    now = datetime.now()
    if time_range_enum == "all":
        start_time = now - timedelta(days=365 * 5)
    elif time_range_enum == "past_day":
        start_time = now - timedelta(days=1)
    elif time_range_enum == "past_week":
        start_time = now - timedelta(weeks=1)
    elif time_range_enum == "past_month":
        start_time = now - timedelta(days=30)
    elif time_range_enum == "past_quarter":
        start_time = now - timedelta(days=90)
    elif time_range_enum == "past_half_year":
        start_time = now - timedelta(days=180)
    elif time_range_enum == "past_year":
        start_time = now - timedelta(days=365)
    else:
        raise ValueError("Invalid time range enum")
    end_time = now
    return start_time.strftime("%Y-%m-%d"), end_time.strftime("%Y-%m-%d")


async def search_finance_db(query, date_range="past_half_year", recall_num=20, doc_type=None):
    """
    搜索金融数据库
    """
    DR_SEARCH_API_KEY = os.getenv("DR_SEARCH_API_KEY", "Shangjian@123")
    DR_SEARCH_BASE_URL_SEARCH = os.getenv(
        "DR_SEARCH_BASE_URL_SEARCH",
        "http://172.28.24.85:30648/api/fin/search_sync_for_agent",
    )

    # 处理时间范围
    start_time, end_time = get_time_range(date_range)
    time_filter = {
        "default": date_range == "all",
        "value": {"end_date": end_time, "start_date": start_time},
    }

    # 处理文档类型
    if doc_type:
        doc_types = []
        if isinstance(doc_type, str):
            doc_types = [doc_type]
        elif isinstance(doc_type, list):
            doc_types = doc_type

        if "all" in doc_types or (isinstance(doc_type, str) and doc_type == "all"):
            doc_type_filter = {"default": False, "value": []}
        else:
            doc_type_values = []
            for dt in doc_types:
                if dt == "summary":
                    doc_type_values.extend([
                        {"document_type": "summary_sse"},
                        {"document_type": "summary_sse_finance"},
                        {"document_type": "foreign_announcement"},
                    ])
                elif dt == "report":
                    doc_type_values.extend([
                        {"document_type": "report"},
                        {"document_type": "foreign_report"},
                    ])
                elif dt in ["company_all_announcement", "comments", "news"]:
                    doc_type_values.append({"document_type": dt})

            doc_type_filter = {"default": False, "value": doc_type_values}
    else:
        doc_type_filter = {"default": True, "value": []}

    guess_custom_filter = {
        "company": {"default": True, "value": []},
        "document_type": doc_type_filter,
        "institution": {"default": True, "value": []},
        "time": time_filter,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{DR_SEARCH_BASE_URL_SEARCH}",
            json={
                "question": query,
                "recall_num": recall_num,
                "custom_filter": guess_custom_filter,
                "es_filter": None,
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
        doc_section = sections[0]
        section_document = doc_section.get("section_document", None)
        if section_document:
            section = section_document.get("text", "")
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

    return ret


async def run_due_diligence():
    """执行宁德时代的尽职调查"""

    print("=" * 80)
    print("宁德时代尽职调查报告")
    print("=" * 80)
    print()

    # 1. 搜索公司基本信息
    print("阶段 1: 获取公司基本信息和最新研报...")
    print("-" * 80)

    query1 = "宁德时代 公司概况 主营业务"
    try:
        result1 = await search_finance_db(
            query=query1,
            date_range="past_year",
            recall_num=10,
            doc_type=["report", "company_all_announcement"]
        )

        print(f"\n检索查询: {query1}")
        print(f"找到 {len(result1)} 条相关信息:\n")
        for i, doc in enumerate(result1[:5], 1):
            print(f"{i}. {doc['title']}")
            print(f"   发布日期: {doc['publish_date']}")
            print(f"   类型: {doc['type_full_name']}")
            print(f"   机构: {doc['institution_name']}")
            print(f"   摘要: {doc['section'][:200]}...")
            print()
    except Exception as e:
        print(f"错误: {e}")
        result1 = []

    # 2. 获取财务数据
    print("\n阶段 2: 获取财务数据和业绩分析...")
    print("-" * 80)

    query2 = "宁德时代 2023年 2024年 财务数据 营收 利润 资产负债"
    try:
        result2 = await search_finance_db(
            query=query2,
            date_range="past_year",
            recall_num=15,
            doc_type=["report", "company_all_announcement"]
        )

        print(f"\n检索查询: {query2}")
        print(f"找到 {len(result2)} 条相关信息:\n")
        for i, doc in enumerate(result2[:5], 1):
            print(f"{i}. {doc['title']}")
            print(f"   发布日期: {doc['publish_date']}")
            print(f"   类型: {doc['type_full_name']}")
            print(f"   机构: {doc['institution_name']}")
            print(f"   摘要: {doc['section'][:200]}...")
            print()
    except Exception as e:
        print(f"错误: {e}")
        result2 = []

    # 3. 获取市场和竞争分析
    print("\n阶段 3: 获取市场和竞争分析...")
    print("-" * 80)

    query3 = "宁德时代 市场地位 竞争格局 动力电池 市场份额"
    try:
        result3 = await search_finance_db(
            query=query3,
            date_range="past_half_year",
            recall_num=10,
            doc_type=["report", "comments"]
        )

        print(f"\n检索查询: {query3}")
        print(f"找到 {len(result3)} 条相关信息:\n")
        for i, doc in enumerate(result3[:5], 1):
            print(f"{i}. {doc['title']}")
            print(f"   发布日期: {doc['publish_date']}")
            print(f"   类型: {doc['type_full_name']}")
            print(f"   机构: {doc['institution_name']}")
            print(f"   摘要: {doc['section'][:200]}...")
            print()
    except Exception as e:
        print(f"错误: {e}")
        result3 = []

    # 4. 获取技术和研发信息
    print("\n阶段 4: 获取技术和研发信息...")
    print("-" * 80)

    query4 = "宁德时代 技术研发 专利 电池技术 创新"
    try:
        result4 = await search_finance_db(
            query=query4,
            date_range="past_half_year",
            recall_num=10,
            doc_type=["report", "news"]
        )

        print(f"\n检索查询: {query4}")
        print(f"找到 {len(result4)} 条相关信息:\n")
        for i, doc in enumerate(result4[:5], 1):
            print(f"{i}. {doc['title']}")
            print(f"   发布日期: {doc['publish_date']}")
            print(f"   类型: {doc['type_full_name']}")
            print(f"   机构: {doc['institution_name']}")
            print(f"   摘要: {doc['section'][:200]}...")
            print()
    except Exception as e:
        print(f"错误: {e}")
        result4 = []

    # 5. 获取风险因素
    print("\n阶段 5: 获取风险因素和合规信息...")
    print("-" * 80)

    query5 = "宁德时代 风险 诉讼 监管 合规"
    try:
        result5 = await search_finance_db(
            query=query5,
            date_range="past_year",
            recall_num=10,
            doc_type=["company_all_announcement", "comments"]
        )

        print(f"\n检索查询: {query5}")
        print(f"找到 {len(result5)} 条相关信息:\n")
        for i, doc in enumerate(result5[:5], 1):
            print(f"{i}. {doc['title']}")
            print(f"   发布日期: {doc['publish_date']}")
            print(f"   类型: {doc['type_full_name']}")
            print(f"   机构: {doc['institution_name']}")
            print(f"   摘要: {doc['section'][:200]}...")
            print()
    except Exception as e:
        print(f"错误: {e}")
        result5 = []

    # 保存完整结果到文件
    print("\n" + "=" * 80)
    print("保存完整结果到文件...")

    all_results = {
        "company": "宁德时代",
        "date": "2026-01-20",
        "sections": {
            "company_info": result1,
            "financial_data": result2,
            "market_analysis": result3,
            "technology_rd": result4,
            "risk_compliance": result5
        }
    }

    output_file = "/Users/xizhongren/Downloads/skills/宁德时代尽调数据.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"✓ 完整数据已保存到: {output_file}")
    print("\n" + "=" * 80)
    print("尽职调查数据收集完成！")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(run_due_diligence())
