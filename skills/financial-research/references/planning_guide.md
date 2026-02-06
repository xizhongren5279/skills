# Planning Guide: Optimizing Research Execution

This document provides a framework for creating efficient research plans that maximize parallel execution and minimize total execution time.

## Core Principles

### 1. Parallelization First
**Default assumption**: Tasks can run in parallel UNLESS there's a clear dependency.

**Why it matters**:
- Parallel execution: 10 tasks in Phase 1 = ~1.5 minutes
- Sequential execution: 10 tasks serially = ~15 minutes

**Rule**: If Task B doesn't need Task A's output, they should run in parallel.

### 2. Minimize Serial Phases
**Target**: 2-3 phases maximum for most research projects.

**Common phase patterns**:
- **2-phase**: Data collection (parallel) → Synthesis
- **3-phase**: Background data (parallel) → Dependent analysis (parallel) → Synthesis

**Anti-pattern**: 5+ phases where each waits for previous - this destroys efficiency.

### 3. Right-size Query Parameters
**recall_num optimization**:
- Don't default to 20 if 10 is sufficient
- More results = more processing time, diminishing returns after 12-15
- Use 5-8 for simple fact-checking, 10-15 for analysis

**date_range optimization**:
- Match the actual time horizon needed
- Don't use "past_year" if "past_quarter" contains the relevant information
- Narrower date range = more focused, relevant results

### 4. Task Decomposition
**Good task**: Single, clear purpose that produces specific output
**Bad task**: Vague or trying to do too many things

**Example**:
- ✅ Good: "Retrieve Company A's short-term investment logic from analyst reports"
- ❌ Bad: "Get all information about Company A"

### 5. Dependency Management
**Ask**: "Does this task truly NEED the output from the previous task to execute?"

**True dependencies**:
- Valuation comparison AFTER getting financial metrics
- Synthesis AFTER data collection

**False dependencies** (parallelize instead):
- Company A analysis doesn't need Company B results
- Historical financials don't need forward forecasts
- Risk analysis doesn't need valuation multiples

---

## Planning Process

### Step 1: Understand the Request
Break down the user's request into:
1. **What**: What type of research? (company/industry/strategy/etc.)
2. **Scope**: Which entities? How deep? What time horizon?
3. **Output**: What format? What level of detail?

### Step 2: Identify Required Information
List ALL information needed for the final output.

**Example: Company deep-dive research**
```
Required information:
- Company overview and recent updates
- Business model and profit drivers
- Market position and competitors
- Historical financials (3-5 years)
- Profitability metrics (ROE, margins)
- Segment revenue breakdown
- Growth drivers and outlook
- Management guidance
- Risk factors
- Analyst forecasts
- Valuation multiples
- Comparable company valuations
```

### Step 3: Map Information to MCP Queries
For each piece of required information, determine:
1. **Which MCP tool**: finance_db / stock_db / user_db / web
2. **Query specifics**: Exact query string, parameters
3. **Dependencies**: Does this require output from another query?

**Example mapping**:
```
1. Company overview → finance_db, query="[Company]公司近况...", date_range="past_quarter", no dependencies
2. Historical revenue → stock_db, query="[Company] 2022-2024年营收", no dependencies
3. ROE analysis → stock_db, query="[Company] 2022-2024年ROE", no dependencies
4. Valuation comp → finance_db, query="[Company]可比公司估值对比...", no dependencies
   (If insufficient) → web, query="[Company]可比公司估值", DEPENDS ON previous query result
```

### Step 4: Group into Phases
**Phase construction rules**:
1. All queries with NO dependencies → Phase 1 (parallel)
2. Queries depending on Phase 1 → Phase 2 (parallel within this phase)
3. Final synthesis always last phase

**Optimization**: Try to minimize dependency depth. Can Phase 2 queries actually run in Phase 1?

