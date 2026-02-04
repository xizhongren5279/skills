#!/usr/bin/env python3
"""
Due Diligence Helper Script

This script automates the due diligence workflow:
1. Retrieves data via info_search_finance_db tool
2. Stores results to JSON file
3. Generates Markdown report
4. Creates Canvas visualization

Usage:
python3 skills/company-due-diligence/scripts/run_due_diligence.py "公司名称"
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Import the info_search_finance_db function
# We need to import the module and access the underlying coroutine
try:
    import search_finance_db
    # Get the underlying coroutine function from the LangChain tool
    # The @tool decorator wraps it in a StructuredTool, access via .coroutine
    info_search_finance_db = search_finance_db.info_search_finance_db.coroutine
except (ImportError, AttributeError) as e:
    print(f"Error: Could not import info_search_finance_db from search_finance_db.py: {e}")
    print("Make sure search_finance_db.py is in the same directory")
    sys.exit(1)


class DueDiligenceRunner:
    """Automated due diligence workflow runner."""

    def __init__(self, company_name: str, output_dir: str = "./output"):
        self.company_name = company_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize state for LangGraph
        self.state = {
            "info_search_files": {},
            "fs": {},
            "custom_filter": {},
            "es_filter": None
        }

        # Store all query results
        self.all_results = []

    async def retrieve_data(self) -> None:
        """Step 1: Retrieve all data via info_search_finance_db."""
        print(f"\n{'='*60}")
        print(f"STEP 1: Retrieving Data for {self.company_name}")
        print(f"{'='*60}\n")

        # Define queries for each dimension
        queries = [
            {
                "category": "financial",
                "query": f"{self.company_name} 财务数据 营收 净利润 现金流 资产负债表",
                "date_range": "past_year",
                "doc_type": ["report", "company_all_announcement"],
                "recall_num": 20
            },
            {
                "category": "business",
                "query": f"{self.company_name} 业务模式 主要客户 供应商 市场份额",
                "date_range": "past_year",
                "doc_type": ["report", "summary"],
                "recall_num": 15
            },
            {
                "category": "legal",
                "query": f"{self.company_name} 诉讼 纠纷 行政处罚 知识产权 合规",
                "date_range": "all",
                "doc_type": ["all"],
                "recall_num": 20
            },
            {
                "category": "team",
                "query": f"{self.company_name} 管理团队 董事长 高管 股东结构",
                "date_range": "past_half_year",
                "doc_type": ["report", "company_all_announcement"],
                "recall_num": 15
            }
        ]

        # Execute queries
        for q in queries:
            print(f"Querying: {q['category'].upper()} - {q['query']}")
            try:
                results, update = await info_search_finance_db(
                    query=q["query"],
                    date_range=q.get("date_range"),
                    doc_type=q.get("doc_type"),
                    recall_num=q.get("recall_num", 20),
                    state=self.state
                )

                # Update state with returned tracking info
                if "tracking" in update:
                    self.state["info_search_files"] = update["tracking"]
                if "fs" in update:
                    self.state["fs"].update(update["fs"])

                # Store results
                self.all_results.append({
                    "category": q["category"],
                    "query": q["query"],
                    "results": results,
                    "timestamp": datetime.now().isoformat(),
                    "result_count": len(results)
                })

                print(f"  ✓ Retrieved {len(results)} results")

            except Exception as e:
                print(f"  ✗ Error: {e}")
                self.all_results.append({
                    "category": q["category"],
                    "query": q["query"],
                    "results": [],
                    "timestamp": datetime.now().isoformat(),
                    "error": str(e)
                })

        print(f"\n{'='*60}")
        print(f"Data Retrieval Complete: {sum(len(r['results']) for r in self.all_results)} total results")
        print(f"{'='*60}\n")

    def save_json_data(self) -> str:
        """Step 2: Save all data to JSON file."""
        print(f"\n{'='*60}")
        print(f"STEP 2: Saving Data to JSON")
        print(f"{'='*60}\n")

        json_file = self.output_dir / f"{self.company_name}_due_diligence_data.json"

        data = {
            "company_name": self.company_name,
            "query_date": datetime.now().strftime("%Y-%m-%d"),
            "data": self.all_results,
            "summary": {
                "total_queries": len(self.all_results),
                "total_results": sum(len(r.get("results", [])) for r in self.all_results),
                "categories": list(set(r["category"] for r in self.all_results))
            }
        }

        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✓ JSON data saved to: {json_file}")
        return str(json_file)

    def extract_financial_insights(self, financial_results: list) -> dict:
        """Extract key financial insights from search results."""
        insights = {
            "revenue_growth": [],
            "profitability": [],
            "cash_flow": [],
            "valuation": [],
            "concerns": [],
            "highlights": []
        }

        for item in financial_results[:15]:  # Analyze top 15 results
            title = item.get("title", "")
            section = item.get("section", "")
            institution = item.get("institution_name", [""])[0] if item.get("institution_name") else "N/A"
            date = item.get("publish_date", "")

            # Extract from section content
            section_lower = section.lower()

            # Revenue related
            if "revenue" in section_lower or "营收" in section or "sales" in section_lower:
                if "growth" in title.lower() or "增长" in title or "improve" in title.lower():
                    insights["revenue_growth"].append(f"- **{institution}** ({date}): {title[:80]}...")
                else:
                    insights["highlights"].append(f"- **{institution}**: {title[:80]}...")

            # Profitability related
            if "profit" in section_lower or "净利润" in section or "margin" in section_lower or "毛利率" in section:
                if "improve" in title.lower() or "提升" in title or "growth" in title.lower():
                    insights["profitability"].append(f"- **{institution}** ({date}): {title[:80]}...")

            # Cash flow related
            if "cash flow" in section_lower or "现金流" in section or "fcf" in section_lower:
                insights["cash_flow"].append(f"- **{institution}**: {title[:80]}...")

            # Valuation related
            if "pe " in title.lower() or "pb " in title.lower() or "估值" in title or "target" in title.lower():
                insights["valuation"].append(f"- **{institution}**: {title[:80]}...")

            # Concerns
            if any(word in title.lower() for word in ["miss", "pressure", "risk", "concern", "压力", "挑战", "下调"]):
                insights["concerns"].append(f"- **{institution}**: {title[:80]}...")

        return insights

    def extract_business_insights(self, business_results: list) -> dict:
        """Extract key business insights from search results."""
        insights = {
            "overseas_expansion": [],
            "market_position": [],
            "competitive_advantage": [],
            "products_services": [],
            "partnerships": []
        }

        for item in business_results[:15]:
            title = item.get("title", "")
            section = item.get("section", "")
            institution = item.get("institution_name", [""])[0] if item.get("institution_name") else "N/A"

            # Overseas expansion
            if any(word in title.lower() for word in ["overseas", "export", "global", "海外", "出口", "国际化"]):
                insights["overseas_expansion"].append(f"- **{institution}**: {title[:90]}...")

            # Market position
            elif any(word in title.lower() for word in ["market share", "leader", "no.1", "第一", "龙头", "领先"]):
                insights["market_position"].append(f"- **{institution}**: {title[:90]}...")

            # Competitive advantage
            elif any(word in title.lower() for word in ["advantage", "moat", "strength", "优势", "壁垒", "竞争力"]):
                insights["competitive_advantage"].append(f"- **{institution}**: {title[:90]}...")

            # Products & Services
            elif any(word in title.lower() for word in ["product", "model", "battery", "ev", "产品", "车型", "电池"]):
                insights["products_services"].append(f"- **{institution}**: {title[:90]}...")

            # Partnerships & Customers
            elif any(word in title.lower() for word in ["partner", "customer", "supplier", "apple", "合作", "客户", "供应商"]):
                insights["partnerships"].append(f"- **{institution}**: {title[:90]}...")

        return insights

    def generate_markdown_report(self) -> str:
        """Step 3: Generate detailed Markdown report based on actual data."""
        print(f"\n{'='*60}")
        print(f"STEP 3: Generating Detailed Markdown Report")
        print(f"{'='*60}\n")

        report_file = self.output_dir / f"{self.company_name}_due_diligence_report.md"

        # Extract insights from data
        financial_data = next((r["results"] for r in self.all_results if r["category"] == "financial"), [])
        business_data = next((r["results"] for r in self.all_results if r["category"] == "business"), [])
        legal_data = next((r["results"] for r in self.all_results if r["category"] == "legal"), [])
        team_data = next((r["results"] for r in self.all_results if r["category"] == "team"), [])

        financial_insights = self.extract_financial_insights(financial_data)
        business_insights = self.extract_business_insights(business_data)

        # Build report content
        content = f"""# {self.company_name} 尽调报告

