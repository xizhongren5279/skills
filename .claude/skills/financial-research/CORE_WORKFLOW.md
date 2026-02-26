# 金融研究Skill核心流程 (不可违反)

## 核心流程图

```
用户问题 → 匹配Question Type → 生成检索PLAN → 执行MCP搜索 → 合成报告
   ↓              ↓                   ↓              ↓            ↓
Step 1.0     Step 1.0            Step 3         Step 4       Step 5-6
```

## ⚠️ 铁律(Iron Law)

```
1. 用户问题 MUST → 匹配question_type (Step 1.0)
2. 匹配结果 MUST → 生成结构化PLAN (Step 3)
3. PLAN中的tasks MUST → 通过Task tool执行 (Step 4)
4. Task tool内 MUST → 调用MCP工具搜索 (Step 4)
5. 搜索结果 MUST → 合成最终报告 (Step 5-6)

违反任何一步 = 违反skill核心要求
```

## 详细流程说明

### Step 1.0: 匹配Question Type (MANDATORY FIRST STEP)

**目的**: 将用户的原始问题匹配到26种预定义的研究问题类型之一

**输入**:
- 用户原始问题(如:"宁德时代深度研究报告")

**执行**:
1. 读取Excel文件: `references/plan_for_question_type.xlsx`
2. 加载所有26种问题类型
3. 使用LLM进行语义匹配(NOT关键词匹配)
4. 返回匹配结果:
   ```json
   {
     "matched_index": 24,
     "matched_type": "如何写一份公司深度研究报告",
     "confidence_score": 0.95,
     "reference_rules": ["规则1", "规则2", ...],
     "reference_workflow": ["步骤1", "步骤2", ...]
   }
   ```

**输出**:
- `matched_workflow.json` 保存到output目录
- 向用户宣布匹配结果

**为什么必须**:
- ✅ 确保所有研究遵循专家设计的模板
- ✅ 提供结构化的workflow指导
- ✅ 保证研究质量和一致性

**禁止行为**:
- ❌ 跳过匹配,直接创建plan
- ❌ 使用关键词匹配代替语义匹配
- ❌ 置信度<0.6不询问用户确认
- ❌ 不保存matched_workflow.json

---

### Step 3: 生成检索PLAN (Based on Matched Workflow)

**目的**: 根据匹配的workflow模板,生成结构化的研究计划

**输入**:
- Step 1.0的matched_workflow
- 用户query的具体参数(实体、时间等)

**执行**:
1. **加载matched_workflow**:
   ```python
   with open(f'{output_dir}/matched_workflow.json') as f:
       matched_workflow = json.load(f)
   ```

2. **将workflow steps映射为tasks** (PRESCRIPTIVE):
   ```python
   tasks = []
   for idx, step in enumerate(matched_workflow['reference_workflow']):
       task = {
           "id": idx + 1,
           "description": extract_title(step),
           "template_step": step,  # 保留原始workflow文本
           "dependencies": infer_dependencies(idx),
           "hints": customize_for_user_query(step, user_query)
       }
       tasks.append(task)
   ```

3. **只定制hints部分** (可定制部分):
   ```python
   hints = {
       "suggested_tools": ["info_search_finance_db", "info_search_stock_db"],
       "time_context": "2025年Q3 (最新披露季度)",
       "customization": "针对宁德时代的[步骤描述]"
   }
   ```

4. **添加planning_constraints**:
   ```python
   plan['planning_constraints'] = {
       'reference_rules': matched_workflow['reference_rules'],
       'workflow_template': matched_workflow['reference_workflow']
   }
   ```

**输出**:
- `plan.json` 保存到output目录
- 直接执行(无需用户确认)

**为什么模板是prescriptive**:
- ✅ Task数量由模板决定(不能增减)
- ✅ Task顺序由模板决定(不能调换)
- ✅ Task描述由模板决定(不能改写)
- ✅ 只有hints可以定制化

**禁止行为**:
- ❌ 不使用matched_workflow创建plan
- ❌ 改变task数量或顺序
- ❌ 自己想plan结构,忽略模板
- ❌ 不保存plan.json就执行

---

### Step 4: 执行MCP搜索 (Through Task Tool)

**目的**: 使用Task tool派生subagent,在subagent中调用MCP工具检索数据

**⚠️ 并行执行强制要求**:
```
并行执行 = 节约50%+时间
顺序执行 = 违反skill要求,浪费用户时间
```

**执行流程**:

```
Main Agent → Task tool → Subagent → MCP tools → Data
                ↓                        ↓
           parallel waves          info_search_*
       (同一波次所有tasks        (每个subagent
        在一条消息中发起)         独立调用MCP)
```

**关键规则**:
1. **MUST use Task tool**: 所有task执行必须通过Task tool
2. **MCP calls in subagent**: MCP工具调用发生在subagent内部,NOT main agent
3. **Parallel execution (CRITICAL)**: 无依赖的tasks必须并行执行(同一波次,一条消息)
4. **Pass workflow context**: Subagent必须接收matched_workflow的reference_rules

**并行执行时间对比**:
- 3个独立tasks顺序执行: Task1(5min) → Task2(5min) → Task3(5min) = 15分钟
- 3个独立tasks并行执行: Task1,2,3同时(5min) = 5分钟
- **节约时间: 67% (10分钟)**

