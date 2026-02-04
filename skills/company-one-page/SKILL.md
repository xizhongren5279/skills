---
name: company-one-page
description: Generate one-page investment decision memos for listed companies across A-share, Hong Kong, and US markets. Use when users request company analysis, investment reports, or one-pagers for specific companies. Supports queries like "Generate a one-page report for [Company Name]" or "Analyze [Company Name]" or "Create investment memo for [Company Name]".
---

# Company One-Page Investment Memo

## Overview

This skill generates comprehensive one-page investment decision memos for listed companies using a **progressive analysis workflow**: retrieve data for each section, immediately analyze it, then move to the next section. This approach minimizes context burden and produces higher quality outputs.

## User Input

Users provide only the company name. The skill automatically:
- Identifies the company across A-share, Hong Kong, or US markets
- Retrieves data section by section
- Generates immediate analysis for each section
- Combines all analyses into a final cohesive report

## Progressive Analysis Workflow

**CRITICAL**: Follow this sequence strictly. For each section:
1. Retrieve data using MCP tools
2. **Immediately** generate the analysis for that section in final report format
3. Save the section analysis
4. Move to next section
5. After all 5 sections are complete, integrate them into the final report

### Section 1: 公司近况

**Step 1.1 - Retrieve Data**

Show progress: "正在检索公司近况..."

Use `mcp__ashare-mcp-research__info_search_finance_db`:
- query: "[Company Name] 公司近况，公司近期发生的股价异动、财报披露，产品业务、战略调整等"
- date_range: "past_quarter"
- recall_num: 10

**Step 1.2 - Generate Section Analysis**

Immediately analyze the retrieved data and write:

```markdown
## 1. 公司近况

[Write ONE paragraph (not bullet points) describing specific events within past 3 months. Must include: stock price movements, earnings releases, product launches, strategic changes. Use concrete data and dates.]
```

Save this as **section_1_analysis**.

---

### Section 2: 核心投资逻辑

**Step 2.1 - Retrieve Data**

Show progress: "正在分析投资逻辑..."

Run these queries in parallel:

1. Stock price catalysts:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 分析引起公司最近3个月内发生股价异动的新闻事件，尤其是概念炒作导致的股价异动"
   - date_range: "past_quarter"
   - recall_num: 8

2. Short-term drivers:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 分析公司业务，整理短期投资逻辑(1-3月)，要从公司业务本身的价值出发来提炼3-5个要点"
   - date_range: "past_quarter"
   - recall_num: 12

3. Long-term drivers:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 分析公司业务，梳理长期投资逻辑(1-3年)，要从公司业务本身的价值出发来提炼3-5个要点"
   - date_range: "past_year"
   - recall_num: 12

4. Management guidance:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 公司管理层业务指引，下个季度的业务指引、明年的业务指引"
   - date_range: "past_half_year"
   - recall_num: 8

5. Risk analysis:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 分析公司核心风险，提炼3-5个风险点"
   - date_range: "past_half_year"
   - recall_num: 5

**Step 2.2 - Generate Section Analysis**

Immediately synthesize the data and write:

```markdown
## 2. 核心投资逻辑

### 2.1 短期逻辑

- [Driver 1: Must include quantitative data. Focus on next 3-6 months. Incorporate recent price catalysts and quarterly guidance.]
- [Driver 2: Quantitative data required]
- [Driver 3: Quantitative data required]
- [Driver 4: If available]
- [Driver 5: If available]

### 2.2 长期逻辑

- [Advantage 1: Must include quantitative data. Focus on 3-5 year sustainable advantages. Incorporate annual guidance.]
- [Advantage 2: Quantitative data required]
- [Advantage 3: Quantitative data required]
- [Advantage 4: If available]
- [Advantage 5: If available]

### 2.3 风险提示

- [Risk 1: Major downside risk]
- [Risk 2: Major downside risk]
- [Risk 3: If applicable]
```

Save this as **section_2_analysis**.

---

### Section 3: 未来事件与核心跟踪指标

**Step 3.1 - Retrieve Data**

Show progress: "正在整理未来催化事件..."

Run these queries in parallel:

1. 1-3 month catalysts:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 整理未来1-3月公司可能发生的财报发布与业绩指引、重大合同与订单、产品里程碑、并购与分拆、股票回购与分红政策、技术或专利突破、重大政策变动"
   - date_range: "past_half_year"
   - recall_num: 15
   - doc_type: "report"

2. 3-6 month catalysts:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 整理未来3-6月公司可能发生的财报发布与业绩指引、重大合同与订单、产品里程碑、并购与分拆、股票回购与分红政策、技术或专利突破、重大政策变动"
   - date_range: "past_half_year"
   - recall_num: 15
   - doc_type: "report"

3. Core tracking metrics:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 分析公司核心跟踪指标，短期(1-2季度)需盯住的财务或经营数据，长期(1-2年)需盯住的战略或行业指标"
   - date_range: "past_year"
   - recall_num: 12
   - doc_type: "report"

**Step 3.2 - Generate Section Analysis**

Immediately create the tables and metrics:

