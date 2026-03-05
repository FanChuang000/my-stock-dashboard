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
        # 1. 嘗試使用最新且最穩定的型號全名
        model = genai.GenerativeModel('models/gemini-1.5-flash-8b') # 嘗試 8b 小型輕量版
        response = model.generate_content("請總結昨日美股盤後表現。")
        return response.text
    except Exception:
        try:
            # 2. 備援方案：嘗試不加 models/ 前綴
            model = genai.GenerativeModel('gemini-1.5-flash-001')
            response = model.generate_content("請總結昨日美股。")
            return response.text
        except Exception as e:
            return f"權限/環境衝突：請檢查 Google AI Studio 帳號狀態。詳細：{str(e)}"
if st.button("✨ 一鍵生成 AI 簡報"):
    with st.spinner("Gemini 正在分析大數據..."):
        try:
            summary = get_gemini_summary()
            st.markdown(summary)
        except Exception as e:
            st.error(f"分析失敗：{e}")

st.divider()
# 這裡繼續接你原本的 yfinance 圖表代碼...
