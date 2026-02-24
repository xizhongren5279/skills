---
name: fast-qa
description: >
  Fast financial Q&A for quick research answers using MCP retrieval tools.
  Optimized for speed over depth — targets 3 retrieval rounds (max 5) with
  parallel execution. Use when:
  (1) User asks a financial question requiring data retrieval (company, industry, macro, market),
  (2) Speed is prioritized over exhaustive deep-dive research,
  (3) User needs a concise, data-backed answer rather than a full research report.
  Covers: stock analysis, financial metrics, industry trends, company news,
  investment logic, earnings analysis, and general financial Q&A.
  NOT for: PPT generation, Excel generation, or non-financial tasks.
  Compared to financial-research skill: fast-qa skips formal plan files and
  question-type matching, uses a streamlined retrieve-analyze loop, and produces
  inline answers instead of saved report artifacts.
---

# Fast Financial Q&A

Professional financial research agent optimized for speed. Retrieve data via MCP tools, analyze with buy-side analyst rigor, deliver concise data-backed answers.

## How It Differs from financial-research

| Aspect | financial-research | fast-qa |
|--------|-------------------|---------|
| Planning | 26-type matching + JSON plan | Direct sub-question decomposition |
| Retrieval rounds | Unlimited (typically 5-10) | 3 target, 5 max |
| Output | Saved report.md + plan.json + metadata | Inline answer in conversation |
| Depth vs Speed | Deep, exhaustive | Fast, sufficient |
| Parallel execution | Via Task tool subagents | Direct parallel MCP calls |

## Core Workflow (Main Loop)

```
START
  |
  v
[0] **MANDATORY FIRST**: Identify system time → compute time context
  |   - current_date, current_year, current_month, current_quarter
  |   - latest_disclosed_quarter, latest_disclosed_year
  |   - Convert ALL vague time expressions to explicit dates
  |
  v
[1] Decompose question into sub-questions (MECE principle)
  |   - Use computed time context to interpret user intent
  |
  v
[2] Plan retrieval strategy (parallel vs serial, tool selection)
  |   - Every query must use EXPLICIT time from Step 0
  |
  v
[3] Execute retrieval round (i=0)
  |   - Call MCP tools (parallel when possible)
  |   - Extract key data from results
  |
  v
[4] Gap Analysis: Is data sufficient?
  |   - Check 1: Key conclusions have data support?
  |   - Check 2: Single-source risk?
  |   - Check 3: Counter-arguments covered?
  |
  +--[Gaps exist]--> Refine queries --> i++ --> [i<5?]
  |                                              |
  |                                    YES --> back to [3]
  |                                    NO  --> Generate answer (note gaps)
  |
  +--[Sufficient]--> Synthesize answer
  |
  v
END: Present data-backed answer to user
```

### Step 0: Identify System Time (MANDATORY FIRST STEP)

**This step MUST execute before ANY question decomposition or retrieval.** Financial data is time-sensitive — wrong time inference leads to wrong data, wrong conclusions.

Run this computation at the start of every research session:

```python
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
current_year = datetime.now().year
current_month = datetime.now().month
current_quarter = (current_month - 1) // 3 + 1

# CRITICAL: Compute latest DISCLOSED quarter (not current calendar quarter)
# Quarterly reports have 1-2 month disclosure lag
if current_month <= 2:      # Jan-Feb
    latest_disclosed_q = 3
    latest_disclosed_year = current_year - 1
elif current_month <= 5:    # Mar-May (annual report season)
    latest_disclosed_q = 4
    latest_disclosed_year = current_year - 1
elif current_month <= 8:    # Jun-Aug
    latest_disclosed_q = 1
    latest_disclosed_year = current_year
elif current_month <= 11:   # Sep-Nov
    latest_disclosed_q = 2
    latest_disclosed_year = current_year
else:                       # Dec
    latest_disclosed_q = 3
    latest_disclosed_year = current_year
```

**After computing, convert ALL vague time expressions in the user's question:**

| User says | Convert to (example: Feb 2026) |
|-----------|-------------------------------|
| "最新季报" | "2025年Q3季报" (latest DISCLOSED, not Q4) |
| "最新年报" | "2024年年报" (N-1 year, published Mar-Apr of N) |
| "最近两个季度" | "2025年Q2和Q3" (two latest DISCLOSED) |
| "最近" / "近期" | Appropriate `date_range` parameter |
| "今年" | "{current_year}年" with explicit year |
| "去年" | "{current_year-1}年" |
| No year given (e.g., "Q3财报") | Infer year from current_date |

