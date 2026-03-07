import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import datetime

# --- 1. 基礎設定 ---
# 建議在 Streamlit Cloud 的 Secrets 中設定 API_KEY
if "API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["API_KEY"])
else:
    st.error("請在 Streamlit Secrets 中設定 API_KEY")

def fetch_cnyes_news():
    """爬取鉅亨網美股頻道最新標題"""
    url = "https://www.cnyes.com/usstock"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 抓取新聞內容 (針對鉅亨網目前的標籤結構進行優化)
        news_items = soup.find_all(['h3', 'a'], limit=30) 
        titles = []
        for item in news_items:
            text = item.get_text(strip=True)
            # 過濾掉選單字眼、太短的標題或重複內容
            if len(text) > 12 and text not in titles:
                titles.append(text)
        
        return "\n".join([f"- {t}" for t in titles[:15]])
    except Exception as e:
        return f"無法取得即時新聞，錯誤原因: {e}"

def ask_gemini_with_context(prompt, context):
    """基礎 AI 呼叫函數"""
    try:
        # 自動選取可用模型 (優先選用 flash)
        model_list = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = next((m for m in model_list if 'flash' in m), model_list[0])
        
        model = genai.GenerativeModel(target_model)
        full_input = f"【參考資料】\n{context}\n\n【指令】\n{prompt}"
        response = model.generate_content(full_input)
        return response.text
    except Exception as e:
        return f"❌ AI 呼叫失敗: {str(e)}"

# --- 2. 網頁介面佈局 ---
st.set_page_config(page_title="美股財經 AI 助理", page_icon="📈")
st.title("📈 美股即時市況摘要")
st.write("本工具會自動爬取鉅亨網最新美股新聞，並由 AI 進行去蕪存菁的總結。")

# 介面元件
target_date = st.date_input("選擇查詢日期", datetime.date.today())
st.info(f"目前顯示日期：{target_date} (AI 將以當前最新新聞進行分析)")

if st.button("🚀 生成今日市況摘要"):
    with st.spinner("正在爬取鉅亨網資訊並進行 AI 分析..."):
        # 1. 執行爬蟲抓取資料
        news_data = fetch_cnyes_news()
        
        # 2. 定義任務指令
        raw_prompt = """你是一位專業的國際財經分析師。請根據提供的「參考資料」，篩選並總結出最重要的三則國際財經或產業新聞。
        要求：
        1. 聚焦於美股走勢、半導體/AI 產業動向、或聯準會相關政策。
        2. 請使用「繁體中文」並以「表格」形式呈現。
        3. 表格欄位須包含：新聞標題、內容要點、以及「對投資者的影響建議」。
        4. 嚴禁編造參考資料中未提到的數據。"""
        
        # 3. 呼叫 AI 處理
        result = ask_gemini_with_context(raw_prompt, news_data)
        
        # 4. 呈現結果
        st.markdown("---")
        st.markdown("### 📊 AI 總結報告")
        st.markdown(result)
        st.caption("資料來源：鉅亨網 (https://www.cnyes.com/usstock)")

# 側邊欄資訊
with st.sidebar:
    st.header("關於此工具")
    st.write("這是一個手動聯網的 AI 應用，確保資料來源精準，避免 AI 產生事實幻想。")
    st.divider()
    st.write("核心技術：")
    st.code("Python / Streamlit\nBeautifulSoup4 (爬蟲)\nGemini 1.5 Flash")