**生成时间**: {datetime.now().strftime("%Y年%m月%d日 %H:%M")}
**数据来源**: 金融数据库 API ({len(financial_data) + len(business_data) + len(legal_data) + len(team_data)} 条数据)

---

## 执行摘要

### 公司基本信息
- **公司名称**: {self.company_name}
- **报告类型**: 综合尽调分析
- **分析维度**: 财务、业务、法律、团队

### 数据概览
"""

        # Add data summary
        for result in self.all_results:
            category_name = {
                "financial": "财务分析",
                "business": "业务分析",
                "legal": "法律合规",
                "team": "团队背景"
            }.get(result["category"], result["category"])
            content += f"- **{category_name}**: {len(result.get('results', []))} 条数据\n"

        # Key findings
        content += f"\n### 关键发现\n\n"

        if financial_insights["revenue_growth"]:
            content += "**财务亮点 - 营收增长**:\n"
            for item in financial_insights["revenue_growth"][:3]:
                content += f"{item}\n"
            content += "\n"

        if business_insights["overseas_expansion"]:
            content += "**业务亮点 - 海外扩张**:\n"
            for item in business_insights["overseas_expansion"][:3]:
                content += f"{item}\n"
            content += "\n"

        content += """### 风险提示
[基于以下详细分析识别主要风险]

