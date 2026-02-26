---
name: company-one-page
description: Generate one-page investment decision memos for listed companies across A-share, Hong Kong, and US markets. Use when users request company analysis, investment reports, or one-pagers for specific companies. Supports queries like "Generate a one-page report for [Company Name]" or "Analyze [Company Name]" or "Create investment memo for [Company Name]".
---

# Company One-Page Investment Memo

## Overview

This skill generates comprehensive one-page investment decision memos for listed companies using **FULL PARALLEL workflow**: ALL 5 sections retrieve AND analyze in parallel within their subagents, then integrate. This approach dramatically reduces generation time to ~1.3-1.4 minutes.

## Critical Reference Documents

**MUST READ before execution**:

1. **`references/COMPANY_ONE_PAGE_INPUT.md`**
   - Defines the 5-section structure and output format requirements
   - Specifies analysis depth for each section
   - Contains table formats and data requirements
   - **Role**: Understanding WHAT to generate

2. **`references/RETRIEVAL_STRATEGY.md`**
   - Contains ALL 18 MCP query templates with exact parameters
   - Specifies date_range, recall_num, doc_type for each query
   - Documents query optimization strategies
   - **Role**: Understanding HOW to retrieve data

**Tool Count per Section** (Total: 18 MCP queries):
- Section 1 (公司近况): **1 query**
- Section 2 (核心投资逻辑): **5 queries**
- Section 3 (未来事件与核心跟踪指标): **3 queries**
- Section 4 (业务拆分): **4 queries**
- Section 5 (财务与估值快照): **5 queries** + 1 web fallback (if needed)

## User Input

Users provide only the company name. The skill automatically:
- Identifies the company across A-share, Hong Kong, or US markets
- Reads `assets/公司一页纸的需求.md` to understand output requirements
- Reads `assets/RETRIEVAL_STRATEGY.md` to get exact query templates
- Spawns 5 parallel subagents - each completes retrieval AND analysis internally
- Combines all section analyses into final cohesive report

## v3.0 Full Parallel Workflow (2 Phases)

### Phase 1: Parallel Retrieval + Analysis (~1.3-1.4 minutes)

**Show progress**: "正在并行检索并分析所有5个section..."

**CRITICAL FIRST STEP**: Get current system time and pass it to ALL subagents:
```python
from datetime import datetime
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
current_date = datetime.now().strftime("%Y-%m-%d")
```

**CRITICAL**: Spawn ALL 5 subagents in a SINGLE message. **Each subagent performs BOTH retrieval AND analysis before returning.**

**Key Innovation**: Subagents不仅检索数据,还立即完成section分析,主工作流只需整合。

**IMPORTANT**: Every subagent prompt MUST include the current system time at the beginning, so all time-based queries (e.g., "最近3个月", "未来1-3月") are accurately interpreted relative to this timestamp.

