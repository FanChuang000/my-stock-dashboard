import streamlit as st
import yfinance as yf
import google.generativeai as genai

# 從 Secrets 讀取 API Key
gen_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=gen_key)

st.set_page_config(page_title="AI 財經儀表板", layout="wide")
st.title("🤖 Gemini AI 昨日美股盤後分析")

# 呼叫 Gemini 模型
def get_gemini_summary():
    # 嘗試使用正式版名稱，若不行則改用較穩定的版本
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest') 
        # 加上具體日期，讓 Gemini 知道你要的是「昨日」的精確資訊
        prompt = "你是一位資深美股策略師。請分析 2026 年 3 月 4 日（昨日）的美股盤後表現，包含標普 500 指數變動、關鍵經濟數據，以及三則影響市場的國際財經新聞。請用繁體中文以條列式呈現，語氣專業且精簡。"
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        # 備援方案：如果 latest 找不到，嘗試使用基礎名稱
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("請總結昨日全球財經大事與美股走勢。")
        return response.text
if st.button("✨ 一鍵生成 AI 簡報"):
    with st.spinner("Gemini 正在分析大數據..."):
        try:
            summary = get_gemini_summary()
            st.markdown(summary)
        except Exception as e:
            st.error(f"分析失敗：{e}")

st.divider()
# 這裡繼續接你原本的 yfinance 圖表代碼...
