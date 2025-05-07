import streamlit as st
import openai

@st.cache_data(show_spinner=False)
def ask_gpt(prompt, key):
    client = openai.OpenAI(api_key=key)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run():
    st.title("🤖 질문 → GPT 응답")
    question = st.text_input("질문을 입력하세요:")
    if st.button("질문하기") and "api_key" in st.session_state:
        answer = ask_gpt(question, st.session_state["api_key"])
        st.success(answer)
