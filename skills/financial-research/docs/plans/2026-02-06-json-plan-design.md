# JSON化研究计划设计文档

**日期**: 2026-02-06
**类型**: 架构改进设计

## 概述

将financial-research skill的研究计划从文本化Phase结构改为JSON化的扁平任务列表，实现依赖驱动的自动执行。

## 核心设计理念

1. **结构化JSON输出**：将研究计划从Markdown格式改为机器可读的JSON结构
2. **扁平化任务模型**：取消Phase概念，使用带依赖关系的扁平任务列表
3. **显式依赖管理**：每个任务明确声明直接依赖，系统可推导执行顺序
4. **自动化执行**：PLAN生成后立即识别可并行任务并启动执行

**关键改进点**：
- 从"人工阅读Phase → 判断并行性"变为"机器解析dependencies → 自动识别并行任务"
- 从"手动控制Phase执行顺序"变为"依赖驱动的自动调度"
- 任务保持高层次抽象（章节级别），具体MCP调用由subagent根据提示自主决定

## JSON PLAN结构定义

### 完整结构

```json
{
  "research_type": "company|industry|strategy|macro|quantitative",
  "topic": "研究主题描述",
  "objectives": [
    "目标1",
    "目标2",
    "目标3"
  ],
  "tasks": [
    {
      "id": 1,
      "description": "分析任务的高层次描述（章节级别）",
      "dependencies": [],
      "hints": {
        "data_needs": ["需要的数据类型1", "需要的数据类型2"],
        "key_questions": ["关键问题1", "关键问题2"],
        "suggested_tools": ["info_search_finance_db", "info_search_stock_db"]
      }
    },
    {
      "id": 2,
      "description": "另一个独立的分析任务",
      "dependencies": [],
      "hints": {...}
    },
    {
      "id": 3,
      "description": "依赖前面结果的分析任务",
      "dependencies": [1, 2],
      "hints": {...}
    }
  ]
}
```

### 字段说明

**顶层字段**：
- `research_type`: 研究类型（company/industry/strategy/macro/quantitative）
- `topic`: 研究主题描述
- `objectives`: 研究目标列表（数组）
- `tasks`: 任务列表（数组）

**任务对象字段**：
- `id`: 任务编号（正整数，连续）
- `description`: 高层次分析任务描述（章节级别）
- `dependencies`: 直接依赖的任务ID列表（只包含直接依赖）
- `hints`: 可选的执行提示对象
  - `data_needs`: 需要的数据类型列表
  - `key_questions`: 关键问题列表
  - `suggested_tools`: 建议的MCP工具列表

## 自动执行与调度逻辑

### 依赖解析与任务分组

```python
# 伪代码示例
wave_1 = [task for task in tasks if task.dependencies == []]
# 在单个message中spawn所有wave_1的subagents（并行）

# 等待wave_1完成后
completed = {1, 2, 3}  # wave_1的任务ID
wave_2 = [task for task in tasks
          if all(dep in completed for dep in task.dependencies)
          and task.id not in completed]
# spawn wave_2的subagents（并行）
```

### 并行执行策略

- 解析JSON，识别dependencies为[]的任务 → 第一批并行任务
- 执行第一批后，识别依赖已满足的任务 → 第二批并行任务
- 重复直到所有任务完成

### Subagent执行模式

- Subagent收到任务description和hints
- 读取references/mcp_tools.md了解可用工具
- 根据hints自主规划需要的MCP查询
- 执行查询并完成分析章节
- **关键**：返回完整的section分析文本（非原始检索数据）

## 完整工作流程

### Step 1: 理解请求（保持不变）
- 识别研究类型
- 提取关键参数
- 必要时用AskUserQuestion澄清

### Step 2: 读取参考文档（保持不变）
- 读取mcp_tools.md、research_workflows.md、planning_guide.md
- 理解可用工具和推荐结构

### Step 3: 生成JSON PLAN（核心变化）
- 确定研究目标（objectives）
- 分解为高层次分析任务（章节级别）
- 分析任务间依赖关系
- 为每个任务添加执行hints
- 输出完整JSON结构

