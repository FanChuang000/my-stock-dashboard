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
    # 嘗試幾種最可能的「完整路徑名稱」
    possible_models = [
        'gemini-1.5-flash',      # 標準名稱
        'models/gemini-1.5-flash', # 路徑名稱
        'gemini-pro'             # 舊版相容名稱
    ]
    
    error_log = []
    for model_name in possible_models:
        try:
            model = genai.GenerativeModel(model_name)
            # 測試簡單的生成
            response = model.generate_content("請總結昨日美股表現，用繁體中文。")
            return response.text
        except Exception as e:
            error_log.append(f"{model_name}: {str(e)}")
            continue
    
    return "所有模型均呼叫失敗。詳細報告：\n" + "\n".join(error_log)
if st.button("✨ 一鍵生成 AI 簡報"):
    with st.spinner("Gemini 正在分析大數據..."):
        try:
            summary = get_gemini_summary()
            st.markdown(summary)
        except Exception as e:
            st.error(f"分析失敗：{e}")

st.divider()
# 這裡繼續接你原本的 yfinance 圖表代碼...
