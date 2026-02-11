# utils/question_type_parser.py
import pandas as pd
from pathlib import Path
import json
import re

class QuestionTypeParser:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self._df = None

    def load_question_types(self) -> list[dict]:
        """Read Excel and return list of question type dictionaries."""
        if self._df is None:
            # Add error handling for file reading
            try:
                # Check if file exists
                if not Path(self.excel_path).exists():
                    raise FileNotFoundError(f"Excel file not found: {self.excel_path}")

                # Read Excel file
                self._df = pd.read_excel(self.excel_path)

            except FileNotFoundError:
                raise
            except Exception as e:
                raise ValueError(f"Failed to read Excel file '{self.excel_path}': {str(e)}")

            # Validate required columns exist
            required_columns = ['问题类型', '类型描述', '问题', '示例']
            missing_columns = [col for col in required_columns if col not in self._df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in Excel file: {missing_columns}")

        # Use to_dict('records') for better performance instead of iterrows()
        return self._df[['问题类型', '类型描述', '问题', '示例']].to_dict('records')

    def match_question_type(self, user_query: str) -> dict:
        """
        Match user query to best question type using LLM semantic matching.

        Args:
            user_query: User's financial research question

        Returns:
            Dictionary with matching prompt for LLM execution
        """
        # Ensure data is loaded
        self.load_question_types()

        # Build matching prompt for LLM semantic matching
        types_summary = []
        for idx, row in self._df.iterrows():
            types_summary.append(f"{idx+1}. {row['问题类型']}: {row['类型描述']}")

        prompt = f"""给定用户问题和26种预定义的研究问题类型,选择最匹配的类型。

用户问题: {user_query}

可选问题类型:
{chr(10).join(types_summary)}

请返回JSON格式:
{{
  "matched_index": <索引号1-26>,
  "confidence_score": <0.0-1.0>,
  "reasoning": "<为什么选择这个类型>"
}}"""

        # This will be called by the main skill which has LLM access
        # Store prompt for external execution
        result = {
            '_matching_prompt': prompt,
            '_needs_llm_execution': True
        }

        return result

    def extract_workflow(self, matched_type: dict) -> dict:
        """
        Extract REFERENCE RULES and REFERENCE WORKFLOW from matched type's example.

        Args:
            matched_type: Dictionary containing matched question type data

        Returns:
            Dictionary with 'reference_rules' and 'reference_workflow' keys
        """
        example_text = matched_type.get('示例', '')

        if not example_text:
            return {
                'reference_rules': [],
                'reference_workflow': []
            }

        # Try to parse as JSON if it looks like JSON
        if example_text.strip().startswith('{'):
            try:
                parsed = json.loads(example_text)
                return {
                    'reference_rules': parsed.get('REFERENCE RULES', []),
                    'reference_workflow': parsed.get('REFERENCE WORKFLOW', [])
                }
            except json.JSONDecodeError:
                pass

        # Fallback: extract from text structure
        rules = []
        workflow = []

        # Look for "REFERENCE RULES" section
        rules_match = re.search(r'REFERENCE RULES[:\s]*(.*?)(?:REFERENCE WORKFLOW|$)',
                               example_text, re.DOTALL | re.IGNORECASE)
        if rules_match:
            rules_text = rules_match.group(1).strip()
            # Split by numbered items or bullet points
            rules = re.findall(r'(?:^|\n)\s*[\d\-\*]+[\.\)]\s*(.+?)(?=\n\s*[\d\-\*]+[\.\)]|\n\n|$)',
                              rules_text, re.DOTALL)
            rules = [r.strip() for r in rules if r.strip()]

        # Look for "REFERENCE WORKFLOW" section
        workflow_match = re.search(r'REFERENCE WORKFLOW[:\s]*(.*?)$',
                                   example_text, re.DOTALL | re.IGNORECASE)
        if workflow_match:
            workflow_text = workflow_match.group(1).strip()
            # Split by numbered items
            workflow = re.findall(r'(?:^|\n)\s*[\d\-\*]+[\.\)]\s*(.+?)(?=\n\s*[\d\-\*]+[\.\)]|\n\n|$)',
                                 workflow_text, re.DOTALL)
            workflow = [w.strip() for w in workflow if w.strip()]

        return {
            'reference_rules': rules,
            'reference_workflow': workflow
        }

    def get_workflow_for_query(self, user_query: str) -> dict:
        """
        End-to-end: match question type and extract workflow using LLM semantic matching.

        Args:
            user_query: User's research question

        Returns:
            Dictionary with question_type, confidence_score, reference_rules, reference_workflow
        """
        # Match question type (returns LLM prompt for external execution)
        matched = self.match_question_type(user_query)

        if matched is None or matched.get('_needs_llm_execution'):
            return matched  # Return LLM prompt for external execution

        # Extract workflow
        workflow_data = self.extract_workflow(matched)

        # Combine results
        return {
            'question_type': matched['问题类型'],
            'type_description': matched['类型描述'],
            'confidence_score': matched['confidence_score'],
            'matched_index': matched.get('matched_index'),
            'reference_rules': workflow_data['reference_rules'],
            'reference_workflow': workflow_data['reference_workflow'],
            'full_example': matched['示例']
        }
