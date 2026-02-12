# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **skills repository** for Claude Code - a collection of modular, self-contained "skills" that extend Claude's capabilities with specialized knowledge, workflows, and tools. Each skill is essentially an onboarding guide that transforms Claude from a general-purpose agent into a specialized agent.

### Core Architecture

**Skill Structure (progressive disclosure design):**
```
skill-name/
├── SKILL.md              # Required: YAML frontmatter (name + description) + markdown body
├── scripts/              # Optional: Executable code (Python/Bash) for deterministic operations
├── references/           # Optional: Documentation loaded as-needed into context
└── assets/               # Optional: Files used in output (templates, fonts, images)
```

**Context Loading Strategy:**
1. Metadata (name + description) - Always loaded (~100 words)
2. SKILL.md body - Loaded when skill triggers (<5k words recommended)
3. Bundled resources - Loaded as needed (unlimited, scripts can execute without reading)

This three-level system minimizes context bloat while providing deep capabilities when needed.

### Key Categories

**Document Processing Skills:**
- `docx/` - Word document creation, editing, tracked changes, redlining
- `pptx/` - PowerPoint slide manipulation, rearrangement, thumbnails
- `pdf/` - PDF form filling, text extraction, bounding box validation
- `xlsx/` - Excel spreadsheet recalculation

**Financial Skills:**
- `financial-research/` - Deep-dive company/industry/macro/strategy/quantitative research
- `company-one-page/` - Standardized one-page company summaries
- `company-due-diligence/` - Due diligence research workflow
- `financial-report-reviewer/` - PDF report analysis and extraction

**Development Workflow Skills** (superpowers):
- `brainstorming/` - Pre-creative work exploration
- `dispatching-parallel-agents/` - 2+ independent tasks without shared state
- `executing-plans/` - Written implementation plans with review checkpoints
- `finishing-a-development-branch/` - Post-implementation decisions (merge/PR/cleanup)
- `receiving-code-review/` - Technical review of feedback before implementation
- `requesting-code-review/` - Verification before merging
- `subagent-driven-development/` - Implementation plans with independent tasks
- `systematic-debugging/` - Bug investigation before proposing fixes
- `test-driven-development/` - Test-first implementation
- `using-git-worktrees/` - Isolated feature work
- `using-superpowers/` - Finding and using skills
- `verification-before-completion/` - Evidence before assertions
- `writing-plans/` - Multi-step task planning before code
- `writing-skills/` - Creating/editing/verifying skills

**Developer Tools:**
- `skill-creator/` - Meta-skill for creating new skills
- `mcp-builder/` - MCP server construction
- `webapp-testing/` - Playwright-based testing
- `web-artifacts-builder/` - HTML/React artifact generation

**Creative/Visual:**
- `algorithmic-art/` - Generative artwork
- `brand-guidelines/` - Brand asset management
- `canvas-design/` - Canvas-based visuals
- `slack-gif-creator/` - Animated GIF generation
- `theme-factory/` - Theme styling

## Common Development Commands

### Creating a New Skill

```bash
# Initialize a new skill from template
python3 skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>

# Example: Create a new public skill
python3 skills/skill-creator/scripts/init_skill.py my-new-skill --path skills/
```

The init script creates:
- SKILL.md with proper YAML frontmatter and TODO placeholders
- Example `scripts/`, `references/`, and `assets/` directories with sample files

### Packaging/Validating Skills

```bash
# Package a skill into distributable .skill file (validates automatically)
python3 skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [output-directory]

# Example
python3 skills/skill-creator/scripts/package_skill.py skills/my-skill ./dist
```

Packaging automatically validates:
- YAML frontmatter format and required fields
- Skill naming conventions and directory structure
- Description completeness
- File organization

### Running Python Scripts

Most scripts are standalone and can be run directly:
```bash
python3 skills/<skill-name>/scripts/<script>.py [args]
```

### Testing MCP Tools

The financial-research skill integrates MCP tools for data retrieval:
- `info_search_finance_db` - Research reports, news, announcements
- `info_search_stock_db` - Quantitative financial data
- `info_search_user_db` - User-uploaded documents
- `info_search_web` - Web search fallback

These are invoked through the skill workflow, not directly.

## Architecture Patterns

### Question Type Matching (financial-research)

The financial-research skill uses a sophisticated LLM-based classification system:

1. **Step 1.0 (MANDATORY FIRST STEP)**: Match user query to 26 predefined research types
   - Reads `references/plan_for_question_type.xlsx` via `utils/question_type_parser.py`
   - Uses semantic LLM matching (NOT keyword matching)
   - Returns confidence score and prescriptive workflow template

2. **Workflow is PRESCRIPTIVE, not suggestive**
   - Tasks are derived from matched workflow template
   - Task order follows template order
   - Only `hints` are customizable (entities, time periods, focus)

3. **Multi-Turn Optimization**
   - Check last 3 turns for existing data before querying
   - Extraction/Clarification → Answer directly (no skill invocation)
   - Extension/Comparison/New Research → Invoke skill with smart planning

### Time Context Inference

Financial research requires explicit time handling with disclosure lag awareness:

```python
from datetime import datetime
current_date = datetime.now().strftime("%Y-%m-%d")
current_year = datetime.now().year
current_month = datetime.now().month
current_quarter = (current_month - 1) // 3 + 1

# CRITICAL: Consider disclosure lag (quarterly reports disclosed 1-2 months after quarter end)
# "最新季报" means latest DISCLOSED quarter, not current calendar quarter
# Example: Feb 2026 (Q1) → Q4 2025 may not be disclosed yet → use Q3 2025
```

### Parallel Execution (MANDATORY)

Financial-research skill enforces parallel execution:
- Use Task tool with `subagent_type="general-purpose"`
- Spawn ALL independent tasks in ONE message
- Do NOT execute sequentially when tasks can run in parallel
- Parallel execution = ~50% time savings vs sequential

## File Conventions

### SKILL.md Frontmatter (REQUIRED)

```yaml
---
name: skill-name
description: Complete description of what the skill does and WHEN to use it. Include specific triggers.
---
```

**Critical:** The `description` field is the PRIMARY triggering mechanism. Include:
- What the skill does
- Specific scenarios/tasks that trigger it
- File types or domains it handles

### Progressive Disclosure

Keep SKILL.md under 500 lines. Split detailed content into reference files:

```markdown
# SKILL.md (overview)

## Advanced Features
- **Feature X**: See [FEATURE_X.md](references/FEATURE_X.md) for complete guide
- **Feature Y**: See [FEATURE_Y.md](references/FEATURE_Y.md)
```

### No Extra Documentation

Do NOT create in skills:
- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md

The skill should only contain files needed for an AI agent to do the job.

## Important Implementation Details

### utils/question_type_parser.py

This utility handles the Excel-based question type database:

```python
from utils.question_type_parser import QuestionTypeParser

parser = QuestionTypeParser('references/plan_for_question_type.xlsx')
types = parser.load_question_types()  # Returns list of 26 type dicts

# For LLM semantic matching
workflow_result = parser.get_workflow_for_query(user_query, use_llm=True)
# Returns: {'_matching_prompt': <prompt>, '_needs_llm_execution': True}

# After LLM executes prompt, extract workflow
matched_type = types[matched_index - 1]
workflow_data = parser.extract_workflow(matched_type)
# Returns: {'reference_rules': [...], 'reference_workflow': [...]}
```

### Financial Research Output Structure

Every research session creates a timestamped output directory:

```
output/{topic}_{timestamp}/
├── report.md                    # Final research report
├── plan.json                    # Research plan with tasks
├── retrieval_metadata.json      # Data lineage (file_id, sources, queries)
└── generation_log.md            # Execution log
```

All 4 files are REQUIRED for complete execution.

## Development Philosophy

1. **Concise is Key** - Challenge each token: "Does Claude really need this?"
2. **Set Appropriate Degrees of Freedom** - Match specificity to task variability
3. **Progressive Disclosure** - Load detail only when needed
4. **No Duplication** - Information lives in SKILL.md OR references, not both
5. **Scripts Over Rewrite** - If code is rewritten repeatedly, make it a script

## Plugin Marketplace

The `.claude-plugin/marketplace.json` configures skill collections:
- `document-skills` - xlsx, docx, pptx, pdf
- `example-skills` - algorithmic-art, brand-guidelines, canvas-design, etc.

## Dependencies

Python scripts typically require:
- `pandas` - Excel processing (question type parser)
- `aiohttp` - Async HTTP (company-due-diligence)
- `langchain-core`, `langgraph` - LangChain integration
- `loguru` - Logging
- `openpyxl` - Excel file reading (implicit via pandas)

No repository-wide requirements.txt - dependencies are skill-specific.
