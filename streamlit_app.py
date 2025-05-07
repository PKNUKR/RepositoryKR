import streamlit as st
import openai

# API 키 입력 받기 및 저장
if 'api_key' not in st.session_state:
    st.session_state.api_key = st.text_input("Enter OpenAI API Key", type="password")

# 질문 입력
question = st.text_input("Ask a question:")

@st.cache_data
def get_response(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# 응답 출력
if question and st.session_state.api_key:
    answer = get_response(st.session_state.api_key, question)
    st.write("Answer:", answer)
