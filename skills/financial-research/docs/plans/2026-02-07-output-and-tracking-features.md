# Output Folder and File Tracking Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add unified output directory structure and track retrieved files metadata for each task in financial-research skill.

**Architecture:**
- Modify SKILL.md to specify output/ directory structure for all generated files
- Add retrieval metadata tracking requirements to subagent prompt template
- Update file saving logic to create structured output folders per research session
- Store full metadata (file_id, title, publish_date, institution_name, company_name, etc.) in single JSON file
- **CRITICAL**: `data_source` field must use exact MCP tool names (`info_search_finance_db`, `info_search_stock_db`, `info_search_user_db`, `info_search_web`) to distinguish between different data retrieval tools

**Tech Stack:** Markdown documentation updates (no code implementation required)

---

## Requirements Summary

### Requirement 1: Store File Information Retrieved by Each Task
- Track full metadata of files/documents retrieved by MCP tools in each task
- Include: file_id, title, publish_date, type_full_name, institution_name, company_name, section, data_source, query
- **CRITICAL**: `data_source` field must distinguish between specific MCP tools:
  - `info_search_finance_db` - Financial database (reports, announcements, news)
  - `info_search_stock_db` - Quantitative stock/market data
  - `info_search_user_db` - User-uploaded documents
  - `info_search_web` - Web search results
- Store in single `retrieval_metadata.json` file with all tasks
- Format: Array of task objects, each containing task_id and retrieved_files array
- Include data_source_summary statistics showing count per MCP tool

### Requirement 2: Unified Output to output/ Folder
- All generated files go to `output/` in skill directory
- Create timestamped subdirectory per research session: `output/{topic}_{YYYYMMDD_HHMMSS}/`
- Save: report.md, generation_log.md, retrieval_metadata.json, plan.json

---

## Task 1: Update SKILL.md with Output Directory Structure

**Files:**
- Modify: `SKILL.md:323-341` (Step 5 and Step 6 sections)

**Step 1: Define output directory structure in SKILL.md**

Locate the "Step 5: Synthesize and Analyze" section, subsection "5. Save outputs" (around line 323).

Replace the existing save outputs specification:

```markdown
**5. Save outputs**:
- Main report: `{topic}_{research_type}_YYYYMMDD_HHMMSS.md`
- Generation log: `{topic}_生成日志_YYYYMMDD_HHMMSS.md` (includes JSON plan, wave execution details, task results)
```

With the new output directory structure:

```markdown
**5. Save outputs**:

All outputs are saved to a timestamped directory in the skill's output folder:

**Directory structure**:
```
output/{topic}_{YYYYMMDD_HHMMSS}/
├── report.md                    # Final research report
├── generation_log.md            # Execution details (plan, waves, task results)
├── retrieval_metadata.json      # File tracking metadata from all tasks
└── plan.json                    # Original execution plan
```

**File specifications**:
- `report.md`: Complete research report with all sections
- `generation_log.md`: JSON plan, wave execution details, task completion info
- `retrieval_metadata.json`: Metadata of all files retrieved by MCP tools (see Requirement 1)
- `plan.json`: The original JSON plan used for execution

**Path construction**:
```python
output_dir = f"output/{sanitize_filename(topic)}_{timestamp}"
os.makedirs(output_dir, exist_ok=True)
```
```

**Step 2: Update Step 6 save output section**

Locate "Step 6: Generate Final Report" section, "Save output" subsection (around line 339).

Replace:
```markdown
**Save output**:
- Filename: `[Topic]_[ResearchType]_YYYYMMDD_HHMMSS.md`
- Also save generation log: `[Topic]_生成日志_YYYYMMDD_HHMMSS.md`
```

With:
```markdown
**Save output**:
- Output directory: `output/{topic}_{YYYYMMDD_HHMMSS}/`
- Files: report.md, generation_log.md, retrieval_metadata.json, plan.json
- Confirm output location to user: "报告已保存至: output/{topic}_{timestamp}/"
```

**Step 3: Verify changes**

Read: `SKILL.md:323-345`
Expected: Updated sections with output/ directory structure documented

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "docs: add output directory structure specification

