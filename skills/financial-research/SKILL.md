---
name: financial-research
description: Use for ANY financial research question including company analysis (deep-dives, quarterly reports, financial comparisons), industry research (competitive landscape, sector trends), quantitative analysis (financial metrics, stock data, performance comparisons), macro research (economic outlook, policy impact), and investment strategy. CRITICAL - Also use for ALL follow-up requests in multi-turn conversations that involve financial data, comparisons, or analysis - e.g., after discussing Company A's financials, user asks to "compare with Company B" / "对比一下公司B" or "analyze business metrics too" / "再看业务数据" or "what about gross margin?" / "毛利率呢?" - these follow-ups MUST trigger this skill. Each follow-up is a NEW skill invocation (not continuation of prior execution). Any mention of companies, stocks, industries, financial metrics, quarterly reports, or market analysis should invoke this skill, regardless of whether it's an initial question or a conversational follow-up. This includes ultra-short forms like "呢?", "那XX呢?", "对比一下Y".
---

# Financial Research

## Overview

This skill enforces a **structured 6-step research process** using MCP tools, Task-based parallel execution, and mandatory output file generation.

**Core Principles**:
1. Research = Plan → Execute → Synthesize → Save. Skip any step and the research is incomplete.
2. **Time Context Matters**: Always infer time-based queries from current system time. "最新季报" must be converted to explicit quarters (e.g., "2024年Q4") before passing to subagents.

**Violating the letter of the rules is violating the spirit of the rules.**

## The Iron Law

```
NO DIRECT MCP QUERIES WITHOUT A JSON PLAN FIRST
NO ANALYSIS WITHOUT TASK TOOL EXECUTION
NO COMPLETION WITHOUT OUTPUT FILES SAVED
NO VAGUE TIME EXPRESSIONS IN QUERIES - CONVERT TO EXPLICIT DATES/QUARTERS
```

## When to Use

Use this skill when users request:
- Company deep-dive analysis (beyond one-page summaries)
- Industry competitive landscape research
- Investment strategy formulation
- Macro economic analysis
- Quantitative comparisons of multiple entities
- Any research requiring: data retrieval + structured analysis + comprehensive report

**Do NOT use** for:
- Simple one-page company summaries (use company-one-page skill)
- Quick factual lookups **in isolation** (single-turn questions with no prior financial context)
- Conversational Q&A without deliverable

**MANDATORY MULTI-TURN RULE**: Once a financial research conversation has started (any mention of companies, stocks, financial metrics, reports), subsequent questions related to financial topics that **require NEW data retrieval** MUST invoke this skill.

**CRITICAL EXCEPTIONS - Answer Directly WITHOUT Skill Invocation When:**

1. **Exact Data Extraction**: Requested metric is explicitly stated in previous turn (< 3 turns ago)
   - Example: Turn 1 retrieved "宁德时代 Q3 毛利率 25%", Turn 2 asks "毛利率是多少?"
   - Action: Answer directly "根据刚才检索的报告,毛利率为25%"
   - Reason: Data is fresh (<10 min), identical query would retrieve identical result

2. **Clarification Questions**: User seeks confirmation/explanation of existing data
   - Example: "Q3是指2024年Q3吗?", "ROE是年化的还是季度的?"
   - Action: Answer directly without retrieval
   - Reason: No new data needed, user wants immediate clarification

3. **Data Freshness**: Previous retrieval was <10 minutes ago, same entity/time/metric
   - Reusing fresh data is MORE accurate than re-querying (avoids inconsistency)

**Invoke Skill WITH Chat History Awareness When:**

1. **New Entity Comparison**: Turn 1 analyzed Entity A, Turn 2 asks "compare with Entity B"
   - Invoke skill BUT plan should retrieve ONLY Entity B
   - Reference Entity A data from previous turn (avoid duplicate query)

2. **Time Period Extension**: Turn 1 retrieved Q3, Turn 2 asks "compare Q2 and Q3"
   - Invoke skill BUT plan should retrieve ONLY Q2
   - Reference Q3 data from previous turn

3. **New Analysis Dimension**: Turn 1 retrieved revenue data, Turn 2 asks "profitability analysis"
   - Invoke skill for new metrics (margins, net income)
   - Can reference Turn 1 revenue for context

**Decision Test Before Invoking Skill:**
```python
if requested_data_in_last_N_turns(user_query, N=3) and is_extraction_or_clarification():
    answer_directly_from_chat_history()
else:
    invoke_skill_with_history_awareness()
```

**In multi-turn financial conversations requiring NEW data, there is NO such thing as "too simple to invoke skill".** But if data already exists in chat history, reuse it efficiently.

## Red Flags - STOP and Follow Process

These thoughts mean you're about to violate the workflow:

| Thought | Reality |
|---------|---------|
| "I'll just query MCP directly" | Plan first. No exceptions. |
| "The plan is obvious, I'll skip JSON" | Write the JSON. Plans expose assumptions. |
| "I can execute queries myself faster" | Use Task tool. Parallelism matters. |
| "I'll save files at the end" | Create output dir now. Prevents forgetting. |
| "This is too simple for full process" | Simple tasks become complex. Follow process. |
| "User just wants quick answer" | Skill triggered = full process required. |
| "I'll synthesize as I go" | Collect all task outputs first. |
| **"This is just a follow-up, not a new question"** | **Check if it's extraction/clarification (answer directly) or new research (invoke skill).** |
| **"User said '再分析' (again), so continue current process"** | **"Again" means NEW invocation, not continuation.** |
| **"'毛利率呢?' is just one metric, too simple"** | **If Turn 1 showed毛利率, answer directly. If not, invoke skill.** |
| **"This doesn't need a deliverable, just answer in chat"** | **Clarifications can be answered in chat. New research needs deliverable.** |
| **"I should re-query for accuracy"** | **Fresh data (<10 min) reuse is MORE accurate than re-querying.** |
| **"All comparisons need full dataset retrieval"** | **Reuse Entity A from Turn 1, retrieve only new Entity B.** |
| **"User asked financial question = invoke skill"** | **Check question type first: Extraction/Clarification vs New Research.** |
| **"Question type matching takes too long"** | **Read Excel once per query. Caching happens automatically.** |
| **"I'll use my own plan structure instead of template"** | **Matched workflow is prescriptive, not suggestive. Use it.** |
| **"Low confidence (<0.6) but I'll proceed anyway"** | **Ask user to confirm or select type manually at <0.6.** |
| **"Template doesn't fit this specific query"** | **Customize hints, not structure. Template order is fixed.** |
| **"I'll skip matching because query is simple"** | **ALL queries must match. Even simple ones benefit from structure.** |

**All of these mean: STOP. Start with Step 1.**

## Question Type Classification (Multi-Turn Context)

Before proceeding to research process, classify the question type:

| Question Type | Characteristics | Action | Deliverable | Example |
|---------------|-----------------|--------|-------------|---------|
| **Extraction** | Data explicitly stated in Turn N-1 | Answer directly | No | "毛利率是多少?" when Turn 1 showed "毛利率25%" |
| **Clarification** | Confirm/explain existing data | Answer directly | No | "Q3是指2024年Q3吗?", "ROE是年化的吗?" |
| **Extension** | Add new dimension to Turn N-1 entity | Invoke skill | Yes | Turn 1 revenue, Turn 2 "profitability analysis" |
| **Comparison (Partial New)** | Compare Turn N-1 entity A with new entity B | Invoke skill (smart plan) | Yes | Turn 1 analyzed 茅台, Turn 2 "compare with 五粮液" |
| **Comparison (Time)** | Compare Turn N-1 time T1 with new time T2 | Invoke skill (smart plan) | Yes | Turn 1 retrieved Q3, Turn 2 "compare Q2 and Q3" |
| **New Research** | Requires completely new data | Invoke skill | Yes | Turn 1 about 茅台, Turn 2 "analyze semiconductor industry" |

**Detection Heuristics:**
- Pattern "X是多少?" + X stated in Turn N-1 → **Extraction**
- Pattern "是指Y吗?" → **Clarification**
- Pattern "对比A和B" + A in Turn N-1 + B new → **Comparison (Partial New)**
- Pattern "对比T1和T2" + T1 in Turn N-1 + T2 new → **Comparison (Time)**
- No relevant data in last 3 turns → **New Research**

**Critical: Semantic Equivalence Rules**

When checking if data is "in Turn N-1", use semantic matching, not just literal string matching:

- **Time Period Equivalence**: Q3 = 第三季度 = 三季度 = 2024年Q3 = 2024年第三季度
- **Metric Name Equivalence**:
  - 毛利率 = gross margin = gross profit margin
  - 营收 = revenue = 收入 = top line
  - 净利润 = net profit = net income = 净利
  - ROE = 净资产收益率 = return on equity
  - PE = 市盈率 = price-to-earnings ratio
- **Multi-Metric Extraction**: If Turn 2 asks "营收和毛利率是多少?" and both were shown in Turn 1, this is still **Extraction** (answer directly with both values)
- **Partial Metric Extraction**: If Turn 2 asks "营收、毛利率和ROE" but only 营收 and 毛利率 were in Turn 1, classify as **Extension** (invoke skill for ROE)

**"最新" in Follow-up Context**:
- Turn 1 retrieved data 9 minutes ago, Turn 2 asks "最新数据是多少?"
- Interpretation: "最新" = "latest data WE HAVE" (from Turn 1), NOT "re-query for fresher data"
- Only re-query if Turn 1 data is >10 minutes old OR user explicitly says "重新检索最新数据"

**Compound Question Types** (Multiple operations in one question):