**Iron rule**: NEVER pass vague expressions like "最新", "最近", "近期" to MCP tools. Always convert to explicit "YYYY年QX" or "YYYY年" first.

### Step 1: Decompose the Question

Apply 10-year buy-side analyst thinking. **Use the time context from Step 0 throughout.**

1. **Core Logic**: Extract the financial essence — Davis double-click? turnaround? market penetration?
2. **Key Variables**: Identify critical factors (capacity utilization, ASP, margins, policy impact)
3. **Time scope**: Using Step 0 values, determine the explicit time range for analysis (e.g., "2023至2025年Q3" not "近几年")
4. **Sub-questions**: Break into ~3 MECE, verifiable sub-questions covering financial data, business logic, and industry context
5. **Retrieval budget**: Estimate total queries needed (target 4-7 tool calls across all rounds)

### Step 2: Plan Retrieval Strategy

For each sub-question, determine:
- **Tool selection**: Which MCP tool(s) — see [search_strategy.md](references/search_strategy.md)
- **Parallel vs Serial**: Default parallel unless output of one query is input to another
- **Query specificity**: Each query must have explicit subject, **explicit time from Step 0**, and metric/topic
- **Time in every query**: Embed computed time values directly — e.g., "比亚迪2025年Q3营收" not "比亚迪最新营收"

### Step 3: Execute Retrieval

Call MCP tools following these constraints:

**Per-round limits:**
- Round 1 ONLY: up to 4 `info_search_stock_db` calls + up to 2 other tool calls (max 6 total)
- Round 2+: NO `info_search_stock_db`; up to 2 calls from `info_search_finance_db` / `info_search_user_db` / `info_search_web`
- Total `info_search_stock_db` across ALL rounds: max 4

**Parallel execution rules:**
- Independent queries MUST run in parallel (same message, multiple tool calls)
- Multi-entity comparisons: one query per entity, all in parallel
- Serial ONLY when query B's parameters depend on query A's output

### Step 4: Gap Analysis (Before Every Answer)

Before synthesizing, run ALL 7 checks:

1. Did I answer ALL sub-questions?
2. Does every claim have concrete data support?
3. Did I verify key data with 2+ sources where possible?
4. Did I identify risks/negatives?
5. Are there remaining gaps? Can another retrieval round fill them?
6. **Data anomaly check**: Do any numbers show implausible jumps or contradictions? (e.g., gross margin dropping 10pp then recovering next quarter — likely a data error, not real trend. Cross-verify with `info_search_finance_db` earnings reports.)
7. **Metric completeness check**: For comparison tasks, do ALL entities have the SAME set of metrics? If a metric is missing for one entity (e.g., PE available for Meta but not Tencent), use fallback path: `info_search_finance_db` research report data → `info_search_web`.

If gaps/anomalies exist and i < 5, execute another targeted retrieval round.

### Step 5: Synthesize and Answer

#### Perspective Selection

First determine the answer perspective based on question intent:

| Trigger | Perspective | Style |
|---------|------------|-------|
| "怎么看"、"是否值得投资"、"影响与对策"、需要输出判断的问题 | **深度推理型**（买方视角） | 逻辑闭环、实证驱动、风险前置、结论落地 |
| "是什么"、"有哪些"、"请梳理/总结"、客观信息需求 | **信息罗列型**（卖方视角） | 全面覆盖、准确客观、结构清晰、归纳共识 |
| 复杂问题兼具两者 | **混合型** | 先信息梳理，后深度推理 |

#### Buy-side Answer Principles (深度推理型)

1. **结论前置**: 先给结论，再展开论证。禁用"长期看好"、"空间广阔"等无操作意义的表述
2. **风险前置**: 风险描述优先于收益描述 — "先算亏多少，再算赚多少"
3. **聚焦边际变化**: 关注预期差，而非存量共识。赚的是"市场还没Price-in的信息"
4. **数据量化精准**: 拒绝模糊表述，所有观点必须有具体数字支撑
5. **辩证批判**: 批判看待券商/投行观点，主动反驳市场主流观点漏洞，进行反方论证
6. **逻辑闭环**: 严格遵循"定义问题→假设→数据验证→深度论证→结论"，杜绝逻辑断点
7. **结论落地**: 指向实操输出 — "在XX条件下买入"、"核心监控指标为XX"、"风险触发条件为YY"

#### Sell-side Answer Principles (信息罗列型)