```python
# Subagent 1: Section 1 - 公司近况 (1 query)
Task(
    subagent_type="general-purpose",
    description="Analyze company updates",
    prompt=f"""You are analyzing section 1 (公司近况) for [Company Name].

**CURRENT SYSTEM TIME**: {current_time} (Date: {current_date})
**IMPORTANT**: All time-based queries must be relative to this timestamp.

STEP 1 - Retrieve data:
Read assets/RETRIEVAL_STRATEGY.md Section 1 for exact query template.
Execute 1 MCP query: mcp__ashare-mcp-research__info_search_finance_db
- query: '[Company Name] 公司近况,公司近期发生的股价异动、财报披露,产品业务、战略调整等'
- date_range: 'past_quarter'
- recall_num: 10

STEP 2 - Analyze and write markdown:
Read assets/公司一页纸的需求.md Section 1 for output format.

## 1. 公司近况
[ONE paragraph describing specific events within past 3 months with concrete data/dates]

Return the complete markdown section as your final output."""
)

# Subagent 2: Section 2 - 核心投资逻辑 (5 queries)
Task(
    subagent_type="general-purpose",
    description="Analyze investment logic",
    prompt=f"""You are analyzing section 2 (核心投资逻辑) for [Company Name].

**CURRENT SYSTEM TIME**: {current_time} (Date: {current_date})
**IMPORTANT**: All time-based queries must be relative to this timestamp.

STEP 1 - Retrieve data (5 parallel queries):
Read assets/RETRIEVAL_STRATEGY.md Section 2 for exact query templates.
Execute 5 MCP queries in PARALLEL (single message with 5 tool calls):

1. stock_catalysts - 股价异动事件
   query: '[Company Name] 分析引起公司最近3个月内发生股价异动的新闻事件，尤其是概念炒作导致的股价异动'
   date_range: 'past_quarter', recall_num: 8

2. short_term_logic - 短期投资逻辑(1-3月)
   query: '[Company Name] 分析公司业务，整理短期投资逻辑(1-3月)，要从公司业务本身的价值出发来提炼3-5个要点'
   date_range: 'past_quarter', recall_num: 12

3. long_term_logic - 长期投资逻辑(1-3年)
   query: '[Company Name] 分析公司业务，梳理长期投资逻辑(1-3年)，要从公司业务本身的价值出发来提炼3-5个要点'
   date_range: 'past_year', recall_num: 12

4. management_guidance - 管理层业务指引
   query: '[Company Name] 公司管理层业务指引，下个季度的业务指引、明年的业务指引'
   date_range: 'past_half_year', recall_num: 8

5. risk_analysis - 核心风险
   query: '[Company Name] 分析公司核心风险，提炼3-5个风险点'
   date_range: 'past_half_year', recall_num: 5

STEP 2 - Analyze and write markdown:
Read assets/公司一页纸的需求.md Section 2 for output format.

## 2. 核心投资逻辑

### 2.1 短期逻辑
- [3-5 bullet points with quantitative data]

### 2.2 长期逻辑
- [3-5 bullet points with quantitative data]

### 2.3 风险提示
- [2-3 major risks]

Return the complete markdown section as your final output."""
)

# Subagent 3: Section 3 - 未来事件与核心跟踪指标 (3 queries)
Task(
    subagent_type="general-purpose",
    description="Analyze future catalysts",
    prompt=f"""You are analyzing section 3 (未来事件与核心跟踪指标) for [Company Name].

**CURRENT SYSTEM TIME**: {current_time} (Date: {current_date})
**IMPORTANT**: All time-based queries (e.g., "未来1-3月", "未来3-6月") must be relative to this timestamp.

STEP 1 - Retrieve data (3 parallel queries):
Read assets/RETRIEVAL_STRATEGY.md Section 3 for exact query templates.
Execute 3 MCP queries in PARALLEL:

1. catalysts_1_3m - 未来1-3月事件
   query: '[Company Name] 整理未来1-3月公司可能发生的财报发布与业绩指引、重大合同与订单、产品里程碑、并购与分拆、股票回购与分红政策、技术或专利突破、重大政策变动'
   date_range: 'past_half_year', recall_num: 15, doc_type: 'report'

2. catalysts_3_6m - 未来3-6月事件
   query: '[Company Name] 整理未来3-6月公司可能发生的财报发布与业绩指引、重大合同与订单、产品里程碑、并购与分拆、股票回购与分红政策、技术或专利突破、重大政策变动'
   date_range: 'past_half_year', recall_num: 15, doc_type: 'report'

3. tracking_metrics - 核心跟踪指标
   query: '[Company Name] 分析公司核心跟踪指标，短期(1-2季度)需盯住的财务或经营数据，长期(1-2年)需盯住的战略或行业指标'
   date_range: 'past_year', recall_num: 12, doc_type: 'report'

STEP 2 - Analyze and write markdown:
Read assets/公司一页纸的需求.md Section 3 for output format.

## 3. 未来事件与核心跟踪指标

### 3.1 1-3月事件催化表
| 时间 | 事件 | 点评/市场预期 |
[5+ rows with specific dates]

### 3.2 3-6月事件催化表
| 时间 | 事件 | 点评/市场预期 |
[5+ rows]

### 3.3 核心跟踪指标
**短期 (1-2季度):** [2-3 metrics]
**长期 (1-2年):** [2-3 metrics]

Return the complete markdown section as your final output."""
)

# Subagent 4: Section 4 - 业务拆分 (4 queries)
Task(
    subagent_type="general-purpose",
    description="Analyze business breakdown",
    prompt=f"""You are analyzing section 4 (业务拆分) for [Company Name].

**CURRENT SYSTEM TIME**: {current_time} (Date: {current_date})
**IMPORTANT**: All time-based queries must be relative to this timestamp.

STEP 1 - Retrieve data (4 parallel queries):
Read assets/RETRIEVAL_STRATEGY.md Section 4 for exact query templates.
Execute 4 MCP queries in PARALLEL:

1. profit_model - 公司盈利方式
   query: '[Company Name] 分析公司盈利方式：梳理2-3个公司最核心的赚钱方式'
   date_range: 'past_quarter', recall_num: 8, doc_type: 'report'

2. market_position - 市场格局
   query: '[Company Name] 分析市场格局：用两句话描述（需要量化数据）其行业地位、市场份额，并点出2-3个最核心的竞争对手'
   date_range: 'past_year', recall_num: 10, doc_type: 'report'

3. business_segments - 各板块业务情况
   query: '[Company Name] 整理各板块业务情况'
   date_range: 'past_quarter', recall_num: 8, doc_type: 'report'

4. revenue_breakdown - 最新财报各板块细分收入
   query: '[Company Name] 最新财报各板块细分收入数据（可以是比例），给出同比变化，输出表格'
   date_range: 'past_half_year', recall_num: 12, doc_type: 'report'

STEP 2 - Analyze and write markdown:
Read assets/公司一页纸的需求.md Section 4 for output format.

## 4. 业务拆分

### 4.1 公司盈利方式
- [2-3 core profit methods]

### 4.2 市场格局
[ONE paragraph with market share % and 2-3 competitors]

### 4.3 各板块业务情况
- [Segment descriptions]

### 4.4 最新财报各板块细分收入
| 板块 | 收入 | 同比变化 |
[Revenue table]

Return the complete markdown section as your final output."""
)

# Subagent 5: Section 5 - 财务与估值快照 (5 queries + 1 web fallback)
Task(
    subagent_type="general-purpose",
    description="Analyze financials valuation",
    prompt=f"""You are analyzing section 5 (财务与估值快照) for [Company Name].

**CURRENT SYSTEM TIME**: {current_time} (Date: {current_date})
**IMPORTANT**: All time-based queries must be relative to this timestamp.

STEP 1 - Retrieve data (5 parallel queries + fallback):
Read assets/RETRIEVAL_STRATEGY.md Section 5 for exact query templates.
Execute 5 MCP queries in PARALLEL:

1. earnings_commentary - 最新财报解读
   query: '[Company Name] 最新财报的财务指标解读'
   date_range: 'past_quarter', recall_num: 10, doc_type: 'report'

2. historical_forecast - 历史与预测
   mcp__ashare-mcp-research__info_search_stock_db
   query: '[Company Name] 整理公司近3年关键财务指标，给出未来3年的关键财务指标'

3. domestic_analysts - 国内券商预测
   query: '[Company Name] 收集整理多家券商（国内券商，3-5家）对公司未来三年的盈利预测（收入、利润、目标价）'
   date_range: 'past_half_year', recall_num: 15, doc_type: 'report'

4. intl_analysts - 国外投行预测
   query: '[Company Name] 收集整理多家券商（国外券商（华尔街的投行），3-5家）对公司未来三年的盈利预测（收入、利润、目标价）'
   date_range: 'past_half_year', recall_num: 15, doc_type: 'foreign_report'

5. valuation_comp - 估值对比
   query: '[Company Name] 进行可比公司估值测算与估值对比，PE、PB等估值指标均可'
   date_range: 'past_year', recall_num: 10, doc_type: 'report'

FALLBACK: If query 5 returns insufficient comparable company data, run:
   mcp__ashare-mcp-research__info_search_web
   query: '[Company Name] 及其可比公司（行业竞争对手）的最新估值对比，包括PE、PB等估值指标'

STEP 2 - Analyze and write markdown:
Read assets/公司一页纸的需求.md Section 5 for output format.

## 5. 财务与估值快照

### 5.1 最新财报解读
- **[关键词1]**: [描述]
- **[关键词2]**: [描述]
- **[关键词3]**: [描述]

### 5.2 历史与预测
| 财务指标 | 2024A | 2025Q2 | 2025E | 2026E | 2027E |
[Financial table]

### 5.3 多方机构盈利预测对比
| 机构 | 发布时间 | 目标价 | 2025E营收 | ... |
[Analyst forecasts - domestic first, then international]

### 5.4 估值对比
| 公司 | 估值指标 |
[Valuation comparison table]

Return the complete markdown section as your final output."""
)
```