| Compound Pattern | Example | Classification | Action |
|------------------|---------|----------------|--------|
| **Comparison + Analysis** | "对比Q2和Q3,并分析增长驱动因素" | Comparison (Time) + Extension | Invoke skill, plan includes both comparison task + analysis task |
| **Extraction + Clarification** | "毛利率是多少?这是年化的吗?" | Extraction + Clarification | Answer directly with both (e.g., "毛利率25%(季度数据,非年化)") |
| **Extension + Comparison** | "分析盈利能力并对比同行" | Extension + Comparison (Partial New) | Invoke skill, plan retrieves profitability metrics + peer data |

**Default rule**: If ANY component requires skill invocation, invoke skill and handle all components together

## Research Process

### Step 1: Understand the Request

**REQUIRED ACTIONS**:

**1.0 Question Type Matching (NEW - Structured Planning)**

**CRITICAL**: This step happens BEFORE reading reference documents and BEFORE creating the plan.

1. **Read Question Type Database**:
   ```python
   from utils.question_type_parser import QuestionTypeParser

   parser = QuestionTypeParser('references/plan_for_question_type.xlsx')
   parser.load_question_types()  # Loads all 26 question types
   ```

2. **Match User Query to Question Type**:

   Generate LLM matching prompt:
   ```python
   workflow_result = parser.get_workflow_for_query(user_query, use_llm=True)

   if workflow_result.get('_needs_llm_execution'):
       matching_prompt = workflow_result['_matching_prompt']
       # Execute matching_prompt with LLM to get matched_index
   ```

   LLM returns JSON:
   ```json
   {
     "matched_index": 2,
     "confidence_score": 0.85,
     "reasoning": "用户问题询问公司研究,最匹配'如何做好公司研究'类型"
   }
   ```

3. **Extract Matched Workflow**:
   ```python
   # Get the matched type data
   types = parser.load_question_types()
   matched_type = types[matched_index - 1]  # Convert 1-indexed to 0-indexed

   # Extract workflow from matched type
   workflow_data = parser.extract_workflow(matched_type)

   # Result contains:
   # - reference_rules: List of guiding principles
   # - reference_workflow: List of workflow steps (prescriptive template)
   # - full_example: Complete example from Excel
   ```

4. **Store Matched Workflow for Step 3**:
   ```python
   matched_workflow = {
       'question_type': matched_type['问题类型'],
       'type_description': matched_type['类型描述'],
       'confidence_score': confidence_score,
       'reference_rules': workflow_data['reference_rules'],
       'reference_workflow': workflow_data['reference_workflow'],
       'full_example': matched_type['示例']
   }

   # This will be used in Step 3 to generate structured plan
   ```

5. **Announce Matched Type to User**:
   ```
   已识别问题类型: {question_type} (置信度: {confidence_score})

   将按照此类型的标准研究流程进行分析。
   ```

**Why this step is mandatory**:
- Ensures consistent, high-quality research plans
- Applies proven workflows from the 26 question type templates
- Reduces randomness and improves reproducibility
- Leverages domain expertise encoded in Excel workflows

**Red Flags for Step 1.0 Violations**:
- Skipping question type matching because "I know what to do"
- Not reading the Excel file each time (workflows may be updated)
- Proceeding with custom plan instead of using matched workflow
- Low confidence match (<0.6) but not asking user to confirm

**1.1 Check Chat History for Available Data (Multi-Turn Efficiency)** (formerly 1.0)

Before proceeding, check last 3 turns for relevant retrieved data:

```python
def check_chat_history_data(user_query, last_N_turns=3):
    """
    Returns classification:
      - "answer_directly": Data available, no skill invocation needed
      - "partial_data_available": Some data available, use smart planning
      - "new_research": No relevant data, full retrieval needed
    """
    extracted_data = {}
    for turn in last_N_turns:
        # Check if turn involved financial research
        if "retrieved" in turn or "report" in turn:
            # Extract: entities, time_periods, metrics, values
            extracted_data[turn.id] = parse_retrieved_data(turn)

    # Match user_query against extracted_data
    if exact_match(user_query, extracted_data):
        return "answer_directly", extracted_data
    elif partial_match(user_query, extracted_data):
        return "partial_data_available", extracted_data
    else:
        return "new_research", {}
```

**Decision Logic:**
- If `answer_directly`: Skip to direct response (no skill invocation)
- If `partial_data_available`: Continue to Step 1.2, pass `extracted_data` to planning
- If `new_research`: Continue to Step 1.2 normally

**1.2 Classify Question Type** (using table above) (formerly 1.1)

- Extraction/Clarification → Answer directly
- Extension/Comparison/New Research → Continue to Step 1.3

**1.3 Identify Research Parameters** (formerly 1.2)