**Example grouping**:
```
Phase 1: Parallel data collection (12 queries)
├─ Company overview
├─ Business model analysis
├─ Competitive position
├─ Historical financials (5 metrics, 5 queries via stock_db)
├─ Segment breakdown
├─ Growth drivers
├─ Risk factors
└─ Management guidance

Phase 2: Synthesis
└─ Integrate all findings into final report
```

### Step 5: Write Detailed Task Specifications
For each task in the plan, specify:
- **Task ID**: For reference (e.g., Task 1.1, Task 1.2)
- **Description**: What this task does
- **Tool**: Exact MCP tool name
- **Query**: Exact query string with company/entity names filled in
- **Parameters**: date_range, recall_num, doc_type (if applicable)
- **Purpose**: What information this retrieves and why
- **Dependencies**: Which tasks must complete first (if any)
- **Expected output**: What the subagent should return

### Step 6: Estimate Execution Time
**Phase time = MAX(task_time for all parallel tasks in phase)**

Rough estimates:
- Single MCP query + light analysis: ~10-20 seconds
- Single MCP query + substantial analysis: ~20-30 seconds
- Phase with 5-10 parallel tasks: ~1-2 minutes
- Phase with 10-15 parallel tasks: ~1.5-2.5 minutes

**Total time = Sum of all phase times**

### Step 7: Present Plan to User
Show:
- Research objectives
- Analysis sections (the final report structure)
- Retrieval strategy (phased breakdown with all tasks)
- Execution strategy (total queries, phases, estimated time)
- Output structure

**Get approval** before execution.

---

## Planning Patterns

### Pattern 1: Independent Multi-Section Research

**Use case**: Research with multiple independent sections (e.g., company report with business analysis, financials, competition, outlook)

**Structure**:
```
Phase 1: Retrieve ALL data in parallel (10-20 queries)
├─ Section 1 queries
├─ Section 2 queries
├─ Section 3 queries
├─ Section 4 queries
└─ Section 5 queries

Phase 2: Synthesis
└─ Integrate into final report
```

**Estimated time**: 1.5-3 minutes

**Characteristics**:
- ✅ Fastest approach
- ✅ No artificial dependencies
- ✅ Scales well (20 parallel queries ≈ 15 parallel queries in time)

### Pattern 2: Two-Stage Dependent Research

**Use case**: Research where second stage depends on first (e.g., need to identify companies before analyzing them)

**Structure**:
```
Phase 1: Foundation data (5-8 parallel queries)
├─ Identify relevant entities
├─ Basic context
└─ Framework data

Phase 2: Deep-dive (10-15 parallel queries)
├─ Entity-specific analysis using Phase 1 results
├─ Comparative analysis
└─ Detailed metrics

Phase 3: Synthesis
└─ Integrate findings
```

**Estimated time**: 3-5 minutes

**Characteristics**:
- Serial dependency is genuine
- Still maximize parallelism within each phase
- Common for industry research, comparative analysis

### Pattern 3: Iterative Refinement

**Use case**: Research where data availability is uncertain, may need fallback

**Structure**:
```
Phase 1: Primary data retrieval (10-15 parallel queries)
├─ Main data sources (finance_db, stock_db)
└─ Core information

Phase 2: Gap filling (0-5 parallel queries, conditional)
├─ Check for missing data
├─ Execute fallback queries (web search) if needed
└─ Alternative data sources

Phase 3: Synthesis
└─ Integrate all available data
```

**Estimated time**: 2-4 minutes (depending on gaps)

**Characteristics**:
- Handles data uncertainty
- Phase 2 may be skipped if Phase 1 is sufficient
- Common for specialized topics or emerging companies

### Pattern 4: Company Comparison

**Use case**: Comparing 2-5 companies across multiple dimensions

**Structure**:
```
Phase 1: Company profiles (Parallel, organized by company)
├─ Company A: overview, business, position (3-5 queries)
├─ Company B: overview, business, position (3-5 queries)
└─ Company C: overview, business, position (3-5 queries)

Phase 2: Cross-company metrics (Parallel, organized by metric)
├─ Revenue for A, B, C (via stock_db)
├─ ROE for A, B, C (via stock_db)
├─ Margins for A, B, C (via stock_db)
└─ Valuations for A, B, C

Phase 3: Synthesis
└─ Comparative analysis and recommendations
```

