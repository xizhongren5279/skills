---
name: financial-research
description: Comprehensive financial research skill for company research, industry analysis, strategy research, macro research, and quantitative analysis. Use when users request any type of financial research tasks, investment analysis, market analysis, economic research, or data-driven financial insights. Supports queries like "研究XX行业的竞争格局", "分析XX宏观经济指标", "对比XX和XX公司", "制定XX投资策略", or any financial research needs beyond simple one-page company reports.
---

# Financial Research

## Overview

This skill provides a comprehensive framework for conducting various types of financial research by intelligently planning retrieval strategies and maximizing parallel execution efficiency using available MCP tools.

## Core Capabilities

1. **Company Research** - Deep-dive analysis beyond one-pagers (detailed financials, business model, competitive positioning)
2. **Industry Research** - Market structure, trends, competitive dynamics, key players
3. **Strategy Research** - Investment themes, sector rotation, portfolio construction
4. **Macro Research** - Economic indicators, policy analysis, market implications
5. **Quantitative Analysis** - Financial metrics comparison, valuation models, performance analysis

## Critical Reference Documents

**Must consult before execution**:

1. **`references/mcp_tools.md`**
   - Complete documentation of all 4 available MCP tools
   - Query syntax, parameters, use cases, and limitations
   - **Role**: Understanding WHAT data retrieval capabilities are available

2. **`references/research_workflows.md`**
   - Workflow templates for each research type
   - Best practices for structuring analysis
   - **Role**: Understanding HOW to approach different research types

3. **`references/planning_guide.md`**
   - Framework for creating efficient research plans
   - Strategies for optimizing serial vs parallel execution
   - **Role**: Understanding HOW to maximize retrieval efficiency

## Research Process

### Step 1: Understand the Request

When a user submits a research request:

1. **Identify the research type**:
   - Company research (specific company deep-dive)
   - Industry research (sector/market analysis)
   - Strategy research (investment themes/ideas)
   - Macro research (economic/policy analysis)
   - Quantitative analysis (data comparison/modeling)
   - Hybrid (combines multiple types)

2. **Extract key parameters**:
   - Target entities (companies, industries, markets)
   - Time horizon (historical periods, forecast periods)
   - Specific questions/focus areas
   - Output format requirements

3. **Clarify ambiguities** (if needed):
   - Use AskUserQuestion for unclear scope or preferences
   - Confirm output detail level
   - Validate entity identification (especially Chinese vs English names)

### Step 2: Read Reference Documents

**MANDATORY**: Before creating any plan, read the relevant reference documents:

```markdown
Read references/mcp_tools.md to understand:
- Which MCP tools can answer which types of questions
- Query syntax and parameter options
- Data availability and limitations

Read references/research_workflows.md section matching your research type to understand:
- Recommended analysis structure
- Key questions to address
- Common pitfalls to avoid

Read references/planning_guide.md to understand:
- How to structure plans for maximum efficiency
- Serial vs parallel execution strategies
- Task decomposition principles
```

### Step 3: Create Research Plan

Based on the request and reference documents, create a structured research plan:

**Plan Structure**:

Generate a JSON plan with the following structure:

```json
{
  "research_type": "company|industry|strategy|macro|quantitative",
  "topic": "研究主题描述",
  "objectives": [
    "目标1",
    "目标2",
    "目标3"
  ],
  "tasks": [
    {
      "id": 1,
      "description": "分析任务的高层次描述（章节级别）",
      "dependencies": [],
      "hints": {
        "data_needs": ["需要的数据类型1", "需要的数据类型2"],
        "key_questions": ["关键问题1", "关键问题2"],
        "suggested_tools": ["info_search_finance_db", "info_search_stock_db"]
      }
    }
  ]
}
```

**Field Definitions**:

**Top-level fields**:
- `research_type`: Research type (company/industry/strategy/macro/quantitative)
- `topic`: Research topic description
- `objectives`: List of research objectives
- `tasks`: Array of task objects

**Task object fields**:
- `id`: Task ID (positive integer, sequential)
- `description`: High-level analysis task description (section-level abstraction)
- `dependencies`: Array of task IDs that this task directly depends on (empty array if no dependencies)
- `hints`: Optional execution hints object
  - `data_needs`: Types of data needed
  - `key_questions`: Key questions to address
  - `suggested_tools`: Recommended MCP tools

**Dependency Rules**:
1. Only include **direct dependencies** in the dependencies array
2. Use empty array `[]` for tasks with no dependencies
3. Task IDs must be sequential positive integers starting from 1
4. Dependencies must reference valid task IDs that exist in the plan
5. No circular dependencies allowed (validate with topological sort)

