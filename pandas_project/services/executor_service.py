# services/executor_service.py
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import re

def run_plotly_code(ai_code, df):
    if not ai_code:
        return None, None, "AI未能返回任何代码。"
        
    # 1. 提取 ```python 里面的内容
    code_matches = re.findall(r'```(?:python)?\n(.*?)```', ai_code, re.DOTALL)
    if code_matches:
        ai_code = max(code_matches, key=len)
    else:
        ai_code = ai_code.replace("```python", "").replace("```", "").strip()
    
    # 2. 找到 import 的位置，把前面的废话全砍掉
    import_idx = ai_code.find("import ")
    if import_idx != -1:
        ai_code = ai_code[import_idx:]
    
    # 3. 暴力替换中文标点（防止 AI 写出中文括号导致报错）
    ai_code = ai_code.replace("，", ",").replace("：", ":").replace("（", "(").replace("）", ")")
    ai_code = ai_code.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    
    ai_code = ai_code.replace("fig.show()", "pass")
    
    if "import matplotlib" in ai_code or "import seaborn" in ai_code:
        return None, None, "AI 错误地使用了不支持的画图库，请重新生成。"

    global_env = {
        "df": df, 
        "pd": pd, 
        "np": np,
        "px": px, 
        "go": go
    }
    
    if df is None or df.empty:
        return None, None, "数据表为空，无法画图。"

    try:
        exec(ai_code, global_env)
        
        if 'fig' not in global_env:
            return None, None, "AI 代码执行成功，但未能生成 'fig' 图表对象。"

        fig = global_env['fig']
        fig.update_layout(modebar_remove=['zoom', 'pan', 'select', 'lasso2d', 'zoomIn', 'zoomOut'])
        
        html_buffer = io.StringIO()
        fig.write_html(html_buffer, include_plotlyjs='cdn')
        html_data = html_buffer.getvalue()
        
        return fig, html_data, None 
        
    except Exception as e:
        return None, None, f"代码执行错误：{str(e)}\n\n===清洗后的代码===\n{ai_code}"