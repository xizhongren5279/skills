# 公司一页纸检索策略详细配置

**文档版本**: v1.0
**创建时间**: 2026-02-06
**用途**: 保留所有版本的检索策略细节,包括query模板、recall_num、date_range等参数

---

## Section 1: 公司近况

### Query 1 - 公司近况综合
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 公司近况，公司近期发生的股价异动、财报披露，产品业务、战略调整等`
- **date_range**: `past_quarter`
- **recall_num**: `10`
- **doc_type**: 不指定（默认全部类型）

**检索目标**: 获取公司最近3个月的关键事件,包括股价变动、财报发布、产品业务、战略调整

---

## Section 2: 核心投资逻辑

### Query 1 - 股价异动事件
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 分析引起公司最近3个月内发生股价异动的新闻事件，尤其是概念炒作导致的股价异动`
- **date_range**: `past_quarter`
- **recall_num**: `8`
- **doc_type**: 不指定

**检索目标**: 识别导致股价波动的催化剂事件

### Query 2 - 短期投资逻辑
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 分析公司业务，整理短期投资逻辑(1-3月)，要从公司业务本身的价值出发来提炼3-5个要点`
- **date_range**: `past_quarter`
- **recall_num**: `12`
- **doc_type**: 不指定

**检索目标**: 提取未来1-3个月的投资驱动因素

### Query 3 - 长期投资逻辑
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 分析公司业务，梳理长期投资逻辑(1-3年)，要从公司业务本身的价值出发来提炼3-5个要点`
- **date_range**: `past_year`
- **recall_num**: `12`
- **doc_type**: 不指定

**检索目标**: 提取未来1-3年的核心竞争优势和增长驱动力

### Query 4 - 管理层业务指引
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 公司管理层业务指引，下个季度的业务指引、明年的业务指引`
- **date_range**: `past_half_year`
- **recall_num**: `8`
- **doc_type**: 不指定

**检索目标**: 获取管理层对未来业绩的前瞻性指引

### Query 5 - 核心风险
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 分析公司核心风险，提炼3-5个风险点`
- **date_range**: `past_half_year`
- **recall_num**: `5`
- **doc_type**: 不指定

**检索目标**: 识别主要下行风险因素

---

## Section 3: 未来事件与核心跟踪指标

### Query 1 - 未来1-3月催化事件
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 整理未来1-3月公司可能发生的财报发布与业绩指引、重大合同与订单、产品里程碑、并购与分拆、股票回购与分红政策、技术或专利突破、重大政策变动`
- **date_range**: `past_half_year`
- **recall_num**: `15`
- **doc_type**: `report`

**检索目标**: 识别近期（1-3月）可能影响股价的事件

### Query 2 - 未来3-6月催化事件
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 整理未来3-6月公司可能发生的财报发布与业绩指引、重大合同与订单、产品里程碑、并购与分拆、股票回购与分红政策、技术或专利突破、重大政策变动`
- **date_range**: `past_half_year`
- **recall_num**: `15`
- **doc_type**: `report`

**检索目标**: 识别中期（3-6月）可能影响股价的事件

### Query 3 - 核心跟踪指标
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 分析公司核心跟踪指标，短期(1-2季度)需盯住的财务或经营数据，长期(1-2年)需盯住的战略或行业指标`
- **date_range**: `past_year`
- **recall_num**: `12`
- **doc_type**: `report`

**检索目标**: 识别需要持续监控的关键指标

---

## Section 4: 业务拆分

### Query 1 - 公司盈利方式
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 分析公司盈利方式：梳理2-3个公司最核心的赚钱方式`
- **date_range**: `past_quarter`
- **recall_num**: `8`
- **doc_type**: `report`

**检索目标**: 理解公司的商业模式和盈利来源

### Query 2 - 市场格局
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 分析市场格局：用两句话描述（需要量化数据）其行业地位、市场份额，并点出2-3个最核心的竞争对手`
- **date_range**: `past_year`
- **recall_num**: `10`
- **doc_type**: `report`

**检索目标**: 了解公司在行业中的竞争地位

### Query 3 - 各板块业务情况
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 整理各板块业务情况`
- **date_range**: `past_quarter`
- **recall_num**: `8`
- **doc_type**: `report`

**检索目标**: 了解各业务板块的运营情况

### Query 4 - 最新财报各板块细分收入
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 最新财报各板块细分收入数据（可以是比例），给出同比变化，输出表格`
- **date_range**: `past_half_year`
- **recall_num**: `12`
- **doc_type**: `report`

**检索目标**: 获取具体的业务板块收入数据

---

## Section 5: 财务与估值快照

### Query 1 - 最新财报解读
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 最新财报的财务指标解读`
- **date_range**: `past_quarter`
- **recall_num**: `10`
- **doc_type**: `report`

**检索目标**: 获取最新财报的专业分析解读

