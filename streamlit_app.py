import streamlit as st
from openai import OpenAI
import sys
import io

# stdout을 UTF-8로 설정 (ascii 오류 방지)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

st.title("GPT 응답 웹 앱")

# API Key 저장
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

api_key_input = st.text_input("Enter OpenAI API Key", type="password", value=st.session_state.api_key)
st.session_state.api_key = api_key_input

question = st.text_input("Ask a question:")

@st.cache_data(show_spinner="Thinking...")
def get_response(api_key, prompt):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",  # 실제로는 gpt-4 사용
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if st.session_state.api_key and question:
    try:
        answer = get_response(st.session_state.api_key, question)
        st.write("Answer:", answer)
    except Exception as e:
        st.error(f"API Error: {e}")