1. Identify research type (company/industry/strategy/macro/quantitative)
2. Extract parameters (entities, time horizon, focus areas)
3. **CRITICAL: Get current system time and infer time-related queries with disclosure lag**:
   ```python
   from datetime import datetime
   current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
   current_date = datetime.now().strftime("%Y-%m-%d")
   current_year = datetime.now().year
   current_month = datetime.now().month
   # Infer current quarter: Q1(1-3), Q2(4-6), Q3(7-9), Q4(10-12)
   current_quarter = (current_month - 1) // 3 + 1

   # IMPORTANT: Consider financial report disclosure lag
   # Quarterly reports: disclosed 1-2 months after quarter end
   # Annual reports: disclosed Jan-Apr of following year
   # "最新季报" means "latest DISCLOSED quarterly report", not just latest calendar quarter

   # Estimate latest disclosed quarter (conservative approach):
   if current_month <= 2:  # Jan-Feb
       # Q4 of previous year likely not disclosed yet
       latest_disclosed_q = 3
       latest_disclosed_year = current_year - 1
   elif current_month <= 5:  # Mar-May
       # Q4 of previous year should be disclosed
       latest_disclosed_q = 4
       latest_disclosed_year = current_year - 1
   elif current_month <= 8:  # Jun-Aug
       # Q1 of current year should be disclosed
       latest_disclosed_q = 1
       latest_disclosed_year = current_year
   elif current_month <= 11:  # Sep-Nov
       # Q2 of current year should be disclosed
       latest_disclosed_q = 2
       latest_disclosed_year = current_year
   else:  # Dec
       # Q3 of current year should be disclosed
       latest_disclosed_q = 3
       latest_disclosed_year = current_year
   ```
   - Use these ACTUAL values to infer "最新季报", "最近两个季度", etc.
   - When user says "最新季报", use latest_disclosed_q/year, NOT current_quarter
   - When user says "最近两个季度", calculate from latest_disclosed_q backwards
   - When user says "近期", determine appropriate date_range parameter
4. Use AskUserQuestion for ambiguities
5. **Create output directory NOW**:
   ```python
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   output_dir = f"output/{topic}_{timestamp}"
   os.makedirs(output_dir, exist_ok=True)
   ```

**Why create dir now**: Prevents forgetting Step 5. Directory exists = commitment to save files.

**Critical Time Inference Logic** (based on ACTUAL system time + disclosure lag):
- Calculate current quarter from current month
- **CRITICAL: Consider disclosure lag** - quarterly reports disclosed 1-2 months after quarter end
- "最新季报" means **latest DISCLOSED quarter**, not current calendar quarter
  - Example: If today is 2026-02-10 (Q1), Q4 2025 may not be disclosed yet
  - Latest disclosed quarter is likely 2025年Q3 (disclosed in Oct 2025)
- "最近两个季度" means two most recent **DISCLOSED** quarters
  - Example: If today is 2026-02-10, likely means 2025年Q2 and Q3
- "近期业绩" → Use date_range="past_quarter"
- Always verify if target quarter data is likely disclosed based on current date

### Step 2: Read Reference Documents

**MANDATORY - NO EXCEPTIONS**: Before Step 3, you MUST read these files using Read tool:

```
1. references/mcp_tools.md - MCP tool capabilities and syntax
2. references/research_workflows.md - Research type templates
3. references/planning_guide.md - Task decomposition strategies
```

**DO NOT**:
- ❌ Skip reading because "I know MCP tools"
- ❌ Skim and proceed
- ❌ Read while planning (read BEFORE planning)
- ❌ Rely on memory from previous sessions

**Red Flags for Step 2 Violations**:
- You're writing JSON plan without having read references
- You're making MCP queries without reading mcp_tools.md
- You think you already know the content

| Excuse | Reality |
|--------|---------|
| "I used MCP tools before" | Syntax changes. Parameters vary. Read it. |
| "References are just documentation" | They contain critical query patterns. |
| "Reading wastes time" | Wrong queries waste MORE time. |
| "I'll check references if stuck" | Read first prevents getting stuck. |

### Step 3: Create Research Plan

**REQUIRED OUTPUT**: Valid JSON plan structure (see below)

**MANDATORY REQUIREMENTS**:
1. MUST generate complete JSON plan
2. **MUST use matched question type's REFERENCE WORKFLOW as template** (from Step 1.0)
3. MUST save plan to `{output_dir}/plan.json`
4. MUST validate structure before Step 4
5. MUST show plan to user before execution
6. **MUST get system time using datetime.now() and include in plan** (current_date, current_year, current_quarter)

**NEW: Using Matched Workflow Template**

The plan structure MUST follow the `reference_workflow` from the matched question type:

1. **Map Workflow Steps to Tasks**:
   ```python
   # matched_workflow from Step 1.0 contains:
   # - reference_workflow: ["步骤1: 描述", "步骤2: 描述", ...]

   tasks = []
   for idx, step_description in enumerate(matched_workflow['reference_workflow']):
       task = {
           "id": idx + 1,
           "description": step_description,  # Use workflow step as task description
           "dependencies": [],  # Determine based on workflow order
           "hints": {
               # Extract hints from step description or use defaults
           }
       }
       tasks.append(task)
   ```

