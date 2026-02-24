# Search Strategy & Query Optimization

Detailed tool selection decision tree, parallel execution patterns, and query optimization rules for fast-qa retrieval.

## Tool Selection Decision Tree

```
For each sub-question:
├── Quantitative Financial Data? (ratios, prices, numerical metrics)
│   ├── YES → Listed company or market index?
│   │         ├── YES → Primary: info_search_stock_db
│   │         │         ├── One metric category per query
│   │         │         ├── Secondary: info_search_finance_db
│   │         │         └── Fallback: info_search_web
│   │         └── NO  → Skip info_search_stock_db
│   │                   → Use: info_search_finance_db
│   │                   └── Fallback: info_search_web
│   └── NO → Qualitative Information
│            ├── User explicitly references personal docs?
│            │   ├── YES → Step 1: info_search_user_db
│            │   │         └── If empty → Step 2: info_search_finance_db
│            │   │                        └── If insufficient → Step 3: info_search_web
│            │   └── NO  → Step 1: info_search_finance_db
│            │             └── If insufficient → Step 2: info_search_web
│            └── All paths: Use info_search_web ONLY after internal sources fail
```

## Selection Priority Order

```
info_search_finance_db (primary, always start here for qualitative)
    → info_search_stock_db (for quantitative metrics of listed companies)
        → info_search_web (fallback only)
```

**Special cases:**
- Company operational data (orders, top 5 customers/suppliers): `info_search_finance_db` first, NOT `info_search_stock_db`
- AI company capital expenditure: `info_search_finance_db`
- Theme-based stock screening (e.g., "which stocks benefit from X?"): `info_search_finance_db` only, NEVER `info_search_stock_db`
- Simple data query → Still use `info_search_finance_db` for context analysis beyond just the number

## Parallel Execution Rules

### Dependency Check Algorithm

Before each retrieval round, for all planned tool calls check:
**"Does Call B's parameters depend on Call A's output?"**

- **NO (independent)** → MUST execute in parallel (same message)
- **YES (dependent)** → Execute serially (wait for prior result)

### Parallel Patterns

**Pattern A: Entity Comparison**
User: "对比阿里和腾讯的PE和2023年净利润"
```
Round 1 (all parallel):
  info_search_stock_db(query="阿里巴巴 PE")
  info_search_stock_db(query="腾讯控股 PE")
  info_search_stock_db(query="阿里巴巴 2023年净利润")
  info_search_stock_db(query="腾讯控股 2023年净利润")
```

**Pattern B: Multi-dimensional Evidence**
User: "分析特斯拉的股价表现和最近的负面新闻"
```
Round 1 (parallel, cross-tool):
  info_search_stock_db(query="特斯拉 近一个月 股价走势")
  info_search_finance_db(query="特斯拉 负面新闻 安全事故 召回", doc_type="news")
```

**Pattern C: Serial Dependency (The Exception)**
User: "查宁德时代最大供应商的最新财报"
```
Round 1: info_search_finance_db(query="宁德时代 第一大供应商 名称")
  → Wait for result: "XX公司"
Round 2: info_search_finance_db(query="XX公司 最新财报")
```

**When first hop fails** (no clear intermediate answer):
```
Round 1: info_search_finance_db(query="宁德时代 第一大供应商 名称")
  → Result: channel strategy reports, no specific name
Round 1 retry: info_search_finance_db(query="宁德时代 前五大供应商 年报披露", date_range="all")
  → Still unclear?
Round 2 fallback: info_search_web(query="宁德时代最大供应商是谁")
  → Still no answer? → Inform user: "数据库中未找到该信息" + provide related context found
```

**Pattern D: Compound Question (Industry + Companies)**
User: "光伏行业是否到底了？隆基和通威值得买吗？"
```
Round 1 (all parallel):
  info_search_finance_db(query="光伏行业 周期底部 产能过剩 供需", doc_type="report")
  info_search_finance_db(query="隆基绿能 投资价值 分析", doc_type="report")
  info_search_finance_db(query="通威股份 投资价值 分析", doc_type="report")
```
Note: Industry query and each company query are independent → all parallel.