- All generated files now go to output/{topic}_{timestamp}/
- Includes report.md, generation_log.md, retrieval_metadata.json, plan.json
- Part of unified output folder requirement"
```

---

## Task 2: Add Retrieval Metadata Tracking to Subagent Prompt

**Files:**
- Modify: `SKILL.md:216-258` (Subagent prompt template section)

**Step 1: Add metadata tracking requirements to subagent prompt**

Locate the "4. Subagent prompt template" section in Step 4 (around line 216).

After the "Execution Requirements" section, add a new "Retrieval Metadata Tracking" section:

```markdown
## Retrieval Metadata Tracking

**CRITICAL**: You must track and return metadata for ALL files retrieved by MCP tools.

For each MCP tool query you execute, extract and save the following metadata from each retrieved file:
- `file_id`: Unique file identifier
- `title`: Document title
- `publish_date`: Publication date
- `type_full_name`: Document type (研报/会议纪要/公告/点评/资讯/etc.)
- `institution_name`: Institution/author name (if applicable)
- `company_name`: Related company name (if applicable)
- `section`: Relevant section/excerpt used in analysis
- `data_source`: **CRITICAL - Must specify exact MCP tool name**:
  - Use `info_search_finance_db` for financial database queries (reports, announcements, news)
  - Use `info_search_stock_db` for quantitative stock/market data queries
  - Use `info_search_user_db` for user-uploaded document queries
  - Use `info_search_web` for web search queries
  - **DO NOT use generic values like "MCP" or "database" - always specify the exact tool name**
- `query`: The query string used to retrieve this file

## Output Format

Return your analysis as a complete Markdown section PLUS retrieval metadata:

\`\`\`json
{
  "task_id": {task_id},
  "section_analysis": "## {Section Title}\\n\\n{Your complete analysis text}",
  "retrieved_files": [
    {
      "file_id": "...",
      "title": "...",
      "publish_date": "YYYY-MM-DD",
      "type_full_name": "...",
      "institution_name": "...",
      "company_name": "...",
      "section": "...",
      "data_source": "info_search_finance_db",
      "query": "..."
    }
  ]
}
\`\`\`

**Notes**:
- `section_analysis`: Your complete section text in Markdown format
- `retrieved_files`: Array of all files retrieved, with full metadata
- **`data_source` MUST be exact MCP tool name**: `info_search_finance_db`, `info_search_stock_db`, `info_search_user_db`, or `info_search_web`
- If a field is not applicable, use `null` or empty string
- For `info_search_stock_db` queries (quantitative data), file_id may be "N/A" - still record the query and data source
- **Example data_source values by use case**:
  - Company research report → `info_search_finance_db`
  - Historical revenue data → `info_search_stock_db`
  - User's uploaded PDF → `info_search_user_db`
  - Recent news article → `info_search_web`
```

**Step 2: Update the old output format requirement**

Find the existing "Output Format" section (around line 248) and replace it with the reference to the new format:

```markdown
## Output Format

See "Retrieval Metadata Tracking" section above for the complete JSON output format.

CRITICAL:
1. Return完整的section分析文本 in `section_analysis` field, not raw retrieval results
2. Include full metadata for ALL retrieved files in `retrieved_files` array
3. Both fields are required in your JSON response
```

**Step 3: Verify changes**

Read: `SKILL.md:216-280`
Expected: Subagent prompt now includes retrieval metadata tracking requirements with complete JSON output format

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "docs: add retrieval metadata tracking to subagent prompt

- Subagents must return JSON with section_analysis + retrieved_files
- Track file_id, title, publish_date, institution, company, section, data_source, query
- Enables file tracking requirement for each task"
```

---

## Task 3: Update Step 5 to Handle Retrieval Metadata

**Files:**
- Modify: `SKILL.md:270-326` (Step 5: Synthesize and Analyze)

**Step 1: Add metadata aggregation to Step 5**

Locate "Step 5: Synthesize and Analyze" section, after "1. Collect section analyses" (around line 274).

Add a new subsection before "2. Integration tasks":

```markdown
**1.5. Aggregate retrieval metadata**:

After collecting all task outputs:

1. **Extract metadata from each task**:
   - Each task returns JSON with `section_analysis` and `retrieved_files`
   - Parse the `retrieved_files` array from each task
   - Maintain task_id association

2. **Build master metadata structure**:
```json
{
  "research_session": {
    "topic": "{topic}",
    "research_type": "{research_type}",
    "timestamp": "{YYYYMMDD_HHMMSS}",
    "total_tasks": 6,
    "total_files_retrieved": 45
  },
  "tasks": [
    {
      "task_id": 1,
      "description": "...",
      "files_retrieved": 8,
      "files": [
        {
          "file_id": "...",
          "title": "...",
          "publish_date": "...",
          "type_full_name": "...",
          "institution_name": "...",
          "company_name": "...",
          "section": "...",
          "data_source": "info_search_finance_db",
          "query": "..."
        }
      ]
    }
  ],
  "data_source_summary": {
    "info_search_finance_db": 30,
    "info_search_stock_db": 10,
    "info_search_user_db": 5,
    "info_search_web": 0
  }
}
```

3. **Save metadata file**:
   - Write to `output/{topic}_{timestamp}/retrieval_metadata.json`
   - Pretty-print JSON with indent=2, ensure_ascii=False
```

**Step 2: Update section 5 save outputs to reference metadata file**

The save outputs section should already reference retrieval_metadata.json from Task 1. Verify it includes:

```markdown
- `retrieval_metadata.json`: Metadata of all files retrieved by MCP tools (see subsection 1.5)
```

**Step 3: Verify changes**

Read: `SKILL.md:270-330`
Expected: Step 5 now includes metadata aggregation logic with clear structure

**Step 4: Commit**

```bash
git add SKILL.md
git commit -m "docs: add metadata aggregation logic to Step 5

- Aggregate retrieved_files arrays from all tasks
- Build master metadata JSON with research session info
- Include data source summary statistics"
```

---

## Task 4: Add Retrieval Metadata to Important Guidelines

**Files:**
- Modify: `SKILL.md:343-369` (Important Guidelines section)

**Step 1: Add guideline for metadata tracking**

Locate the "Important Guidelines" section (around line 343).

After guideline 9 ("Cite sources"), add guideline 10:

```markdown
10. **Track retrieval metadata**: Always save complete file metadata to retrieval_metadata.json:
    - Every MCP tool query result must include file_id, title, publish_date, institution, company
    - Maintain task association (which task retrieved which files)
    - **Include exact data_source (MCP tool name)**: `info_search_finance_db`, `info_search_stock_db`, `info_search_user_db`, or `info_search_web`
    - Include query string used for each retrieval
    - Generate summary statistics (total files per data source)
    - Enables traceability and data lineage tracking
    - **DO NOT use generic values** - always specify exact MCP tool name for data_source field
```

The existing guideline 10 should become guideline 11.

**Step 2: Verify changes**

Read: `SKILL.md:343-380`
Expected: New guideline 10 added, existing guideline renumbered

**Step 3: Commit**

```bash
git add SKILL.md
git commit -m "docs: add metadata tracking to important guidelines

- Guideline 10: Track retrieval metadata for all MCP queries
- Emphasize traceability and data lineage"
```

---

## Task 5: Create output/ Directory and Add .gitignore

**Files:**
- Create: `output/.gitignore`

**Step 1: Create output directory with .gitignore**

Create the output directory and gitignore file:

```bash
mkdir -p output
cat > output/.gitignore << 'EOF'
# Ignore all generated research outputs
*

# But keep this .gitignore file
!.gitignore

# This directory stores generated research reports
# Each research session creates a timestamped subdirectory:
# - {topic}_{YYYYMMDD_HHMMSS}/
#   - report.md
#   - generation_log.md
#   - retrieval_metadata.json
#   - plan.json
EOF
```

**Step 2: Verify directory created**

Run: `ls -la output/`
Expected: Directory exists with .gitignore file

**Step 3: Verify .gitignore content**

Run: `cat output/.gitignore`
Expected: Ignores all files except .gitignore itself, includes documentation comment

**Step 4: Commit**

```bash
git add output/.gitignore
git commit -m "feat: create output directory for research reports

