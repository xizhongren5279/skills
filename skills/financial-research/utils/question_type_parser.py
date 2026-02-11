# utils/question_type_parser.py
import pandas as pd
from pathlib import Path

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

    def match_question_type(self, user_query: str, use_llm: bool = True) -> dict | None:
        """
        Match user query to best question type.

        Args:
            user_query: User's financial research question
            use_llm: If True, use LLM for semantic matching. If False, use simple heuristics.

        Returns:
            Dictionary with matched type data and confidence_score
        """
        if self._df is None:
            self.load_question_types()

        if not use_llm:
            # Simple fallback: keyword matching
            return self._keyword_match(user_query)

        # Build matching prompt
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

    def _keyword_match(self, user_query: str) -> dict:
        """Fallback keyword-based matching."""
        # Simple heuristic matching
        query_lower = user_query.lower()

        matched_idx = 0  # Default to first type
        confidence = 0.5

        # Basic keyword matching logic
        if '估值' in query_lower or 'pe' in query_lower or 'pb' in query_lower:
            matched_idx = 1  # 如何做好公司估值分析
        elif '行业' in query_lower or '竞争' in query_lower:
            matched_idx = 3  # 如何做好行业研究
        elif '财报' in query_lower or '业绩' in query_lower:
            matched_idx = 5  # 如何做好公司年报的业绩点评

        matched_row = self._df.iloc[matched_idx]
        return {
            '问题类型': matched_row['问题类型'],
            '类型描述': matched_row['类型描述'],
            '问题': matched_row['问题'],
            '示例': matched_row['示例'],
            'confidence_score': confidence,
            'matched_index': matched_idx
        }
