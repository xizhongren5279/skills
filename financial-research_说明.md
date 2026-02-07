# Financial Research Skill 使用说明

## 概述

这是一个通用的金融研究skill,可以处理各种类型的金融研究任务,包括:
- 公司研究
- 行业研究  
- 策略研究
- 宏观研究
- 量化分析

## 核心特点

### 1. 智能规划
- 收到研究需求后,自动制定详细的检索计划
- 计划包含所有MCP查询的具体参数和执行顺序
- 向用户展示计划并获得批准后再执行

### 2. 高效并行
- 最大化并行检索,通常2-3个phase完成整个研究
- Phase 1: 并行检索所有基础数据(10-20个queries)
- Phase 2: 如有依赖,处理依赖查询
- Phase N: 整合所有findings生成最终报告

### 3. 参考文档驱动
Skill包含3个关键参考文档:
- **mcp_tools.md**: 4种MCP工具的完整文档和使用示例
- **research_workflows.md**: 6种研究类型的详细workflow模板
- **planning_guide.md**: 如何优化规划以最大化效率

执行前,skill会先阅读相关参考文档,确保使用正确的工具和策略。

## 使用方式

直接提出研究需求即可,例如:

```
"研究新能源汽车行业的竞争格局"
"深度分析英伟达的业务和财务表现"  
"对比腾讯和阿里巴巴的估值"
"分析2025年美联储政策对市场的影响"
```

Skill会:
1. 理解你的需求
2. 制定详细的研究计划
3. 向你展示计划并等待批准
4. 执行并行检索
5. 生成最终研究报告

## 性能

| 研究复杂度 | 预计时间 |
|-----------|---------|
| 简单(3-5 sections) | 2-3分钟 |
| 中等(5-8 sections) | 3-5分钟 |
| 复杂(10+ sections) | 5-8分钟 |

## 与company-one-page的区别

| 维度 | company-one-page | financial-research |
|------|------------------|-------------------|
| 用途 | 快速生成标准化的公司一页纸 | 任意类型的金融研究 |
| 结构 | 固定的5-section结构 | 灵活的自定义结构 |
| 深度 | 一页纸概览 | 深度调研 |
| 触发词 | "生成XX公司一页纸" | "研究/分析/对比..." |

两个skills互补,各司其职。

## 文件位置

```
/Users/xizhongren/Downloads/skills/
├── financial-research.skill          # 打包好的skill文件
└── skills/financial-research/        # 源文件目录
    ├── SKILL.md
    ├── README.md
    └── references/
        ├── mcp_tools.md
        ├── research_workflows.md
        └── planning_guide.md
```

## 安装

将 `financial-research.skill` 文件导入到你的Claude环境中即可使用。

---

生成时间: 2026-02-06