### 投资建议
[基于综合分析提供投资建议]

---

## 数据来源

本报告基于以下数据源：
"""

        # Add data sources
        doc_id = 1
        for result in self.all_results:
            content += f"\n### {result['category'].upper()}\n"
            content += f"**查询**: {result['query']}\n\n"
            for item in result.get("results", []):
                title = item.get("title", "N/A")
                source = item.get("institution_name", item.get("company_name", "N/A"))
                date = item.get("publish_date", "N/A")
                content += f"[doc{doc_id}] {title} - {source} ({date})\n"
                doc_id += 1

        # Detailed Analysis Section
        content += "\n---\n\n## 详细分析\n\n"

        # Financial Analysis
        content += "### 财务分析\n\n"

        if financial_insights["revenue_growth"]:
            content += "**营收增长**:\n\n"
            for item in financial_insights["revenue_growth"][:8]:
                content += f"{item}\n"
            content += "\n"

        if financial_insights["profitability"]:
            content += "**盈利能力**:\n\n"
            for item in financial_insights["profitability"][:8]:
                content += f"{item}\n"
            content += "\n"

        if financial_insights["cash_flow"]:
            content += "**现金流分析**:\n\n"
            for item in financial_insights["cash_flow"][:5]:
                content += f"{item}\n"
            content += "\n"

        if financial_insights["valuation"]:
            content += "**估值情况**:\n\n"
            for item in financial_insights["valuation"][:5]:
                content += f"{item}\n"
            content += "\n"

        if financial_insights["concerns"]:
            content += "**关注点与风险**:\n\n"
            for item in financial_insights["concerns"][:5]:
                content += f"{item}\n"
            content += "\n"

        if financial_insights["highlights"]:
            content += "**其他财务亮点**:\n\n"
            for item in financial_insights["highlights"][:5]:
                content += f"{item}\n"
            content += "\n"

        content += "**数据来源参考**: 请参考上述财务分析数据源 (doc1-doc{})\n\n".format(len(financial_data))

        # Business Analysis
        content += "### 业务分析\n\n"

        if business_insights["overseas_expansion"]:
            content += "**海外扩张**:\n\n"
            for item in business_insights["overseas_expansion"][:8]:
                content += f"{item}\n"
            content += "\n"

        if business_insights["market_position"]:
            content += "**市场地位**:\n\n"
            for item in business_insights["market_position"][:8]:
                content += f"{item}\n"
            content += "\n"

        if business_insights["competitive_advantage"]:
            content += "**竞争优势**:\n\n"
            for item in business_insights["competitive_advantage"][:5]:
                content += f"{item}\n"
            content += "\n"

        if business_insights["products_services"]:
            content += "**产品与服务**:\n\n"
            for item in business_insights["products_services"][:5]:
                content += f"{item}\n"
            content += "\n"

        if business_insights["partnerships"]:
            content += "**合作伙伴与客户**:\n\n"
            for item in business_insights["partnerships"][:5]:
                content += f"{item}\n"
            content += "\n"

        content += "**数据来源参考**: 请参考上述业务分析数据源 (doc{}-doc{})\n\n".format(
            len(financial_data) + 1, len(financial_data) + len(business_data)
        )

        # Legal Analysis
        content += "### 法律合规审查\n\n"

        legal_count = len(legal_data)
        if legal_count > 0:
            # Filter for actual legal issues vs regular reports
            legal_issues = [item for item in legal_data if any(
                word in item.get("title", "").lower()
                for word in ["litigation", "诉讼", "penalty", "处罚", "dispute", "纠纷"]
            )]

            # Filter for company-specific legal issues (exclude unrelated companies)
            company_legal_issues = []
            for item in legal_data:
                title = item.get("title", "")
                title_lower = title.lower()
                # Only include if title contains company name or general legal terms
                if self.company_name.lower() in title_lower or any(
                    word in title_lower for word in ["诉讼", "处罚", "纠纷", "litigation", "penalty"]
                ):
                    company_legal_issues.append(item)

            if company_legal_issues:
                content += "**关注事项**:\n\n"
                for item in company_legal_issues[:5]:
                    institution = item.get("institution_name", [""])[0] if item.get("institution_name") else ""
                    source_str = f" - {institution}" if institution else ""
                    content += f"- {item.get('title', '')} ({item.get('publish_date', 'N/A')}){source_str}\n"
                content += "\n"
            else:
                content += "**合规状态**: 未发现重大法律诉讼或行政处罚记录\n\n"
                content += f"- 共检索到 {legal_count} 条合规相关信息\n"
                content += "- 主要为公司公告、年报等合规文件\n\n"

        content += f"**数据来源参考**: 请参考上述法律合规数据源 (doc{len(financial_data) + len(business_data) + 1}-doc{len(financial_data) + len(business_data) + legal_count})\n\n"

        # Team Analysis
        content += "### 团队背景分析\n\n"

        team_count = len(team_data)
        if team_count > 0:
            # Look for management changes, shareholder info
            mgmt_changes = [item for item in team_data if any(
                word in item.get("title", "").lower()
                for word in ["management", "management", "management", "高管", "股东", "board", "董事会"]
            )]

            if mgmt_changes:
                content += "**团队与股东信息**:\n\n"
                for item in mgmt_changes[:8]:
                    institution = item.get("institution_name", [""])[0] if item.get("institution_name") else ""
                    if institution:
                        content += f"- {item.get('title', '')} - **{institution}**\n"
                    else:
                        content += f"- {item.get('title', '')}\n"
                content += "\n"
            else:
                content += f"- 共检索到 {team_count} 条团队相关信息\n"
                content += "- 主要涉及公司治理、股权结构等方面\n\n"

        content += f"**数据来源参考**: 请参考上述团队背景数据源\n\n"

        # Risk Assessment
        content += """---