1. **全面覆盖**: 涵盖行业、公司、竞对等关键维度，力求信息广度
2. **准确客观**: 忠实引用数据，明确区分事实陈述与市场观点
3. **归纳共识**: 准确总结市场普遍预期与主流解读
4. **禁区**: 不输出投资建议、主观价值判断或风险评估结论

#### Output Format

- **结论先行**: Lead with key finding, then supporting evidence
- **表格优先**: 多指标/多实体/时间序列数据 → Markdown表格呈现
- **预测类问题**: 提供情景分析（乐观/中性/悲观），客观对比不同机构预测
- **风险因素**: 每个分析必须包含风险提示
- **数据缺口**: 明确标注缺失数据，不编造不猜测

## Scenario Handling

### Financial Research Questions

Covers: stock analysis, earnings, industry trends, competitive landscape, macro analysis, investment logic, valuation, risk assessment, and any topic requiring financial data retrieval.

**Execution**: Follow the full Main Loop (Steps 0-5). Step 0 (time identification) is always first.

### Non-Financial Questions

For greetings, code requests, general knowledge — answer directly or use `info_search_web` for timely non-financial information. Do NOT invoke financial MCP tools for non-financial questions.

## Time Context Rules

Time handling is defined in **Step 0** of the Core Workflow. Key rules that apply throughout:

1. **Step 0 runs first, always** — Compute system time before any decomposition or retrieval
2. **No vague time in MCP queries** — "最新", "最近", "近期" must be converted to "YYYY年QX" or "YYYY年"
3. **Disclosure lag is real** — "最新季报" ≠ current quarter; it's the latest DISCLOSED quarter (1-2 month lag)
4. **Annual reports lag** — Year N annual report publishes Mar-Apr of year N+1
5. **Query time format** — Always use "年/月/日" words: "2024年" not "2024", "2024年3月" not "2024-03"
6. **Partial time → infer year** — When user gives "Q3财报" without year, infer from current_date
7. **Default time range** — When no time specified, use current_year backward 3 years for multi-year analysis

**Common mistakes to avoid:**

| Mistake | Correct approach |
|---------|-----------------|
| Passing "最新季报" to MCP tool | Convert to "2025年Q3季报" (per Step 0 computation) |
| Assuming current quarter is disclosed | Check disclosure lag — Feb Q1 → latest is prev-year Q3 |
| Using "latest" or "recent" in queries | Always use explicit "YYYY年" or "YYYY年QX" |
| Forgetting to run Step 0 | Step 0 is MANDATORY before any other step |

## Multi-Turn Conversation

### Core Principle

Chat history serves ONE purpose: **understanding user intent**. Each turn MUST independently retrieve all data needed for the answer. Never rely on prior turns' retrieved data — it may be stale, incomplete, or missing source traceability.

### Question Type Classification

On each follow-up turn, classify the user's question into one of 6 types before acting:

| Type | Detection Pattern | Action |
|------|------------------|--------|
| **Extraction** | "刚才说的X是多少？", "上面提到的Y呢？", asks for a number/fact already in prior answer | Answer directly from chat context. No retrieval. |
| **Clarification** | "什么意思？", "为什么这么说？", "能解释一下X吗？", asks to explain prior answer | Answer directly from chat context. No retrieval. |
| **Extension** | "再深入分析一下X", "X的风险呢？", asks to go deeper on same entity/topic | New retrieval for the extension dimension only. |
| **Comparison (Partial New)** | "和比亚迪对比一下", introduces new entity for comparison with prior entity | Plan for ALL entities; retrieve only those not available from chat history (see Chat History Check). |
| **Comparison (Time)** | "去年呢？", "Q3的数据呢？", same entity but different time period | Retrieve data for the new time period. |
| **New Research** | Completely different topic/entity from prior turns | Full new retrieval (treat as fresh question). |

### Detection Heuristics

```
IF question asks for a specific data point already present in prior answer
   → Extraction (answer directly)

IF question asks "why" or "what does X mean" about prior answer
   → Clarification (answer directly)

IF question adds a NEW entity for comparison (e.g., "和XX对比")
   → Comparison (Partial New)
   → Plan for ALL entities, then apply Chat History Check to skip available data

IF question changes only the time dimension (e.g., "去年的呢？", "Q3呢？")
   → Comparison (Time)
   → Retrieve the new time period data

IF question deepens analysis on same entity (e.g., "风险分析", "估值呢？")
   → Extension
   → New retrieval for the extension topic

IF question is about a completely different subject
   → New Research
   → Full workflow from Step 0

IF classified as Extraction but data point NOT found or too vague in chat history
   → Reclassify as Extension
   → Execute retrieval for that dimension
```

