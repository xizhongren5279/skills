#!/usr/bin/env python3
"""
Financial Data Extraction Tool for Due Diligence

Extracts key financial metrics from company financial documents (PDF, Excel, etc.)
to support due diligence analysis.

Usage:
    extract_financial_data.py <file-path> [--output json|csv]

Examples:
    extract_financial_data.py financial_report.pdf
    extract_financial_data.py financials.xlsx --output json
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class FinancialDataExtractor:
    """Extract and structure financial data from various file formats."""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_type = self.file_path.suffix.lower()

    def extract(self) -> Dict[str, Any]:
        """Extract financial data based on file type."""
        if self.file_type == '.pdf':
            return self._extract_from_pdf()
        elif self.file_type in ['.xlsx', '.xls']:
            return self._extract_from_excel()
        elif self.file_type == '.csv':
            return self._extract_from_csv()
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def _extract_from_pdf(self) -> Dict[str, Any]:
        """Extract financial data from PDF documents."""
        try:
            import pdfplumber
        except ImportError:
            return {
                "error": "pdfplumber not installed. Run: pip install pdfplumber",
                "file": str(self.file_path),
                "suggested_manual_extraction": self._get_extraction_template()
            }

        data = self._get_extraction_template()

        try:
            with pdfplumber.open(self.file_path) as pdf:
                full_text = ""
                tables = []

                for page in pdf.pages:
                    # Extract text
                    full_text += page.extract_text() or ""

                    # Extract tables
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)

                data["source_file"] = str(self.file_path)
                data["extracted_text_preview"] = full_text[:500]
                data["tables_found"] = len(tables)
                data["raw_tables"] = tables[:3]  # First 3 tables

        except Exception as e:
            data["extraction_error"] = str(e)

        return data

    def _extract_from_excel(self) -> Dict[str, Any]:
        """Extract financial data from Excel files."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "pandas not installed. Run: pip install pandas openpyxl",
                "file": str(self.file_path),
                "suggested_manual_extraction": self._get_extraction_template()
            }

        data = self._get_extraction_template()

        try:
            # Read all sheets
            excel_file = pd.ExcelFile(self.file_path)
            data["source_file"] = str(self.file_path)
            data["sheets"] = excel_file.sheet_names

            # Store sheet data
            sheets_data = {}
            for sheet_name in excel_file.sheet_names[:5]:  # First 5 sheets
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                sheets_data[sheet_name] = {
                    "rows": len(df),
                    "columns": list(df.columns),
                    "preview": df.head(10).to_dict('records')
                }

            data["sheets_data"] = sheets_data

        except Exception as e:
            data["extraction_error"] = str(e)

        return data

    def _extract_from_csv(self) -> Dict[str, Any]:
        """Extract financial data from CSV files."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "pandas not installed. Run: pip install pandas",
                "file": str(self.file_path),
                "suggested_manual_extraction": self._get_extraction_template()
            }

        data = self._get_extraction_template()

        try:
            df = pd.read_csv(self.file_path)
            data["source_file"] = str(self.file_path)
            data["rows"] = len(df)
            data["columns"] = list(df.columns)
            data["preview"] = df.head(10).to_dict('records')

        except Exception as e:
            data["extraction_error"] = str(e)

        return data

    def _get_extraction_template(self) -> Dict[str, Any]:
        """Return template structure for financial data."""
        return {
            "company_name": None,
            "report_period": None,
            "currency": "CNY",

            # Income Statement
            "revenue": {
                "current_period": None,
                "prior_period": None,
                "yoy_growth": None
            },
            "gross_profit": {
                "current_period": None,
                "prior_period": None,
                "margin": None
            },
            "operating_profit": {
                "current_period": None,
                "prior_period": None,
                "margin": None
            },
            "net_profit": {
                "current_period": None,
                "prior_period": None,
                "margin": None
            },

            # Balance Sheet
            "total_assets": None,
            "total_liabilities": None,
            "shareholders_equity": None,
            "debt_to_equity_ratio": None,

            # Cash Flow
            "operating_cash_flow": None,
            "investing_cash_flow": None,
            "financing_cash_flow": None,
            "free_cash_flow": None,

            # Key Metrics
            "roa": None,  # Return on Assets
            "roe": None,  # Return on Equity
            "current_ratio": None,
            "quick_ratio": None,

            # Notes
            "data_quality": "raw_extraction",
            "manual_review_required": True
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_financial_data.py <file-path> [--output json|csv]")
        print("\nSupported formats: PDF, Excel (.xlsx, .xls), CSV")
        print("\nExamples:")
        print("  extract_financial_data.py financial_report.pdf")
        print("  extract_financial_data.py financials.xlsx --output json")
        sys.exit(1)

    file_path = sys.argv[1]
    output_format = "json"

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]

    print(f"📊 Extracting financial data from: {file_path}")
    print(f"   Output format: {output_format}")
    print()

    try:
        extractor = FinancialDataExtractor(file_path)
        data = extractor.extract()

        if output_format == "json":
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("Note: CSV output format not yet implemented. Showing JSON instead.")
            print(json.dumps(data, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
