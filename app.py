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
    try:
        # 強制指定目前最穩定的 flash 版本
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
        
        prompt = "今天是 2026 年 3 月 5 日。請分析 2026 年 3 月 4 日（昨日）的美股盤後表現、主要指數漲跌幅度，以及三則最重要的國際財經要聞。請用繁體中文回答。"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 顯示具體的錯誤代碼，幫助我們診斷是「權限不足」還是「名稱錯誤」
        return f"診斷訊息：{str(e)}"
if st.button("✨ 一鍵生成 AI 簡報"):
    with st.spinner("Gemini 正在分析大數據..."):
        try:
            summary = get_gemini_summary()
            st.markdown(summary)
        except Exception as e:
            st.error(f"分析失敗：{e}")

st.divider()
# 這裡繼續接你原本的 yfinance 圖表代碼...
