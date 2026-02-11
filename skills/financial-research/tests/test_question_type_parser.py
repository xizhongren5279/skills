# tests/test_question_type_parser.py
import pytest
from utils.question_type_parser import QuestionTypeParser

@pytest.fixture
def sample_excel_path():
    return "references/plan_for_question_type.xlsx"

def test_parser_initialization(sample_excel_path):
    parser = QuestionTypeParser(sample_excel_path)
    assert parser is not None
    assert parser.excel_path == sample_excel_path

def test_load_question_types(sample_excel_path):
    parser = QuestionTypeParser(sample_excel_path)
    types = parser.load_question_types()

    assert isinstance(types, list)
    assert len(types) == 26  # Excel has 26 question types
    assert all('问题' in t for t in types)
    assert all('问题类型' in t for t in types)
    assert all('类型描述' in t for t in types)
    assert all('示例' in t for t in types)