- All generated files will be saved to output/{topic}_{timestamp}/
- .gitignore prevents committing generated reports to git
- Each session gets isolated subdirectory"
```

---

## Task 6: Update README.md with Output Information

**Files:**
- Modify: `README.md` (add Output section)

**Step 1: Read current README.md structure**

Read: `README.md`

**Step 2: Add Output section before or after usage examples**

Add a new "## Output" section:

```markdown
## Output

All generated research reports are saved to the `output/` directory in a timestamped subdirectory:

```
output/
└── {topic}_{YYYYMMDD_HHMMSS}/
    ├── report.md                    # Complete research report
    ├── generation_log.md            # Execution details and task logs
    ├── retrieval_metadata.json      # File tracking metadata
    └── plan.json                    # Execution plan used
```

**Files**:
- **report.md**: Final research report with all analysis sections
- **generation_log.md**: JSON plan, wave execution details, task completion info
- **retrieval_metadata.json**: Complete metadata of all files retrieved by MCP tools during research
- **plan.json**: The JSON execution plan used for this research

**Retrieval Metadata**:

The `retrieval_metadata.json` file tracks all documents retrieved during research:
- File identifiers and titles
- Publication dates and sources
- Institution and company associations
- Which task retrieved which files
- Query strings used
- Data source summary statistics

This enables full traceability of data sources used in the research.
```

**Step 3: Verify README updated**

Read: `README.md`
Expected: New Output section added with clear documentation

**Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add output directory documentation to README

- Explain output/{topic}_{timestamp}/ structure
- Document all generated files (report, log, metadata, plan)
- Describe retrieval metadata tracking feature"
```

---

## Task 7: Create Example Retrieval Metadata File

**Files:**
- Create: `docs/plans/test-cases/example-retrieval-metadata.json`

**Step 1: Create example metadata file**

Create comprehensive example showing the expected metadata structure:

```json
{
  "research_session": {
    "topic": "特斯拉公司深度分析",
    "research_type": "company",
    "timestamp": "20260207_143522",
    "total_tasks": 5,
    "total_files_retrieved": 23
  },
  "tasks": [
    {
      "task_id": 1,
      "description": "公司概况与业务模式",
      "files_retrieved": 6,
      "files": [
        {
          "file_id": "report_12345678",
          "title": "特斯拉2025年度投资价值分析",
          "publish_date": "2025-12-15",
          "type_full_name": "深度研究报告",
          "institution_name": "中金公司",
          "company_name": "特斯拉",
          "section": "公司介绍部分:特斯拉成立于2003年...主要业务包括电动汽车制造、储能系统、太阳能产品...",
          "data_source": "info_search_finance_db",
          "query": "特斯拉公司业务模式和发展历史"
        },
        {
          "file_id": "report_87654321",
          "title": "特斯拉Cybertruck量产进展跟踪",
          "publish_date": "2026-01-08",
          "type_full_name": "行业动态点评",
          "institution_name": "国泰君安",
          "company_name": "特斯拉",
          "section": "Cybertruck于2023年11月开始交付...截至2025年Q4产能已达到月产2万辆...",
          "data_source": "info_search_finance_db",
          "query": "特斯拉最新产品动态和Cybertruck进展"
        }
      ]
    },
    {
      "task_id": 2,
      "description": "财务表现与盈利能力",
      "files_retrieved": 8,
      "files": [
        {
          "file_id": "N/A",
          "title": "特斯拉历史财务数据",
          "publish_date": "2026-02-07",
          "type_full_name": "量化数据查询",
          "institution_name": null,
          "company_name": "特斯拉",
          "section": "FY2023营收: $96.8B, FY2024营收: $105.2B, FY2025营收: $118.5B",
          "data_source": "info_search_stock_db",
          "query": "特斯拉2023-2025年营业收入"
        },
        {
          "file_id": "N/A",
          "title": "特斯拉毛利率数据",
          "publish_date": "2026-02-07",
          "type_full_name": "量化数据查询",
          "institution_name": null,
          "company_name": "特斯拉",
          "section": "FY2023毛利率: 18.2%, FY2024毛利率: 17.8%, FY2025毛利率: 19.3%",
          "data_source": "info_search_stock_db",
          "query": "特斯拉2023-2025年毛利率趋势"
        },
        {
          "file_id": "report_11223344",
          "title": "特斯拉盈利能力深度拆解",
          "publish_date": "2025-11-20",
          "type_full_name": "专题研究",
          "institution_name": "华泰证券",
          "company_name": "特斯拉",
          "section": "特斯拉毛利率改善主要得益于:1)规模效应降低单车成本...2)4680电池产能爬坡...",
          "data_source": "info_search_finance_db",
          "query": "特斯拉盈利能力分析和毛利率驱动因素"
        }
      ]
    },
    {
      "task_id": 3,
      "description": "竞争格局与市场地位",
      "files_retrieved": 5,
      "files": [
        {
          "file_id": "report_55667788",
          "title": "全球电动车市场竞争格局2025",
          "publish_date": "2025-12-28",
          "type_full_name": "行业研究",
          "institution_name": "招商证券",
          "company_name": null,
          "section": "全球电动车销量排名:比亚迪360万辆(份额19.2%),特斯拉180万辆(9.6%),大众130万辆...",
          "data_source": "info_search_finance_db",
          "query": "全球电动车市场份额和竞争格局"
        }
      ]
    },
    {
      "task_id": 4,
      "description": "技术优势与创新能力",
      "files_retrieved": 3,
      "files": []
    },
    {
      "task_id": 5,
      "description": "未来展望与投资建议",
      "files_retrieved": 1,
      "files": []
    }
  ],
  "data_source_summary": {
    "info_search_finance_db": 18,
    "info_search_stock_db": 5,
    "info_search_user_db": 0,
    "info_search_web": 0
  }
}
```

