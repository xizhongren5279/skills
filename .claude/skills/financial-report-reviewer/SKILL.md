---
name: financial-report-reviewer
description: "Professional financial report analysis and commentary generation. Use this skill when analyzing quarterly/annual financial reports from listed companies in PDF format, generating financial commentary by mimicking the style and structure of previous analyst reports, extracting key financial metrics and business insights from earnings reports, or creating structured markdown analysis comparing current quarter performance with historical commentary patterns."
---

# Financial Report Reviewer

## Overview

This skill helps generate professional financial report commentary by learning from and mimicking existing analyst reports. It analyzes historical commentary to understand writing patterns, terminology, and structural preferences, then applies that style to create new commentary for the latest quarter's financial report.

## Core Workflow

### Step 1: Analyze Historical Commentary Style

Read and analyze the previous quarter's commentary to understand:

**Style Elements:**
- Tone and voice (analytical, cautious, optimistic, etc.)
- Sentence structure and paragraph organization
- Use of financial terminology and industry jargon
- Emphasis patterns (what gets highlighted, what gets minimized)

**Structural Patterns:**
- Opening format (summary statement, key highlights, etc.)
- Content flow (metrics first, business analysis second, or vice versa)
- How financial data is presented and contextualized
- Closing format (outlook, risks, recommendations, etc.)

**Key Themes to Identify:**
- Metrics the analyst consistently tracks
- Business segments highlighted
- Competitive positioning references
- Management commentary integration

### Step 2: Extract Current Quarter Data

Use the PDF extraction script to pull key information from the new financial report:

```bash
scripts/extract_pdf_report.py <path-to-report.pdf>
```

**Key Data to Extract:**
- Revenue and profit metrics (YoY, QoQ growth)
- Segment-level performance
- Guidance and outlook statements
- Management discussion highlights
- Notable one-time items or exceptional items
- Balance sheet and cash flow highlights

### Step 3: Generate Matched Commentary

Apply the learned style to create new commentary following the historical patterns:

**Structure Matching:**
- Mirror the opening/hook style from historical commentary
- Use similar paragraph transitions
- Match the level of detail in each section
- Apply consistent emphasis and framing

**Content Generation:**
- Present current quarter data using historical terminology
- Highlight comparable metrics
- Draw similar types of insights and observations
- Maintain consistent forward-looking vs. retrospective balance

### Step 4: Quality Review

Before finalizing, verify:

- **Style consistency**: Does it sound like the same analyst?
- **Data accuracy**: Are all metrics correctly stated?
- **Logical flow**: Do insights follow naturally from the data?
- **Completeness**: Are all key topics covered?

## Output Format

The skill generates structured Markdown output:

```markdown
# [Company Name] Q[Quarter] [Year] Earnings Review

## Summary
[Brief overview following historical style]

## Financial Performance
- Revenue: [amount] ([growth]% YoY / [growth]% QoQ)
- Net Income: [amount] ([growth]% YoY / [growth]% QoQ)
- [Other key metrics...]

## Business Analysis
[Segment performance, operational highlights...]

## Outlook
[Guidance, future expectations...]

## Key Takeaways
- [Point 1]
- [Point 2]
```

## Reference Materials

For detailed guidance on specific aspects, see:

- **Financial metrics reference**: See `references/metrics.md` for standard financial definitions and calculation methods
- **Common terminology**: See `references/terminology.md` for industry-standard phrasing and concepts
- **Analysis templates**: See `references/templates.md` for commentary structure examples

## Scripts

### extract_pdf_report.py

Extracts text and tables from financial report PDFs.

**Usage:**
```bash
scripts/extract_pdf_report.py <pdf-file-path>
```

**Requirements:**
- PyPDF2 or pdfplumber
- tabula-py for table extraction

Install dependencies:
```bash
pip install pdfplumber tabula-py
```

## Best Practices

1. **Always start with historical analysis** - Understanding the existing style is critical for consistency
2. **Extract structured data first** - Don't try to parse PDF on the fly; extract and organize data systematically
3. **Iterate on style matching** - Generate first pass, then refine to better match historical patterns
4. **Maintain objectivity** - Financial commentary should remain factual and balanced regardless of style
5. **Contextualize numbers** - Never present raw metrics without explanation or comparison
