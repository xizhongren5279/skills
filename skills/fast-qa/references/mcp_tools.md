# MCP Tools Reference

Complete documentation for all available MCP retrieval tools.

## Tools Overview

| Tool | Purpose | Data Source |
|------|---------|-------------|
| `info_search_finance_db` | Research reports, announcements, news, analyst comments | Financial database |
| `info_search_stock_db` | Financial metrics, market data (listed companies) | Structured data |
| `info_search_user_db` | User-uploaded private documents | User knowledge base |
| `info_search_web` | Web search fallback | Online sources |

---

## 1. info_search_finance_db

**Full name**: `mcp__ashare-mcp-research__info_search_finance_db`

**Purpose**: Search financial database for research reports, company announcements, analyst comments, news, and qualitative financial content.

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | str | YES | - | Natural language search query |
| `date_range` | str | no | None | Time filter |
| `recall_num` | int | no | 15 | Number of results |
| `doc_type` | str | no | None | Document type filter |

### date_range Options

| Value | Meaning | Use Case |
|-------|---------|----------|
| `"all"` | All time | Historical analysis, unfamiliar topics |
| `"past_day"` | Last 24h | Breaking news |
| `"past_week"` | Last 7 days | Recent developments |
| `"past_month"` | Last 30 days | Recent trends |
| `"past_quarter"` | Last 3 months | Latest quarterly report, short-term |
| `"past_half_year"` | Last 6 months | Medium-term, last 2 quarterly reports |
| `"past_year"` | Last 12 months | Annual analysis (DEFAULT) |

### doc_type Options

| Value | Type | Content |
|-------|------|---------|
| `"report"` | Research reports | Strategy, company, industry, macro, bond research (CORE type — include in every search) |
| `"summary"` | Meeting summaries | Earnings calls, expert calls, analyst meetings |
| `"company_all_announcement"` | Announcements | Filings, IPOs, financing, official disclosures |
| `"comments"` | Analyst comments | Quick takes, commentary from brokers |
| `"news"` | News | Short-form financial news from third parties |
| `"foreign_report"` | Foreign research | International analyst reports |
| `"all"` | All types | Use when uncertain about which type |

**doc_type selection rule**: Always combine `"report"` with 1+ other types. Use `"all"` only when you truly cannot determine which types to search.

### Query Rules

- One company per query — split multi-company queries
- For unfamiliar topics: set `date_range="all"` and `doc_type="all"`
- Cross-time-period analysis: use a single query with time range, not multiple queries

### Examples

```python
# Company recent updates
info_search_finance_db(query="特斯拉公司近况 股价异动 财报披露 业务变化", date_range="past_quarter", recall_num=10)

# Investment logic
info_search_finance_db(query="英伟达长期投资逻辑 业务价值分析", date_range="past_year", recall_num=12, doc_type="report")

# Risk analysis
info_search_finance_db(query="比亚迪核心风险分析", date_range="past_half_year", recall_num=8)

# Industry research
info_search_finance_db(query="新能源汽车行业竞争格局 市场份额", date_range="past_year", recall_num=15, doc_type="report")
```

### Return Format

JSON list with: `title`, `file_id`, `publish_date`, `type_full_name`, `institution_name`, `company_name`, `section`

---

## 2. info_search_stock_db

**Full name**: `mcp__ashare-mcp-research__info_search_stock_db`

**Purpose**: Query quantitative financial and market data for listed companies (A-share, Hong Kong, US markets).

### Critical Rule

**EVERY query MUST include THREE elements**:
1. **Time** (absolute or relative)
2. **Company name**
3. **ONE metric category**

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | str | YES | Natural language query with time + company + metric |

### Supported Metrics

- **Profitability**: ROE, net profit margin, gross margin
- **Growth**: Revenue YoY growth, net profit YoY growth
- **Leverage**: Debt-to-asset ratio, current ratio, quick ratio
- **Cash flow**: Operating cash flow / revenue ratio
- **Market data**: Open/high/low/close prices, volume, PE, PB, market cap
- **Business metrics**: R&D spend, R&D-to-revenue ratio, dividends
- **Segment data**: Revenue/profit by product line, by region
- **Macro**: Interest rates, SHIBOR, money supply (M1, M2)

### Query Rules

- **Same-category metrics can share one query**: e.g., "2023年苹果公司的营业收入、净利润、毛利率" (all profitability)
- **Different categories require separate queries**: e.g., profitability vs dividends
- **One company per query**: Multi-company = multiple parallel queries
- **Prefer time ranges**: "比亚迪2020至2024年ROE趋势" rather than querying each year
- **Time format**: Use "年/月/日" words explicitly, not just numbers
- **Total calls across all rounds**: max 4

### Cross-Market Data Caveats

- **A-share**: Most complete data coverage — profitability, valuation, market data all available
- **Hong Kong stocks**: Some metrics (e.g., PE) may not be returned. Fallback: use `info_search_finance_db` for analyst report data
- **US stocks**: Generally good coverage but check fiscal year alignment (some US companies have non-calendar fiscal years)
- **Currency**: Results are in local currency (CNY for A-share, HKD for HK, USD for US). Always note units when comparing

### Examples

```python
info_search_stock_db(query="2024年比亚迪的ROE是多少?")
info_search_stock_db(query="苹果公司2023年Q1至Q4的季度营收")
info_search_stock_db(query="最近腾讯的股价走势")
info_search_stock_db(query="宁德时代2022至2024年的营业收入和净利润")
```

### Return Format

JSON with `text` field containing query results.

---

## 3. info_search_user_db

**Full name**: `mcp__ashare-mcp-research__info_search_user_db`

**Purpose**: Search user-uploaded private documents.

**Activation condition**: ONLY when user explicitly references their documents (e.g., "我的知识库", "我上传的报告", "结合我的文档").

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | str | YES | - | Natural language search query |
| `user_id` | int | YES | - | User identifier |
| `file_ids` | list[int] | YES | - | File IDs to search |
| `recall_num` | int | no | 10 | Number of results |

### Return Format

JSON list with: `title`, `file_id`, `publish_date`, `section`

---

## 4. info_search_web

**Full name**: `mcp__ashare-mcp-research__info_search_web`

**Purpose**: Web search — use as FALLBACK only when internal databases lack data.

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | str | YES | Natural language search query |

### When to Use

- `info_search_finance_db` returned insufficient results
- Need very recent information (last few hours)
- Non-China market data not in database
- Supplementary perspectives

**Never use as first choice for financial data.**

### Return Format

JSON with `answer` (synthesized) and `references` (source URLs).

---

## Error Handling

- **Insufficient results**: Increase `recall_num` (+5), expand `date_range`, remove `doc_type` filter, try web fallback
- **Ambiguous company**: Use full official name, specify market (A股/港股/美股)
- **Missing data**: Note gaps in answer, use "-" in tables, try alternative sources
- **Metric not returned by stock_db** (e.g., PE missing for HK stock):
  1. Fallback to `info_search_finance_db(query="XX公司 估值分析 PE 市盈率", doc_type="report")` — analyst reports often contain these
  2. If still missing, try `info_search_web(query="XX公司 最新PE 市盈率")`
  3. If unavailable from all sources, note in answer: "XX指标暂无数据"
- **Data anomaly** (e.g., a metric showing implausible values):
  1. Cross-verify with `info_search_finance_db` earnings report data
  2. If discrepancy confirmed, flag in answer and prefer the research report figure
  3. Common causes: data scope mismatch (quarterly vs annual), delayed data update, formula differences across data providers
