import streamlit as st
import openai

def run():
    st.title("💬 GPT와 채팅")
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    user_input = st.chat_input("메시지를 입력하세요")
    if user_input and "api_key" in st.session_state:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        client = openai.OpenAI(api_key=st.session_state["api_key"])
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=st.session_state["messages"]
        )
        reply = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": reply})

    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).write(msg["content"])

    if st.button("🧹 Clear"):
        st.session_state["messages"] = []
