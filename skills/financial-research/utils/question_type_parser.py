# utils/question_type_parser.py
import pandas as pd

class QuestionTypeParser:
    def __init__(self, excel_path: str):
        self.excel_path = excel_path
        self._df = None

    def load_question_types(self) -> list[dict]:
        """Read Excel and return list of question type dictionaries."""
        if self._df is None:
            self._df = pd.read_excel(self.excel_path)

        types = []
        for _, row in self._df.iterrows():
            types.append({
                '问题类型': row['问题类型'],
                '类型描述': row['类型描述'],
                '问题': row['问题'],
                '示例': row['示例']
            })

        return types
