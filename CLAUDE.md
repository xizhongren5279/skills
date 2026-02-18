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

### Skill Categories

Skills live in `skills/` and fall into five groups: document processing (`xlsx`, `docx`, `pptx`, `pdf`), financial (`financial-research`, `company-one-page`, `company-due-diligence`, `financial-report-reviewer`), development workflow superpowers (`brainstorming`, `writing-plans`, `systematic-debugging`, etc.), developer tools (`skill-creator`, `mcp-builder`, `webapp-testing`, `web-artifacts-builder`), and creative/visual (`algorithmic-art`, `canvas-design`, `slack-gif-creator`, etc.). Run `ls skills/` for the full list.

**Marketplace bundles** (`.claude-plugin/marketplace.json`) only include `document-skills` and `example-skills`. Financial skills and superpowers are standalone — they are NOT in any marketplace bundle.

## Common Development Commands

### Creating a New Skill

```bash
# Initialize a new skill from template
python3 skills/skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>

# Example: Create a new public skill
python3 skills/skill-creator/scripts/init_skill.py my-new-skill --path skills/
```

The init script creates SKILL.md with proper YAML frontmatter and TODO placeholders, plus example `scripts/`, `references/`, and `assets/` directories.

### Packaging/Validating Skills

```bash
# Validate skill structure only
python3 skills/skill-creator/scripts/quick_validate.py <path/to/skill-folder>

# Package into distributable .skill file (ZIP archive, validates automatically)
python3 skills/skill-creator/scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

Validation checks: YAML frontmatter format/fields, naming conventions, description completeness, file organization.

### Running Scripts

Most scripts are standalone:
```bash
python3 skills/<skill-name>/scripts/<script>.py [args]
node skills/<skill-name>/scripts/<script>.js [args]
```

### MCP Tools (financial-research)

The financial-research skill uses MCP tools invoked through the skill workflow, not directly:
- `info_search_finance_db` - Research reports, news, announcements
- `info_search_stock_db` - Quantitative financial data
- `info_search_user_db` - User-uploaded documents
- `info_search_web` - Web search fallback

## Development Infrastructure

- **No test framework**: No pytest config, no test directories, no CI/CD pipelines
- **No linting/formatting**: No ESLint, Prettier, flake8, or similar configured
- **No root package.json**: The root `node_modules/` was installed manually and contains `pptxgenjs`, `playwright`, `sharp`, `jszip`, `image-size`
- **Multi-IDE support**: `.agents/`, `.cursor/`, `.codebuddy/`, `.qoder/`, `.trae/`, `.windsurf/` directories contain skill symlinks for various AI coding tools

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

Financial skills, superpowers, and `remotion-best-practices` are NOT bundled — they exist as standalone skills outside marketplace config.

## Dependencies

No repository-wide requirements.txt or package.json — dependencies are skill-specific.

**Python** (varies by skill): `pandas`, `openpyxl`, `aiohttp`, `langchain-core`, `langgraph`, `loguru`, `pillow`, `imageio`, `numpy`

**Node.js** (root `node_modules/`, no package.json): `pptxgenjs`, `playwright`, `sharp`, `jszip`, `image-size`

## Key Resources

- `skills/writing-skills/references/anthropic-best-practices.md` (45KB) - Comprehensive skill authoring best practices
- `skills/writing-skills/references/testing-skills-with-subagents.md` - Testing methodology for skills
- `skills/financial-research/references/plan_for_question_type.xlsx` - 26 research type templates (the database driving question type matching)