**Task Abstraction Level**:
- Tasks should be at **chapter/section level** (e.g., "Financial performance analysis")
- Each task corresponds to one major section in the final report
- Subagents will determine specific MCP queries based on hints
- Typical plan has 4-7 tasks total

**Key Principles**:

1. **Flat task structure**: No Phase concept; use dependencies array to express execution order
2. **Maximize parallelism**: Default to empty dependencies unless true dependency exists
3. **Section-level abstraction**: Each task = one major report section (800-1500 words)
4. **Dependency minimization**: Only declare direct dependencies; system infers transitive dependencies
5. **Clear hints**: Provide execution guidance without over-specifying exact queries
6. **Optimize task count**: Target 4-7 tasks for balanced parallelism and manageability

### Step 4: Execute Research Plan

Once the JSON plan is generated:

**1. Validate plan structure**:
```python
# Validate JSON structure
def validate_plan(plan):
    # Check required fields
    assert 'research_type' in plan
    assert 'topic' in plan
    assert 'objectives' in plan
    assert 'tasks' in plan

    # Check task structure
    task_ids = set()
    for task in plan['tasks']:
        assert 'id' in task
        assert 'description' in task
        assert 'dependencies' in task
        task_ids.add(task['id'])

    # Validate dependencies reference valid IDs
    for task in plan['tasks']:
        for dep_id in task['dependencies']:
            assert dep_id in task_ids, f"Invalid dependency: {dep_id}"

    # Check for circular dependencies (topological sort)
    assert is_acyclic(plan['tasks']), "Circular dependency detected"
```

**2. Parse dependencies and identify execution waves**:
```python
# Identify tasks by wave
completed = set()
waves = []

while len(completed) < len(plan['tasks']):
    # Find tasks with all dependencies satisfied
    current_wave = [
        task for task in plan['tasks']
        if task['id'] not in completed
        and all(dep_id in completed for dep_id in task['dependencies'])
    ]

    if not current_wave:
        raise Exception("Circular dependency or orphaned tasks detected")

    waves.append(current_wave)
    completed.update(task['id'] for task in current_wave)
```

**3. Execute waves sequentially, tasks within wave in parallel**:

For each wave:
- Spawn ALL tasks in the wave using Task tool with general-purpose subagents in a single message
- Each subagent receives the task description, hints, and any dependent task results
- Subagent reads references/mcp_tools.md, executes MCP queries, and returns complete section analysis
- Wait for all tasks in wave to complete before proceeding to next wave

**4. Subagent prompt template**:

```markdown
You are executing Task {task_id} for the research plan on "{topic}".

## Research Context
- Research Type: {research_type}
- Topic: {topic}
- Objectives: {objectives}

## Your Task
{task_description}

## Execution Hints
- Data Needs: {hints.data_needs}
- Key Questions: {hints.key_questions}
- Suggested Tools: {hints.suggested_tools}

{If task has dependencies:}
## Context from Previous Tasks
{Include section text from dependent tasks}

## Execution Requirements
1. Read `references/mcp_tools.md` to understand available MCP tools
2. Based on the task requirements and hints, determine which MCP queries to execute
3. Execute the necessary MCP tool calls
4. Analyze the retrieved data
5. Write a complete section analysis (800-1500 words) with:
   - Specific quantitative data (numbers, percentages, dates)
   - Data source citations
   - Clear insights and findings

## Output Format
Return your analysis as a complete Markdown section:

\`\`\`markdown
## {Section Title Based on Task Description}

{Your analysis with quantitative data, insights, and source citations}
\`\`\`

CRITICAL: Return完整的section分析文本, not raw retrieval results.
```

**5. Progress tracking**:
- Display wave indicators: "执行Wave 1: 3个并行任务..."
- Show task completion: "Task 1 完成: 公司概况与业务模式分析"
- Report wave completion: "Wave 1 完成，进入Wave 2..."

**6. Error handling**:
- If a task fails, mark it as failed and block dependent tasks
- Continue executing independent tasks
- Use placeholder for failed sections: "[数据获取失败: {reason}]"

### Step 5: Synthesize and Analyze

After all tasks complete:

**1. Collect section analyses**:
- Input: All section analysis texts from completed tasks
- Each section is already analyzed and written (not raw data)

**2. Integration tasks**:
- **Consistency check**: Verify data consistency across sections (e.g., revenue numbers match)
- **Gap filling**: Identify missing critical information, add notes where data unavailable
- **Flow improvement**: Add transitional paragraphs between sections if needed
- **Executive summary**: Create summary of key findings from all sections

**3. Quality validation**:
- All sections present (or marked as failed with reason)
- Quantitative data included in each section
- No placeholder text in successful sections
- Source citations present
- Logical narrative flow

