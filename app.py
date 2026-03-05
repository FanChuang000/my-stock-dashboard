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
        # 獲取模型清單
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 核心策略：優先找 "flash"，因為它的免費配額最高！
        # 按照 3-flash -> 1.5-flash -> 任何 flash 的順序找
        selected_model = next((m for m in available_models if 'gemini-3-flash' in m), 
                         next((m for m in available_models if '1.5-flash' in m), 
                         next((m for m in available_models if 'flash' in m), available_models[0])))
        
        st.write(f"🚀 自動選用高配額模型：{selected_model}")
        
        model = genai.GenerativeModel(selected_model)
        prompt = "請以專業美股分析師身分，總結昨日美股盤後表現與三則財經要聞，使用繁體中文。"
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        if "429" in str(e):
            return "⚠️ 目前 Google API 免費額度過載，請稍等一分鐘後再試，或更換為 Flash 模型。"
        return f"連線失敗：{str(e)}"
if st.button("✨ 一鍵生成 AI 簡報"):
    with st.spinner("Gemini 正在分析大數據..."):
        try:
            summary = get_gemini_summary()
            st.markdown(summary)
        except Exception as e:
            st.error(f"分析失敗：{e}")

st.divider()
# 這裡繼續接你原本的 yfinance 圖表代碼...
