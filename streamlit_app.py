import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="ChatBot")

st.title("Chat with GPT")

# API Key 저장
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""

api_key_input = st.text_input("Enter OpenAI API Key", type="password", value=st.session_state.api_key)
st.session_state.api_key = api_key_input

# 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear 버튼
if st.button("Clear"):
    st.session_state.messages = []

# 사용자 입력
user_input = st.text_input("You: ", key="user_input")

# 응답 함수
def get_response(api_key, messages):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",  # or gpt-3.5-turbo for lower cost
        messages=messages
    )
    return response.choices[0].message.content

# 대화 처리
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    try:
        reply = get_response(st.session_state.api_key, st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        reply = "API Error: " + str(e).encode("ascii", errors="ignore").decode()
        st.session_state.messages.append({"role": "assistant", "content": reply})

# 채팅 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