2. **Apply Reference Rules as Constraints**:
   ```python
   # matched_workflow['reference_rules'] contains guiding principles
   # Add these as planning constraints in the plan metadata

   plan['planning_constraints'] = {
       'question_type': matched_workflow['question_type'],
       'reference_rules': matched_workflow['reference_rules'],
       'template_source': 'plan_for_question_type.xlsx'
   }
   ```

3. **Customize Task Hints Based on User Query**:
   - While task descriptions come from the template, customize the `hints` section
   - Map user's specific entities/time periods into the template structure
   - Preserve template workflow order and task breakdown

**JSON Structure** (Enhanced with Question Type Metadata):
```json
{
  "research_type": "company|industry|strategy|macro|quantitative",
  "topic": "研究主题",
  "current_date": "YYYYMMDD-HHMMSS (from datetime.now())",
  "current_year": 2024,
  "current_quarter": 1,
  "objectives": ["目标1", "目标2"],

  "question_type_metadata": {
    "matched_type": "如何做好公司研究",
    "type_description": "描述",
    "confidence_score": 0.85,
    "template_source": "plan_for_question_type.xlsx"
  },

  "planning_constraints": {
    "reference_rules": ["规则1", "规则2"],
    "workflow_template": ["步骤1", "步骤2"]
  },

  "data_strategy": {
    "available_from_chat_history": {
      "turn_N": {
        "entity": "实体名称",
        "time_period": "时间段",
        "metrics_available": ["指标1", "指标2"],
        "retrieval_timestamp": "YYYYMMDD-HHMMSS"
      }
    },
    "new_data_needed": {
      "entities": ["新实体"],
      "time_periods": ["新时间段"],
      "metrics": ["新指标"]
    },
    "duplicate_query_prevention": [
      "DO NOT re-query [entity] [time_period] - data available from Turn N"
    ]
  },
  "tasks": [
    {
      "id": 1,
      "description": "步骤1描述 (from reference_workflow)",
      "template_step": "步骤1原文",
      "dependencies": [],
      "hints": {
        "data_needs": ["数据类型"],
        "data_available_from_turn_N": "实体X 时间T: 指标A=值1, 指标B=值2",
        "only_retrieve": "明确列出需要新检索的数据",
        "reuse_strategy": "如何结合chat history数据与新检索数据",
        "customization": "基于用户查询的定制化提示",
        "key_questions": ["问题"],
        "suggested_tools": ["info_search_finance_db"],
        "time_context": "明确的时间范围(基于current_date推算,如'2024年Q3和Q4',避免'最近'等模糊表述)"
      }
    }
  ]
}
```

**DO NOT**:
- ❌ Skip JSON and do narrative description
- ❌ Make plan "in your head" without writing it
- ❌ Start execution without user seeing plan
- ❌ Proceed with invalid JSON structure

**Red Flags for Step 3 Violations**:
- Moving to queries without JSON file created
- Thinking "plan is simple, I'll skip formalism"
- Starting to explain what you'll do instead of writing JSON

| Excuse | Reality |
|--------|---------|
| "Plan is obvious" | Writing exposes assumptions and gaps. |
| "JSON is bureaucratic" | Structure enables parallelism. |
| "I'll plan as I go" | Leads to sequential execution and inefficiency. |
| "User didn't ask for plan" | Process requires it. Not negotiable. |

**Validation Code**:
```python
# MUST validate before Step 4
assert 'research_type' in plan
assert 'tasks' in plan
assert all('id' in t and 'dependencies' in t for t in plan['tasks'])
# Validate no circular dependencies
assert is_acyclic(plan['tasks'])
```

### Step 4: Execute Research Plan

**MANDATORY TOOL**: Use `Task` tool with `subagent_type="general-purpose"`

**REQUIRED EXECUTION PATTERN**:
1. Parse plan into execution waves (tasks with satisfied dependencies)
2. For EACH wave, spawn ALL tasks in parallel using Task tool in ONE message
3. Wait for wave completion before proceeding to next wave
4. Collect task outputs (each returns JSON with `section_analysis` and `retrieved_files`)

**DO NOT**:
- ❌ Execute MCP queries yourself
- ❌ Run tasks sequentially when they can be parallel
- ❌ Skip Task tool and do inline execution
- ❌ Forget to pass task context to subagents

**Red Flags for Step 4 Violations**:
- Calling mcp__ashare-mcp-research tools directly in main conversation
- Running tasks one at a time when they have no dependencies
- Thinking "Task tool overhead isn't worth it"

| Excuse | Reality |
|--------|---------|
| "I'm faster than Task tool" | You're sequential. Task tool is parallel. |
| "Simple research doesn't need subagents" | Skill triggered = use Task tool. |
| "Task tool is for complex cases" | It's for ALL cases in this skill. |
| "I'll parallelize manually" | Task tool handles waves correctly. |

