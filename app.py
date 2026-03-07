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
        # 1. 取得所有支援生成內容的模型列表
        model_list = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # 2. 優先尋找名稱中有 'flash' 的模型，如果沒有就選第一個
        # 這樣可以自動避開 models/ 前綴不一致的問題
        target_model_name = next((m for m in model_list if 'flash' in m), model_list[0])
        
        # 3. 初始化模型並開啟聯網功能 (工具參數)
        model = genai.GenerativeModel(
            model_name=target_model_name,
            tools=[{"google_search_retrieval": {}}]
        )
        
        # 4. 呼叫 AI
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
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
