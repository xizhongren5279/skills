#!/bin/bash

echo "Running validation suite..."
echo ""

echo "1. Testing question type parser..."
pytest tests/test_question_type_parser.py -v
if [ $? -ne 0 ]; then
    echo "❌ Unit tests failed"
    exit 1
fi
echo "✅ Unit tests passed"
echo ""

echo "2. Testing integration..."
pytest tests/integration/ -v
if [ $? -ne 0 ]; then
    echo "❌ Integration tests failed"
    exit 1
fi
echo "✅ Integration tests passed"
echo ""

echo "3. Validating Excel file..."
python3 -c "
from utils.question_type_parser import QuestionTypeParser
parser = QuestionTypeParser('references/plan_for_question_type.xlsx')
types = parser.load_question_types()
assert len(types) == 26, f'Expected 26 types, got {len(types)}'
print(f'✅ Excel file valid: {len(types)} question types loaded')
"
if [ $? -ne 0 ]; then
    echo "❌ Excel validation failed"
    exit 1
fi

echo ""
echo "🎉 All validations passed!"
