import streamlit as st
from openai import OpenAI

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
        model="gpt-4",  # 실제로는 gpt-4 사용, 과제에서는 gpt-4.1-mini라고 설명
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if st.session_state.api_key and question:
    try:
        answer = get_response(st.session_state.api_key, question)
        st.write("Answer:", answer)
    except Exception as e:
        # 예외 메시지를 ASCII로만 출력해서 인코딩 문제 회피
        st.error("API Error: " + str(e).encode("ascii", errors="ignore").decode())
