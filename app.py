import streamlit as st
import yfinance as yf
import google.generativeai as genai
import datetime
import pandas as pd

# 配置與初始化
st.set_page_config(page_title="AI 全方位美股研究站", layout="wide")
gen_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=gen_key)

# --- 功能 1: 自訂日期區塊 ---
st.title("🚀 AI 投資研究儀表板")
target_date = st.sidebar.date_input("1. 選擇分析日期", datetime.date.today() - datetime.timedelta(days=1))

# --- 功能 2: 個股深入查詢 ---
st.sidebar.divider()
st.sidebar.subheader("2. 個股深度分析")
symbol = st.sidebar.text_input("輸入美股代號 (如: NVDA)", "").upper()

# --- 定義 AI 函數 ---
def ask_gemini(prompt):
    model = genai.GenerativeModel('gemini-1.5-flash') # 或你之前測試成功的名稱
    response = model.generate_content(prompt)
    return response.text

# --- 頁面主體：市場焦點與自動化報表 ---
tab1, tab2, tab3 = st.tabs(["昨日市況分析", "個股研究專區", "市場焦點 (強勢股)"])

with tab1:
    if st.button("生成指定日期分析"):
        prompt = f"請分析 {target_date} 當日美股大盤走勢與重要財經新聞，請用繁體中文條列摘要。"
        st.info(ask_gemini(prompt))

with tab2:
    if symbol:
        st.header(f"🔍 個股分析：{symbol}")
        # 抓取數據
        stock = yf.Ticker(symbol)
        df = stock.history(period="1mo")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.line_chart(df['Close'])
        with col2:
            latest_price = df['Close'].iloc[-1]
            st.metric(f"{symbol} 最新股價", f"${latest_price:.2f}")
            st.write("技術簡評：近一個月走勢如上圖。")
            
        # AI 針對個股的新聞統整
        if st.button(f"生成 {symbol} AI 研究報告"):
            with st.spinner("正在蒐集個股新聞與法人評價..."):
                stock_prompt = f"請針對美股代號 {symbol}，統整近期的重要新聞、法人展望及目標價。請用繁體中文回答。"
                st.markdown(ask_gemini(stock_prompt))

with tab3:
    st.header("🔥 市場強勢股掃描")
    if st.button("掃描近五日強勢股原因"):
        with st.spinner("正在掃描市場強勢標的..."):
            # 這裡我們利用 AI 的搜尋能力來找強勢股（省去爬蟲大量數據的開發）
            scanner_prompt = """
            請幫我找出在最近 5 個交易日內，美股市場中表現最「強勢」的幾支股票（漲幅顯著或新聞熱度高）。
            並針對這些股票：
            1. 總結股價強勁的原因。
            2. 提供法人的未來展望。
            請用繁體中文以表格或條列式整理。
            """
            st.markdown(ask_gemini(scanner_prompt))