### Step 4: 自动执行PLAN（新增）

**Wave 1**: 识别dependencies=[]的任务
- 并行spawn subagents执行这些任务
- 每个subagent完成检索后，立即撰写该任务对应的section分析
- 返回：完整的section文本（非原始检索数据）

**Wave 2**: 识别依赖已满足的任务
- 传递前序任务的section分析作为context
- 执行检索 → 撰写section分析
- 返回：section文本

重复直到所有任务完成，累积所有section分析

### Step 5: 整合与生成报告（修正版）

- 输入：所有任务产出的section分析文本
- 检查section间的一致性和逻辑连贯性
- 补充必要的过渡段落和executive summary
- 组装最终Markdown报告
- 保存报告和生成日志

**关键区别**：分析发生在任务执行时，最后只做轻量级整合，而非重新分析所有数据。

## 具体示例

以"深度分析特斯拉公司"为例：

```json
{
  "research_type": "company",
  "topic": "特斯拉公司深度分析",
  "objectives": [
    "全面评估特斯拉的业务模式和竞争优势",
    "分析财务表现和增长驱动因素",
    "评估风险因素和未来展望"
  ],
  "tasks": [
    {
      "id": 1,
      "description": "公司概况与业务模式分析",
      "dependencies": [],
      "hints": {
        "data_needs": ["公司背景", "主营业务", "商业模式"],
        "key_questions": ["核心产品线是什么", "收入结构如何"],
        "suggested_tools": ["info_search_finance_db"]
      }
    },
    {
      "id": 2,
      "description": "财务表现与关键指标分析",
      "dependencies": [],
      "hints": {
        "data_needs": ["近3年营收利润", "ROE", "毛利率", "现金流"],
        "key_questions": ["盈利能力趋势", "财务健康度"],
        "suggested_tools": ["info_search_stock_db", "info_search_finance_db"]
      }
    },
    {
      "id": 3,
      "description": "竞争格局与市场地位",
      "dependencies": [],
      "hints": {
        "data_needs": ["行业竞争对手", "市场份额", "技术优势"],
        "key_questions": ["主要竞争对手有哪些", "差异化优势"],
        "suggested_tools": ["info_search_finance_db"]
      }
    },
    {
      "id": 4,
      "description": "综合评估与投资建议",
      "dependencies": [1, 2, 3],
      "hints": {
        "data_needs": ["最新研报观点", "分析师评级"],
        "key_questions": ["综合评价", "投资价值判断"],
        "suggested_tools": ["info_search_finance_db"]
      }
    }
  ]
}
```

**执行过程**：
- Wave 1: 任务1、2、3并行执行（3个subagents同时启动）
- 每个完成后输出对应section的完整分析
- Wave 2: 任务4执行，接收前3个section作为context
- 最终整合4个section生成完整报告

## Subagent Prompt模板

```markdown
你正在执行研究计划中的任务 {task_id}: {task_description}

## 研究背景
- 研究类型: {research_type}
- 研究主题: {topic}
- 总体目标: {objectives}

## 你的任务
{task_description}

## 执行提示
- 需要的数据: {hints.data_needs}
- 关键问题: {hints.key_questions}
- 建议工具: {hints.suggested_tools}

{如果有dependencies，则包含：}
## 前序任务的分析结果
{依赖任务的section文本}

## 执行要求
1. 阅读 references/mcp_tools.md 了解可用MCP工具的详细用法
2. 根据任务需求，自主决定需要执行哪些MCP查询
3. 执行检索并分析数据
4. 撰写完整的section分析（800-1500字，包含具体数据和洞察）
5. 返回格式：
   ```markdown
   ## {section标题}

   {分析内容，必须包含定量数据、具体时间、来源引用}
   ```

注意：返回完整的分析文本，不是原始检索结果。
```

**关键设计**：
- 提供充分context但不过度限制
- 明确要求输出格式（完整section）
- 强调定量和具体性

