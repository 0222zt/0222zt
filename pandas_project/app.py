# app.py
import streamlit as st
import pandas as pd
from components.ui import inject_custom_css, render_kpi_cards
from services.ai_service import generate_chart_code, generate_insight_stream
from services.executor_service import run_plotly_code
from config import CHART_TYPES, DEFAULT_COLOR

# 1. 页面初始化配置
st.set_page_config(page_title="AI 商业数据洞察平台", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_custom_css()

st.title("📊 AI 商业数据洞察平台")
st.caption("上传业务数据，一键生成 11 种交互式商业图表与深度 AI 洞察报告")

# 2. 状态管理
if "chart_fig" not in st.session_state: 
    st.session_state.chart_fig = None
if "html_data" not in st.session_state: 
    st.session_state.html_data = None
if "error" not in st.session_state: 
    st.session_state.error = None
if "gen_btn" not in st.session_state: 
    st.session_state.gen_btn = False
if "ai_code" not in st.session_state: 
    st.session_state.ai_code = None

df = None

# ================= 左侧侧边栏 =================
with st.sidebar:
    st.markdown("### 📁 1. 数据接入")
    uploaded_file = st.file_uploader("支持 CSV / Excel", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                try:
                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding='gbk')
            else:
                df = pd.read_excel(uploaded_file)
            
            df.columns = df.columns.astype(str).str.strip()
            if not df.empty: 
                st.success(f"✅ 读取成功: {len(df)} 行数据")
            else: 
                st.error("⚠️ 数据为空，请检查文件。")
        except Exception as e:
            st.error(f"❌ 解析失败: {e}")

    st.markdown("---")
    st.markdown("### ⚙️ 2. 分析配置")
    chart_type = st.selectbox("图表类型", CHART_TYPES)
    theme_color = st.color_picker("主色调", DEFAULT_COLOR)
    custom_title = st.text_input("标题（可选）", "")
    user_input = st.text_area("业务诉求（AI 分析侧重）", "请分析数据趋势，并标出最高点与异常值。")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 一键生成分析报告"):
        st.session_state.gen_btn = True
        st.session_state.chart_fig = None
        st.session_state.html_data = None
        st.session_state.error = None
        st.session_state.ai_code = None

# ================= 右侧主区 =================
if df is not None:
    render_kpi_cards(df)
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    if st.session_state.gen_btn:
        if st.session_state.chart_fig is None and st.session_state.error is None:
            with st.spinner("🤖 AI 正在编写 Plotly 交互代码..."):
                ai_code, api_error = generate_chart_code(df.columns.tolist(), chart_type, theme_color, custom_title, user_input)
                
                if api_error:
                    st.session_state.error = api_error
                elif ai_code:
                    with st.spinner("🎨 正在渲染高清图表..."):
                        fig, html_data, exec_error = run_plotly_code(ai_code, df)
                        if exec_error:
                            st.session_state.error = exec_error
                            st.session_state.ai_code = ai_code
                        else:
                            st.session_state.chart_fig = fig
                            st.session_state.html_data = html_data
                            st.session_state.ai_code = ai_code

        if st.session_state.error:
            st.error(f"❌ 生成失败: {st.session_state.error}")
            if st.session_state.ai_code:
                with st.expander("🔍 查看 AI 生成的报错代码"):
                    st.code(st.session_state.ai_code, language='python')
        else:
            col_chart, col_table = st.columns([2.5, 1], gap="large")
            
            with col_chart:
                st.markdown(f"#### 🎨 {chart_type} 交互展示")
                st.plotly_chart(st.session_state.chart_fig, use_container_width=True)
                
                st.download_button(
                    label="📥 下载交互式图表 (HTML)",
                    data=st.session_state.html_data,
                    file_name="interactive_chart.html",
                    mime="text/html"
                )
            
            with col_table:
                st.markdown("#### 📄 数据明细")
                st.dataframe(df, use_container_width=True, height=480, hide_index=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown("### 💡 深度业务洞察 (AI 实时生成)")
                with st.spinner("✍️ 正在分析并撰写报告..."):
                    st.write_stream(generate_insight_stream(df.head(3).to_dict(), chart_type))
                    
    else:
        st.markdown("#### 📄 数据预览")
        st.dataframe(df, use_container_width=True, height=300, hide_index=True)
        st.info("👈 请在左侧配置参数，点击「一键生成分析报告」体验交互式图表")