### Semantic Equivalence Rules

When checking if data "already exists" in chat history, recognize equivalent expressions:

| Expression A | ≡ Equivalent to | Expression B |
|-------------|------------------|-------------|
| Q3 | = | 第三季度 |
| ROE | = | 净资产收益率 |
| 毛利率 | = | 销售毛利率 |
| 营收 | = | 营业收入 |
| PE | = | 市盈率 |
| 比亚迪 | = | 002594.SZ |
| 宁德时代 | = | CATL / 300750.SZ |

### Chat History Check (3-Turn Lookback)

Before planning retrieval, scan the last 3 turns:

```
for each sub-question in current turn:
    scan last 3 turns for semantically equivalent data
    if found AND data is from retrieved source (not model inference):
        mark as available_from_chat_history
        DO NOT re-retrieve (saves quota)
    else:
        mark as needs_retrieval
```

**"最新" in follow-up context**: When user says "最新" in a follow-up (e.g., "最新的数据呢？"), it means "the latest data we have access to" — use the Step 0 time computation, not a new web search for real-time data.

### Duplicate Query Prevention

Before executing any MCP call, check if an identical or semantically equivalent query was already executed in the current turn or the previous 2 turns. If so, reuse the result instead of re-querying.

Semantic equivalence for queries:
- Same company + same metric + overlapping time range → duplicate
- e.g., "宁德时代2024年营收" and "宁德时代2024年营业收入" → duplicate

### Compound Follow-ups

A follow-up may combine multiple types. Decompose before acting:

**Example**: "和比亚迪对比一下，另外宁德时代的风险呢？"
- Part 1: Comparison (Partial New) → Retrieve data for both entities
- Part 2: Extension → New retrieval for risk analysis of original entity

### Multi-Turn Example (3 Turns)

```
Turn 1: "分析宁德时代2024年的盈利情况"
  → Type: New Research
  → Step 0: Compute time context (Feb 2026 → latest disclosed = 2025年Q3)
  → Retrieval: stock_db("宁德时代 2024年 营收、净利润、毛利率")
              + finance_db("宁德时代 2024年 盈利分析 业绩", doc_type="report")
  → Answer: 2024年营收X亿，净利润Y亿，毛利率Z%...

Turn 2: "和比亚迪对比一下"
  → Type: Comparison (Partial New)
  → Implicit intent: Compare 宁德时代 and 比亚迪 2024年盈利
  → Chat history check: 宁德时代 2024年盈利数据 → available_from_chat_history ✓
  → Retrieval: stock_db("比亚迪 2024年 营收、净利润、毛利率")
              + finance_db("比亚迪 2024年 盈利分析 业绩", doc_type="report")
  → Note: 宁德时代 data reused from Turn 1 (no duplicate query)
  → Answer: Comparison table with both companies' data

Turn 3: "宁德时代的毛利率是多少？"
  → Type: Extraction
  → Data already in Turn 1 answer: 毛利率 = Z%
  → Action: Answer directly, no retrieval needed
```

### Red Flags (Common Multi-Turn Mistakes)

| Mistake | Correct Approach |
|---------|-----------------|
| Re-retrieving data that exists in prior turn's answer | Check chat history first — reuse if available |
| Only retrieving new entity in comparison, omitting original | Retrieve ALL entities for symmetric comparison |
| Treating "去年呢？" as New Research | It's Comparison (Time) — only retrieve new time period |
| Answering Extraction questions with new retrieval | Data is already in context — answer directly |
| Ignoring implicit entity from prior turns | "对比一下" implies comparing with the entity just discussed |
| Using stale data from 5+ turns ago without re-retrieving | 3-turn lookback limit — beyond that, re-retrieve |

## Complex Question Patterns

Some question types require specific decomposition strategies. See [references/search_strategy.md](references/search_strategy.md) for full details.

### Compound Questions (Industry + Company)

Questions like "光伏行业是否处于周期底部？隆基和通威的投资价值？" combine industry analysis with company-specific analysis.

**Strategy**: Split into parallel sub-tasks:
- Sub-task A: `info_search_finance_db` for industry-level analysis (e.g., "光伏行业 周期底部 供需分析")
- Sub-task B: `info_search_finance_db` for each company (one query per company, parallel)
- Sub-task C: `info_search_stock_db` for company financials (budget stock_db calls carefully)

