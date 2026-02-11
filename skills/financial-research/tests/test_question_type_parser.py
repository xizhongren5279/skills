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

def test_file_not_found():
    """Test error handling when Excel file doesn't exist."""
    parser = QuestionTypeParser("nonexistent_file.xlsx")
    with pytest.raises(FileNotFoundError) as exc_info:
        parser.load_question_types()
    assert "Excel file not found" in str(exc_info.value)
    assert "nonexistent_file.xlsx" in str(exc_info.value)

def test_match_question_type(sample_excel_path):
    """Test keyword-based question type matching."""
    parser = QuestionTypeParser(sample_excel_path)
    parser.load_question_types()

    # Test with keyword matching (no LLM)
    user_query = "分析宁德时代的业务模式和竞争优势"
    matched = parser.match_question_type(user_query, use_llm=False)

    assert matched is not None
    assert '问题类型' in matched
    assert '类型描述' in matched
    assert '示例' in matched
    assert 'confidence_score' in matched
    assert 0.0 <= matched['confidence_score'] <= 1.0

def test_match_question_type_llm_mode(sample_excel_path):
    """Test LLM-based question type matching mode."""
    parser = QuestionTypeParser(sample_excel_path)
    parser.load_question_types()

    user_query = "分析宁德时代的业务模式"
    result = parser.match_question_type(user_query, use_llm=True)

    # In LLM mode, returns prompt for external execution
    assert result is not None
    assert '_matching_prompt' in result
    assert '_needs_llm_execution' in result

def test_extract_workflow_from_example(sample_excel_path):
    """Test extracting workflow from matched type's example field."""
    parser = QuestionTypeParser(sample_excel_path)
    parser.load_question_types()

    # Get a matched type (use keyword matching for test)
    matched = parser.match_question_type("公司估值分析", use_llm=False)

    # Extract workflow from the example field
    workflow = parser.extract_workflow(matched)

    assert workflow is not None
    assert 'reference_rules' in workflow
    assert 'reference_workflow' in workflow
    assert isinstance(workflow['reference_workflow'], list)

def test_get_workflow_for_query(sample_excel_path):
    """Test end-to-end workflow: query -> match -> extract workflow."""
    parser = QuestionTypeParser(sample_excel_path)

    # End-to-end: query -> match -> extract workflow
    workflow = parser.get_workflow_for_query("如何评估比亚迪的估值水平?", use_llm=False)

    assert workflow is not None
    assert 'question_type' in workflow
    assert 'confidence_score' in workflow
    assert 'reference_rules' in workflow
    assert 'reference_workflow' in workflow