**Wait for ALL 5 subagents to complete before proceeding to Phase 2.**

**Expected Phase 1 time**: ~1.3-1.4 minutes (max of all 5 parallel subagents, including both retrieval and analysis)

---

### Phase 2: Final Integration (~10 seconds)

**Show progress**: "正在整合最终报告..."

Once all 5 subagents return their analyzed sections:

#### Step 2.1: Combine All Sections

```python
# All subagents have returned:
# - section_1_analysis (markdown)
# - section_2_analysis (markdown)
# - section_3_analysis (markdown)
# - section_4_analysis (markdown)
# - section_5_analysis (markdown)

final_report = f"""# {company_name} 公司一页纸

**生成时间**: {timestamp}

---

{section_1_analysis}

{section_2_analysis}

{section_3_analysis}

{section_4_analysis}

{section_5_analysis}

---
*本报告由 FinGPT Agent 自动生成，采用并行检索+分析架构*
"""
```

#### Step 2.2: Quality Review

Quick sanity checks:
- All 5 sections present
- Tables properly formatted (use "-" for missing data, delete fully empty rows)
- No placeholder text like "[Company Name]"
- Quantitative data included
- 国内券商在前, 国际投行在后 (Section 5.3)

#### Step 2.3: Save Final Output

Save as: `[Company Name]_公司一页纸_YYYYMMDD_HHMMSS.md`

