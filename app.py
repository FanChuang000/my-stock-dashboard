{\rtf1\ansi\ansicpg950\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import yfinance as yf\
import requests\
\
# 1. \uc0\u20171 \u38754 \u35373 \u23450 \
st.set_page_config(page_title="AI \uc0\u36001 \u32147 \u23566 \u35712 \u20736 \u34920 \u26495 ", layout="wide")\
st.title("\uc0\u55358 \u56598  AI \u26152 \u26085 \u32654 \u32929 \u30436 \u24460 \u20998 \u26512 ")\
\
# 2. \uc0\u21152 \u20837  Perplexity AI \u25688 \u35201 \u21151 \u33021 \
def get_ai_summary(api_key):\
    url = "https://api.perplexity.ai/chat/completions"\
    payload = \{\
        "model": "sonar-pro", # \uc0\u20351 \u29992 \u20855 \u20633 \u32879 \u32178 \u33021 \u21147 \u30340 \u27169 \u22411 \
        "messages": [\
            \{"role": "system", "content": "\uc0\u20320 \u26159 \u19968 \u20301 \u23560 \u26989 \u32654 \u32929 \u20998 \u26512 \u24107 \u65292 \u35531 \u29992 \u32321 \u39636 \u20013 \u25991 \u32317 \u32080 \u26152 \u26085 \u32654 \u32929 \u34920 \u29694 \u12289 \u37325 \u35201 \u32147 \u28639 \u25976 \u25818 \u21450 \u19977 \u20214 \u22283 \u38555 \u36001 \u32147 \u22823 \u20107 \u12290 "\},\
            \{"role": "user", "content": "\uc0\u35531 \u25552 \u20379 \u26152 \u26085 \u32654 \u32929 \u30436 \u24460 \u33287 \u22283 \u38555 \u26032 \u32862 \u25688 \u35201 \u12290 "\}\
        ]\
    \}\
    headers = \{\
        "Authorization": f"Bearer \{api_key\}",\
        "Content-Type": "application/json"\
    \}\
    response = requests.post(url, json=payload, headers=headers)\
    return response.json()['choices'][0]['message']['content']\
\
# 3. \uc0\u20596 \u37002 \u27396 \u35373 \u23450  API Key\
api_key = st.sidebar.text_input("\uc0\u36664 \u20837  Perplexity API Key", type="password")\
\
if st.button("\uc0\u29983 \u25104 \u20170 \u26085  AI \u31777 \u22577 "):\
    if api_key:\
        with st.spinner("AI \uc0\u27491 \u22312 \u32763 \u38321 \u36001 \u32147 \u26032 \u32862 ..."):\
            summary = get_ai_summary(api_key)\
            st.markdown("### \uc0\u55357 \u56522  \u26152 \u26085 \u24066 \u22580 \u26680 \u24515 \u25688 \u35201 ")\
            st.info(summary)\
    else:\
        st.error("\uc0\u35531 \u20808 \u22312 \u24038 \u20596 \u36664 \u20837  API Key \u25165 \u33021 \u22519 \u34892  AI \u20998 \u26512 \u12290 ")\
\
st.divider()\
\
# 4. \uc0\u21407 \u26377 \u30340 \u32929 \u20729 \u30435 \u25511 \u21151 \u33021  (\u20445 \u25345 \u19981 \u35722 )\
st.subheader("\uc0\u55357 \u56520  \u37325 \u40670 \u27161 \u30340 \u21363 \u26178 \u36208 \u21218 ")\
# ... (\uc0\u27492 \u34389 \u25509 \u32396 \u20043 \u21069 \u30340  yfinance \u20195 \u30908 )}