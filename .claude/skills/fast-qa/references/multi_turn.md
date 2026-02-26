# Multi-Turn Conversation

## Core Principle

Chat history serves ONE purpose: **understanding user intent**. Each turn MUST independently retrieve all data needed for the answer. Never rely on prior turns' retrieved data — it may be stale, incomplete, or missing source traceability.

## Question Type Classification

On each follow-up turn, classify the user's question into one of 6 types before acting:

| Type | Detection Pattern | Action |
|------|------------------|--------|
| **Extraction** | "刚才说的X是多少？", "上面提到的Y呢？", asks for a number/fact already in prior answer | Answer directly from chat context. No retrieval. |
| **Clarification** | "什么意思？", "为什么这么说？", "能解释一下X吗？", asks to explain prior answer | Answer directly from chat context. No retrieval. |
| **Extension** | "再深入分析一下X", "X的风险呢？", asks to go deeper on same entity/topic | New retrieval for the extension dimension only. |
| **Comparison (Partial New)** | "和比亚迪对比一下", introduces new entity for comparison with prior entity | Plan for ALL entities; retrieve only those not available from chat history (see Chat History Check). |
| **Comparison (Time)** | "去年呢？", "Q3的数据呢？", same entity but different time period | Retrieve data for the new time period. |
| **New Research** | Completely different topic/entity from prior turns | Full new retrieval (treat as fresh question). |

## Detection Heuristics

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

## Semantic Equivalence Rules

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

## Chat History Check (3-Turn Lookback)

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

## Duplicate Query Prevention

Before executing any MCP call, check if an identical or semantically equivalent query was already executed in the current turn or the previous 2 turns. If so, reuse the result instead of re-querying.

Semantic equivalence for queries:
- Same company + same metric + overlapping time range → duplicate
- e.g., "宁德时代2024年营收" and "宁德时代2024年营业收入" → duplicate

## Compound Follow-ups

A follow-up may combine multiple types. Decompose before acting:

**Example**: "和比亚迪对比一下，另外宁德时代的风险呢？"
- Part 1: Comparison (Partial New) → Retrieve data for both entities
- Part 2: Extension → New retrieval for risk analysis of original entity

## Multi-Turn Example (3 Turns)

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

## Red Flags (Common Multi-Turn Mistakes)

| Mistake | Correct Approach |
|---------|-----------------|
| Re-retrieving data that exists in prior turn's answer | Check chat history first — reuse if available |
| Only retrieving new entity in comparison, omitting original | Retrieve ALL entities for symmetric comparison |
| Treating "去年呢？" as New Research | It's Comparison (Time) — only retrieve new time period |
| Answering Extraction questions with new retrieval | Data is already in context — answer directly |
| Ignoring implicit entity from prior turns | "对比一下" implies comparing with the entity just discussed |
| Using stale data from 5+ turns ago without re-retrieving | 3-turn lookback limit — beyond that, re-retrieve |
