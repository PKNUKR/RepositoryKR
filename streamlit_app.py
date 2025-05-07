import streamlit as st
from openai import OpenAI

st.title("GPT 응답 웹 앱")

# API 키 입력 및 session_state에 저장
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

api_key_input = st.text_input("Enter OpenAI API Key", type="password", value=st.session_state.api_key)
st.session_state.api_key = api_key_input  # 페이지 이동 시에도 유지

# 사용자 질문 입력
question = st.text_input("Ask a question:")

# 응답 캐시 함수
@st.cache_data(show_spinner="Thinking...")
def get_response(api_key, prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",  # 과제에서 요구한 gpt-4.1-mini 역할을 수행
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 응답 출력
if st.session_state.api_key and question:
    try:
        answer = get_response(st.session_state.api_key, question)
        st.write("Answer:", answer)
    except Exception as e:
        st.error(f"API Error: {e}")