**Step 2: Verify file created**

Run: `cat docs/plans/test-cases/example-retrieval-metadata.json | python -m json.tool`
Expected: Valid JSON with comprehensive example structure

**Step 3: Add README explaining the example**

Create: `docs/plans/test-cases/README-metadata.md`

```markdown
# Retrieval Metadata Example

This directory contains an example of the retrieval metadata JSON structure.

## File: example-retrieval-metadata.json

Shows the complete structure of `retrieval_metadata.json` generated by financial-research skill.

**Key features**:
- Research session metadata (topic, type, timestamp, counts)
- Task-level organization with file arrays
- Full file metadata (file_id, title, publish_date, institution, company, section, data_source, query)
- Data source summary statistics

**Use cases**:
- Understand what metadata is tracked
- Validate metadata extraction logic
- Reference for building downstream data pipelines
- Traceability of research data sources
```

**Step 4: Commit**

```bash
git add docs/plans/test-cases/example-retrieval-metadata.json docs/plans/test-cases/README-metadata.md
git commit -m "docs: add example retrieval metadata structure

- Comprehensive example showing all metadata fields
- Includes multiple tasks with different data sources
- Demonstrates quantitative vs qualitative data tracking
- Added README explaining the example"
```

---

## Verification Checklist

After completing all tasks, verify:

- [ ] SKILL.md documents output directory structure
- [ ] SKILL.md includes retrieval metadata tracking in subagent prompt
- [ ] SKILL.md Step 5 includes metadata aggregation logic
- [ ] SKILL.md Important Guidelines includes metadata tracking
- [ ] output/ directory exists with .gitignore
- [ ] README.md documents output structure and metadata tracking
- [ ] Example metadata file exists and is valid JSON
- [ ] All commits have clear messages
- [ ] No code implementation (documentation-only changes)

---

## Execution Handoff

Plan complete and saved to `docs/plans/2026-02-07-output-and-tracking-features.md`.

**Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Manual execution (yourself)** - These are documentation changes only, you can implement directly by editing SKILL.md, README.md, and creating the output/ directory

**Which approach?**
