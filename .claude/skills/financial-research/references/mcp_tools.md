# MCP Tools Reference

This document provides complete documentation for all available MCP tools in the financial research environment.

## Available Tools Overview

| Tool | Purpose | Data Source | Use Case |
|------|---------|-------------|----------|
| `info_search_finance_db` | Search financial database | Research reports, announcements, news, analyst comments | Qualitative company/industry analysis |
| `info_search_user_db` | Search user documents | User-uploaded files | Private research documents |
| `info_search_stock_db` | Query quantitative data | Financial metrics, market data | Quantitative metrics and comparisons |
| `info_search_web` | Web search | Online sources | Fallback for missing data |

---

## 1. info_search_finance_db

**Full name**: `mcp__ashare-mcp-research__info_search_finance_db`

**Purpose**: Search the financial database for research reports, company announcements, analyst comments, news articles, and other qualitative financial content.

### Parameters

```python
{
    "query": str,              # Natural language search query (REQUIRED)
    "date_range": str | None,  # Time filter (optional, default: None)
    "recall_num": int,         # Number of results to return (optional, default: 15)
    "doc_type": str | None     # Document type filter (optional, default: None)
}
```

### Parameter Details

#### query (REQUIRED)
- Natural language description of information needed
- Include time references if date_range is not sufficient
- Be specific about what you're looking for

**Examples**:
```python
"比亚迪公司近况，公司近期发生的股价异动、财报披露、产品业务、战略调整等"
"新能源汽车行业的竞争格局和市场份额分布"
"特斯拉管理层对2025年的业务指引和预期"
"分析半导体行业的供应链风险和地缘政治影响"
```

#### date_range (optional)
Filters results by publication date. Available options:

| Value | Meaning | Use Case |
|-------|---------|----------|
| `"all"` | All time periods | Historical analysis, long-term trends |
| `"past_day"` | Last 24 hours | Breaking news, real-time events |
| `"past_week"` | Last 7 days | Recent developments |
| `"past_month"` | Last 30 days | Recent trends |
| `"past_quarter"` | Last 3 months | Quarterly updates, short-term logic |
| `"past_half_year"` | Last 6 months | Medium-term trends |
| `"past_year"` | Last 12 months | Annual analysis, long-term logic |
| `None` | No filter (same as "all") | Default behavior |

**Selection guidelines**:
- Company updates/recent news: `"past_quarter"`
- Short-term investment logic: `"past_quarter"` to `"past_half_year"`
- Long-term investment logic: `"past_year"`
- Management guidance: `"past_half_year"`
- Industry trends: `"past_year"`
- Breaking news/events: `"past_week"` or `"past_day"`

#### recall_num (optional, default: 15)
Number of documents to retrieve.

**Selection guidelines**:
- Quick fact-checking: 5-8
- Standard analysis: 10-15
- Comprehensive research: 15-20
- Trade-off: More results = more context but slower processing

**Typical values**:
- Company news/updates: 8-10
- Investment logic analysis: 12-15
- Risk analysis: 5-8
- Management guidance: 8-10
- Industry analysis: 15-20

#### doc_type (optional)
Filter by document type. Available options:

| Value | Document Type | Description |
|-------|--------------|-------------|
| `"all"` | All types | Default, no filtering |
| `"report"` | Research reports | Analyst reports, industry reports |
| `"summary"` | Meeting summaries | Earnings call transcripts, investor meetings |
| `"company_all_announcement"` | Company announcements | Official filings, disclosures |
| `"comments"` | Analyst comments | Quick takes, commentary |
| `"news"` | News articles | Financial news, press releases |
| `"foreign_report"` | Foreign research | International analyst reports |
| `None` | No filter | Same as "all" |

**Selection guidelines**:
- In-depth analysis: `"report"`
- Management insights: `"summary"`
- Official information: `"company_all_announcement"`
- Quick market views: `"comments"`
- Recent developments: `"news"`
- Global perspective: `"foreign_report"`

### Usage Examples

**Example 1: Company recent updates**
```python
mcp__ashare-mcp-research__info_search_finance_db(
    query="特斯拉公司近况，股价异动、财报披露、产品业务、战略调整",
    date_range="past_quarter",
    recall_num=10,
    doc_type=None
)
```

**Example 2: Investment logic**
```python
mcp__ashare-mcp-research__info_search_finance_db(
    query="英伟达长期投资逻辑(1-3年)，从公司业务本身的价值出发",
    date_range="past_year",
    recall_num=12,
    doc_type="report"
)
```

**Example 3: Risk analysis**
```python
mcp__ashare-mcp-research__info_search_finance_db(
    query="比亚迪核心风险分析",
    date_range="past_half_year",
    recall_num=8,
    doc_type=None
)
```

**Example 4: Industry research**
```python
mcp__ashare-mcp-research__info_search_finance_db(
    query="新能源汽车行业竞争格局，市场份额和主要竞争对手",
    date_range="past_year",
    recall_num=15,
    doc_type="report"
)
```

### Return Format

