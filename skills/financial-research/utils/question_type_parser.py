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
