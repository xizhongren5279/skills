# Test Cases for JSON Plan Execution

This directory contains test cases for validating the JSON plan-based research execution.

## Files

- `tesla-analysis-plan.json`: Example JSON plan for Tesla company analysis
- `validate_plan.py`: Python script to validate JSON plan structure and dependencies

## Validation

To validate a JSON plan:

```bash
./validate_plan.py <plan-file.json>
```

Example:
```bash
./validate_plan.py tesla-analysis-plan.json
```

The script checks:
- Required fields present
- Valid research_type
- Task IDs sequential and valid
- Dependencies reference valid task IDs
- No circular dependencies
- Calculates execution waves

## Manual Testing

To test the full execution flow with Tesla analysis:

1. **Load the financial-research skill** in a Claude session with MCP tools configured

2. **Request Tesla analysis**:
   ```
   使用financial-research skill深度分析特斯拉公司
   ```

3. **Verify JSON plan generation**:
   - Skill should read references
   - Generate JSON plan matching tesla-analysis-plan.json structure
   - Automatically start execution (no user approval needed)

4. **Monitor execution**:
   - Should see "执行Wave 1: 5个并行任务..."
   - Tasks 1-5 execute in parallel (5 subagents spawned)
   - Should see "Wave 1 完成，进入Wave 2..."
   - Task 6 executes (receives sections from tasks 1-5)

5. **Verify output**:
   - Final report saved as `特斯拉公司深度分析_company_YYYYMMDD_HHMMSS.md`
   - Generation log saved as `特斯拉公司深度分析_生成日志_YYYYMMDD_HHMMSS.md`
   - Report should have 6 sections (one per task)
   - Each section should be 800-1500 words with quantitative data

## Expected Performance

- **Wave 1** (Tasks 1-5 parallel): ~2-3 minutes
- **Wave 2** (Task 6): ~1-2 minutes
- **Integration**: ~30 seconds
- **Total**: ~4-6 minutes

## Validation Checklist

After execution, verify:

- [ ] JSON plan generated with correct structure
- [ ] Dependencies correctly identified (Wave 1: [1,2,3,4,5], Wave 2: [6])
- [ ] All tasks executed in correct order
- [ ] Each section is complete analysis (not raw data)
- [ ] Section 6 includes context from sections 1-5
- [ ] Final report has all 6 sections
- [ ] Generation log documents execution process
- [ ] Execution time within expected range

## Troubleshooting

**Issue**: Validation script fails with "File not found"
- **Solution**: Run from financial-research directory: `./docs/plans/test-cases/validate_plan.py docs/plans/test-cases/tesla-analysis-plan.json`

**Issue**: Circular dependency detected
- **Solution**: Review dependencies array, ensure no cycles (A→B→C→A)

**Issue**: Task IDs not sequential
- **Solution**: Ensure task IDs are 1, 2, 3, ... with no gaps

**Issue**: Invalid dependency reference
- **Solution**: All IDs in dependencies array must exist in tasks list