**Estimated time**: 3-5 minutes

**Characteristics**:
- Logical grouping: profiles, then metrics
- Could also do all in Phase 1 if no dependencies
- Scale with N companies: ~5-7 queries per company

### Pattern 5: Macro → Sector → Stocks Research

**Use case**: Top-down strategy research from macro to individual stocks

**Structure**:
```
Phase 1: Macro & Sector (Parallel)
├─ Macro environment analysis
├─ Policy analysis
├─ Sector relative performance
└─ Sector fundamentals

Phase 2: Stock Selection (Parallel, conditional on Phase 1 findings)
├─ Top picks in identified sectors
├─ Financial metrics for candidates
├─ Analyst views
└─ Valuation analysis

Phase 3: Synthesis
└─ Strategy formulation and recommendations
```

**Estimated time**: 3-5 minutes

**Characteristics**:
- Top-down logic flow
- Phase 2 scope may adjust based on Phase 1 insights
- Common for strategy/thematic research

---

## Optimization Strategies

### Strategy 1: Aggressive Parallelization
**Principle**: When in doubt, parallelize.

**Technique**: In the planning phase, actively look for dependencies. If you can't find a clear one, assume tasks can run in parallel.

**Example**:
```
Question: "Should valuation analysis wait for financial analysis?"
Answer: NO - both can retrieve data in parallel, synthesis can integrate later
```

### Strategy 2: Task Consolidation
**Principle**: Can one query serve multiple purposes?

**Technique**: Before adding a new query, check if an existing query in the plan already covers it.

**Example**:
```
❌ Separate queries for "Company A profitability" and "Company A ROE and margins"
✅ Single query: "Company A profitability metrics including ROE, net margin, gross margin"
```

**Trade-off**: Don't over-consolidate - if query becomes too broad, results may be less focused.

### Strategy 3: Right-size Recall
**Principle**: More results ≠ better results, but slower results.

**Technique**:
- Start with moderate recall_num (10-12)
- Increase to 15-20 only for comprehensive research or when topic is niche
- Use 5-8 for quick fact checks

**Impact**: recall_num=20 vs recall_num=10 can add 5-10 seconds per query.

### Strategy 4: Targeted date_range
**Principle**: Narrower date range = faster, more relevant results.

**Technique**:
- Recent news/updates: past_quarter
- Short-term logic: past_quarter to past_half_year
- Long-term logic: past_year
- Historical analysis: past_year or all

**Impact**: "past_quarter" may be 2x faster than "past_year" for processing.

### Strategy 5: Prune Low-Value Queries
**Principle**: Not every piece of information adds equal value.

**Technique**: Before finalizing plan, ask for each query: "How does this change the final output?"

If the answer is "marginally" or "nice to have", consider removing it.

**Example**:
```
Core queries (keep): Company financials, competitive position, growth outlook
Marginal queries (evaluate): Historical stock price performance, detailed product specs
```

**Trade-off**: Completeness vs speed. For time-sensitive analysis, prioritize core insights.

### Strategy 6: Subagent Task Design
**Principle**: Subagents should be self-contained and return structured output.

**Technique**: Each subagent prompt should include:
1. Clear context (what research this is for)
2. Exact MCP query to execute with parameters
3. What to extract/analyze from results
4. Expected output format

**Example prompt**:
```
You are executing Task 1.2: Retrieve Company A's short-term investment logic.

YOUR TASK:
1. Execute this MCP query:
   mcp__ashare-mcp-research__info_search_finance_db(
       query="[Company A] 短期投资逻辑(1-3月),从业务价值出发",
       date_range="past_quarter",
       recall_num=12,
       doc_type="report"
   )

2. Analyze the results and extract:
   - 3-5 key short-term investment drivers
   - Supporting quantitative data for each
   - Time-sensitive catalysts (next 1-3 months)

3. Return your findings as:
   **Short-term Investment Logic (1-3 months):**
   - [Point 1 with data]
   - [Point 2 with data]
   - [Point 3 with data]
```