```markdown
## 3. 未来事件与核心跟踪指标

### 3.1 1-3月事件催化表

| 时间 | 事件 | 点评/市场预期 |
| :--- | :--- | :--- |
| [Specific date or "X周"] | [Event description] | [Expected impact on stock] |
| [Add 5+ rows] | | |

### 3.2 3-6月事件催化表

| 时间 | 事件 | 点评/市场预期 |
| :--- | :--- | :--- |
| [Specific date or "X月"] | [Event description] | [Expected impact on stock] |
| [Add 5+ rows] | | |

### 3.3 核心跟踪指标

**短期 (1-2季度):**
- [Metric 1: Include current market expectation/consensus]
- [Metric 2: Include current market expectation/consensus]
- [Metric 3: If applicable]

**长期 (1-2年):**
- [Metric 1: Include strategic targets or industry benchmarks]
- [Metric 2: Include strategic targets or industry benchmarks]
- [Metric 3: If applicable]
```

Save this as **section_3_analysis**.

---

### Section 4: 业务拆分

**Step 4.1 - Retrieve Data**

Show progress: "正在分析业务结构..."

Run these queries in parallel:

1. Profit model:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 分析公司盈利方式：梳理2-3个公司最核心的赚钱方式"
   - date_range: "past_quarter"
   - recall_num: 8
   - doc_type: "report"

2. Market positioning:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 分析市场格局：用两句话描述（需要量化数据）其行业地位、市场份额，并点出2-3个最核心的竞争对手"
   - date_range: "past_year"
   - recall_num: 10
   - doc_type: "report"

3. Business segments:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 整理各板块业务情况"
   - date_range: "past_quarter"
   - recall_num: 8
   - doc_type: "report"

4. Revenue breakdown:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 最新财报各板块细分收入数据（可以是比例），给出同比变化，输出表格"
   - date_range: "past_half_year"
   - recall_num: 12
   - doc_type: "report"

**Step 4.2 - Generate Section Analysis**

Immediately write the business breakdown:

```markdown
## 4. 业务拆分

### 4.1 公司盈利方式

- [Core profit method 1]
- [Core profit method 2]
- [Core profit method 3 if applicable]

### 4.2 市场格局

[ONE paragraph with quantitative data: industry position, market share percentage, and name 2-3 main competitors with their market shares]

### 4.3 各板块业务情况

- [Segment 1: Brief description]
- [Segment 2: Brief description]
- [Segment 3: Brief description]

### 4.4 最新财报各板块细分收入

| 板块 | 收入（百万元/占比） | 同比变化 |
| :--- | :--- | :--- |
| [Segment 1] | [Revenue/Percentage] | [YoY %] |
| [Segment 2] | [Revenue/Percentage] | [YoY %] |
| [Add more rows as needed] | | |

注: 使用"-"表示数据缺失
```

Save this as **section_4_analysis**.

---

### Section 5: 财务与估值快照

**Step 5.1 - Retrieve Data**

Show progress: "正在整理财务与估值数据..."

Run these queries in parallel:

1. Latest earnings commentary:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 最新财报的财务指标解读"
   - date_range: "past_quarter"
   - recall_num: 10
   - doc_type: "report"

2. Historical and forecast data:
   - Tool: `mcp__ashare-mcp-research__info_search_stock_db`
   - query: "[Company Name] 整理公司近3年关键财务指标，给出未来3年的关键财务指标"

3. Domestic analyst forecasts:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 收集整理多家券商（国内券商，3-5家）对公司未来三年的盈利预测（收入、利润、目标价）"
   - date_range: "past_half_year"
   - recall_num: 15
   - doc_type: "report"

4. International analyst forecasts:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 收集整理多家券商（国外券商（华尔街的投行），3-5家）对公司未来三年的盈利预测（收入、利润、目标价）"
   - date_range: "past_half_year"
   - recall_num: 15
   - doc_type: "foreign_report"

5. Valuation comparison:
   - Tool: `mcp__ashare-mcp-research__info_search_finance_db`
   - query: "[Company Name] 进行可比公司估值测算与估值对比，PE、PB等估值指标均可"
   - date_range: "past_year"
   - recall_num: 10
   - doc_type: "report"

6. Valuation comparison fallback (if step 5 returns insufficient comparable company data):
   - Tool: `mcp__ashare-mcp-research__info_search_web`
   - query: "[Company Name] 及其可比公司（行业竞争对手）的最新估值对比，包括PE、PB等估值指标"

**Step 5.2 - Generate Section Analysis**

