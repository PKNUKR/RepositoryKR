import streamlit as st
import openai
import PyPDF2

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def run():
    st.title("📄 ChatPDF")
    uploaded_file = st.file_uploader("PDF 파일 업로드", type="pdf")
    
    if st.button("🧹 Clear"):
        st.session_state.pop("pdf_text", None)

    if uploaded_file and "api_key" in st.session_state:
        st.session_state["pdf_text"] = extract_text_from_pdf(uploaded_file)

    if "pdf_text" in st.session_state:
        question = st.text_input("PDF 내용에 대해 질문하세요:")
        if question:
            client = openai.OpenAI(api_key=st.session_state["api_key"])
            messages = [
                {"role": "system", "content": "다음은 업로드된 PDF의 내용입니다:\n" + st.session_state["pdf_text"][:4000]},
                {"role": "user", "content": question}
            ]
            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=messages
            )
            st.success(response.choices[0].message.content)