**Subagent Prompt Template** (passed to Task tool):
```markdown
You are executing Task {task_id} for research on "{topic}".

## CRITICAL REQUIREMENTS
1. **Current system time**: {current_date} (Format: YYYYMMDD-HHMMSS)
   - Current year: {current_year}
   - Current quarter: Q{current_quarter}
   - Use these ACTUAL values to infer time-related queries
2. Read references/mcp_tools.md FIRST
3. **Check Chat History Data BEFORE querying MCP**
4. Execute MCP queries ONLY for missing data
5. Return JSON with section_analysis, retrieved_files, AND data_source_breakdown

## Chat History Data (DO NOT Re-Query)
{available_data_from_previous_turns}

**Examples:**
- Turn 1 retrieved: 宁德时代 2024 Q3 - 营收1000亿, 毛利率25%, ROE18% (timestamp: 20260211-143022)
- Turn 2 retrieved: 比亚迪 2024 Q3 - 营收800亿, 毛利率22%, ROE15% (timestamp: 20260211-143518)

**CRITICAL: Duplicate Query Prevention (MANDATORY VALIDATION)**

**BEFORE calling any MCP tool (`info_search_finance_db`, `info_search_stock_db`), you MUST:**
1. Check if the EXACT data (entity + time period + metric) is listed in "Chat History Data" above
2. If listed AND timestamp <10 minutes ago → **DO NOT call MCP tool**
   - Use the value directly from chat history
   - Cite source: "数据来源: Turn N检索 (timestamp)"
3. If data is stale (>10 minutes) OR not exactly matching (different time period/metric) → Query MCP

**VALIDATION REQUIREMENT**:
- If you query MCP for data that is listed in "Chat History Data" AND <10 min old, you MUST explain why in `data_source_breakdown.duplicate_query_explanation`
- Valid reasons: "User explicitly requested fresh data", "Chat history data incomplete (missing X metric)"
- Invalid reason: "To ensure accuracy" (chat history IS accurate)

**Track data sources in your response** - this is audited for duplicate query prevention

## Time Inference Guide
- When query mentions "最新/最近/近期", calculate based on current_year, current_quarter, AND disclosure lag
- **CRITICAL: Disclosure Lag Awareness**
  - Quarterly reports: disclosed 1-2 months after quarter end
  - "最新季报" means latest DISCLOSED report, not latest calendar quarter
  - Example: If current_date is 20260210 (Feb 2026, Q1), Q4 2025 may NOT be disclosed yet
  - Latest disclosed quarter might be Q3 2025 (disclosed Oct 2025)
- "最新季报" → Calculate latest DISCLOSED quarter considering disclosure lag
- "最近两个季度" → Two most recent DISCLOSED quarters (may not include current or just-ended quarter)
- Always include explicit time periods in MCP queries (e.g., "2025年Q2和Q3" not "最近两个季度")
- Handle year rollover: If current_quarter=1, previous quarters may be in previous year
- **Verify data availability**: If MCP returns "未披露", acknowledge and explain disclosure lag

## Your Task
{task_description}

## Hints
{hints}

## Output Format
Return JSON:
{
  "section_analysis": "## Title\\n\\nComplete analysis text (800-1500 words)",
  "retrieved_files": [
    {
      "file_id": 123,
      "title": "...",
      "publish_date": "...",
      "data_source": "info_search_finance_db",  // EXACT tool name
      "query": "..."
    }
  ],
  "data_source_breakdown": {
    "from_chat_history": [
      {"metric": "宁德时代 Q3 毛利率", "value": "25%", "source": "Turn 1"}
    ],
    "from_new_retrieval": [
      {"metric": "宁德时代 Q2 毛利率", "value": "23%", "source": "MCP query"}
    ]
  }
}
```

### Step 5: Synthesize and Analyze

**REQUIRED OUTPUTS**:
1. Aggregate `retrieval_metadata.json` from all task outputs
2. Synthesize final `report.md` from all section analyses
3. Generate `generation_log.md` with execution details

**MANDATORY ACTIONS**:
1. Extract `retrieved_files` from ALL task outputs
2. Build master metadata structure
3. Assemble final report with all sections
4. Validate completeness

**DO NOT**:
- ❌ Skip metadata aggregation
- ❌ Forget to count data sources
- ❌ Save incomplete report

**Master Metadata Structure**:
```json
{
  "research_session": {
    "topic": "...",
    "timestamp": "...",
    "total_files_retrieved": 42
  },
  "tasks": [
    {
      "task_id": 1,
      "description": "...",
      "files": [/* all retrieved_files */]
    }
  ],
  "data_source_summary": {
    "info_search_finance_db": 28,
    "info_search_stock_db": 10,
    "info_search_user_db": 0,
    "info_search_web": 4
  }
}
```

### Step 6: Save All Output Files

**MANDATORY FILE SAVES**:

```
output/{topic}_{timestamp}/
├── report.md                    ← Final research report (REQUIRED)
├── plan.json                    ← Research plan (REQUIRED)
├── retrieval_metadata.json      ← Data lineage (REQUIRED)
└── generation_log.md            ← Execution log (REQUIRED)
```

**CRITICAL**: ALL 4 files must be saved. Missing any file = incomplete execution.