**Pattern E: Macro-Company Intersection**
User: "美联储降息对中国房地产龙头有什么影响？"
```
Round 1 (parallel, split macro from sector):
  info_search_finance_db(query="美联储降息 新兴市场 资金流向 利率传导 影响")
  info_search_finance_db(query="中国房地产龙头 保利发展 万科 销售 融资成本")
```
NEVER combine "美联储降息" and "中国房地产" in a single query — results will be off-topic.

**Pattern F: Cross-Market Comparison**
User: "对比腾讯和Meta的PE和市值"
```
Round 1 (parallel):
  info_search_stock_db(query="腾讯控股 2025年 PE和市值")
  info_search_stock_db(query="Meta Platforms 2025年 PE和市值")
```
If one entity has missing metrics (e.g., Tencent PE not returned):
```
Round 2 (fallback):
  info_search_finance_db(query="腾讯控股 估值分析 PE 市盈率", doc_type="report")
```
Always note currency differences in the answer (HKD vs USD).

## Retrieval Round Limits

### Round Budget

| Round | info_search_stock_db | Other tools | Max total |
|-------|---------------------|-------------|-----------|
| Round 1 | Up to 4 | Up to 2 | 6 |
| Round 2+ | 0 | Up to 2 | 2 |

- **Total rounds**: target 3, max 5
- **Total info_search_stock_db calls**: max 4 across ALL rounds
- If Round 1 used 4 stock_db calls, no more in subsequent rounds

### When to Use Only info_search_stock_db

When a round uses ONLY `info_search_stock_db` (no other tools), up to 6 parallel calls are allowed to maximize efficiency.

## Query Optimization

### Query Construction Rules

1. **Explicit subject**: Every query names the specific company/index
2. **Explicit time**: Use "年/月/日" words — "2024年" not "2024", "2024年3月" not "2024-03"
3. **Time ranges**: Use "XX至XX年" format for spans
4. **One entity per query**: "宁德时代 2024年营收" not "宁德时代和比亚迪 2024年营收"
5. **Specific over vague**: Include concrete indicators rather than broad topics
6. **Cross-period analysis**: Use a single query with time range, not separate queries per period

### recall_num Guidelines

| Use Case | recall_num |
|----------|-----------|
| Quick fact-check | 5-8 |
| Standard analysis | 10-15 |
| Comprehensive research | 15-20 |
| Company news/updates | 8-10 |
| Investment logic | 12-15 |
| Risk analysis | 5-8 |

### date_range Selection

| Analysis Timeframe | date_range |
|-------------------|-----------|
| Breaking news | `"past_week"` or `"past_day"` |
| Recent developments | `"past_quarter"` |
| Short-term logic | `"past_quarter"` to `"past_half_year"` |
| Medium-term trends | `"past_half_year"` |
| Long-term logic | `"past_year"` |
| Historical/unfamiliar topic | `"all"` |
| Latest quarterly report | `"past_quarter"` |
| Latest two quarterly reports | `"past_half_year"` |

### info_search_stock_db Query Patterns

**Same-category metrics → single query:**
```python
# Good: profitability metrics in one query
info_search_stock_db(query="2023年苹果公司的营业收入、净利润、毛利率")
```

**Different-category metrics → separate queries:**
```python
# Profitability vs dividends → two queries in parallel
info_search_stock_db(query="2023年苹果公司的营业收入、净利润、毛利率")
info_search_stock_db(query="2023年苹果公司的分红")
```

**Traversal pattern for index tracking:**
User: "写一个2025年四季度的市场点评，参考这些指标：万得全A、沪深300、上证指数"
```python
# Parallel queries for each index
info_search_stock_db(query="2025年第四季度万得全A指数的点位")
info_search_stock_db(query="2025年第四季度沪深300指数的点位")
info_search_stock_db(query="2025年第四季度上证指数的点位")
```

## stock_db Quota Management

`info_search_stock_db` is limited to **4 calls total**. When comparing 3+ companies across multiple metric categories, 4 calls may not be enough.

### Prioritization Strategy

