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
        # 1. 檢索可用模型並選取
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        selected_model = next((m for m in available_models if 'flash' in m), available_models[0])
        
        # 2. 關鍵修正：加入 google_search_retrieval 工具 (1.5版) 
        # 或 google_search (2.0/3.0版)
        # 修改這一行即可
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash', 
            tools=[{"google_search_retrieval": {}}] # 這就是開啟「官方聯網」的鑰匙
        )
        
        # 3. 呼叫 AI 並生成內容
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

with tab2:
    if not symbol:
        st.info("👈 請先在左側欄位輸入美股代號（例如: AAPL）")
    else:
        st.header(f"個股分析：{symbol}")
        try:
            # 抓取 yfinance 數據
            stock_data = yf.Ticker(symbol)
            hist = stock_data.history(period="1mo")
            
            if hist.empty:
                st.warning(f"找不到代號 '{symbol}' 的數據，請檢查輸入是否正確。")
            else:
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.line_chart(hist['Close'])
                with col2:
                    current_price = hist['Close'].iloc[-1]
                    prev_price = hist['Close'].iloc[-2]
                    change = ((current_price - prev_price) / prev_price) * 100
                    st.metric("最新股價", f"${current_price:.2f}", f"{change:.2f}%")
                
                if st.button(f"生成 {symbol} AI 研究報告"):
                    with st.spinner(f"正在分析 {symbol} 相關資訊..."):
                        p = f"請針對美股 {symbol} 提供最新研究報告：包含近期新聞總結、法人未來展望與目標價。請用繁體中文。"
                        st.markdown(ask_gemini(p))
        except Exception as e:
            st.error(f"數據抓取錯誤: {e}")

with tab3:
    st.header("📈 強勢股掃描與展望")
    if st.button("掃描近五日強勢股原因"):
        with st.spinner("AI 正在掃描大數據..."):
            p = """請找出近期美股中表現強勁（漲幅大或討論度高）的股票。
            針對這些標的，總結其股價上漲的原因，並附上法人對其未來的看法。請用繁體中文表格呈現。"""
            st.markdown(ask_gemini(p))