### Macro-Company Intersection

Questions like "美联储降息对中国房地产龙头有什么影响？" span macro events and specific sectors.

**Strategy**: NEVER query macro event + sector in a single query (results will be off-topic). Split:
- Path A: Macro transmission logic — "美联储降息 对新兴市场 资金流向 利率传导"
- Path B: Sector fundamentals — "中国房地产龙头 保利发展 融资成本 销售数据"
- Synthesize the causal link yourself in the answer

### Cross-Market Comparison

Questions like "对比腾讯(港股)和Meta(美股)的估值" involve different markets.

**Key rules**:
- **Currency**: HKD vs USD vs CNY — always note currency units, convert to same base for comparison
- **Data asymmetry**: Some metrics may be available for one market but missing in another (e.g., PE for US stocks but not HK). Use `info_search_finance_db` research reports or `info_search_web` as fallback
- **Naming**: Use official names — "腾讯控股" for HK, "Meta Platforms" for US

### Multi-hop Retrieval (Serial Dependency)

Questions like "查茅台最大经销商的经营状况" require chained queries.

**Failure handling for first hop**:
1. If first hop returns no clear intermediate answer → **refine query** (try different keywords, broaden date_range to "all")
2. If still unclear → **try `info_search_web`** as supplementary source
3. If still no answer → **inform user** that the specific data point is not available in the database, and provide what related information was found

### Theme-based Stock Screening

Questions like "碳中和政策下哪些公司最受益？" require finding specific beneficiary stocks.

**Query optimization**: Use two rounds:
- Round 1 (background): "碳中和 十五五 政策方向" → understand the theme
- Round 2 (targets): "碳中和 受益龙头股 推荐标的 投资机会" with `doc_type="report"` → get specific stock picks

Avoid vague queries like "碳中和 新能源公司" — too broad, returns policy reports instead of stock picks.

### stock_db Quota Management

When 4 `info_search_stock_db` calls are not enough (e.g., 3+ company comparison needing multiple metric categories):

1. **Prioritize**: Use stock_db for core metrics (profitability, growth); use `info_search_finance_db` for supplementary metrics (valuation, dividends) which often appear in research reports
2. **Merge**: Combine same-category metrics into one query (e.g., "营收、净利润、毛利率" = 1 call, not 3)
3. **Fallback**: For valuation metrics (PE/PB/市值), `info_search_finance_db` with query "XX公司 估值分析 PE PB" often contains these numbers in analyst reports

## MCP Tools Overview

Four retrieval tools available. See [references/mcp_tools.md](references/mcp_tools.md) for complete documentation.

| Tool | Purpose | Priority |
|------|---------|----------|
| `info_search_stock_db` | Quantitative financial/market data (listed companies) | For metrics, ratios, prices |
| `info_search_finance_db` | Research reports, news, analyst views, announcements | Primary for qualitative data |
| `info_search_user_db` | User's private uploaded documents | Only when user explicitly references |
| `info_search_web` | Web search | Fallback only |

**Selection order**: `info_search_finance_db` first > `info_search_stock_db` for numbers > `info_search_web` as fallback

See [references/search_strategy.md](references/search_strategy.md) for the complete tool selection decision tree, parallel execution patterns, and query optimization rules.

## Quality Standards

1. **Default doubt**: First source may be biased/outdated — seek 2-3 independent sources for key claims
2. **Data priority**: MCP database > web search > model knowledge
3. **Specific queries**: Every query must specify subject, time, and topic — no vague queries
4. **One entity per query**: Multi-entity comparisons require separate queries per entity, in parallel
5. **Time ranges over points**: Prefer "2022至2024年营收" over querying each year separately
6. **Minimum retrieval depth**: At least 3 retrieval calls for any non-trivial financial question
7. **Anomaly detection**: If a metric shows >30% swing between adjacent periods with no obvious cause, cross-verify with `info_search_finance_db` before reporting — it may be a data error or mismatched data scope
8. **Metric symmetry**: In comparison tasks, all entities must have the same metrics. If one is missing, explicitly note it and attempt fallback retrieval

## Example Triggers

- "比亚迪最新的营收情况如何？"
- "分析一下宁德时代的投资价值"
- "对比腾讯和阿里的PE"
- "最近半导体行业有什么新动态？"
- "茅台的股价走势和估值分析"
- "帮我看看新能源汽车行业的竞争格局"
- "雅鲁藏布江下游水电工程会带来哪些投资机会？"
- "特斯拉最近的负面新闻对股价有什么影响？"