Returns JSON with list of results, each containing:
- `title`: Document title
- `file_id`: Unique identifier
- `publish_date`: Publication date
- `type_full_name`: Document type
- `institution_name`: Publishing institution
- `company_name`: Related company
- `section`: Relevant text excerpt

---

## 2. info_search_stock_db

**Full name**: `mcp__ashare-mcp-research__info_search_stock_db`

**Purpose**: Query quantitative financial and market data for companies (A-share, Hong Kong, US markets).

### Critical Requirement

**EVERY query MUST include THREE elements**:
1. **Time specification** (absolute or relative)
2. **Company name** (clear identification)
3. **One specific metric** (only query ONE metric per call)

### Parameters

```python
{
    "query": str  # Natural language query with time, company, and ONE metric (REQUIRED)
}
```

### Time Expressions

**Absolute time**:
- Specific years: "2024年", "2023年"
- Quarters: "2023年Q1", "2024年Q4"
- Months: "2024年3月"
- Dates: "2024-01-15"

**Relative time**:
- Recent: "最近", "最新", "近期"
- Past periods: "过去N天/周/月/年"
- Current periods: "本季度", "今年"
- Previous periods: "上季度", "去年"
- Time ranges: "2023年Q1至Q4", "最近三个月", "过去一年"

### Supported Metrics

**Profitability**:
- ROE (净资产收益率)
- 净利润率
- 毛利率
- 营业利润率

**Growth**:
- 营收同比增长
- 净利润同比增长
- EPS增长率

**Leverage**:
- 资产负债率
- 流动比率
- 速动比率

**Cash flow**:
- 经营现金流/营收比率
- 自由现金流

**Market data**:
- 开盘价, 最高价, 最低价, 收盘价
- 成交量, 成交额
- 市盈率(PE), 市净率(PB)
- 市值

**Business metrics**:
- 研发投入, 研发占营收比
- 分红, 每股股利
- 各业务板块收入

**Macro indicators**:
- 利率 (interest rates)
- SHIBOR
- 货币供应量 (M1, M2)
- GDP增长率

### Usage Examples

**Example 1: Single year profitability**
```python
mcp__ashare-mcp-research__info_search_stock_db(
    query="2024年比亚迪的ROE是多少?"
)
```

**Example 2: Time series data**
```python
mcp__ashare-mcp-research__info_search_stock_db(
    query="检索苹果公司2023年Q1至Q4的季度营收"
)
```

**Example 3: Relative time**
```python
mcp__ashare-mcp-research__info_search_stock_db(
    query="最近腾讯的股价走势"
)
```

**Example 4: Year-over-year comparison**
```python
mcp__ashare-mcp-research__info_search_stock_db(
    query="阿里巴巴过去一年的营收增长率"
)
```

**Example 5: Business metric**
```python
mcp__ashare-mcp-research__info_search_stock_db(
    query="2023年宁德时代的研发投入占营收比例"
)
```

### Important Notes

1. **One metric per query**: If you need multiple metrics, make multiple queries in parallel
2. **Clear company identification**: Use official company names
3. **Time specificity**: Be explicit about time periods
4. **Market coverage**: Supports A-share (A股), Hong Kong (港股), US (美股)

### Return Format

Returns JSON with a `text` field containing the query results.

---

## 3. info_search_user_db

**Full name**: `mcp__ashare-mcp-research__info_search_user_db`

**Purpose**: Search within user-uploaded documents for private research materials.

### Parameters

```python
{
    "query": str,           # Natural language search query (REQUIRED)
    "user_id": int,         # User identifier (REQUIRED)
    "file_ids": list[int],  # List of file IDs to search (REQUIRED)
    "recall_num": int       # Number of results (optional, default: 10)
}
```

### Parameter Details

#### query (REQUIRED)
Natural language description of information needed from user documents.

#### user_id (REQUIRED)
User's unique identifier (integer).

#### file_ids (REQUIRED)
List of file IDs (integers) to search within. Must specify which documents to search.

#### recall_num (optional, default: 10)
Number of results to return (5-20 typically sufficient).

### Usage Example

```python
mcp__ashare-mcp-research__info_search_user_db(
    query="这些研报中对特斯拉2025年交付量的预测",
    user_id=12345,
    file_ids=[101, 102, 103, 104],
    recall_num=10
)
```

### Return Format

Returns JSON with list of results containing:
- `title`: Document title
- `file_id`: File identifier
- `publish_date`: Date (if available)
- `section`: Relevant excerpt

### When to Use

- User explicitly mentions their uploaded documents
- Research requires proprietary/internal materials
- Need to reference specific files user has provided

---

## 4. info_search_web

**Full name**: `mcp__ashare-mcp-research__info_search_web`

**Purpose**: Web search for information not available in the financial database.

### Parameters

```python
{
    "query": str  # Natural language search query (REQUIRED)
}
```

### When to Use

Use as a **FALLBACK** when:
- Financial database lacks sufficient data
- Need very recent information (last few hours/days)
- Looking for non-China market information
- Seeking alternative perspectives or data sources
- Comparative company data not in database

