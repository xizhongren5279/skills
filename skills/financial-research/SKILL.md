---
name: financial-research
description: Use when users request financial research beyond simple one-page summaries - company deep-dives, industry analysis, strategy research, macro research, or quantitative analysis requiring structured investigation with data retrieval and synthesis
---

# Financial Research

## Overview

This skill enforces a **structured 6-step research process** using MCP tools, Task-based parallel execution, and mandatory output file generation.

**Core Principle**: Research = Plan → Execute → Synthesize → Save. Skip any step and the research is incomplete.

**Violating the letter of the rules is violating the spirit of the rules.**

## The Iron Law

```
NO DIRECT MCP QUERIES WITHOUT A JSON PLAN FIRST
NO ANALYSIS WITHOUT TASK TOOL EXECUTION
NO COMPLETION WITHOUT OUTPUT FILES SAVED
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
- Quick factual lookups
- Conversational Q&A without deliverable

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

**All of these mean: STOP. Start with Step 1.**

## Research Process

### Step 1: Understand the Request

**REQUIRED ACTIONS**:
1. Identify research type (company/industry/strategy/macro/quantitative)
2. Extract parameters (entities, time horizon, focus areas)
3. Use AskUserQuestion for ambiguities
4. **Create output directory NOW**:
   ```python
   timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   output_dir = f"output/{topic}_{timestamp}"
   os.makedirs(output_dir, exist_ok=True)
   ```

**Why create dir now**: Prevents forgetting Step 5. Directory exists = commitment to save files.

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
2. MUST save plan to `{output_dir}/plan.json`
3. MUST validate structure before Step 4
4. MUST show plan to user before execution

**JSON Structure**:
```json
{
  "research_type": "company|industry|strategy|macro|quantitative",
  "topic": "研究主题",
  "objectives": ["目标1", "目标2"],
  "tasks": [
    {
      "id": 1,
      "description": "章节级描述",
      "dependencies": [],
      "hints": {
        "data_needs": ["数据类型"],
        "key_questions": ["问题"],
        "suggested_tools": ["info_search_finance_db"]
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
1. Read references/mcp_tools.md FIRST
2. Execute MCP queries for this task
3. Return JSON with section_analysis and retrieved_files

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
  ]
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

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Direct MCP queries without plan | Write JSON plan first |
| Sequential execution of independent tasks | Use Task tool with waves |
| No output files saved | Create output dir in Step 1 |
| Skipped reading references | Read before planning |
| Incomplete metadata tracking | Collect retrieved_files from ALL tasks |
| Missing generation_log.md | Document execution as you proceed |

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

## Example Triggers

Requests that should trigger this skill:
- "宁德时代深度研究报告"
- "研究新能源汽车行业竞争格局"
- "对比英伟达和AMD的AI芯片业务"
- "2025年港股市场展望"
- "分析美联储政策对A股影响"

## Performance Expectations

- Simple research (4-5 tasks): 3-5 minutes
- Medium research (6-8 tasks): 5-8 minutes
- Complex research (10+ tasks): 8-12 minutes

Efficiency comes from parallelism, not skipping steps.

---

**REMEMBER**: This skill is discipline-enforcing. Follow every step. No exceptions. No rationalizations.
