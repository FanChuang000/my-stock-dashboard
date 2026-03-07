import streamlit as st
import yfinance as yf
import google.generativeai as genai
import datetime
import pandas as pd

# 1. 基礎配置
st.set_page_config(page_title="AI 投資研究儀表板", layout="wide")

# 檢查 Secrets 是否存在 (避免部署時報錯)
if "GEMINI_API_KEY" not in st.secrets:
    st.error("請在 Streamlit Secrets 中設定 GEMINI_API_KEY")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 側邊欄設定
st.sidebar.title("🛠️ 控制面板")
target_date = st.sidebar.date_input("1. 選擇分析日期", datetime.date.today() - datetime.timedelta(days=1))

st.sidebar.divider()
st.sidebar.subheader("2. 個股深度分析")
symbol = st.sidebar.text_input("輸入美股代號 (如: NVDA)", "").upper().strip()

# 3. 定義 AI 函數 (加入智慧模型選取)
def ask_gemini(prompt):
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        
        # 修正後的寫法：使用最新的 google_search 標籤
        model = genai.GenerativeModel(
            model_name=target_model_name,
            tools=[{"google_search": {}}]  # <--- 這裡改掉了
        )
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        # 如果新版不行，就回退到舊版嘗試（雙重保險）
        try:
            model = genai.GenerativeModel(model_name=target_model_name, tools=[{"google_search_retrieval": {}}])
            response = model.generate_content(prompt)
            return response.text
        except:
            return f"❌ AI 呼叫失敗: {str(e)}"
# 4. 主介面
st.title("🤖 AI 全方位美股研究站")

tab1, tab2, tab3 = st.tabs(["📊 昨日市況分析", "🔍 個股研究專區", "🔥 市場焦點"])

with tab1:
    st.subheader(f"📅 查詢日期：{target_date}")
    if st.button("生成市況摘要"):
        with st.spinner("AI 正在翻閱歷史新聞..."):
            prompt = f"你是資深分析師。請分析 {target_date} 當日美股大盤走勢、主要指數漲跌幅度，並列出三件重要的國際財經要聞。請用繁體中文回答。"
            result = ask_gemini(prompt)
            st.markdown(result)
