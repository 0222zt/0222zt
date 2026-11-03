# components/ui.py
import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        /* 全局背景 */
        .stApp { background-color: #f8f9fa; }
        [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e9ecef; box-shadow: 2px 0 10px rgba(0,0,0,0.02); }
        
        /* 🌟 修复：把顶栏背景变透明，不再使用 visibility: hidden */
        header { background-color: transparent !important; }
        
        /* 🌟 修复：彻底隐藏侧边栏的折叠按钮，防止手贱点没 */
        button[data-testid="baseButton-headerNoPadding"] { display: none !important; }

        /* KPI 卡片专属 CSS */
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #ffffff 0%, #f1f4f8 100%);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
            border-left: 5px solid #1f77b4;
            transition: all 0.3s ease;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(31, 119, 180, 0.15);
            border-left: 5px solid #ff7f0e;
        }
        div[data-testid="stMetricValue"] { font-size: 32px !important; font-weight: 800 !important; color: #212529; font-family: 'PingFang SC', sans-serif; }
        div[data-testid="stMetricLabel"] { font-size: 14px !important; color: #6c757d; font-weight: 600; }

        /* 生成按钮动效 */
        div.stButton > button:first-child {
            background: linear-gradient(90deg, #1f77b4 0%, #4CA1AF 100%);
            color: white; border-radius: 8px; font-weight: bold; border: none; padding: 12px 24px; width: 100%;
            transition: all 0.3s;
            box-shadow: 0 4px 10px rgba(31, 119, 180, 0.3);
        }
        div.stButton > button:first-child:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 15px rgba(31, 119, 180, 0.5);
        }
        
        /* 隐藏 Streamlit 底部杂项 */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def render_kpi_cards(df):
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    if len(num_cols) > 0:
        metric_cols = st.columns(min(len(num_cols), 4))
        icons = ["💰", "📈", "📊", "💵"]
        for i, col_name in enumerate(num_cols[:4]):
            with metric_cols[i]:
                short_name = col_name if len(col_name) <= 6 else col_name[:6] + ".."
                st.metric(label=f"{icons[i%4]} {short_name} 总计", value=f"{df[col_name].sum():,.2f}")