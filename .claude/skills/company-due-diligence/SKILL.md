---
name: company-due-diligence
description: "Comprehensive due diligence analysis for private (non-listed) companies, focusing on investment decision-making for VC/PE scenarios. Use this skill when conducting systematic evaluation of target companies across financial, business, legal, and team dimensions. Retrieves structured company data via financial database API, applies multi-dimensional analysis frameworks, generates professional due diligence reports in Markdown format, and provides investment recommendations. Supports scenarios including pre-investment evaluation, M&A analysis, partnership assessment, and supplier/customer review."
---

# Company Due Diligence

## Overview

This skill enables comprehensive due diligence analysis of private (non-listed) companies for investment decision-making. It provides a systematic framework to evaluate companies across four key dimensions: financial health, business competitiveness, legal compliance, and team capability. The skill retrieves structured data from a financial database API, applies rigorous evaluation frameworks, and generates professional due diligence reports.

## Core Workflow

Due diligence follows a **standardized five-step process**:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Due Diligence Workflow                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Data Retrieval via info_search_finance_db Tool                  │
│     └─ All data queries go through this tool                        │
│     └─ Results automatically saved to JSON array                    │
│                                                                     │
│  2. Store Data to JSON File                                         │
│     └─ Array format: [query1_results, query2_results, ...]          │
│     └─ File: {company_name}_due_diligence_data.json                 │
│                                                                     │
│  3. Multi-Dimensional Analysis                                      │
│     └─ Financial, Business, Legal, Team                             │
│                                                                     │
│  4. Generate Markdown Report                                        │
│     └─ Structure following report_template.md                       │
│     └─ File: {company_name}_due_diligence_report.md                 │
│                                                                     │
│  5. Generate Canvas Visualization                                   │
│     └─ Use json-canvas skill to create .canvas file                 │
│     └─ File: {company_name}_due_diligence.canvas                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Step 1: Data Retrieval via info_search_finance_db

**CRITICAL RULE**: All data retrieval must go through the `info_search_finance_db` tool from `scripts/search_finance_db.py`.

**Tool Function**: `info_search_finance_db(query, date_range, recall_num, doc_type, state)`

**Parameters**:
- `query` (str): Natural language query with clear semantics and specific time information
- `date_range` (Optional): `"all"`, `"past_day"`, `"past_week"`, `"past_month"`, `"past_quarter"`, `"past_half_year"`, `"past_year"`
- `recall_num` (Optional): Number of search results (default: 20)
- `doc_type` (Optional): `"all"`, `"report"`, `"summary"`, `"company_all_announcement"`, `"comments"`, `"news"` (can be a list)
- `state` (dict): LangGraph state containing `info_search_files`, `fs`, `custom_filter`, `es_filter`

**Usage Examples**:

```python
# Financial data query
await info_search_finance_db(
    query="宁德时代 2024年 财务数据 营收 净利润 现金流",
    date_range="past_year",
    doc_type=["report", "company_all_announcement"],
    recall_num=20,
    state=state
)

# Business operations query
await info_search_finance_db(
    query="宁德时代 主要客户 供应商 市场份额 2024",
    date_range="past_year",
    doc_type=["report", "summary"],
    recall_num=15,
    state=state
)

# Legal compliance query
await info_search_finance_db(
    query="宁德时代 诉讼 纠纷 行政处罚 知识产权",
    date_range="all",
    doc_type=["all"],
    recall_num=20,
    state=state
)

# Team and management query
await info_search_finance_db(
    query="宁德时代 管理团队 董事长 高管 股东结构",
    date_range="past_half_year",
    doc_type=["report", "company_all_announcement"],
    recall_num=15,
    state=state
)
```

**Important Guidelines**:
- **Single company per query**: Never include multiple companies in one query
- **Specific time information**: Always include year/time in query when needed
- **Doc type selection**: Prefer combinations like `["report", "summary"]` or `["report", "company_all_announcement"]`. Use `"all"` only when unsure
- **Default date_range**: Use `"past_half_year"` for recent financial data

**Data Retrieved**:
- **Financial data**: Income statements, balance sheets, cash flow statements, financial ratios
- **Company information**: Registration details, legal structure, shareholders, management team
- **Legal compliance**: Litigation records, penalties, licenses, IP, tax status
- **Business operations**: Customers, suppliers, products, market position, operational metrics

**Automatic Storage**: The tool automatically saves results to `state["fs"]["/finance_db_summary/{query}.json"]`

### Step 2: Store Data to JSON File

