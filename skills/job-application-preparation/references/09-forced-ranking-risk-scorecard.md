# 强制分布 / 末位淘汰文化风险评分卡
### Forced Ranking / Stack Ranking Culture Risk Scorecard

> 用途:在评估目标公司时,自动检测"强制分布考核"文化风险,并输出风险分数,作为岗位筛选/优先级排序的输入维度之一。
>
> 来源: 内部评估框架, 2026-07-12. 整合至 job-evaluation 框架的 Scorecard 体系中,作为独立维度(权重 15%)。

---

## 评分逻辑

总分 100 分,分数越高 = 风险越高(越可能存在强制分布/末位淘汰文化)。
四大类信号,每类都有独立权重。

| 类别 | 权重上限 | 核心问题 |
|---|---|---|
| A. 领导层背景 | 30 | 决策者是谁,背景是什么 |
| B. 资本结构与市场压力 | 25 | 谁在背后施压,压力有多大 |
| C. 已观察到的行为证据 | 35 | 是否已经有实锤(评论/新闻) |
| D. 保护性信号(反向扣分) | -20 | 是否有稳定性证据 |

---

## A类:领导层背景信号(满分30)

| 信号 | 分值 | 检测方法 |
|---|---|---|
| CEO/CPO/CTO 在过去1-3年内更换,新任高管主要职业背景在 Google/Amazon/Meta/Microsoft/硅谷创业公司 | +12 | LinkedIn/公司官网高管简介 + 新闻搜索"[公司] new CEO" |
| 新高管上任后6个月内发生 >10% 规模裁员 | +10 | 新闻搜索"[公司] layoffs [年份]" |
| 高管薪酬报告/年报中明确写"benchmark against Silicon Valley / US peers" | +8 | 年报(ASX/NASDAQ公告)或财经媒体报道 |

## B类:资本结构与市场压力信号(满分25)

| 信号 | 分值 | 检测方法 |
|---|---|---|
| 主要机构投资者以美元VC/PE为主(Sequoia, Blackbird, General Atlantic, T. Rowe Price等),即便未上市 | +6 | 公司融资历史(Crunchbase/新闻) |
| 正在筹备/已完成美股(NASDAQ/NYSE)上市,而非本地交易所 | +6 | IPO相关新闻 |
| 已上市公司近12个月股价较高点下跌 >30% | +8 | 股价新闻/财经数据 |
| 官方沟通中出现"AI moment / AI transition / redefine how work gets done"式话术,用于解释组织调整 | +5 | 公司博客/CEO对外声明关键词搜索 |

## C类:已观察到的行为证据(满分35,权重最高)

| 信号 | 分值 | 检测方法 |
|---|---|---|
| Glassdoor/Blind 近12个月评论中出现"stack ranking" / "forced distribution" / "bell curve" / "rank and yank" 等词 | +15 | Glassdoor/Blind 评论关键词抓取 |
| 评论中出现明确的多档位评级体系(4档以上)+ 配额/quota 描述 | +10 | 搜索"[公司名] performance rating buckets" |
| 近12个月内发生 >10% 规模裁员,且非行业性大规模衰退导致 | +6 | 新闻搜索 |
| 评论中出现"reorg every 3-6 months"或类似高频组织调整描述 | +4 | Glassdoor/Blind |

## D类:保护性信号(反向扣分,最多 -20)

| 信号 | 分值 | 检测方法 |
|---|---|---|
| 高管团队稳定,CEO任期 >5年且无重大更换 | -6 | LinkedIn/公司历史 |
| 公司仍在净增长headcount(非裁员状态) | -5 | 招聘页面/新闻 |
| 有公开、近期(非十年前)反对强制曲线的官方声明 | -5 | 公司博客搜索 |
| 工程师主导型文化,对外内容以技术/产品为主而非"high performance culture"话术 | -4 | 公司工程博客基调分析 |

## 风险分级

| 总分 | 风险等级 | 建议 |
|---|---|---|
| 0–20 | 低风险 | 正常评估其他维度 |
| 21–45 | 中低风险 | 面试中主动询问绩效考核机制 |
| 46–70 | 中高风险 | 需评估自身"稳定进前20%"的把握 |
| 71–100 | 高风险 | 除非有极强的差异化竞争力支撑,否则建议降低优先级 |

## Agent 输出格式

```json
{
 "company": "string",
 "risk_score": 0,
 "risk_level": "low | medium_low | medium_high | high",
 "signals_detected": {
   "leadership": [],
   "capital_pressure": [],
   "behavioral_evidence": [],
   "protective_factors": []
 },
 "recommendation": "string",
 "confidence": "low | medium | high",
 "data_sources_checked": ["glassdoor", "blind", "news", "linkedin"],
 "last_updated": "YYYY-MM-DD"
}
```

## 使用建议

- C类证据是核心,权重最高、可信度也最高
- 对于私有公司,不要因为"未上市"就默认B类不适用
- 每次评分附带 `confidence` 字段
- 建议作为现有CV/岗位匹配打分体系里的一个独立维度(权重15%),不是一票否决项