**IMPORTANT for Section 5.4 估值对比**: If the valuation comparison query in Step 5.1 (query #5) returns insufficient data for comparable companies (e.g., competitor valuation metrics are missing), immediately use the web search fallback (query #6) to retrieve publicly available valuation data before writing Section 5.4.

Immediately create financial tables and commentary:

```markdown
## 5. 财务与估值快照

### 5.1 最新财报解读

- **[关键词1]**: [结合业务情况的具体描述]
- **[关键词2]**: [结合业务情况的具体描述]
- **[关键词3]**: [结合业务情况的具体描述，可选]

### 5.2 历史与预测

| 财务指标 (百万元) | 2024A | 2025Q2（最新） | 2025E | 2026E | 2027E |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 营业收入 | [data] | [data] | [data] | [data] | [data] |
| 同比增速 | [data] | [data] | [data] | [data] | [data] |
| 归母净利润 | [data] | [data] | [data] | [data] | [data] |
| 同比增速 | [data] | [data] | [data] | [data] | [data] |
| 毛利率 (%) | [data] | [data] | [data] | [data] | [data] |

注: 使用"-"表示数据缺失，删除全部缺失的行

### 5.3 多方机构盈利预测对比

| 机构 | 发布时间 | 目标价 | 2025E 营收(百万元) | 2025E 净利润(百万元) | 2026E 营收(百万元) | 2026E 净利润(百万元) | 2027E 营收(百万元) | 2027E 净利润(百万元) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| [国内券商1] | [Date] | [Price] | [Rev] | [Profit] | [Rev] | [Profit] | [Rev] | [Profit] |
| [国内券商2] | [Date] | [Price] | [Rev] | [Profit] | [Rev] | [Profit] | [Rev] | [Profit] |
| [Add 3-5 more domestic] | | | | | | | | |
| [国际投行1] | [Date] | [Price] | [Rev] | [Profit] | [Rev] | [Profit] | [Rev] | [Profit] |
| [国际投行2] | [Date] | [Price] | [Rev] | [Profit] | [Rev] | [Profit] | [Rev] | [Profit] |
| [Add 3-5 more international] | | | | | | | | |

注: 国内券商在前，国际投行在后。使用"-"表示数据缺失，删除全部缺失的行

### 5.4 估值对比

| 公司 | 估值指标（PE、PB等） |
| :--- | :--- |
| [Company Name] | [Current valuation with year] |
| [Competitor A] | [Valuation with year] |
| [Competitor B] | [Valuation with year] |

注: 选择最适合该行业的估值指标(PE/PB/PS等)。使用"-"表示数据缺失
```

Save this as **section_5_analysis**.

---

## Final Integration Phase

After completing all 5 sections, **integrate the analyses into one cohesive report**:

**Step 6.1 - Combine All Sections**

1. Read all saved section analyses:
   - section_1_analysis
   - section_2_analysis
   - section_3_analysis
   - section_4_analysis
   - section_5_analysis

2. Combine them in order with this structure:

```markdown
# [Company Name] 公司一页纸

[section_1_analysis content]

[section_2_analysis content]

[section_3_analysis content]

[section_4_analysis content]

[section_5_analysis content]
```

3. Review for:
   - Consistency in tone and terminology
   - No duplicate information across sections
   - All quantitative data is present
   - Tables are properly formatted
   - All "-" markers are used for missing data

**Step 6.2 - Save Final Outputs**

1. Save the integrated report as: `[Company Name]_公司一页纸.md`
2. Inform user: "✅ 报告生成完成！已保存为 [Company Name]_公司一页纸.md"

## Important Guidelines

1. **Progressive workflow is mandatory**: Never skip ahead. Complete each section's retrieval AND analysis before moving to the next.

2. **Immediate analysis**: After each data retrieval, immediately generate that section's final-format content. Do not accumulate data.

3. **Context management**: By analyzing section-by-section, you avoid context overload and produce higher quality analysis for each section.

4. **Progress feedback**: Show users clear progress indicators:
   - "正在检索公司近况..." (Section 1)
   - "正在分析投资逻辑..." (Section 2)
   - "正在整理未来催化事件..." (Section 3)
   - "正在分析业务结构..." (Section 4)
   - "正在整理财务与估值数据..." (Section 5)
   - "正在整合最终报告..." (Final phase)

5. **Handle missing data gracefully**:
   - Use "-" for missing table cells
   - Delete entire table rows where all data is missing
   - Note data gaps in section analysis

6. **Quantitative data required**: All investment logic, business analysis, and market positioning must include specific numbers, percentages, metrics.

7. **Report language**: The entire report must be in Chinese.

8. **MCP tool parameters**:
   - `date_range`: "past_quarter", "past_half_year", "past_year"
   - `recall_num`: Reduced from original to 5-15 per query to minimize context burden
   - `doc_type`: "report", "company_all_announcement", "foreign_report"

9. **Date precision**: Use specific dates when available; otherwise use "X周" or "X月".

10. **Reduced recall_num rationale**: Smaller retrieval sets (8-15 items) are analyzed immediately, producing better insights than accumulating large datasets (30+ items) for later processing.

11. **Adaptive retrieval strategy**: If the initial queries for a section return insufficient data to meet the writing requirements:
   - **First attempt**: Modify the query keywords or adjust parameters (date_range, recall_num) and retry with `info_search_finance_db`
   - **Second attempt (fallback)**: Use `mcp__ashare-mcp-research__info_search_web` as a backup to search for publicly available information
   - **Stop after 1-2 attempts**: If adequate data is still unavailable, proceed to write the section analysis based on whatever information is available, using "-" for missing data
   - **Rationale**: This prevents excessive retrieval that can consume too many tokens and delay overall completion. It's better to complete the report with some data gaps than to get stuck searching indefinitely.
