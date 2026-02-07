# 并行Subagent执行引擎

## 概述

这个执行引擎实现了**任务内并行subagent**优化方案,可以将原本串行的MCP查询改为并行执行,显著提升研究效率。

### 核心创新

**传统架构(v1):**
```
Task → Agent → 串行MCP查询 (瓶颈)
           ↓
       5-7分钟 × 6任务 = 28.3分钟
```

**优化架构(v2):**
```
Task → 并行Subagents → 每个处理一部分MCP查询
           ↓
       Main Agent 聚合结果
           ↓
     预计9.3分钟 (67%提速)
```

## 文件说明

1. **`parallel_executor.py`** - Python执行引擎
   - 解析v2 JSON计划
   - 为每个subtask生成提示词
   - 调度并行Task调用
   - 聚合JSON结果
   - 生成性能报告

2. **`nvidia-dcf-valuation-plan-v2-parallel.json`** - v2并行计划示例
   - 包含6个任务的完整DCF估值计划
   - 每个任务定义了2-4个subtasks
   - 指定了aggregation配置
   - 预测执行时间9.3分钟

## v2 JSON计划格式

### 必需字段

```json
{
  "version": "2.0-parallel",
  "optimization": {
    "strategy": "parallel_subagents",
    "expected_speedup": "60-70%",
    "expected_time": "10-12分钟"
  },
  "tasks": [
    {
      "id": 1,
      "description": "任务描述",
      "dependencies": [前置任务ID],
      "execution_strategy": "parallel_subagents",
      "subtasks": [
        {
          "id": "1.1",
          "description": "子任务描述",
          "model": "haiku",
          "data_queries": [
            "查询1",
            "查询2"
          ],
          "output_format": "json",
          "estimated_time": "15秒"
        }
      ],
      "aggregation": {
        "description": "聚合任务描述",
        "model": "sonnet",
        "estimated_time": "90秒"
      },
      "total_estimated_time": "105秒"
    }
  ]
}
```

### 关键概念

**Subtasks** - 可并行执行的子任务
- `id`: 子任务唯一标识
- `description`: 子任务描述
- `model`: 使用的模型(haiku/sonnet)
- `data_queries`: MCP查询列表(可选)
- `task`: 任务说明(可选,与data_queries二选一)
- `output_format`: 输出格式(json/text)
- `estimated_time`: 预计耗时

**Aggregation** - 聚合子任务结果
- `description`: 聚合任务描述
- `model`: 使用的模型
- `estimated_time`: 预计耗时

## 使用方法

### 1. 准备v2计划文件

参考`nvidia-dcf-valuation-plan-v2-parallel.json`,创建你的研究计划:

```bash
# 验证JSON格式
cat your-plan.json | python -m json.tool
```

### 2. 在Claude Code中运行

**重要:** 执行引擎需要在Claude Code环境中运行,因为它依赖Task tool进行并行subagent调用。

```python
# 在Claude Code对话中:
executor = ParallelExecutor('nvidia-dcf-valuation-plan-v2-parallel.json')
report = executor.execute()
```

### 3. 并行Task调用模式

执行引擎会生成如下的并行Task调用(在Claude Code环境中实际执行):

```xml
<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">general-purpose</parameter>
    <parameter name="description">营收与增长数据</parameter>
    <parameter name="model">haiku</parameter>
    <parameter name="prompt">
      你是金融研究专家,正在执行以下研究任务的一个子任务:

      # 研究主题
      英伟达DCF估值模型与目标价测算

      # 主任务
      历史财务数据收集与分析

      # 你的子任务
      营收与增长数据

      # 数据查询要求
      请使用MCP工具查询以下数据:
      1. 英伟达FY2020-2025各年营业收入
      2. 英伟达FY2020-2025营收同比增长率
      ...

      # 输出格式
      请以JSON格式返回结果...
    </parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">general-purpose</parameter>
    <parameter name="description">盈利能力数据</parameter>
    <parameter name="model">haiku</parameter>
    <parameter name="prompt">...</parameter>
  </invoke>

  <!-- 更多并行subtask调用 -->
</function_calls>
```

### 4. 查看执行报告

执行完成后,会生成JSON格式的性能报告:

```json
{
  "execution_time": {
    "total_seconds": 560,
    "total_minutes": 9.3,
    "baseline_seconds": 1698,
    "predicted_seconds": 600,
    "speedup_percent": 67
  },
  "waves": [...],
  "tasks": [...]
}
```

## 性能预测

### Task 2示例:历史财务数据收集

**v1串行执行:**
- MCP查询: 28次 × 10秒 = 280秒(4.7分钟)
- 数据整理: 90秒
- 内容生成: 30秒
- **总计: 7分钟**

**v2并行执行:**
- 4个subtasks并行,每个7次查询
- 并行MCP查询: max(7×10秒) = 70秒
- 聚合: 60秒
- **总计: 2.2分钟**
- **节省: 69%**

### 整体预测

| 阶段 | v1耗时 | v2并行耗时 | 节省 |
|------|--------|-----------|------|
| Wave 1 (Task 1,2) | 7.0 min | 2.5 min | 64% |
| Wave 2 (Task 3,5) | 7.0 min | 2.5 min | 64% |
| Wave 3 (Task 4) | 7.0 min | 3.0 min | 57% |
| Wave 4 (Task 6) | 7.3 min | 2.8 min | 62% |
| **总计** | **28.3 min** | **10.8 min** | **62%** |

## 实测验证

我们通过实际测试验证了并行Task调用的可行性:

**测试1: 3个并行Task**
```
Task A (净利润数据): 30秒
Task B (现金流数据): 44秒
Task C (资产负债表): 18秒

串行: 92秒, 并行: 44秒
节省: 52% ✅
```

**测试2: 3个并行Task(更复杂)**
```
Task A (盈利能力, 4查询): 90秒
Task B (现金流, 13查询): 238秒
Task C (资产负债表, 6查询): 135秒

串行: 463秒 (7.7分钟), 并行: 238秒 (4分钟)
节省: 48% ✅
```

## 最佳实践

### Subtask划分原则

1. **均衡workload** - 每个subtask查询数量相近(5-10个)
2. **逻辑独立** - 子任务之间无依赖,可并行
3. **模型匹配** - 数据收集用haiku,分析用sonnet
4. **JSON输出** - 便于aggregation处理

### 模型选择策略

```
├─ 数据收集/简单整理 → haiku
├─ 复杂分析/深度洞察 → sonnet
└─ Aggregation → 根据任务复杂度选择
```

### Aggregation设计

- **输入**: 所有subtask的JSON结果
- **任务**: 整合数据,生成分析报告
- **输出**: 完整的任务输出(文本/表格/图表)

## 故障排除

### 问题1: JSON解析错误

```bash
# 验证JSON格式
python -c "import json; json.load(open('your-plan.json'))"
```

### 问题2: Subtask结果格式不一致

确保所有subtask使用`output_format: "json"`,并在提示词中明确JSON schema。

### 问题3: Aggregation超时

如果aggregation任务过重:
- 将部分分析移到subtask
- 增加aggregation的estimated_time
- 考虑使用更快的模型

## 扩展性

### 添加新的研究类型

1. 创建新的v2 JSON计划
2. 定义subtasks和aggregation
3. 使用parallel_executor.py执行

### 集成到生产环境

```python
from parallel_executor import ParallelExecutor

# 批量处理
companies = ['NVDA', 'AAPL', 'MSFT']
for company in companies:
    plan = f'{company}-dcf-plan-v2.json'
    executor = ParallelExecutor(plan)
    report = executor.execute()
    # 保存报告...
```

## 局限性

1. **需要Claude Code环境** - 依赖Task tool,无法在纯Python环境运行
2. **并发限制** - Task tool可能有并发请求上限
3. **MCP服务端支持** - 假设MCP服务端支持并发请求

## 下一步优化

- [ ] Wave 0预加载基础数据
- [ ] 智能缓存(避免重复查询)
- [ ] 增量更新(只更新变化部分)
- [ ] 自动重试失败的subtask
- [ ] 实时进度显示

## 参考文档

- `性能优化方案对比.md` - 详细对比3种优化方案
- `并行subagent优化方案.md` - 架构设计文档
- `执行报告_英伟达DCF分析_20260207.md` - v1执行基准报告

---

**最后更新:** 2026-02-07
**版本:** 1.0
**作者:** AI Research System
