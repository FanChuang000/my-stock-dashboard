import streamlit as st
import yfinance as yf
import requests

# 介面設定
st.set_page_config(page_title="AI 財經導讀儀表板", layout="wide")
st.title("📈 昨日美股表現與 AI 分析")

# 1. 加入 Perplexity AI 摘要功能
def get_ai_summary(api_key):
    url = "https://api.perplexity.ai/chat/completions"
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": "你是一位專業美股分析師，請用繁體中文總結昨日美股表現及三件財經大事。"},
            {"role": "user", "content": "請提供昨日美股新聞摘要。"}
        ]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()['choices'][0]['message']['content']

# 側邊欄：輸入 API Key
api_key = st.sidebar.text_input("輸入 Perplexity API Key", type="password")

if st.button("生成今日 AI 簡報"):
    if api_key:
        with st.spinner("AI 正在分析新聞..."):
            try:
                summary = get_ai_summary(api_key)
                st.info(summary)
            except Exception as e:
                st.error(f"發生錯誤: {e}")
    else:
        st.warning("請先輸入 API Key")

st.divider()

# 2. 股價監控
target_stocks = ["AAPL", "TSLA", "NVDA", "^GSPC"]
cols = st.columns(len(target_stocks))

for i, ticker in enumerate(target_stocks):
    data = yf.Ticker(ticker).history(period="2d")
    latest = data['Close'].iloc[-1]
    prev = data['Close'].iloc[-2]
    delta = ((latest - prev) / prev) * 100
    cols[i].metric(ticker, f"${latest:.2f}", f"{delta:.2f}%")
