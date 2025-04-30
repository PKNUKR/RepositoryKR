import streamlit as st
import openai

# API Key 입력
api_key = st.text_input("🔑 OpenAI API Key", type="password")

# 질문 입력
user_input = st.text_area("❓ 질문을 입력하세요:")

if st.button("답변 받기"):
    if not api_key:
        st.warning("API Key를 입력하세요.")
    elif not user_input:
        st.warning("질문을 입력하세요.")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[{"role": "user", "content": user_input}]
            )

            st.success("💬 GPT의 답변:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"에러 발생: {e}")
            