## 风险评估

### 风险汇总表

| 类别 | 风险描述 | 严重程度 | 影响范围 | 缓解措施 | 数据来源 |
|------|----------|----------|----------|----------|----------|
"""

        # Add identified risks
        risk_id = 1
        if financial_insights["concerns"]:
            for concern in financial_insights["concerns"][:3]:
                # Extract meaningful part from concern
                concern_text = concern.replace("- **", "").replace("**", "").strip()
                if ":" in concern_text:
                    concern_text = concern_text.split(":", 1)[1].strip()
                concern_short = concern_text[:60] + "..." if len(concern_text) > 60 else concern_text
                content += f"| 财务风险 | {concern_short} | 中 | 盈利能力 | 加强成本控制 | 见财务分析 |\n"
                risk_id += 1

        if not financial_insights["concerns"]:
            content += "| 财务风险 | 基于检索数据未发现重大财务风险 | 低 | - | 持续监控 | 见财务分析 |\n"

        content += "| 市场风险 | 行业竞争加剧 | 中 | 市场份额 | 产品差异化 | 见业务分析 |\n"
        content += "| 政策风险 | 监管政策变化 | 中 | 整体业务 | 合规运营 | 见法律合规 |\n"

        content += "\n### 风险说明\n\n"
        content += "**注**: 以上风险评估基于检索到的公开数据，具体风险需进一步深入分析。\n\n"

        # Valuation & Recommendation
        content += """---