## 实现变更点

### 1. SKILL.md更新

**Step 3"创建研究计划"部分**：
- 删除Markdown格式的Phase结构示例
- 替换为JSON PLAN结构说明
- 强调任务抽象层次和dependencies规则

**Step 4"执行研究计划"部分**：
- 删除"展示计划给用户审核"的说明
- 替换为自动解析dependencies并分波执行
- 更新subagent prompt模板

### 2. references/planning_guide.md更新

添加"JSON PLAN创建指南"章节：
- 如何分解研究为章节级任务
- 如何识别任务依赖关系
- 如何撰写有效的hints
- 避免过度依赖（保持并行度）

### 3. 新增实现逻辑（在执行时）

- 依赖解析算法（识别可并行任务波次）
- Subagent context传递机制（前序任务结果）
- Section累积和最终整合逻辑

### 不需要改变的

- references/mcp_tools.md（工具文档保持不变）
- references/research_workflows.md（分析框架保持不变）
- 最终报告格式和保存逻辑

## 错误处理与边缘情况

### 1. 依赖关系问题

**循环依赖检测**：
- 在生成PLAN时验证无环
- 算法：拓扑排序，如果失败则存在循环
- 处理：拒绝生成，要求重新规划

**无效依赖ID**：
- 验证：所有dependency中的ID必须存在于tasks中
- 处理：生成阶段验证并修正

### 2. Subagent执行失败

**单个任务失败**：
- 记录失败原因和任务ID
- 阻塞所有依赖该任务的下游任务
- 用占位符标记该section："[数据获取失败：原因]"
- 继续执行其他独立任务

**重试策略**：
- MCP工具超时或网络错误：自动重试1次
- 数据不存在：不重试，返回说明
- Subagent崩溃：记录并标记失败

### 3. 数据质量问题

- Section分析过于简短（<300字）：警告但接受
- Section缺少定量数据：在最终整合时补充说明
- 前后section矛盾：在整合阶段标注并尝试调和

## 性能优化考虑

### 1. 任务粒度平衡

**过粗**（如只有2-3个大任务）：
- 问题：并行度低，总时间长
- 解决：鼓励将大任务拆分为独立子任务

**过细**（如10+个小任务）：
- 问题：subagent启动开销大，context传递复杂
- 解决：合并相关的小任务为章节级任务

**建议粒度**：4-7个任务为宜

### 2. 依赖关系优化

**最小化依赖链长度**：
- 避免：Task1→Task2→Task3→Task4（4层串行）
- 优化：Task1→Task4，Task2→Task4，Task3→Task4（2层并行）

**识别伪依赖**：
- 问题："综合分析"不一定真的需要所有前序任务
- 优化：只声明真正必需的依赖

### 3. Hints精准度

- **好的hint**："近3年财务数据，重点关注营收和ROE"
- **差的hint**："使用info_search_stock_db查询特斯拉2021-2024年ROE"
- **原因**：过于具体限制了subagent灵活性

### 4. 执行时间估算

- Wave数量 ≈ 最长依赖链长度
- 每个wave时间 ≈ 最慢任务的时间（2-4分钟）
- 总时间 ≈ Wave数量 × 3分钟

## 迁移策略

- **向后兼容**：新版本支持JSON PLAN，旧案例逐步迁移
- **文档先行**：先更新SKILL.md和planning_guide.md
- **渐进实现**：先实现PLAN生成，再实现自动执行
- **测试验证**：用现有研究案例测试新流程

## 设计原则总结

1. ✅ JSON化PLAN：结构化、机器可读
2. ✅ 扁平化任务：显式dependencies，无Phase概念
3. ✅ 任务抽象层次：章节级别，subagent自主决定MCP调用
4. ✅ 自动执行：依赖驱动的并行调度
5. ✅ 即时分析：每个任务完成检索后立即写section
6. ✅ 轻量整合：最终只整合section文本

---

*设计完成日期: 2026-02-06*