**Preference**: Always try `info_search_finance_db` or `info_search_stock_db` FIRST before falling back to web search.

### Usage Example

```python
mcp__ashare-mcp-research__info_search_web(
    query="特斯拉及其可比公司（行业竞争对手）的最新估值对比，包括PE、PB等估值指标"
)
```

### Return Format

Returns JSON with:
- `answer`: Synthesized answer from web sources
- `references`: List of source URLs and titles

---

## Tool Selection Decision Tree

```
START: What type of information do I need?

├─ Qualitative analysis (reports, news, analyst views)
│  ├─ User's private documents?
│  │  └─ YES → info_search_user_db
│  └─ NO → info_search_finance_db
│
├─ Quantitative data (metrics, financials, market data)
│  └─ info_search_stock_db
│
└─ Information likely missing from database
   └─ info_search_web (fallback)
```

## Query Optimization Best Practices

### 1. Parallel Execution
When multiple queries are independent, execute them in parallel:

```python
# GOOD: All 5 queries in parallel
Task(subagent_type="general-purpose",
     prompt="Execute these 5 queries in PARALLEL (single message):\n1. Query A\n2. Query B...")

# BAD: Sequential queries
Task 1 → wait → Task 2 → wait → Task 3...
```

### 2. Right-sizing recall_num
Don't over-retrieve:

```python
# Fact checking: 5-8 results
recall_num=8

# Standard analysis: 10-15 results
recall_num=12

# Comprehensive research: 15-20 results
recall_num=15
```

### 3. Appropriate date_range
Match the analysis timeframe:

```python
# Short-term (1-3 months)
date_range="past_quarter"

# Medium-term (6 months)
date_range="past_half_year"

# Long-term (1-3 years)
date_range="past_year"
```

### 4. Specific doc_type
Use filters to get higher quality results:

```python
# For in-depth analysis
doc_type="report"

# For management views
doc_type="summary"

# For foreign perspective
doc_type="foreign_report"
```

### 5. One metric per stock_db query
Break down complex requests:

```python
# BAD: "特斯拉2024年的ROE和净利润率"
# GOOD: Two parallel queries
Query 1: "2024年特斯拉的ROE"
Query 2: "2024年特斯拉的净利润率"
```

---

## Common Patterns

### Pattern 1: Company Recent Updates
```python
info_search_finance_db(
    query=f"{company}公司近况,股价异动、财报披露、产品业务、战略调整",
    date_range="past_quarter",
    recall_num=10
)
```

### Pattern 2: Investment Logic (Short-term)
```python
info_search_finance_db(
    query=f"{company}短期投资逻辑(1-3月),从业务价值出发",
    date_range="past_quarter",
    recall_num=12,
    doc_type="report"
)
```

### Pattern 3: Investment Logic (Long-term)
```python
info_search_finance_db(
    query=f"{company}长期投资逻辑(1-3年),从业务价值出发",
    date_range="past_year",
    recall_num=12,
    doc_type="report"
)
```

### Pattern 4: Risk Analysis
```python
info_search_finance_db(
    query=f"{company}核心风险分析",
    date_range="past_half_year",
    recall_num=8
)
```

### Pattern 5: Industry Competitive Landscape
```python
info_search_finance_db(
    query=f"{industry}竞争格局,市场份额,主要竞争对手",
    date_range="past_year",
    recall_num=15,
    doc_type="report"
)
```

### Pattern 6: Financial Metrics Time Series
```python
info_search_stock_db(
    query=f"{company}2022至2024年的年度营业收入"
)
```

### Pattern 7: Valuation Comparison
```python
# First try finance_db
info_search_finance_db(
    query=f"{company}可比公司估值对比,PE、PB等估值指标",
    date_range="past_year",
    recall_num=10,
    doc_type="report"
)

# If insufficient, fallback to web
info_search_web(
    query=f"{company}及其可比公司最新估值对比，包括PE、PB"
)
```

---

## Error Handling

### Insufficient Results
- If recall_num too low, increase it (try +5)
- If date_range too narrow, expand it
- Try removing doc_type filter
- Consider web search fallback

### Ambiguous Companies
- Use full official names
- Include market specification (A股/港股/美股) if ambiguous
- Verify company identification with user if uncertain

### Missing Data
- Note gaps explicitly in report
- Use "-" in tables for missing values
- Document data limitations in methodology notes
- Try alternative data sources (web search)

---

## Summary

**Tool selection**:
- Qualitative → `info_search_finance_db`
- Quantitative → `info_search_stock_db`
- User docs → `info_search_user_db`
- Fallback → `info_search_web`

**Optimization principles**:
- Maximize parallelization
- Right-size recall_num
- Use appropriate date_range
- Filter with doc_type when relevant
- One metric per stock_db query

**Quality checks**:
- Verify all required parameters present
- Confirm query clarity and specificity
- Validate time specifications
- Check for dependencies before parallelizing
