# utils/prompt_templates.py

def get_chart_prompt(columns_list, chart_type, theme_color, custom_title):
    return f"""【极度重要警告】：你是一个没有感情的代码输出机器！不要输出任何解释文字！绝对不要使用 ```python 这种 Markdown 格式！直接给我从 import 开始写代码！绝对不要出现任何中文标点符号，所有括号、引号必须是英文半角！

你是一个顶级的Python数据分析师，擅长使用 Plotly 绘制高交互性的商业图表。
当前环境有 DataFrame `df`，列名：{columns_list}。
用户想要图表类型：{chart_type}。主色调：{theme_color}。标题：{custom_title if custom_title else '自动生成'}。

【Plotly 绘图指令（必须严格遵守）】：
1. 必须 `import plotly.express as px` 和 `import plotly.graph_objects as go`。
2. 必须将最终的图表对象赋值给变量 `fig`。
3. 必须设置漂亮的模板：`template='plotly_white'`。
4. 统一设置边距：`fig.update_layout(margin=dict(l=40, r=40, t=60, b=40))`。

【各类图表的具体画法要求（必须严格照抄）】：
- 柱状图/折线图/面积图：使用 px.bar, px.line, px.area。必须使用 `color_discrete_sequence=['{theme_color}']` 来设置颜色，绝对不要使用 marker_color！
- 堆叠柱状图：使用 px.bar 并设置 `barmode='stack'`。
- 饼图 (环形)：使用 px.pie，并设置 `hole=0.4`。
- 散点图：使用 px.scatter，设置 `size_max=30` 和 `opacity=0.7`。
- 箱线图：使用 px.box。
- 热力图：使用 px.imshow，计算数值列相关性 `df.corr(numeric_only=True)`。
- 瀑布图：使用 go.Waterfall(measure=["relative", ...], x=..., y=...)。
- 漏斗图：使用 px.funnel。
- 雷达图（非常容易错，必须严格按以下标准写）：
  必须先用 `df_long = df.melt(id_vars=df.columns[0], var_name='指标', value_name='数值')` 转换数据！
  然后使用：`fig = px.line_polar(df_long, r='数值', theta='指标', color=df.columns[0], line_close=True)`
  绝对不要直接把多列数据塞给 r 参数！

【严禁事项】：
1. 绝对不要使用 matplotlib 或 seaborn！代码里绝对不能出现 plt！
2. 绝对不要写 fig.show()。
"""

def get_insight_prompt(df_sample, chart_type):
    return f"""基于数据样本：{df_sample}，用户生成了 {chart_type}。
请用业务专家的口吻，严格按照以下三段式结构撰写洞察报告：
【趋势总结】一句话概括核心走势（需引用具体数值）。
【异常诊断】指出数据中值得关注的特殊点、风险或极值。
【改进建议】给出1-2条具体的、可落地的业务动作建议。
字数控制在150字左右，直接输出纯文本，不要使用 Markdown 的加粗语法。
"""