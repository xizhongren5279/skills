# Question Type Workflow Example

This document shows a complete example of the question type matching and structured planning workflow.

## Example User Query

"分析宁德时代2024年的业务表现和投资价值"

## Step 1.0: Question Type Matching

### 1. Load Question Types

```python
from utils.question_type_parser import QuestionTypeParser

parser = QuestionTypeParser('references/plan_for_question_type.xlsx')
types = parser.load_question_types()

print(f"Loaded {len(types)} question types")
# Output: Loaded 26 question types
```

### 2. Generate Matching Prompt

```python
workflow_result = parser.get_workflow_for_query(
    "分析宁德时代2024年的业务表现和投资价值",
    use_llm=True
)

matching_prompt = workflow_result['_matching_prompt']
```

### 3. LLM Matching Result

LLM returns:
```json
{
  "matched_index": 22,
  "confidence_score": 0.88,
  "reasoning": "用户问题涉及业务表现和投资价值分析,最匹配'如何做好上市公司基本面分析'类型"
}
```

### 4. Extract Matched Workflow

```python
matched_type = types[21]  # Index 22 - 1 = 21

workflow_data = parser.extract_workflow(matched_type)

print("Question Type:", matched_type['问题类型'])
# Output: 如何做好上市公司基本面分析

print("Reference Workflow Steps:", len(workflow_data['reference_workflow']))
# Output: 6 (example - actual number depends on Excel content)
```

## Step 3: Plan Generation Using Template

### Template Workflow (from Excel)

Assume the matched type has this workflow:
1. 收集公司基本信息
2. 分析财务数据和经营指标
3. 评估业务模式和竞争优势
4. 分析行业地位和市场份额
5. 评估管理层和公司治理
6. 综合评估投资价值

### Generated Plan (plan.json)

```json
{
  "research_type": "company",
  "topic": "宁德时代2024年基本面分析",
  "current_date": "20260211-143000",
  "current_year": 2026,
  "current_quarter": 1,

  "question_type_metadata": {
    "matched_type": "如何做好上市公司基本面分析",
    "type_description": "全面分析上市公司的基本面,包括财务、业务、行业地位等",
    "confidence_score": 0.88,
    "template_source": "plan_for_question_type.xlsx"
  },

  "planning_constraints": {
    "reference_rules": [
      "确保数据来源可靠,优先使用官方披露",
      "定量分析与定性分析相结合",
      "关注长期价值而非短期波动"
    ],
    "workflow_template": [
      "收集公司基本信息",
      "分析财务数据和经营指标",
      "评估业务模式和竞争优势",
      "分析行业地位和市场份额",
      "评估管理层和公司治理",
      "综合评估投资价值"
    ]
  },

  "tasks": [
    {
      "id": 1,
      "description": "收集公司基本信息",
      "template_step": "收集公司基本信息",
      "dependencies": [],
      "hints": {
        "data_needs": ["公司概况", "主营业务", "组织架构"],
        "suggested_tools": ["info_search_finance_db"],
        "time_context": "2024年全年",
        "customization": "重点关注宁德时代的业务结构和产品线"
      }
    },
    {
      "id": 2,
      "description": "分析财务数据和经营指标",
      "template_step": "分析财务数据和经营指标",
      "dependencies": [],
      "hints": {
        "data_needs": ["营收", "净利润", "ROE", "毛利率", "现金流"],
        "suggested_tools": ["info_search_stock_db", "info_search_finance_db"],
        "time_context": "2024年Q1-Q4季度数据",
        "customization": "对比2023年数据,分析增长趋势"
      }
    },
    {
      "id": 3,
      "description": "评估业务模式和竞争优势",
      "template_step": "评估业务模式和竞争优势",
      "dependencies": [1],
      "hints": {
        "data_needs": ["业务模式", "核心技术", "客户结构"],
        "suggested_tools": ["info_search_finance_db"],
        "time_context": "2024年最新情况",
        "customization": "分析动力电池业务的护城河"
      }
    },
    {
      "id": 4,
      "description": "分析行业地位和市场份额",
      "template_step": "分析行业地位和市场份额",
      "dependencies": [],
      "hints": {
        "data_needs": ["市场份额", "行业排名", "竞争对手对比"],
        "suggested_tools": ["info_search_finance_db"],
        "time_context": "2024年行业数据",
        "customization": "与比亚迪、LG化学等对手对比"
      }
    },
    {
      "id": 5,
      "description": "评估管理层和公司治理",
      "template_step": "评估管理层和公司治理",
      "dependencies": [1],
      "hints": {
        "data_needs": ["管理层背景", "战略规划", "治理结构"],
        "suggested_tools": ["info_search_finance_db"],
        "time_context": "近期管理层动态",
        "customization": "关注战略转型和新业务拓展"
      }
    },
    {
      "id": 6,
      "description": "综合评估投资价值",
      "template_step": "综合评估投资价值",
      "dependencies": [2, 3, 4, 5],
      "hints": {
        "data_needs": ["估值水平", "成长性", "风险因素"],
        "suggested_tools": ["info_search_finance_db", "info_search_stock_db"],
        "time_context": "基于2024年数据的前瞻分析",
        "customization": "结合行业趋势给出投资建议"
      }
    }
  ]
}
```

## Key Benefits

1. **Consistent Structure**: All "公司基本面分析" questions follow the same 6-step workflow
2. **Proven Template**: Workflow comes from domain expert-designed Excel templates
3. **Customized Execution**: While structure is fixed, hints are tailored to user's specific query
4. **Reproducible**: Same question type always produces similar plan structure
5. **Auditable**: plan.json records which template was used and matching confidence

## Validation Checklist

Before executing the plan, verify:
- [ ] `question_type_metadata` is populated with matched type
- [ ] `tasks[].template_step` matches `planning_constraints.workflow_template` steps
- [ ] Task dependencies reflect logical workflow order
- [ ] `hints.customization` fields contain user-query-specific details
- [ ] All tasks include appropriate `suggested_tools` from reference workflow