Inform user: "✅ 报告生成完成！已保存为 [Company Name]_公司一页纸_YYYYMMDD_HHMMSS.md"

---



## Important Guidelines

1. **Read reference documents first**: Always read both `公司一页纸的需求.md` and `RETRIEVAL_STRATEGY.md` before execution

2. **Get current system time FIRST**: Before spawning subagents, obtain current system time using `datetime.now()` and pass it to ALL subagent prompts. This ensures all time-based queries are accurate.

3. **Full parallelism is mandatory**: Always spawn ALL 5 subagents in a single message

4. **Each subagent is self-contained**: Retrieve data → Analyze → Return markdown. No raw data exchange. Each subagent receives current system time in its prompt.

5. **Exact query parameters**: Use exact query templates, date_range, recall_num from RETRIEVAL_STRATEGY.md. All time references in queries are interpreted relative to the provided current system time.

6. **Wait for completion**: Do not start Phase 2 until ALL 5 subagents return analyzed sections

7. **Progress feedback**: Show clear progress indicators:
   - "正在并行检索并分析所有5个section..." (Phase 1)
   - "正在整合最终报告..." (Phase 2)

8. **Handle missing data gracefully**: Use "-" for missing table cells and delete fully empty rows

9. **Quantitative data required**: All investment logic, business analysis must include specific numbers

10. **Report language**: Entire report must be in Chinese

11. **Table requirements**:
    - Section 3: Each event table must have 5+ rows
    - Section 5.3: 国内券商在前, 国际投行在后
    - Use "-" for missing data, delete rows where all data is missing

---

## Query Count Summary

| Section | Queries | Tools |
|---------|---------|-------|
| 1. 公司近况 | 1 | finance_db |
| 2. 核心投资逻辑 | 5 | finance_db (×5) |
| 3. 未来事件与核心跟踪指标 | 3 | finance_db (×3) |
| 4. 业务拆分 | 4 | finance_db (×4) |
| 5. 财务与估值快照 | 5 + 1 fallback | stock_db (×1), finance_db (×4), web (×1 if needed) |
| **Total** | **18 + 1 fallback** | **3 tool types** |

---
