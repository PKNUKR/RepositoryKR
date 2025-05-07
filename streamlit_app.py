import streamlit as st
import openai

# API 키 입력
api_key = st.text_input("Enter OpenAI API Key", type="password")

# 질문 입력
question = st.text_input("Ask a question:")

@st.cache_data
def get_response(api_key, prompt):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 올바른 모델 이름 사용
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# 응답 출력
if api_key and question:
    try:
        answer = get_response(api_key, question)
        st.write("Answer:", answer)
    except Exception as e:
        st.error(f"Error: {e}")
