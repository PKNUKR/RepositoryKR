import streamlit as st
from pages import simple_qa, chat, chatbot, chatpdf

st.set_page_config(page_title="GPT 실습 앱", layout="wide")

st.sidebar.title("📚 GPT 기능 선택")
page = st.sidebar.radio("페이지 선택", ["질문응답", "Chat", "Chatbot", "ChatPDF"])

# API Key 입력 & session 저장
api_key = st.sidebar.text_input("🔑 OpenAI API Key 입력", type="password")
if api_key:
    st.session_state["api_key"] = api_key

# 페이지 라우팅
if page == "질문응답":
    simple_qa.run()
elif page == "Chat":
    chat.run()
elif page == "Chatbot":
    chatbot.run()
elif page == "ChatPDF":
    chatpdf.run()