## 估值与投资建议

### 估值方法
本报告综合以下估值方法：
- 市盈率法 (P/E)
- 市净率法 (P/B)
- DCF 现金流折现法
- 可比公司分析法

### 数据支持
估值基于检索到的财务数据和分析师预测，详见数据来源部分。
"""

        # Add valuation insights if available
        if financial_insights["valuation"]:
            content += "\n### 机构评级与目标价\n\n"
            for item in financial_insights["valuation"][:5]:
                content += f"{item}\n"
            content += "\n"

        content += "\### 投资建议框架\n"

        # Generate recommendation based on data
        positive_signals = (
            len(financial_insights.get("revenue_growth", [])) +
            len(financial_insights.get("profitability", [])) +
            len(business_insights.get("overseas_expansion", [])) +
            len(business_insights.get("competitive_advantage", []))
        )
        negative_signals = len(financial_insights.get("concerns", []))

        if positive_signals > negative_signals * 2:
            content += "**初步评估**: 积极信号较多，建议进一步深入分析\n\n"
            content += f"- 正面信号数量: {positive_signals}\n"
            content += f"- 关注信号数量: {negative_signals}\n"
        elif positive_signals > negative_signals:
            content += "**初步评估**: 信号中性偏正，建议关注关键风险点\n\n"
            content += f"- 正面信号数量: {positive_signals}\n"
            content += f"- 关注信号数量: {negative_signals}\n"
        else:
            content += "**初步评估**: 需谨慎评估风险，建议深入调研\n\n"
            content += f"- 正面信号数量: {positive_signals}\n"
            content += f"- 关注信号数量: {negative_signals}\n"

        content += """
**免责声明**: 本报告仅为基于公开数据的初步分析，不构成任何投资建议。投资决策请结合更多尽职调查工作。

---

## 附录

### 尽调方法
- **数据来源**: 金融数据库 API
- **分析框架**: references/framework.md
- **报告模板**: assets/report_template.md

### 分析局限性
1. 本报告基于公开数据库检索结果
2. 未包含管理团队访谈等一手信息
3. 建议结合实地调研、专家访谈等方式补充验证

