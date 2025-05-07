import streamlit as st
import openai

LIBRARY_CONTEXT = """
[예시 규정 텍스트 입력] 예: 부경대학교 도서관은 학부생에게 최대 5권을 14일간 대출 가능합니다...
"""

def run():
    st.title("📖 부경대 도서관 챗봇")
    question = st.text_input("도서관 관련 질문 입력:")
    if question and "api_key" in st.session_state:
        client = openai.OpenAI(api_key=st.session_state["api_key"])
        messages = [
            {"role": "system", "content": f"다음은 부경대 도서관 규정입니다:\n{LIBRARY_CONTEXT}"},
            {"role": "user", "content": question}
        ]
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=messages
        )
        st.success(response.choices[0].message.content)
