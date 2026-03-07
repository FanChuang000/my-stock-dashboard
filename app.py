import streamlit as st
import google.generativeai as genai
import requests  # <--- 新增這行
from bs4 import BeautifulSoup  # <--- 新增這行

def fetch_cnyes_news():
    """專門抓取鉅亨網美股頭條的爬蟲"""
    url = "https://www.cnyes.com/usstock"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取新聞標題與連結 (根據鉅亨網目前的結構)
        news_items = soup.find_all('h3', limit=10) # 抓前 10 則
        news_list = [item.get_text(strip=True) for item in news_items]
        
        return "\n".join(news_list) if news_list else "無法取得新聞列表"
    except Exception as e:
        return f"爬蟲發生錯誤: {e}"

def ask_gemini_with_data(prompt, context):
    """將抓到的資料與 Prompt 結合送給 AI"""
    try:
        # 這裡我們用最基礎、最穩定的模型設定，不加任何 tools
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(target_model_name)
        
        full_prompt = f"以下是從鉅亨網抓取的最新資訊：\n{context}\n\n任務：{prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ AI 處理失敗: {str(e)}"

# --- Streamlit 介面部分 ---
with tab1:
    st.subheader(f"📅 查詢日期：{target_date}")
    if st.button("生成市況摘要"):
        with st.spinner("正在爬取鉅亨網最新資訊..."):
            # 先爬資料
            news_context = fetch_cnyes_news()
            
            # 再丟給 AI 總結
            prompt = f"請分析 {target_date} 當日最重要的三則財經要聞，並用繁體中文表格呈現。"
            result = ask_gemini_with_data(prompt, news_context)
            st.markdown(result)
