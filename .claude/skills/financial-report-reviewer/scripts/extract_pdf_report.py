#!/usr/bin/env python3
"""
Extract text and tables from financial report PDFs.

This script parses PDF financial reports and extracts:
- Text content organized by page
- Tables containing financial data
- Key metrics with contextual information

Usage:
    python extract_pdf_report.py <pdf-file-path>
"""

import sys
import json
import re
from pathlib import Path

def extract_with_pdfplumber(pdf_path):
    """Extract text and tables using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        print("Error: pdfplumber not installed. Install with: pip install pdfplumber")
        sys.exit(1)

    results = {
        "file": str(pdf_path),
        "pages": [],
        "tables": [],
        "key_sections": {}
    }

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                results["pages"].append({
                    "page_number": i,
                    "text": page_text
                })

            # Extract tables
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    results["tables"].append({
                        "page": i,
                        "headers": table[0] if table else [],
                        "rows": table[1:] if len(table) > 1 else []
                    })

    # Identify key sections
    full_text = " ".join([p["text"] for p in results["pages"]])
    results["key_sections"] = identify_key_sections(full_text)

    return results


def identify_key_sections(text):
    """Identify key financial sections in the report."""
    sections = {}

    # Common section headers in financial reports
    section_patterns = {
        "financial_highlights": r"(?:Financial Highlights|Key Financial Data|Executive Summary)",
        "revenue": r"(?:Revenue|Sales|Operating Income|Top Line)",
        "profit": r"(?:Net Income|Net Profit|Earnings|Bottom Line)",
        "guidance": r"(?:Guidance|Outlook|Future Outlook|Forward Looking)",
        "risk_factors": r"(?:Risk Factors|Risks and Uncertainties)",
        "management_discussion": r"(?:Management's Discussion|MD&A|Business Overview)"
    }

    text_lower = text.lower()

    for section_key, pattern in section_patterns.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        if matches:
            # Extract text around the match (context window)
            contexts = []
            for match in matches:
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 500)
                contexts.append(text[start:end].strip())
            sections[section_key] = contexts

    return sections


def extract_key_metrics(text):
    """Extract key financial metrics from text."""
    metrics = {}

    # Revenue patterns
    revenue_patterns = [
        r"(?:revenue|total revenue|net revenue|sales)[\s,]+of[\s,]+[$¥€]?[\d,]+(?:\.\d+)?[\s]*(?:million|billion|thousand)?",
        r"[$¥€]?[\d,]+(?:\.\d+)?[\s]*(?:million|billion)?[\s]+(?:in revenue|sales)"
    ]

    # Growth patterns
    growth_patterns = [
        r"(?:increased|decreased|grew|declined)[\s]+by[\s]+[\d.]+%",
        r"[\d.]+%[\s]*(?:year-over-year|YoY|quarter-over-quarter|QoQ)"
    ]

    for pattern in revenue_patterns + growth_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            metric_type = "revenue" if "revenue" in pattern.lower() or "sales" in pattern.lower() else "growth"
            if metric_type not in metrics:
                metrics[metric_type] = []
            metrics[metric_type].extend(matches)

    return metrics


def format_output(results):
    """Format extracted data for display."""
    output = []

    output.append(f"# Extracted from: {results['file']}")
    output.append(f"Total pages with text: {len(results['pages'])}")
    output.append(f"Total tables found: {len(results['tables'])}")
    output.append("")

    # Key sections
    if results["key_sections"]:
        output.append("## Key Sections Identified")
        for section_name, contexts in results["key_sections"].items():
            output.append(f"\n### {section_name.replace('_', ' ').title()}")
            for ctx in contexts[:3]:  # Limit to first 3 matches
                output.append(f"- {ctx[:200]}...")

    # Sample tables
    if results["tables"]:
        output.append("\n## Sample Tables")
        for i, table in enumerate(results["tables"][:3], 1):
            output.append(f"\n### Table {i} (Page {table['page']})")
            if table["headers"]:
                output.append("Headers: " + " | ".join(str(h) for h in table["headers"]))
            if table["rows"]:
                output.append(f"Rows: {len(table['rows'])} data rows")

    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_report.py <pdf-file-path>")
        print("\nThis script extracts text and tables from financial report PDFs.")
        sys.exit(1)

    pdf_path = Path(sys.argv[1])

    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    if not pdf_path.suffix.lower() == ".pdf":
        print(f"Error: Not a PDF file: {pdf_path}")
        sys.exit(1)

    print(f"Extracting data from: {pdf_path}")
    print("=" * 60)

    results = extract_with_pdfplumber(pdf_path)

    # Print formatted output
    print(format_output(results))

    # Optionally save JSON
    json_path = pdf_path.with_suffix(".json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nFull results saved to: {json_path}")


if __name__ == "__main__":
    main()
