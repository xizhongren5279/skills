# Research Workflows

This document provides detailed workflow templates for each type of financial research supported by this skill.

## Table of Contents

1. [Company Research](#company-research)
2. [Industry Research](#industry-research)
3. [Strategy Research](#strategy-research)
4. [Macro Research](#macro-research)
5. [Quantitative Analysis](#quantitative-analysis)
6. [Comparative Analysis](#comparative-analysis)

---

## Company Research

### Purpose
Deep-dive analysis of a specific company beyond one-page summaries.

### Typical Structure

```markdown
# [Company Name] 深度研究报告

## 1. 公司概况
- 基本信息 (成立时间、上市情况、总部、主要市场)
- 发展历程与重要里程碑
- 股权结构与管理团队

## 2. 业务分析
### 2.1 核心业务拆解
- 各业务板块描述
- 收入与利润贡献
- 业务协同效应

### 2.2 商业模式
- 盈利模式
- 价值链定位
- 核心竞争力

### 2.3 产品与服务
- 主要产品线
- 技术优势
- 创新能力

## 3. 行业地位与竞争
### 3.1 市场份额与排名
- 全球/区域市场地位
- 增长轨迹
- 与竞争对手对比

### 3.2 竞争优势与壁垒
- 技术壁垒
- 规模优势
- 品牌/渠道优势

### 3.3 主要竞争对手
- 竞争对手分析
- 竞争策略对比

## 4. 财务分析
### 4.1 历史财务表现
- 营收与利润趋势 (3-5年)
- 关键财务比率分析
- 现金流分析

### 4.2 盈利能力与质量
- ROE/ROIC分解
- 利润率趋势
- 盈利可持续性

### 4.3 财务健康度
- 资产负债结构
- 偿债能力
- 运营效率

## 5. 增长前景
### 5.1 增长驱动因素
- 行业增长
- 市占率提升
- 新业务/新市场

### 5.2 未来3年展望
- 业绩预测
- 关键假设
- 敏感性分析

## 6. 风险因素
- 行业风险
- 经营风险
- 财务风险
- 监管/政策风险

## 7. 估值分析
### 7.1 估值方法
- PE/PB估值
- DCF估值
- EV/EBITDA等

### 7.2 可比公司估值
- 同行业估值对比
- 估值合理性分析

### 7.3 投资建议
- 合理估值区间
- 投资评级
- 目标价

## 8. 附录
- 数据来源
- 重要图表
- 专业术语说明
```

### Key Data Requirements

**Qualitative data** (via `info_search_finance_db`):
- Company background and history
- Business model analysis
- Industry positioning
- Competitive landscape
- Management guidance
- Risk factors
- Analyst opinions

**Quantitative data** (via `info_search_stock_db`):
- Historical financials (3-5 years)
- Quarterly trends
- Key financial ratios (ROE, margins, leverage)
- Valuation multiples (PE, PB, EV/EBITDA)
- Stock performance

### Typical Retrieval Plan Structure

**Phase 1: Background & Business (Parallel)**
- Company overview and recent updates
- Business model and profit drivers
- Market position and competitors
- Product/technology analysis

**Phase 2: Financial Deep-Dive (Parallel)**
- Historical revenue/profit trends
- Key financial ratios (ROE, margins, etc.)
- Segment revenue breakdown
- Cash flow analysis

**Phase 3: Forward-Looking (Parallel)**
- Growth drivers and future outlook
- Management guidance
- Analyst forecasts
- Risk factors

**Phase 4: Valuation (May depend on Phase 2-3)**
- Comparable company valuations
- Valuation methods and models
- Target price synthesis

**Estimated queries**: 12-18 MCP calls
**Estimated time**: 3-5 minutes

### Common Pitfalls

❌ **Lack of quantitative data**: Include specific numbers, not just qualitative descriptions
❌ **Outdated information**: Pay attention to date_range, prioritize recent data
❌ **Insufficient competitor analysis**: Must include 2-3 key competitors with data
❌ **Weak financial analysis**: Go beyond surface metrics, analyze trends and drivers
❌ **Missing risk discussion**: Every investment case has risks - identify them explicitly

---

## Industry Research

### Purpose
Analyze industry structure, trends, competitive dynamics, and investment opportunities within a sector.

### Typical Structure

```markdown
# [Industry Name] 行业研究报告

## 1. 行业概述
### 1.1 行业定义与范围
- 产业链结构
- 细分市场划分
- 相关行业

### 1.2 行业规模与增长
- 市场规模 (历史与预测)
- 增长率趋势
- 全球/区域分布

## 2. 行业驱动因素
### 2.1 需求侧分析
- 下游需求变化
- 终端用户行为
- 消费/投资趋势

### 2.2 供给侧分析
- 产能变化
- 技术进步
- 成本结构演变

### 2.3 政策与监管
- 相关政策
- 监管环境
- 补贴与税收

## 3. 竞争格局
### 3.1 市场结构
- 集中度 (CR3/CR5/HHI)
- 竞争态势 (完全竞争/寡头/垄断)
- 进入壁垒

### 3.2 主要参与者
- Top 5-10企业
- 市场份额
- 竞争策略

### 3.3 价值链分析
- 上游议价能力
- 下游议价能力
- 价值分配

## 4. 行业趋势
### 4.1 技术趋势
- 技术革新方向
- 颠覆性技术
- 技术成熟度

### 4.2 商业模式演变
- 新兴商业模式
- 传统模式挑战
- 创新案例

### 4.3 整合与并购
- M&A趋势
- 行业整合逻辑
- 案例分析

## 5. 行业财务特征
### 5.1 盈利能力
- 行业平均利润率
- ROE/ROIC水平
- 盈利能力趋势

### 5.2 资本密集度
- 资本支出需求
- 折旧摊销水平
- 现金流特征

### 5.3 周期性特征
- 经济周期敏感度
- 季节性波动
- 库存周期

## 6. 投资机会与风险
### 6.1 投资主题
- 细分领域机会
- 产业链环节机会
- 技术路线选择

### 6.2 行业风险
- 周期性风险
- 政策风险
- 竞争加剧风险
- 技术替代风险

## 7. 投资标的推荐
- 推荐公司列表
- 推荐逻辑
- 风险提示

## 8. 附录
- 数据来源
- 行业图表
- 专业术语
```

### Key Data Requirements

**Industry-level data**:
- Market size and growth rates
- Supply-demand dynamics
- Industry concentration (CR3/CR5)
- Average profitability metrics
- Technology trends

**Company-level data**:
- Top players and market shares
- Comparative financial metrics
- Strategic positioning
- Recent developments

**Policy/macro data**:
- Relevant policies and regulations
- Subsidy programs
- Trade dynamics

### Typical Retrieval Plan Structure

**Phase 1: Industry Overview (Parallel)**
- Industry definition and market size
- Growth trends and forecasts
- Policy and regulatory environment
- Technology trends

**Phase 2: Competitive Landscape (Parallel)**
- Market structure and concentration
- Top 5-10 players analysis
- Competitive dynamics
- Entry barriers

**Phase 3: Company Deep-Dives (Parallel)**
- Detailed analysis of top 3-5 players
- Market share data
- Financial metrics comparison
- Strategic positioning

**Phase 4: Forward-Looking (Parallel)**
- Industry outlook
- Emerging opportunities
- Risk factors
- Investment themes

**Estimated queries**: 15-25 MCP calls
**Estimated time**: 4-6 minutes

### Common Pitfalls

❌ **Too company-focused**: Industry research should prioritize industry-level insights, not just company stories
❌ **Missing competitive dynamics**: Must explain WHY some companies win and others lose
❌ **Weak quantification**: Include market size, growth rates, market shares with numbers
❌ **No forward view**: Research must include industry outlook and trends, not just history
❌ **Incomplete value chain**: Analyze upstream and downstream, not just the core industry

---

## Strategy Research

### Purpose
Develop investment themes, strategies, or portfolio recommendations based on market analysis.

### Typical Structure

```markdown
# [Strategy Theme] 投资策略报告

## 1. 策略概述
- 核心投资主题
- 适用市场环境
- 预期收益与风险特征
- 投资期限

## 2. 宏观与市场环境
### 2.1 宏观背景
- 经济周期阶段
- 货币与财政政策
- 利率与流动性环境

### 2.2 市场特征
- 当前市场估值水平
- 市场情绪与风险偏好
- 资金流向

## 3. 投资逻辑
### 3.1 主题驱动因素
- 为什么这个主题现在重要?
- 关键催化剂
- 可持续性分析

### 3.2 历史回溯
- 类似投资主题的历史表现
- 成功/失败案例
- 经验教训

## 4. 行业与板块选择
### 4.1 受益行业/板块
- 直接受益行业
- 间接受益行业
- 受益逻辑与传导路径

### 4.2 行业对比
- 各行业投资价值排序
- 风险收益比较
- 配置建议权重

## 5. 标的筛选
### 5.1 选股标准
- 定量标准 (财务指标)
- 定性标准 (竞争力、管理等)
- 估值要求

### 5.2 推荐标的池
- 核心组合 (5-10只)
- 各标的投资亮点
- 建议仓位权重

### 5.3 标的对比
| 标的 | 投资亮点 | 风险点 | 估值 | 建议权重 |
|------|---------|-------|------|---------|
| ... | ... | ... | ... | ... |

## 6. 风险与对冲
### 6.1 主要风险
- 宏观风险
- 政策风险
- 行业风险
- 个股风险

### 6.2 风险监控指标
- 需要跟踪的领先指标
- 止损/减仓触发条件

### 6.3 对冲策略 (可选)
- 对冲工具
- 对冲比例

## 7. 实施建议
### 7.1 建仓策略
- 初始仓位
- 加仓条件
- 建仓节奏

### 7.2 持仓管理
- 再平衡策略
- 动态调整逻辑

### 7.3 退出策略
- 止盈目标
- 止损条件
- 退出信号

## 8. 总结
- 核心观点回顾
- 预期回报与风险
- 跟踪与更新计划
```

### Key Data Requirements

**Macro data**:
- Economic indicators
- Policy environment
- Market valuation levels
- Liquidity conditions

**Sector/industry data**:
- Sector performance trends
- Relative valuations
- Earnings growth forecasts
- Sector rotation signals

**Stock-level data**:
- Candidate stocks meeting criteria
- Financial metrics for comparison
- Valuation multiples
- Analyst recommendations

### Typical Retrieval Plan Structure

**Phase 1: Macro & Market Context (Parallel)**
- Macroeconomic environment analysis
- Market valuation and sentiment
- Policy environment
- Historical precedents for similar themes

**Phase 2: Sector Analysis (Parallel)**
- Beneficiary sectors identification
- Sector relative valuations
- Sector fundamentals and trends
- Cross-sector comparison

**Phase 3: Stock Selection (Parallel)**
- Top picks in each sector
- Financial metrics for screening
- Valuation analysis
- Analyst views on key stocks

**Phase 4: Risk & Implementation (Parallel)**
- Risk factors identification
- Risk monitoring indicators
- Portfolio construction guidance
- Entry/exit strategies

**Estimated queries**: 12-20 MCP calls
**Estimated time**: 3-5 minutes

### Common Pitfalls

❌ **Weak macro linkage**: Must clearly explain HOW macro environment supports the theme
❌ **No historical context**: Learn from similar past themes - what worked and what didn't
❌ **Too many stocks**: Focus on 5-10 highest-conviction names, not a long list
❌ **Missing risk framework**: Must include risk monitoring and exit strategies
❌ **Static view**: Strategy should include dynamic adjustment rules

---

## Macro Research

### Purpose
Analyze macroeconomic trends, policies, and their implications for financial markets.

### Typical Structure

```markdown
# [Macro Topic] 宏观研究报告

## 1. 研究概述
- 核心议题
- 研究范围 (全球/区域/国家)
- 研究期限

## 2. 经济现状
### 2.1 增长
- GDP增长率
- 增长动力分解 (消费/投资/出口)
- 产出缺口

### 2.2 通胀
- CPI/PPI水平与趋势
- 核心通胀
- 通胀预期

### 2.3 就业
- 失业率
- 劳动力参与率
- 工资增长

### 2.4 外部平衡
- 经常账户
- 资本流动
- 汇率

## 3. 政策分析
### 3.1 货币政策
- 利率水平与路径
- 央行资产负债表
- 流动性环境
- 政策立场 (鸽派/鹰派)

### 3.2 财政政策
- 财政赤字/盈余
- 政府债务水平
- 财政刺激/紧缩措施

### 3.3 其他相关政策
- 产业政策
- 监管政策
- 贸易政策

## 4. 经济展望
### 4.1 基准情景
- GDP增长预测
- 通胀预测
- 政策路径预期

### 4.2 风险情景
- 上行风险
- 下行风险
- 尾部风险

### 4.3 关键假设与前提
- 主要假设列表
- 敏感性分析

## 5. 市场影响
### 5.1 对股市的影响
- 盈利影响
- 估值影响
- 板块影响

### 5.2 对债市的影响
- 收益率曲线
- 信用利差
- 久期策略

### 5.3 对汇率/商品的影响
- 汇率走势
- 大宗商品价格
- 黄金等避险资产

## 6. 投资建议
### 6.1 大类资产配置
- 股债比例
- 区域配置
- 风格配置

### 6.2 行业配置
- 受益行业
- 受损行业

### 6.3 风险对冲
- 对冲工具
- 风险管理

## 7. 关键跟踪指标
- 需要持续监控的经济指标
- 政策信号
- 市场指标

## 8. 附录
- 经济数据图表
- 政策文本摘要
- 术语解释
```

### Key Data Requirements

**Economic indicators**:
- GDP, CPI, PPI, unemployment
- PMI, retail sales, industrial production
- Trade balance, FDI

**Policy data**:
- Interest rate decisions and guidance
- Fiscal measures
- Regulatory changes

**Market data**:
- Yield curves
- Credit spreads
- Currency exchange rates
- Commodity prices

### Typical Retrieval Plan Structure

**Phase 1: Economic Data Collection (Parallel)**
- GDP and growth components
- Inflation indicators
- Employment data
- External balance

**Phase 2: Policy Analysis (Parallel)**
- Monetary policy stance and outlook
- Fiscal policy measures
- Other relevant policies
- Policy impact analysis

**Phase 3: Market Implications (Parallel)**
- Equity market implications
- Bond market implications
- Currency and commodity implications
- Sector rotation implications

**Phase 4: Outlook & Strategy (May depend on Phase 1-3)**
- Economic forecasts
- Risk scenarios
- Asset allocation recommendations
- Tracking indicators

**Estimated queries**: 10-18 MCP calls
**Estimated time**: 3-5 minutes

### Common Pitfalls

❌ **Data dump without insight**: Don't just list economic data - explain what it means
❌ **Weak linkage to markets**: Must clearly connect macro analysis to investment implications
❌ **No forward view**: Macro research must include forecasts and scenarios
❌ **Ignoring policy**: Policy analysis is as important as economic data
❌ **Missing cross-asset view**: Consider implications across stocks, bonds, FX, commodities

---

## Quantitative Analysis

### Purpose
Data-driven financial analysis, metric comparisons, and quantitative modeling.

### Typical Structure

```markdown
# [Analysis Topic] 量化分析报告

## 1. 分析目标
- 研究问题
- 分析方法
- 数据范围

## 2. 数据与方法
### 2.1 数据来源
- 数据库
- 时间范围
- 样本选择

### 2.2 分析方法
- 统计方法
- 模型说明
- 假设条件

## 3. 描述性统计
- 样本统计特征
- 数据分布
- 异常值处理

## 4. 核心分析
### 4.1 [分析维度1]
- 具体指标计算
- 横向对比 (cross-sectional)
- 纵向对比 (time-series)
- 可视化图表

### 4.2 [分析维度2]
- ...

### 4.3 [分析维度3]
- ...

## 5. 关键发现
- Finding 1: [具体发现 + 支撑数据]
- Finding 2: ...
- Finding 3: ...

## 6. 投资启示
- 对投资决策的指导意义
- 可操作的建议
- 局限性说明

## 7. 附录
- 详细数据表格
- 技术说明
- 公式推导
```

### Common Quantitative Analysis Types

**1. Valuation Analysis**
- Compare valuation multiples (PE, PB, PS, EV/EBITDA) across companies
- Historical valuation ranges and mean reversion
- Valuation vs growth (PEG analysis)
- Sector relative valuations

**2. Financial Performance Analysis**
- Profitability metrics comparison (ROE, ROIC, margins)
- Growth metrics comparison (revenue CAGR, earnings growth)
- Efficiency metrics (asset turnover, working capital)
- DuPont analysis

**3. Risk Analysis**
- Volatility and beta analysis
- Downside risk metrics
- Credit risk indicators
- Leverage analysis

**4. Factor Analysis**
- Value factor exposure
- Growth factor exposure
- Quality factor exposure
- Momentum signals

**5. Correlation & Portfolio Analysis**
- Stock correlation matrices
- Portfolio diversification analysis
- Risk-adjusted returns (Sharpe ratio, etc.)
- Attribution analysis

### Key Data Requirements

**Stock-level quantitative data** (via `info_search_stock_db`):
- Historical financials (revenue, profit, margins, ROE, etc.)
- Valuation multiples (PE, PB, PS, etc.)
- Market data (prices, returns, volatility)
- Balance sheet metrics

**NOTE**: Each metric requires a separate query to `info_search_stock_db`

### Typical Retrieval Plan Structure

**Phase 1: Collect Core Metrics (Parallel)**
- Metric 1 for all companies
- Metric 2 for all companies
- Metric 3 for all companies
- ...
- Metric N for all companies

**Phase 2: Calculate Derived Metrics & Analyze**
- Compute ratios and derived metrics
- Perform statistical analysis
- Generate comparison tables
- Create visualizations

**Important**: For comparing multiple metrics across multiple companies, retrieve each metric in a separate parallel query.

**Estimated queries**: Highly variable (N_metrics × 1 for single company, N_metrics for multi-company comparison)
**Estimated time**: 1-4 minutes depending on scope

### Common Pitfalls

❌ **Insufficient sample size**: Need enough data points for statistical significance
❌ **Ignoring outliers**: Must identify and explain outliers, not just exclude them
❌ **Missing context**: Quantitative findings must be interpreted with qualitative context
❌ **Overfitting**: Be cautious about overly complex models with limited data
❌ **No robustness check**: Test sensitivity of findings to assumptions

---

## Comparative Analysis

### Purpose
Side-by-side comparison of 2-5 companies, typically within the same industry.

### Typical Structure

```markdown
# [Company A] vs [Company B] vs [Company C] 对比分析

## 1. 公司概览对比
| 项目 | Company A | Company B | Company C |
|------|-----------|-----------|-----------|
| 成立时间 | ... | ... | ... |
| 上市时间 | ... | ... | ... |
| 总部 | ... | ... | ... |
| 主营业务 | ... | ... | ... |
| 市值 | ... | ... | ... |

## 2. 业务对比
### 2.1 业务范围
- Company A: [描述]
- Company B: [描述]
- Company C: [描述]

### 2.2 商业模式差异
| 维度 | Company A | Company B | Company C |
|------|-----------|-----------|-----------|
| 盈利模式 | ... | ... | ... |
| 目标客户 | ... | ... | ... |
| 渠道策略 | ... | ... | ... |

### 2.3 产品/服务对比
- 产品线广度与深度
- 技术路线差异
- 创新能力对比

## 3. 竞争地位对比
### 3.1 市场份额
- 全球市场份额排名
- 区域市场对比
- 份额趋势

### 3.2 竞争优势
- Company A优势: ...
- Company B优势: ...
- Company C优势: ...

## 4. 财务对比
### 4.1 规模与增长
| 指标 | Company A | Company B | Company C |
|------|-----------|-----------|-----------|
| 2024营收 | ... | ... | ... |
| 营收3年CAGR | ... | ... | ... |
| 2024净利润 | ... | ... | ... |
| 净利润3年CAGR | ... | ... | ... |

### 4.2 盈利能力
| 指标 | Company A | Company B | Company C |
|------|-----------|-----------|-----------|
| 毛利率 | ... | ... | ... |
| 净利率 | ... | ... | ... |
| ROE | ... | ... | ... |
| ROIC | ... | ... | ... |

### 4.3 财务质量
| 指标 | Company A | Company B | Company C |
|------|-----------|-----------|-----------|
| 资产负债率 | ... | ... | ... |
| 流动比率 | ... | ... | ... |
| 经营现金流/营收 | ... | ... | ... |

## 5. 估值对比
| 指标 | Company A | Company B | Company C |
|------|-----------|-----------|-----------|
| PE (TTM) | ... | ... | ... |
| PB | ... | ... | ... |
| PS | ... | ... | ... |
| EV/EBITDA | ... | ... | ... |

### 5.1 估值合理性分析
- 估值差异原因
- 估值吸引力排序

## 6. 增长前景对比
### 6.1 增长驱动因素
- Company A: [核心驱动力]
- Company B: [核心驱动力]
- Company C: [核心驱动力]

### 6.2 未来3年预测对比
| 指标 | Company A | Company B | Company C |
|------|-----------|-----------|-----------|
| 2025E营收 | ... | ... | ... |
| 2026E营收 | ... | ... | ... |
| 2027E营收 | ... | ... | ... |

## 7. 风险对比
- Company A主要风险: ...
- Company B主要风险: ...
- Company C主要风险: ...

## 8. 投资建议
### 8.1 各公司投资亮点
- Company A: ...
- Company B: ...
- Company C: ...

### 8.2 投资排序与理由
1. [Company X]: [理由]
2. [Company Y]: [理由]
3. [Company Z]: [理由]

## 9. 总结
- 核心结论
- 最优选择及理由
```

### Key Data Requirements

**For each company**:
- Business overview and model
- Market position and competitive advantages
- Historical and forecast financials
- Valuation multiples
- Growth drivers and risks

**Cross-company comparisons**:
- Side-by-side metric tables
- Relative strengths/weaknesses
- Differentiation factors

### Typical Retrieval Plan Structure

**Phase 1: Company Profiles (Parallel by Company)**
- Company A overview, business, competitive position
- Company B overview, business, competitive position
- Company C overview, business, competitive position

**Phase 2: Financial Comparison (Parallel by Metric)**
- Revenue and growth for A, B, C
- Profitability metrics for A, B, C
- Balance sheet metrics for A, B, C
- Valuation multiples for A, B, C

**Phase 3: Forward-Looking (Parallel)**
- Growth drivers for A, B, C
- Analyst forecasts for A, B, C
- Risk factors for A, B, C

**Phase 4: Synthesis**
- Cross-company insights
- Investment ranking
- Recommendations

**Estimated queries**: 15-25 MCP calls (scales with number of companies)
**Estimated time**: 3-5 minutes

### Common Pitfalls

❌ **Unbalanced coverage**: Give equal depth to each company, avoid bias
❌ **Missing "why" analysis**: Don't just show differences - explain WHY they exist
❌ **No clear recommendation**: Comparative analysis should lead to actionable conclusions
❌ **Apples-to-oranges comparison**: Ensure companies are truly comparable
❌ **Snapshot vs trend**: Compare trends over time, not just current snapshots

---

## General Best Practices Across All Research Types

### 1. Structure and Clarity
- Use consistent section numbering
- Lead with executive summary for long reports
- Use tables for quantitative comparisons
- Include visualizations where helpful (describe in text)

### 2. Data Quality
- Always cite data sources and dates
- Note data limitations explicitly
- Use consistent time periods for comparisons
- Handle missing data transparently (use "-")

### 3. Quantitative Rigor
- Include specific numbers, not vague descriptions
- Show calculations and assumptions
- Provide context (vs history, vs peers, vs expectations)
- Use year-over-year or sequential comparisons

### 4. Balanced Perspective
- Present both bullish and bearish views
- Acknowledge uncertainties
- Discuss risks explicitly
- Consider alternative scenarios

### 5. Actionability
- Translate analysis into investment implications
- Provide specific recommendations when appropriate
- Include risk management guidance
- Define tracking metrics for ongoing monitoring

### 6. Language and Tone
- Use professional, objective language
- Avoid hype or excessive pessimism
- Define technical terms
- Maintain consistency (Chinese/English, terminology)

### 7. Quality Checks
- No placeholder text ([Company Name], etc.)
- All tables complete with data (or marked with "-")
- Logical flow from section to section
- Conclusions supported by analysis
- Proper formatting (markdown)

---

## Adapting Workflows

These templates are **starting points**, not rigid requirements. Adapt based on:

- **User requirements**: What specific questions need answering?
- **Data availability**: What can the MCP tools actually retrieve?
- **Time constraints**: Can simplify for quick analysis
- **Output format**: User may request specific structure
- **Research focus**: Emphasize most relevant sections

**Guiding principle**: Deliver the most valuable insights efficiently, not just fill a template.
