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
    # 嘗試清單中的模型名稱，直到一個成功為止
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    
    for name in model_names:
        try:
            model = genai.GenerativeModel(name)
            # 加上當前日期引導，讓 AI 更有方向感
            prompt = "今天是 2026 年 3 月 5 日。請分析 2026 年 3 月 4 日（昨日）的美股盤後表現與三大國際財經要聞，用繁體中文條列式回答。"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # 如果這個模型不行，就試下一個
            continue
            
    return "抱歉，目前無法連線至 Gemini 模型，請檢查 API Key 權限或稍後再試。"
if st.button("✨ 一鍵生成 AI 簡報"):
    with st.spinner("Gemini 正在分析大數據..."):
        try:
            summary = get_gemini_summary()
            st.markdown(summary)
        except Exception as e:
            st.error(f"分析失敗：{e}")

st.divider()
# 這裡繼續接你原本的 yfinance 圖表代碼...