### Strategy 7: Fallback Planning
**Principle**: Some data may not be available - plan for it.

**Technique**:
- Identify critical vs optional data
- Specify fallback queries (usually web search)
- Make fallback conditional: "If insufficient data, then..."

**Example**:
```
Task 3.4: Comparable company valuations
- Primary: info_search_finance_db(..., doc_type="report")
- Fallback: If <3 comparable companies found, use info_search_web(...)
```

---

## Common Planning Mistakes

### Mistake 1: Over-serialization
**Symptom**: Plan has 5+ sequential phases with <5 queries each.

**Problem**: Each phase transition adds time, eliminating parallel efficiency.

**Fix**: Merge phases. Ask "What truly depends on what?"

**Example**:
```
❌ Bad:
Phase 1: Company overview (2 queries)
Phase 2: Business analysis (3 queries)
Phase 3: Financials (4 queries)
Phase 4: Outlook (2 queries)
Phase 5: Synthesis
Total: ~6-8 minutes

✅ Good:
Phase 1: All data collection (11 queries in parallel)
Phase 2: Synthesis
Total: ~2-3 minutes
```

### Mistake 2: False Dependencies
**Symptom**: Tasks marked as dependent when they're not.

**Problem**: Artificial sequencing that slows execution.

**Fix**: Challenge each dependency. Does Task B really need Task A's output to start?

**Example**:
```
❌ False dependency: "Must get Company A data before Company B data"
✅ Reality: Both can retrieve simultaneously
```

### Mistake 3: Vague Task Specifications
**Symptom**: Task descriptions like "Analyze the company" or "Get financial data".

**Problem**: Subagent doesn't know exactly what to do, may retrieve wrong data.

**Fix**: Be specific:
- Exact MCP tool and query
- Exact parameters
- Expected output format

### Mistake 4: Ignoring Tool Limitations
**Symptom**: Single `stock_db` query trying to get multiple metrics.

**Problem**: `stock_db` only handles ONE metric per query.

**Fix**: Break into multiple parallel queries:
```
❌ Bad: "Get Company A's ROE, net margin, and revenue growth" (1 query)
✅ Good:
- Task 2.1: Get Company A's ROE
- Task 2.2: Get Company A's net margin
- Task 2.3: Get Company A's revenue growth
(3 parallel queries)
```

### Mistake 5: Retrieve Then Analyze Separately
**Symptom**: Phase 1 retrieves raw data, Phase 2 analyzes it serially by section.

**Problem**: Analysis becomes serial bottleneck.

**Fix**: Have each subagent retrieve AND analyze within the same task.

**Example**:
```
❌ Bad (from company-one-page v2.0):
Phase 1: Retrieve data for all 5 sections (parallel)
Phase 2: Analyze section 1 → section 2 → section 3 → section 4 → section 5 (serial)

✅ Good (from company-one-page v3.0):
Phase 1:
- Subagent 1: Retrieve + analyze section 1
- Subagent 2: Retrieve + analyze section 2
- Subagent 3: Retrieve + analyze section 3
- Subagent 4: Retrieve + analyze section 4
- Subagent 5: Retrieve + analyze section 5
(All in parallel)
Phase 2: Integrate final report
```

### Mistake 6: No Synthesis Phase
**Symptom**: Plan ends after data collection.

**Problem**: Final report quality suffers, no integration of insights.

**Fix**: Always include final synthesis phase to:
- Integrate findings from all tasks
- Resolve inconsistencies
- Generate cohesive narrative
- Quality check

### Mistake 7: Unrealistic Time Estimates
**Symptom**: Estimating 5 minutes for 30 queries or 30 seconds for complex analysis.

**Problem**: User expectations not managed.

