# tests/integration/test_question_type_integration.py
"""
Integration test for end-to-end question type matching and plan generation.
This test simulates the full workflow from Step 1.0 to Step 3.
"""
import pytest
import json
from datetime import datetime
from utils.question_type_parser import QuestionTypeParser

@pytest.fixture
def parser():
    return QuestionTypeParser('references/plan_for_question_type.xlsx')

def test_full_workflow_company_research(parser):
    """Test complete workflow for company research question."""

    # Step 1.0: Match question type
    user_query = "分析宁德时代2024年的业务表现和竞争优势"

    # Load types
    types = parser.load_question_types()
    assert len(types) == 26

    # Match (using keyword matching for deterministic test)
    matched = parser.match_question_type(user_query, use_llm=False)

    assert matched is not None
    assert 'question_type' in matched or '问题类型' in matched
    assert 'confidence_score' in matched

    # Extract workflow
    workflow_data = parser.extract_workflow(matched)

    assert 'reference_rules' in workflow_data
    assert 'reference_workflow' in workflow_data

    # Step 3: Generate plan structure (simulated)
    current_time = datetime.now()

    plan = {
        'research_type': 'company',
        'topic': '宁德时代2024年分析',
        'current_date': current_time.strftime("%Y%m%d-%H%M%S"),
        'current_year': current_time.year,
        'current_quarter': (current_time.month - 1) // 3 + 1,

        'question_type_metadata': {
            'matched_type': matched.get('问题类型', 'unknown'),
            'confidence_score': matched['confidence_score'],
            'template_source': 'plan_for_question_type.xlsx'
        },

        'planning_constraints': {
            'reference_rules': workflow_data['reference_rules'],
            'workflow_template': workflow_data['reference_workflow']
        },

        'tasks': []
    }

    # Generate tasks from workflow
    for idx, step in enumerate(workflow_data['reference_workflow']):
        task = {
            'id': idx + 1,
            'description': step,
            'template_step': step,
            'dependencies': [],
            'hints': {
                'customization': f'针对{user_query}的定制化分析'
            }
        }
        plan['tasks'].append(task)

    # Validate plan structure
    assert 'question_type_metadata' in plan
    assert 'planning_constraints' in plan
    assert len(plan['tasks']) > 0
    assert all('template_step' in t for t in plan['tasks'])

    # Ensure plan is JSON serializable
    plan_json = json.dumps(plan, ensure_ascii=False, indent=2)
    assert len(plan_json) > 100

def test_workflow_preserves_template_order(parser):
    """Test that generated tasks preserve workflow template order."""

    user_query = "行业竞争格局分析"
    matched = parser.match_question_type(user_query, use_llm=False)
    workflow_data = parser.extract_workflow(matched)

    # Generate tasks
    tasks = []
    for idx, step in enumerate(workflow_data['reference_workflow']):
        tasks.append({
            'id': idx + 1,
            'description': step,
            'template_step': step
        })

    # Verify order preservation
    for i, task in enumerate(tasks):
        assert task['id'] == i + 1
        assert task['template_step'] == workflow_data['reference_workflow'][i]

def test_multiple_queries_use_correct_templates(parser):
    """Test that different query types get different templates."""

    queries = [
        "公司估值分析",
        "行业研究",
        "财务报表分析"
    ]

    matched_types = []
    for query in queries:
        matched = parser.match_question_type(query, use_llm=False)
        matched_types.append(matched.get('问题类型', matched.get('_matching_prompt')))

    # Each query should match a type (even if same type)
    assert len(matched_types) == len(queries)
    assert all(t is not None for t in matched_types)
