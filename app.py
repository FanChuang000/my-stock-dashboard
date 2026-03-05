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
        # 1. 先列出所有你的 API Key 可以使用的模型
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 2. 優先尋找最新的 Gemini 3 或 2.5 版本
        # 如果找不到，就從清單中隨便抓一個包含 'gemini' 字眼的
        selected_model = next((m for m in available_models if 'gemini-3' in m), 
                         next((m for m in available_models if '2.5' in m), 
                         available_models[0]))
        
        st.write(f"🔍 自動選用模型：{selected_model}") # 讓你知道它選了誰
        
        model = genai.GenerativeModel(selected_model)
        prompt = "今天是 2026 年 3 月 5 日。請總結昨日（3 月 4 日）美股盤後表現與三大國際財經要聞，用繁體中文條列呈現。"
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"連線失敗，請嘗試重新產生 API Key。詳細錯誤：{str(e)}"
if st.button("✨ 一鍵生成 AI 簡報"):
    with st.spinner("Gemini 正在分析大數據..."):
        try:
            summary = get_gemini_summary()
            st.markdown(summary)
        except Exception as e:
            st.error(f"分析失敗：{e}")

st.divider()
# 這裡繼續接你原本的 yfinance 圖表代碼...
