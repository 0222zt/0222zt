# services/ai_service.py
import requests
import json
import sys
import os

# 动态添加根目录到 sys.path，防止跨文件夹引用报错
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import API_KEY, API_URL, MODEL_NAME
from utils.prompt_templates import get_chart_prompt, get_insight_prompt

def generate_chart_code(columns_list, chart_type, theme_color, custom_title, user_input):
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://localhost:8501", 
        "X-Title": "AI Data Agent"
    }
    
    system_prompt = get_chart_prompt(columns_list, chart_type, theme_color, custom_title)
    
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        "temperature": 0.1 # 降低随机性
    }
    
    try:
        res = requests.post(API_URL, headers=headers, json=data, timeout=60)
        if res.status_code == 200:
            return res.json()['choices'][0]['message']['content'], None
        else:
            return None, f"API报错 [{res.status_code}]：{res.text}"
    except Exception as e:
        return None, f"网络异常：{str(e)}"

def generate_insight_stream(df_sample, chart_type):
    headers = {
        "Content-Type": "application/json", 
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://localhost:8501",
        "X-Title": "AI Data Agent"
    }
    
    prompt = get_insight_prompt(df_sample, chart_type)
    data = {
        "model": MODEL_NAME, 
        "messages": [{"role": "user", "content": prompt}],
        "stream": True
    }
    
    try:
        res = requests.post(API_URL, headers=headers, json=data, stream=True, timeout=60)
        for line in res.iter_lines():
            if line:
                chunk = line.decode('utf-8')
                if chunk.startswith("data: ") and chunk != "data: [DONE]":
                    try:
                        json_data = json.loads(chunk[6:])
                        content = json_data['choices'][0]['delta'].get('content', '')
                        if content:
                            yield content
                    except:
                        pass
    except Exception as e:
        yield f"\n\n❌ 洞察生成中断：{str(e)}"