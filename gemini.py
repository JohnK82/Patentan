import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def initialize_gemini(api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def main():
    st.title("특허 분석 챗봇 🤖")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        try:
            model = initialize_gemini(api_key)
            
            # PDF 파일 업로드
            uploaded_file = st.file_uploader("특허 PDF 파일을 업로드하세요", type=['pdf'])
            
            if uploaded_file:
                patent_text = extract_text_from_pdf(uploaded_file)
                
                # 분석 옵션
                analysis_type = st.selectbox(
                    "분석 유형을 선택하세요:",
                    ["특허 요약", "주요 청구항 분석", "기술 분야 분석"]
                )
                
                if st.button("분석 시작"):
                    with st.spinner("분석 중..."):
                        prompt = f"""다음 특허 문서를 {analysis_type}해주세요:
                        {patent_text[:8000]}"""  # API 제한으로 텍스트 길이 제한
                        
                        response = model.generate_content(prompt)
                        st.write(response.text)
                        
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
    else:
        st.warning("API 키를 입력해주세요.")

if __name__ == "__main__":
    main()