**Fix**: Use rough guidelines:
- 10-15 parallel queries: ~1.5-2.5 minutes
- 20-25 parallel queries: ~2-3 minutes
- Add 0.5-1 minute per additional serial phase
- Add buffer for synthesis (0.5-1 minute)

---

## Plan Template

Use this template when presenting a research plan to the user:

```markdown
# Research Plan: [Title]

## Research Type
[Company/Industry/Strategy/Macro/Quantitative/Comparative]

## Objectives
- [Objective 1]
- [Objective 2]
- [Objective 3]

## Analysis Sections
The final report will include:
1. [Section 1 Name]
   - Key questions: [...]
   - Data requirements: [...]
2. [Section 2 Name]
   - ...
[Continue for all sections]

## Retrieval Strategy

### Phase 1: [Phase Name] (Parallel)
All tasks in this phase execute simultaneously:

**Task 1.1: [Task Name]**
- Tool: `mcp__ashare-mcp-research__[tool_name]`
- Query: "[Exact query string]"
- Parameters:
  - date_range: '[value]'
  - recall_num: [number]
  - doc_type: '[value]' (if applicable)
- Purpose: [What this retrieves and why]
- Output: [Expected output format]

**Task 1.2: [Task Name]**
- Tool: ...
[Continue for all tasks in Phase 1]

### Phase 2: [Phase Name] (Depends on Phase 1)
Tasks in this phase require Phase 1 completion:

**Task 2.1: [Task Name]**
- Depends on: Task 1.X
- Tool: ...
[Continue for all tasks in Phase 2]

[Add more phases if needed]

### Phase N: Final Synthesis
- Integrate findings from all phases
- Resolve inconsistencies
- Generate final report
- Quality checks

## Execution Strategy
- **Total MCP queries**: [N]
- **Parallel phases**: [X]
- **Serial dependencies**: [Brief description]
- **Estimated execution time**: [X-Y minutes]

## Output Structure
```
[Outline of final report structure with section names]
```

## Quality Checks
- [ ] All sections have quantitative data
- [ ] No placeholder text
- [ ] Data sources cited
- [ ] Consistent time periods
- [ ] Missing data noted with "-"
- [ ] Logical flow and narrative

---

**Does this plan address your research needs? Any adjustments before I proceed?**
```

---

## Execution Checklist

Before executing a plan:

**Planning Quality**:
- [ ] All tasks have clear, specific descriptions
- [ ] MCP tool names and queries are exact (not placeholders)
- [ ] Parameters specified (date_range, recall_num, doc_type)
- [ ] Dependencies verified (not false dependencies)
- [ ] Phases minimize serial bottlenecks

**Efficiency**:
- [ ] Maximum parallelization within phases
- [ ] 2-3 phases maximum (unless true dependencies require more)
- [ ] recall_num right-sized (not defaulting to 20)
- [ ] date_range appropriate for analysis timeframe
- [ ] No redundant queries

**Execution Readiness**:
- [ ] Subagent prompts include context, exact queries, and expected output
- [ ] Final synthesis phase included
- [ ] Time estimate provided to user
- [ ] Plan presented to user for approval

**Output Quality**:
- [ ] Output structure defined
- [ ] Quality check criteria listed
- [ ] Data handling rules specified (e.g., "-" for missing data)

---

## Summary

**Core principles**:
1. Parallelize by default
2. Minimize serial phases (target: 2-3)
3. Right-size queries (recall_num, date_range)
4. Specific task specs (exact tools, queries, parameters)
5. Dependency management (challenge each dependency)
6. Subagents retrieve AND analyze
7. Always synthesize at the end

**Typical timeline**:
- Simple research: ~2-3 minutes (1 parallel phase + synthesis)
- Medium research: ~3-5 minutes (2 phases + synthesis)
- Complex research: ~5-8 minutes (3 phases + synthesis)

**Success metrics**:
- Execution time < 5 minutes for most research
- 80%+ of queries in Phase 1 (parallel)
- User approval before execution
- High-quality final output with quantitative data

By following these principles and patterns, research execution becomes dramatically faster while maintaining or improving output quality.