**Purpose**: Consolidate all query results into a single JSON file for analysis and reference.

**JSON Structure**:
```json
{
  "company_name": "宁德时代",
  "query_date": "2025-01-20",
  "data": [
    {
      "category": "financial",
      "query": "宁德时代 2024年 财务数据 营收 净利润 现金流",
      "results": [...],
      "timestamp": "2025-01-20T10:00:00"
    },
    {
      "category": "business",
      "query": "宁德时代 主要客户 供应商 市场份额 2024",
      "results": [...],
      "timestamp": "2025-01-20T10:05:00"
    },
    {
      "category": "legal",
      "query": "宁德时代 诉讼 纠纷 行政处罚 知识产权",
      "results": [...],
      "timestamp": "2025-01-20T10:10:00"
    },
    {
      "category": "team",
      "query": "宁德时代 管理团队 董事长 高管 股东结构",
      "results": [...],
      "timestamp": "2025-01-20T10:15:00"
    }
  ]
}
```

**Storage Process**:
1. Execute all queries via `info_search_finance_db`
2. Collect results from `state["fs"]`
3. Consolidate into structured JSON array
4. Save to `{company_name}_due_diligence_data.json`

### Step 3: Multi-Dimensional Analysis (Reference framework.md)

Analyze the collected data across four dimensions using the framework in `references/framework.md`:

#### 3.1 Financial Analysis
- Revenue, profitability, cash flow, balance sheet health
- Financial ratios and trends
- Risk assessment

#### 3.2 Business Analysis
- Business model and competitive positioning
- Market and industry analysis
- Product and technology assessment
- Customer and sales analysis

#### 3.3 Legal & Compliance Review
- Corporate structure and registration
- Licenses, permits, litigation
- IP and material contracts

#### 3.4 Team & Management
- Management team background
- Shareholder structure
- Organization and talent retention

### Step 4: Generate Markdown Report

**Output File**: `{company_name}_due_diligence_report.md`

**Report Structure** (follow `assets/report_template.md`):
```markdown
# [Company Name] Due Diligence Report

## Executive Summary
- Company overview
- Key findings
- Investment recommendation

## Financial Analysis
[Detailed financial analysis with data references]

## Business Analysis
[Detailed business analysis with data references]

## Legal Compliance
[Detailed legal review with data references]

## Team Background
[Detailed team analysis with data references]

## Risk Assessment
[Risk matrix and mitigation strategies]

## Valuation & Investment Recommendation
[Valuation methodology and recommendation]
```

**Data References**: Cite sources using `[docN]` format where N corresponds to file IDs in the JSON data.

### Step 5: Generate Canvas Visualization

**Purpose**: Create visual overview of key findings using the json-canvas skill.

**Output File**: `{company_name}_due_diligence.canvas`

**Canvas Structure**:
```
┌────────────────────────────────────────────────────────────┐
│  Group: [Company Name] Due Diligence                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Financial │  │ Business │  │  Legal   │  │   Team   │  │
│  │ Analysis │  │ Analysis │  │ Review   │  │ Review   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────────────────────────────────────────────────┐ │
│  │              Risk Assessment & Summary                │ │
│  └──────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────┘
```

**Creation Steps**:
1. Load json-canvas skill
2. Create nodes for each analysis dimension
3. Add edges showing relationships
4. Export as .canvas file

**Configuration**:
- Environment variables: `DR_SEARCH_API_KEY`, `DR_SEARCH_BASE_URL_SEARCH`
- See `scripts/search_finance_db.py` for API endpoints

---

## Analysis Framework Reference

For detailed analysis methods in each dimension, refer to `references/framework.md`:

- **Financial Analysis**: Revenue, profitability, cash flow, balance sheet, ratios
- **Business Analysis**: Business model, market, product, customer analysis
- **Legal Compliance**: Corporate structure, licenses, litigation, IP
- **Team Background**: Management team, shareholders, organization
- **Risk Assessment**: Checklist and rating methodology
- **Data Verification**: Cross-validation methods

## Report Output Format

The skill generates Markdown format reports following this structure:

```markdown
# [Company Name] Due Diligence Report

## Executive Summary
- Basic company information
- Key strengths and risks
- Overall assessment scores (1-5 rating across four dimensions)
- Investment recommendation and valuation range

## Financial Analysis
- 3-year financial summary tables
- Revenue, profitability, cash flow, balance sheet analysis
- Financial ratio analysis
- Financial risk assessment

## Business Analysis
- Business model evaluation
- Market and competitive landscape
- Product and technology assessment
- Customer and sales analysis
- Business risk assessment

## Legal Compliance
- Corporate structure and registration
- Licenses and permits
- Litigation and disputes
- Intellectual property
- Material contracts
- Labor compliance

## Team Background
- Core management profiles
- Shareholder background
- Organization structure
- Team risk assessment

## Comprehensive Risk Assessment
- Risk summary table (category, description, severity, impact, mitigation)
- Risk matrix visualization

## Valuation & Investment Recommendation
- Valuation methodologies and results
- Investment recommendation with rationale
- Pre-investment conditions (if applicable)
- Post-investment management suggestions

## Appendices
- Due diligence methodology
- Reference document list
- Disclaimers
```

## Resources

### scripts/search_finance_db.py

**Primary data retrieval tool** for querying company information from financial database API.

**Supported data types**:
- Financial data (statements, ratios, metrics)
- Company information (registration, shareholders, management)
- Legal compliance (litigation, penalties, licenses, IP)
- Business operations (customers, suppliers, products, metrics)

**Key features**:
- Company search by name
- Comprehensive data retrieval across all dimensions
- Targeted queries for specific data types
- Structured JSON output for programmatic analysis
- Human-readable summary format

**Usage examples**:
```bash
# Search for companies
scripts/search_finance_db.py --search "公司名称"

# Get comprehensive report
scripts/search_finance_db.py --company-id "12345" --type comprehensive --year 2023

# Get specific data type
scripts/search_finance_db.py --company "公司名称" --type financial --year 2023

# Save output to file
scripts/search_finance_db.py --company-id "12345" --type comprehensive --output-file report.json
```

**Configuration**: Set `FINANCE_DB_API_URL` and `FINANCE_DB_API_KEY` environment variables, or pass via `--api-url` and `--api-key` arguments.

**When to use**: This is the primary tool for all due diligence data gathering. Use it at the start of every analysis to retrieve company data.

### scripts/extract_financial_data.py

**Fallback tool** for extracting financial metrics from local company documents when API data is unavailable.

**Supported formats**: PDF, Excel (.xlsx, .xls), CSV

**Usage**:
```bash
scripts/extract_financial_data.py <file-path> [--output json|csv]
```

**Output**: Structured JSON with financial metrics template including:
- Income statement items (revenue, gross profit, operating profit, net profit)
- Balance sheet items (assets, liabilities, equity)
- Cash flow items (operating, investing, financing cash flows)
- Key ratios (ROA, ROE, current ratio, debt-to-equity)

**When to use**: Only use this tool when:
1. The target company is not available in the financial database API
2. You need to supplement API data with proprietary documents
3. Analyzing historical documents not yet in the database

**Note**: The script provides a structured template even when automated extraction fails, guiding manual data entry.

### references/framework.md

Comprehensive due diligence framework document covering:
- Detailed financial analysis indicators and methodologies
- Business analysis dimensions and evaluation criteria
- Legal compliance review checklist
- Team background assessment framework
- Risk assessment checklist across all dimensions
- Data verification methods and cross-checking procedures

**When to read**: Reference this document when conducting deep analysis in any specific dimension or when uncertain about evaluation criteria.

### assets/report_template.md

Professional due diligence report template with complete structure and placeholder guidance.

**When to use**: Copy this template as the starting point for generating the final due diligence report. Fill in analysis findings systematically following the template structure.

## Best Practices

1. **Systematic Approach**: Follow the four-phase workflow systematically to ensure comprehensive coverage

2. **Data-Driven Analysis**: Base conclusions on verified data and documented evidence, not assumptions

3. **Cross-Validation**: Verify critical information across multiple data dimensions from the API. For high-stakes decisions, supplement API data with direct document review or management interviews

4. **Risk-Focused**: Actively search for red flags and potential issues, not just confirming positives

5. **Industry Context**: Compare metrics against industry benchmarks and peers

6. **Materiality Focus**: Prioritize analysis of material risks and key value drivers

7. **Professional Skepticism**: Question anomalies, inconsistencies, and overly optimistic claims. Pay attention to data quality indicators in API responses

8. **Document Sources**: Note data sources and timestamps for key findings to support conclusions. API responses include source metadata

9. **Clear Communication**: Present findings clearly with specific evidence, avoiding vague statements

10. **Actionable Recommendations**: Provide specific, implementable recommendations for risk mitigation

11. **API Data Quality**: Always review the data quality metadata included in API responses. Note any gaps, outdated information, or low-confidence fields that require additional verification