**4. Assemble final report**:
```markdown
# {topic}

**生成时间**: {timestamp}
**研究类型**: {research_type}

## 核心发现

{Executive summary: 3-5 bullet points of key findings}

## 详细分析

{Section 1 from Task 1}

{Section 2 from Task 2}

...

{Section N from Task N}

## 数据来源

- 金融数据库检索: {count} queries
- 用户文档库: {count} queries (if applicable)
- 网络搜索: {count} queries (if applicable)

---

*本报告由financial-research skill生成 | {timestamp}*
```

**5. Save outputs**:

All generated files are saved to a unified output directory:

```
output/{topic}_{timestamp}/
├── report.md                    # Main research report
├── generation_log.md           # Execution log with wave details
├── retrieval_metadata.json     # Query logs and data sources
└── plan.json                   # Research plan structure
```

**File Specifications**:
- `report.md`: Main research report following the format template
- `generation_log.md`: Includes JSON plan, wave execution details, task results
- `retrieval_metadata.json`: All query logs with timestamps, tools used, and result counts
- `plan.json`: Original research plan in JSON format

**Python Path Construction**:
```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"output/{topic}_{timestamp}"
os.makedirs(output_dir, exist_ok=True)
```

### Step 6: Generate Final Report

Structure the final report according to the research type:

**Common Elements**:
- Title and metadata (generation time, research type)
- Executive summary (key findings)
- Detailed analysis sections
- Data tables and charts (as applicable)
- Sources and methodology notes
- Footer with generation metadata

**Save output**:
- All files saved to: `output/{topic}_{timestamp}/`
- Confirm with message: "研究报告已保存至: output/{topic}_{timestamp}/"

## Important Guidelines

1. **ALWAYS read references first**: Never skip reading mcp_tools.md, research_workflows.md, and planning_guide.md

2. **Plan before execute**: Always create and present a detailed plan before starting retrieval

3. **Maximize parallelization**: Default to parallel execution unless there are clear dependencies

4. **Use exact MCP syntax**: Follow the exact tool names, query formats, and parameters from mcp_tools.md

5. **Provide progress feedback**: Keep user informed with clear wave indicators

6. **Handle data gaps gracefully**: Use "-" for missing data, note data limitations explicitly

7. **Quantitative focus**: Always include specific numbers, percentages, dates, and concrete data

8. **Language consistency**: Use Chinese for Chinese market research, adjust based on context

9. **Cite sources**: Include reference to data sources (report dates, analyst names, etc.)

10. **Save generation logs**: Always save both the final report and a detailed generation log documenting:
    - Plan structure
    - MCP queries executed
    - Key findings per wave
    - Integration decisions
    - Quality checks performed

## Tool Usage Summary

Available MCP tools (see references/mcp_tools.md for details):

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `info_search_finance_db` | Search research reports, announcements, news | query, date_range, recall_num, doc_type |
| `info_search_user_db` | Search user-uploaded documents | query, user_id, file_ids, recall_num |
| `info_search_stock_db` | Query quantitative financial/market data | query (must include time, company, metric) |
| `info_search_web` | Web search fallback | query |

**Tool selection logic**:
- Company/industry qualitative analysis → `info_search_finance_db`
- User's private documents → `info_search_user_db`
- Quantitative metrics/comparisons → `info_search_stock_db`
- External/recent info not in database → `info_search_web`

## Performance Optimization

**Efficiency Targets**:
- Simple research (3-5 sections): ~2-3 minutes
- Medium research (5-8 sections): ~3-5 minutes
- Complex research (10+ sections): ~5-8 minutes

**Optimization Strategies**:
1. **Aggressive parallelization**: Group 5-10 independent queries per wave
2. **Minimize waves**: Aim for 2-3 waves maximum
3. **Right-size queries**: Use recall_num judiciously (8-15 typically sufficient)
4. **Reuse data**: If multiple sections need same data, retrieve once and reference

## Example Triggers

This skill should activate for requests like:

- "研究新能源汽车行业的竞争格局和发展趋势"
- "深度分析特斯拉的业务模式和盈利能力"
- "对比英伟达和AMD在AI芯片领域的竞争优势"
- "分析2024年美联储政策对A股市场的影响"
- "制定一个聚焦AI主题的投资组合策略"
- "量化分析茅台和五粮液的估值差异"
- "宏观经济视角下的2025年港股市场展望"

## Relationship with Other Skills

**company-one-page skill**: Specialized for quick one-page investment memos with standardized 5-section structure. Use that for "生成XX公司一页纸" requests.

**financial-research skill** (this skill): For all other financial research needs requiring flexible analysis, custom structure, or deeper investigation beyond one-pagers.

---

*This skill leverages parallel execution and intelligent planning to deliver high-quality financial research efficiently.*