**Subagent Prompt结构**:
```markdown
You are executing Task {id} for "{topic}".

## Matched Question Type: {matched_type}
## Reference Rules (MUST Follow):
{reference_rules}

## Your Task Template:
{template_step}

## Customization for This Query:
{hints['customization']}

## CRITICAL REQUIREMENTS:
1. Read references/mcp_tools.md FIRST
2. Call MCP tools (info_search_finance_db, info_search_stock_db)
3. Use EXPLICIT time periods (e.g., "2025年Q3", NOT "最新")
4. Return JSON with section_analysis and retrieved_files

## Suggested Tools:
{hints['suggested_tools']}

## Time Context:
{hints['time_context']}
```

**输出**:
- 每个task返回JSON:
  ```json
  {
    "section_analysis": "## 标题\n\n分析内容...",
    "retrieved_files": [...]
  }
  ```

**为什么必须用Task tool**:
- ✅ **实现真正的并行执行** (核心优势,节约50%+时间)
- ✅ **同一波次的所有tasks在一条消息中发起** (并行而非顺序)
- ✅ 隔离subagent上下文,避免污染
- ✅ 每个task独立调用MCP工具
- ✅ 可以并发检索多个实体/时间段

**禁止行为**:
- ❌ 在main conversation直接调用mcp__ashare-mcp-research__*
- ❌ **顺序执行可以并行的tasks** (严重时间浪费,违反核心要求)
- ❌ **多条消息分别发起并行tasks** (必须在一条消息中发起)
- ❌ 不传递matched_workflow给subagent
- ❌ 使用模糊时间表达("最新","最近")

---

### Step 5-6: 合成报告并保存

**目的**: 汇总所有task结果,生成最终报告并保存文件

**执行**:
1. 收集所有task的section_analysis
2. 聚合retrieved_files生成metadata
3. 按workflow顺序组装最终report.md
4. 保存4个必需文件:
   - report.md
   - plan.json
   - matched_workflow.json (Step 1.0已保存)
   - generation_log.md

**输出目录结构**:
```
output/{topic}_{timestamp}/
├── matched_workflow.json  ← Step 1.0保存
├── plan.json              ← Step 3保存
├── task1_xxx.json         ← Step 4各task输出
├── task2_xxx.json
├── ...
├── report.md              ← Step 5生成
└── generation_log.md      ← Step 6生成
```

---

## 关键检查点(Checkpoints)

### ✅ Step 1.0完成检查
- [ ] 读取了plan_for_question_type.xlsx
- [ ] 进行了LLM语义匹配(NOT关键词)
- [ ] 获得了matched_index和confidence_score
- [ ] 保存了matched_workflow.json
- [ ] 向用户宣布了匹配结果

### ✅ Step 3完成检查
- [ ] 加载了matched_workflow.json
- [ ] Tasks数量 = reference_workflow步骤数
- [ ] Tasks顺序遵循workflow顺序
- [ ] 每个task有template_step字段
- [ ] planning_constraints包含reference_rules
- [ ] 保存了plan.json

### ✅ Step 4完成检查
- [ ] 使用了Task tool (NOT直接MCP调用)
- [ ] Subagent prompt包含matched_workflow上下文
- [ ] 并行执行了无依赖的tasks
- [ ] 所有MCP调用使用了显式时间
- [ ] 收集了所有task的JSON输出

### ✅ Step 5-6完成检查
- [ ] 汇总了所有section_analysis
- [ ] 生成了retrieval_metadata.json
- [ ] 保存了report.md
- [ ] 保存了generation_log.md
- [ ] 向用户展示了完成消息

---

## 常见错误及修正

| 错误行为 | 正确行为 |
|---------|---------|
| 跳过Step 1.0,直接创建plan | 必须先匹配question_type |
| 用关键词匹配代替LLM语义匹配 | 使用LLM进行语义理解匹配 |
| 不使用matched_workflow模板 | Tasks必须来自workflow steps |
| 在main conversation调用MCP工具 | 通过Task tool → subagent → MCP |
| 顺序执行独立tasks | 解析依赖,并行执行waves |
| 使用"最新季报"等模糊时间 | 计算显式季度(如"2025年Q3") |
| 不保存matched_workflow.json | Step 1.0必须保存此文件 |
| Plan中tasks不遵循模板顺序 | 严格按reference_workflow顺序 |

---

## 总结

**核心原则**:
1. **Question Type Matching First**: 任何研究必须先匹配问题类型
2. **Template is Prescriptive**: Workflow模板是强制性的,不是建议性的
3. **MCP via Subagent Only**: MCP工具只能在Task tool的subagent中调用
4. **Explicit Time Always**: 时间表达必须显式(如"2025年Q3")
5. **Save All Artifacts**: 保存所有中间和最终文件

**流程不可逆**:
```
Step 1.0 → Step 3 → Step 4 → Step 5-6
(必须按顺序,不可跳步)
```

**最终交付物**:
- matched_workflow.json (问题类型匹配结果)
- plan.json (结构化研究计划)
- task*_*.json (各task执行输出)
- report.md (最终研究报告)
- generation_log.md (执行日志)

遵循此核心流程 = 保证研究质量和一致性
