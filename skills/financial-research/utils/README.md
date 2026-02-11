# Utils Module

Utility functions and classes for the financial research skill.

## QuestionTypeParser

Parses question types from Excel file and matches user queries to predefined research workflows.

### Usage

```python
from utils.question_type_parser import QuestionTypeParser

# Initialize parser
parser = QuestionTypeParser('references/plan_for_question_type.xlsx')

# Load all question types (26 types from Excel)
types = parser.load_question_types()

# Match user query to question type (keyword-based)
user_query = "分析宁德时代的投资价值"
matched = parser.match_question_type(user_query, use_llm=False)

print(f"Matched type: {matched['问题类型']}")
print(f"Confidence: {matched['confidence_score']}")

# Extract workflow from matched type
workflow_data = parser.extract_workflow(matched)

print(f"Reference rules: {workflow_data['reference_rules']}")
print(f"Workflow steps: {workflow_data['reference_workflow']}")

# End-to-end: query -> match -> extract
workflow = parser.get_workflow_for_query(user_query, use_llm=False)

print(f"Question type: {workflow['question_type']}")
print(f"Workflow has {len(workflow['reference_workflow'])} steps")
```

### LLM-Based Matching

For production use with LLM:

```python
# Get matching prompt for LLM execution
result = parser.get_workflow_for_query(user_query, use_llm=True)

if result.get('_needs_llm_execution'):
    # Execute the matching prompt with LLM
    matching_prompt = result['_matching_prompt']

    # LLM returns: {"matched_index": 5, "confidence_score": 0.85, "reasoning": "..."}
    # Then use matched_index to get workflow
```

### API Reference

#### `QuestionTypeParser.__init__(excel_path: str)`

Initialize parser with path to Excel file.

**Parameters:**
- `excel_path`: Path to `plan_for_question_type.xlsx`

#### `load_question_types() -> list[dict]`

Load all 26 question types from Excel.

**Returns:** List of dictionaries with keys: `问题类型`, `类型描述`, `问题`, `示例`

#### `match_question_type(user_query: str, use_llm: bool = True) -> dict | None`

Match user query to best question type.

**Parameters:**
- `user_query`: User's financial research question
- `use_llm`: If True, returns LLM prompt for execution. If False, uses keyword matching.

**Returns:** Dictionary with matched type data and `confidence_score`

#### `extract_workflow(matched_type: dict) -> dict`

Extract REFERENCE RULES and REFERENCE WORKFLOW from matched type.

**Parameters:**
- `matched_type`: Dictionary from `match_question_type()`

**Returns:** Dictionary with `reference_rules` and `reference_workflow` lists

#### `get_workflow_for_query(user_query: str, use_llm: bool = True) -> dict`

End-to-end workflow: match type and extract workflow.

**Parameters:**
- `user_query`: User's research question
- `use_llm`: Whether to use LLM for matching

**Returns:** Dictionary with `question_type`, `confidence_score`, `reference_rules`, `reference_workflow`

### Excel File Format

Expected columns in `plan_for_question_type.xlsx`:
- `问题类型`: Question type name
- `类型描述`: Description of the question type
- `问题`: Questions this type addresses
- `示例`: Example with REFERENCE RULES and REFERENCE WORKFLOW

### Testing

Run tests:
```bash
# Unit tests
pytest tests/test_question_type_parser.py -v

# Integration tests
pytest tests/integration/test_question_type_integration.py -v

# All tests
pytest tests/ -v
```