**DO NOT**:
- ❌ Output report to chat only
- ❌ Skip saving metadata
- ❌ Forget generation log
- ❌ Save some files but not all

**Red Flags for Step 6 Violations**:
- Presenting report in chat without file saves
- Thinking "user can see output already"
- Forgetting to create files until user asks

| Excuse | Reality |
|--------|---------|
| "User can see output in chat" | Files enable reproducibility and audit. |
| "I'll save if user asks" | Save is mandatory, not optional. |
| "Output is just for reference" | All research must be saved. |
| "I forgot" | Create output dir in Step 1 to prevent this. |

**Completion Message**:
```
研究报告已生成并保存至: output/{topic}_{timestamp}/

生成的文件:
- report.md (主报告)
- plan.json (研究计划)
- retrieval_metadata.json (数据溯源)
- generation_log.md (执行日志)
```

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "User wants quick answer" | Skill triggered = full process required |
| "This is simple research" | Simple becomes complex. Follow process. |
| "I'll optimize by skipping steps" | Process IS the optimization |
| "Planning wastes time" | Wrong execution wastes MORE time |
| "I know what to do" | Writing plan exposes blind spots |
| "Task tool adds overhead" | Parallelism saves MORE time |
| "I'll save files later" | You'll forget. Save as you go. |
| "Spirit over letter" | Letter IS spirit. No shortcuts. |
| **"'最新季报' is clear enough"** | **Get system time, calculate explicit quarters. Pass to subagents.** |
| **"Time context is obvious"** | **Pass current_date/year/quarter to subagents. They can't access system time.** |
| **"Current quarter is 'latest'"** | **NO. Latest = latest DISCLOSED (1-2 months lag). Calculate carefully.** |
| **"Just use current_quarter - 1"** | **NO. Consider disclosure lag. Feb 2026 → Q3 2025, not Q4 2025.** |
| **"Follow-up is continuation of Turn 1"** | **NO. Classify question type. Extraction → direct answer. New research → new invocation.** |
| **"'对比一下B公司' is just adding data"** | **Comparison = invoke skill BUT reuse A from Turn 1, retrieve only B.** |
| **"'毛利率呢?' doesn't need deliverable"** | **If Turn 1 has毛利率, answer directly (no deliverable). If not, invoke skill.** |
| **"User said '再分析' so I continue analyzing"** | **'Again' = invoke skill again, not continue current process.** |
| **"This follow-up is too narrow/simple"** | **Check chat history first. If data available, answer directly. If not, invoke skill.** |
| **"I should re-query to ensure freshness"** | **<10 min data is fresh. Re-query wastes quota and causes inconsistency.** |
| **"Comparison requires retrieving both entities"** | **NO. Retrieve only missing entity. Reuse available data from chat history.** |
| **"All financial questions invoke skill"** | **NO. Extraction/Clarification can be answered directly from chat history.** |
| **"Chat history might be inaccurate"** | **Chat history from Turn N-1 is authoritative source. Trust it.** |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Direct MCP queries without plan | Write JSON plan first |
| Sequential execution of independent tasks | Use Task tool with waves |
| No output files saved | Create output dir in Step 1 |
| Skipped reading references | Read before planning |
| Incomplete metadata tracking | Collect retrieved_files from ALL tasks |
| Missing generation_log.md | Document execution as you proceed |
| **Using vague time expressions in queries** | **Get datetime.now(), convert to explicit quarters, pass to subagents** |
| **Not inferring time context** | **Use datetime.now() to calculate quarters, not hardcoded dates** |
| **Forgetting time fields in plan.json** | **Include current_date, current_year, current_quarter from datetime.now()** |
| **Ignoring disclosure lag** | **"最新季报" ≠ current quarter. Consider 1-2 month disclosure lag.** |
| **Assuming all quarters are disclosed** | **Verify: Q4 disclosed Mar-Apr, Q3 in Oct-Nov, Q2 in Jul-Aug, Q1 in Apr-May** |
| **Re-invoking skill for data in Turn N-1** | **Check chat history first. Extraction/Clarification → answer directly.** |
| **Duplicate queries in comparison tasks** | **Reuse Entity A from Turn 1, plan retrieves only Entity B.** |
| **Not checking question type** | **Classify: Extraction/Clarification vs New Research before invoking.** |
| **Ignoring data_strategy in plan** | **Include available_from_chat_history and duplicate_query_prevention.** |
| **Not passing chat history to subagents** | **Include {available_data_from_previous_turns} in subagent prompt.** |
| **Not reading Excel in Step 1.0** | **Load question types BEFORE creating plan** |
| **Using custom plan structure instead of template** | **Use matched workflow as task template** |
| **Proceeding with confidence <0.6 without confirmation** | **Ask user to confirm at low confidence** |
| **Not including question_type_metadata in plan** | **Always record which type was matched** |
| **Skipping workflow extraction** | **Extract reference_rules and reference_workflow from matched type** |

## Tool Usage Summary