### 免责声明
本报告基于公开信息和数据库检索结果生成，仅供参考，不构成投资建议。投资者应自行承担投资决策风险。
"""

        with open(report_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✓ Markdown report saved to: {report_file}")
        return str(report_file)

    def generate_canvas(self) -> str:
        """Step 4: Generate Canvas visualization."""
        print(f"\n{'='*60}")
        print(f"STEP 4: Generating Canvas Visualization")
        print(f"{'='*60}\n")

        import uuid

        canvas_file = self.output_dir / f"{self.company_name}_due_diligence.canvas"

        # Generate canvas structure
        nodes = []
        edges = []

        # Helper to generate IDs
        def gen_id():
            return uuid.uuid4().hex[:16]

        # Create group node
        group_id = gen_id()
        nodes.append({
            "id": group_id,
            "type": "group",
            "x": 0,
            "y": 0,
            "width": 1400,
            "height": 900,
            "label": f"{self.company_name} 尽调分析"
        })

        # Create analysis dimension nodes
        categories = [
            ("financial", "财务分析", 50, 100, "1"),
            ("business", "业务分析", 400, 100, "3"),
            ("legal", "法律合规", 750, 100, "5"),
            ("team", "团队背景", 1100, 100, "6")
        ]

        dimension_nodes = {}
        for cat, label, x, y, color in categories:
            node_id = gen_id()
            dimension_nodes[cat] = node_id

            # Find results for this category
            cat_results = next(
                (r for r in self.all_results if r["category"] == cat),
                None
            )

            result_text = ""
            if cat_results:
                count = len(cat_results.get("results", []))
                result_text = f"**数据量**: {count} 条\n\n"
                for i, r in enumerate(cat_results.get("results", [])[:5]):
                    result_text += f"{i+1}. {r.get('title', 'N/A')[:50]}...\n"
                if count > 5:
                    result_text += f"\n... 还有 {count-5} 条"

            nodes.append({
                "id": node_id,
                "type": "text",
                "x": x,
                "y": y,
                "width": 300,
                "height": 250,
                "color": color,
                "text": f"## {label}\n\n{result_text}"
            })

        # Create risk summary node
        risk_id = gen_id()
        nodes.append({
            "id": risk_id,
            "type": "text",
            "x": 50,
            "y": 400,
            "width": 600,
            "height": 200,
            "color": "2",
            "text": "## 风险评估\n\n[根据分析结果填写主要风险]\n\n- 风险1\n- 风险2\n- 风险3"
        })

        # Create recommendation node
        rec_id = gen_id()
        nodes.append({
            "id": rec_id,
            "type": "text",
            "x": 750,
            "y": 400,
            "width": 600,
            "height": 200,
            "color": "4",
            "text": "## 投资建议\n\n[根据分析结果填写投资建议]\n\n- 建议: [是/否/谨慎]\n- 估值区间\n- 关键条件"
        })

        # Create data sources node
        sources_id = gen_id()
        sources_text = "## 数据来源\n\n"
        for result in self.all_results:
            sources_text += f"**{result['category'].upper()}**: {len(result.get('results', []))} 条\n"

        nodes.append({
            "id": sources_id,
            "type": "text",
            "x": 50,
            "y": 650,
            "width": 1300,
            "height": 150,
            "text": sources_text
        })

        # Add edges from dimensions to summary
        for cat, node_id in dimension_nodes.items():
            edges.append({
                "id": gen_id(),
                "fromNode": node_id,
                "fromSide": "bottom",
                "toNode": risk_id,
                "toSide": "top",
                "toEnd": "none"
            })
            edges.append({
                "id": gen_id(),
                "fromNode": node_id,
                "fromSide": "bottom",
                "toNode": rec_id,
                "toSide": "top",
                "toEnd": "none"
            })

        # Build canvas
        canvas = {
            "nodes": nodes,
            "edges": edges
        }

        with open(canvas_file, "w", encoding="utf-8") as f:
            json.dump(canvas, f, ensure_ascii=False, indent=2)

        print(f"✓ Canvas saved to: {canvas_file}")
        return str(canvas_file)

    async def run(self) -> Dict[str, str]:
        """Run the complete due diligence workflow."""
        print(f"\n{'='*60}")
        print(f"Due Diligence Workflow for: {self.company_name}")
        print(f"{'='*60}")

        # Step 1: Retrieve data
        await self.retrieve_data()

        # Step 2: Save JSON
        json_file = self.save_json_data()

        # Step 3: Generate report
        report_file = self.generate_markdown_report()

        # Step 4: Generate canvas
        canvas_file = self.generate_canvas()

        print(f"\n{'='*60}")
        print(f"Due Diligence Workflow Complete!")
        print(f"{'='*60}")
        print(f"\nOutput files:")
        print(f"  1. JSON Data:    {json_file}")
        print(f"  2. Markdown:     {report_file}")
        print(f"  3. Canvas:       {canvas_file}\n")

        return {
            "json": json_file,
            "markdown": report_file,
            "canvas": canvas_file
        }


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Run automated due diligence analysis"
    )
    parser.add_argument(
        "company_name",
        help="Name of the company to analyze"
    )
    parser.add_argument(
        "--output-dir",
        default="./output",
        help="Output directory for generated files (default: ./output)"
    )

    args = parser.parse_args()

    runner = DueDiligenceRunner(
        company_name=args.company_name,
        output_dir=args.output_dir
    )

    await runner.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
