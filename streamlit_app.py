import streamlit as st
import openai

# 제목
st.title("💬 GPT-4.1-mini 챗봇")

# API Key 입력 받기 (비밀번호 형태로 숨김)
api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")

# 질문 입력 받기
question = st.text_area("❓ 궁금한 점을 입력하세요")

# 응답 출력
if st.button("답변 받기"):
    if not api_key:
        st.warning("API Key를 입력해주세요.")
    elif not question:
        st.warning("질문을 입력해주세요.")
    else:
        try:
            openai.api_key = api_key

            response = openai.ChatCompletion.create(
                model="gpt-4.0-turbo",
                messages=[{"role": "user", "content": question}],
            )

            answer = response['choices'][0]['message']['content']
            st.success("💡 GPT의 답변:")
            st.write(answer)
        except Exception as e:
            st.error(f"에러 발생: {e}")