1. **Core metrics first**: Use stock_db for profitability (营收/净利润/毛利率) and growth (YoY) — these are stock_db's strength
2. **Merge same-category**: "营收、净利润、毛利率" in one query = 1 call, not 3
3. **Valuation from finance_db**: PE, PB, market cap often appear in analyst reports — use `info_search_finance_db(query="XX公司 估值分析 PE PB 市盈率", doc_type="report")` instead of stock_db
4. **Dividends from finance_db**: Dividend data frequently in earnings reports — use `info_search_finance_db(query="XX公司 分红 股利 派息", doc_type="company_all_announcement")`

### Example: 4-company comparison, 2 metric categories

User: "对比宁德时代、比亚迪、国轩高科、亿纬锂能的盈利和估值"
```
Round 1 (4 stock_db calls — used up quota):
  info_search_stock_db(query="宁德时代 2024年 营收、净利润、毛利率")
  info_search_stock_db(query="比亚迪 2024年 营收、净利润、毛利率")
  info_search_stock_db(query="国轩高科 2024年 营收、净利润、毛利率")
  info_search_stock_db(query="亿纬锂能 2024年 营收、净利润、毛利率")

Round 2 (stock_db exhausted, use finance_db for valuation):
  info_search_finance_db(query="锂电池行业龙头 估值对比 PE PB", doc_type="report")
```

## Theme-based Stock Screening

Theme queries (e.g., "哪些公司受益于X政策/趋势？") often return policy analysis instead of stock picks if the query is too broad.

### Two-round Strategy

**Round 1 — Background**: Broad query to understand the theme
```python
info_search_finance_db(query="碳中和 十五五 政策方向 投资主线", date_range="past_quarter", doc_type="report")
```

**Round 2 — Targets**: Specific query for beneficiary stocks
```python
info_search_finance_db(query="碳中和 受益龙头股 推荐标的 重点公司", date_range="past_quarter", doc_type="report")
```

### Query Keyword Tips

| Goal | Good keywords | Bad keywords (too broad) |
|------|--------------|------------------------|
| Find stock picks | "受益标的", "推荐", "龙头股", "重点公司" | "公司", "企业", "产业" |
| Find competitive landscape | "竞争格局", "市场份额", "龙头对比" | "行业分析", "发展趋势" |
| Find earnings impact | "业绩弹性", "利润影响", "营收增量" | "影响", "变化" |

## Cross-Market Comparison Notes

When comparing companies across markets (A股 vs 港股 vs 美股):

1. **Currency awareness**: Always note currency — HKD, USD, CNY. Convert to same base for meaningful comparison (approximate rates are acceptable)
2. **Data field differences**: Hong Kong stocks may have fewer metric fields than A-shares or US stocks in stock_db. If a metric is missing:
   - Fallback 1: `info_search_finance_db` with "XX公司 估值 PE" — analyst reports often contain these
   - Fallback 2: `info_search_web` for real-time market data
3. **Company names**: Use market-specific official names:
   - A股: "贵州茅台", "比亚迪"
   - 港股: "腾讯控股", "美团-W"
   - 美股: "Meta Platforms", "Tesla"
4. **Fiscal year differences**: Some US companies have non-calendar fiscal years (e.g., Apple FY ends Sep). Note this in comparisons

## Data Anomaly Detection

When reviewing stock_db results, check for:

1. **Implausible swings**: >30% change in a normally stable metric (e.g., gross margin) between adjacent periods without known cause → likely data error or scope mismatch
2. **Scope mismatch**: Annual vs quarterly vs cumulative data mixed in results — verify data_date alignment
3. **Zero or null values**: May indicate data not yet disclosed rather than actual zero

### Verification workflow
```
Anomaly detected (e.g., gross margin dropped from 25% to 15% in one year)
  → Round N+1: info_search_finance_db(query="XX公司 YYYY年 毛利率 变化原因", doc_type="report")
  → If report confirms the change: report it with explanation
  → If report shows different number: flag stock_db data as potentially inaccurate, use report data
```

## Verification Requirements

- Cross-validate quantitative results across tools
- Ensure comprehensive coverage before concluding
- Never use `info_search_user_db` unless user explicitly references their documents
- Check data anomalies before reporting (see Data Anomaly Detection above)
- In cross-market comparisons, ensure currency units are noted and metrics are symmetric
