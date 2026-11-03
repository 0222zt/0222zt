# AI 商业数据洞察平台 (AI Data Agent)

一个基于大语言模型（LLM）与 Plotly 构建的自动化商业数据分析与交互式可视化 Web 应用。

##  项目简介
本项目旨在解决非技术用户在数据处理与汇报时“画图难、写分析结论更烦”的痛点。用户只需上传 CSV/Excel 业务数据，系统即可通过 AI 自动生成包含 11 种高阶商业图表的交互式报表，并附赠深度商业洞察报告。

##  核心功能
- 全能数据接入：支持上传 CSV / Excel，自动处理编码与表头格式。
- 11 种商业图表生成：支持柱状图、折线图、面积图、堆叠柱状图、环形图、散点图、箱线图、热力图、瀑布图、漏斗图、雷达图。
- 高交互式渲染：底层采用 Plotly 引擎，图表支持悬停查看数据，并支持一键下载为可交互 HTML 文件。
- AI 深度业务洞察：接入 LLM，采用流式输出（打字机效果），严格按照“趋势总结-异常诊断-改进建议”的三段式结构生成商业分析报告。
- 商业级 UI/UX：基于 Streamlit 定制 CSS，包含 KPI 数据指标卡、微动效，并引入状态管理防止页面重绘导致的图表丢失。

## 技术架构
- 前端交互：Streamlit + 自定义 CSS
- 数据可视化：Plotly Express / Graph Objects
- 大模型引擎：OpenRouter API (Free Tier)
- 架构设计：采用 MVC 分层设计
  - app.py：视图层（UI 渲染与状态调度）
  - services/ai_service.py：服务层（LLM 通信与流式处理）
  - services/executor_service.py：执行层（AI 代码的沙盒清洗与安全执行）
  - components/ui.py：组件层（高定 CSS 与 KPI 卡片）
  - config.py / utils/：配置与提示词管理

## 注意事项 & 故障排查
由于本项目为保证零成本运行，接入了 OpenRouter 的公共免费模型池，免费 API 存在以下客观限制：
1. 模型下架：免费模型随时可能下线。如遇到，请修改 config.py 中的 MODEL_NAME 为其他免费模型。
2. 并发限流：免费池排队人数较多，偶尔会返回错误或生成超时。
3. 应对策略：如果遇到报错，请不要慌张，稍等几秒钟，重新点击“一键生成分析报告”多试几次即可。系统已内置完善的异常捕获机制，不会导致页面崩溃。

##  本地运行
1. 克隆仓库并安装依赖：pip install -r requirements.txt
2. 在 config.py 中填入你的 API_KEY
3. 运行应用：streamlit run app.py

---
Developed by [蒋虹宇] | 2026