**MCP Tools** (via subagents):
- `info_search_finance_db` - Research reports, news, announcements
- `info_search_stock_db` - Quantitative financial data (metrics, prices)
- `info_search_user_db` - User-uploaded documents
- `info_search_web` - Web search fallback

**Main Tools** (direct usage):
- `Read` - Read reference documents (Step 2)
- `Task` - Spawn subagents for parallel execution (Step 4)
- `Write` - Save output files (Step 6)
- `AskUserQuestion` - Clarify requirements (Step 1)

## Complete Multi-Turn Example (Chat History Reuse)

**Turn 1: Initial Research**
- User: "分析宁德时代2024年Q3季报"
- Action: Invoke skill (new research)
- Plan task: Retrieve 宁德时代 Q3 metrics
- Subagent queries MCP, retrieves: 营收1000亿, 毛利率25%, ROE18%, 净利润150亿
- Output: report.md saved, shows all metrics

**Turn 2: Extraction (Answer Directly)**
- User: "毛利率是多少?"
- Step 1.0: Check chat history → 毛利率=25% found in Turn 1 (3 minutes ago)
- Question Type: **Extraction**
- Action: Answer directly WITHOUT skill invocation
- Response: "根据刚才检索的宁德时代2024年Q3季报,毛利率为25%"
- Time: <5 seconds
- MCP queries: 0

**Turn 3: Comparison (Smart Planning)**
- User: "对比一下比亚迪的"
- Step 1.0: 宁德时代 data in Turn 1, 比亚迪 NOT in history → `partial_data_available`
- Question Type: **Comparison (Partial New)**
- Action: Invoke skill with data_strategy
- Plan.json:
```json
{
  "data_strategy": {
    "available_from_chat_history": {
      "turn_1": {
        "entity": "宁德时代",
        "time_period": "2024 Q3",
        "metrics_available": ["营收", "毛利率", "ROE", "净利润"],
        "retrieval_timestamp": "20260211-143022"
      }
    },
    "new_data_needed": {
      "entities": ["比亚迪"],
      "time_periods": ["2024 Q3"],
      "metrics": ["营收", "毛利率", "ROE", "净利润"]
    },
    "duplicate_query_prevention": [
      "DO NOT re-query 宁德时代 Q3 - data in Turn 1"
    ]
  },
  "tasks": [{
    "id": 1,
    "description": "对比宁德时代与比亚迪2024年Q3财务指标",
    "hints": {
      "data_available_from_turn_1": "宁德时代 Q3: 营收1000亿, 毛利率25%, ROE18%, 净利润150亿",
      "only_retrieve": "比亚迪 2024 Q3 财务数据",
      "reuse_strategy": "使用Turn 1宁德时代数据,仅检索比亚迪数据"
    }
  }]
}
```
- Subagent receives:
```markdown
## Chat History Data (DO NOT Re-Query)
- Turn 1: 宁德时代 2024 Q3 - 营收1000亿, 毛利率25%, ROE18%, 净利润150亿 (20260211-143022)

## Your Task
对比宁德时代与比亚迪2024年Q3财务指标
**ONLY retrieve 比亚迪 data. Use 宁德时代 data from Turn 1.**
```
- Subagent queries MCP ONLY for 比亚迪 Q3 data
- Subagent output:
```json
{
  "section_analysis": "## 宁德时代 vs 比亚迪 2024 Q3对比分析\n\n宁德时代营收1000亿...",
  "retrieved_files": [{"entity": "比亚迪", "file_id": 456}],
  "data_source_breakdown": {
    "from_chat_history": [
      {"entity": "宁德时代", "metrics": "营收1000亿, 毛利率25%, ROE18%", "source": "Turn 1"}
    ],
    "from_new_retrieval": [
      {"entity": "比亚迪", "metrics": "营收800亿, 毛利率22%, ROE15%", "source": "MCP query"}
    ]
  }
}
```
- Time: 3-4 minutes (vs 5-6 min if re-queried both)
- MCP queries: 1 (vs 2 in baseline)
- Efficiency gain: 50% fewer queries, 30% faster

## Example Triggers

Requests that should trigger this skill:
- "宁德时代深度研究报告"
- "对比宁德时代最新两个季报"
- "分析比亚迪Q3和Q4财报"
- "研究新能源汽车行业竞争格局"
- "对比英伟达和AMD的AI芯片业务"
- "茅台vs五粮液财务对比"
- "理想汽车最近几个季度业绩变化"
- "2025年港股市场展望"
- "分析美联储政策对A股影响"
- "特斯拉估值分析"
- "半导体行业研究"
- "腾讯营收增长趋势"

## Performance Expectations

- Simple research (4-5 tasks): 3-5 minutes
- Medium research (6-8 tasks): 5-8 minutes
- Complex research (10+ tasks): 8-12 minutes

Efficiency comes from parallelism, not skipping steps.

---

**REMEMBER**: This skill is discipline-enforcing. Follow every step. No exceptions. No rationalizations.