### Query 2 - 历史与预测财务指标
- **工具**: `mcp__ashare-mcp-research__info_search_stock_db`
- **query模板**: `[Company Name] 整理公司近3年关键财务指标，给出未来3年的关键财务指标`
- **date_range**: 不适用（stock_db特定查询）
- **recall_num**: 不适用
- **doc_type**: 不适用

**检索目标**: 获取历史财务数据和机构预测数据

### Query 3 - 国内券商盈利预测
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 收集整理多家券商（国内券商，3-5家）对公司未来三年的盈利预测（收入、利润、目标价）`
- **date_range**: `past_half_year`
- **recall_num**: `15`
- **doc_type**: `report`

**检索目标**: 汇总国内券商的研报预测

### Query 4 - 国际投行盈利预测
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 收集整理多家券商（国外券商（华尔街的投行），3-5家）对公司未来三年的盈利预测（收入、利润、目标价）`
- **date_range**: `past_half_year`
- **recall_num**: `15`
- **doc_type**: `foreign_report`

**检索目标**: 汇总国际投行的研报预测

### Query 5 - 估值对比
- **工具**: `mcp__ashare-mcp-research__info_search_finance_db`
- **query模板**: `[Company Name] 进行可比公司估值测算与估值对比，PE、PB等估值指标均可`
- **date_range**: `past_year`
- **recall_num**: `10`
- **doc_type**: `report`

**检索目标**: 获取公司与同行的估值对比数据

### Query 6 - 估值对比（Web Fallback）
- **工具**: `mcp__ashare-mcp-research__info_search_web`
- **query模板**: `[Company Name] 及其可比公司（行业竞争对手）的最新估值对比，包括PE、PB等估值指标`
- **触发条件**: 当Query 5返回的可比公司数据不足时
- **date_range**: 不适用（web搜索）
- **recall_num**: 不适用
- **doc_type**: 不适用

**检索目标**: 通过网络搜索补充估值对比数据

---

## 参数说明

### date_range选项
- `past_day`: 近1天
- `past_week`: 近1周
- `past_month`: 近1个月
- `past_quarter`: 近1季度（3个月）
- `past_half_year`: 近半年（6个月）
- `past_year`: 近1年
- `all`: 全部时间

### doc_type选项
- `all`: 全部文档类型（默认）
- `report`: 研报
- `summary`: 会议纪要
- `company_all_announcement`: 公司公告
- `comments`: 点评
- `news`: 资讯
- `foreign_report`: 外资研报

### recall_num建议范围
- **关键section（如投资逻辑、财务估值）**: 10-15条
- **普通section**: 8-10条
- **风险分析等辅助信息**: 5-8条

---

## 版本历史

### v1.0 (初始版本)
- **架构**: Section内并行,Section间串行
- **总查询数**: 18个MCP queries
- **并行策略**:
  - Section 1: 1个query（无需并行）
  - Section 2: 5个queries并行
  - Section 3: 3个queries并行
  - Section 4: 4个queries并行
  - Section 5: 5个queries并行 + 1个web fallback
- **性能**: ~13分钟

### v2.0 (Section全并行)
- **架构**: 5个Section全并行检索,串行分析
- **总查询数**: 18个MCP queries (保持不变)
- **并行策略**: 5个subagents同时启动,每个subagent内部执行该section的所有queries
- **性能**: ~6.5分钟

### v3.0 (检索+分析全并行)
- **架构**: 5个Section并行检索+分析
- **总查询数**: 18个MCP queries (保持不变)
- **并行策略**: 5个subagents同时启动,每个subagent完成检索+分析后返回markdown
- **性能**: ~4.5分钟（实测1.3-1.4分钟）
- **关键创新**: 分析工作在subagent内部完成,主流程只负责整合

---

## 检索策略优化建议

### 1. recall_num调优
- 如果信息量不足,适当增加recall_num (如10→15)
- 如果检索时间过长,适当减少recall_num (如15→10)

### 2. date_range调优
- 短期事件(如财报、股价异动): 使用`past_quarter`
- 长期趋势(如战略分析、竞争格局): 使用`past_year`
- 机构预测: 使用`past_half_year`

### 3. doc_type优化
- 财务分析类: 优先使用`report`
- 国际投行数据: 使用`foreign_report`
- 综合信息: 使用默认(不指定doc_type)

### 4. Query优化原则
- **具体化**: 明确指定需要的信息维度
- **量化要求**: 在query中强调"量化数据"、"具体数字"
- **时间边界**: 在query中明确时间范围(如"未来1-3月")
- **格式要求**: 在query中指定输出格式(如"输出表格")

---

## 使用说明

1. **实施新公司检索时**: 直接使用本文档中的query模板,替换`[Company Name]`为实际公司名称
2. **调试检索效果**: 如果某section信息不足,参考"检索策略优化建议"调整参数
3. **版本迭代**: 如果修改检索策略,请在"版本历史"中记录变更
4. **参数记录**: 所有参数修改都应同步更新到对应section的配置中

---

**维护者**: Claude Code v3.0
**最后更新**: 2026-02-06
