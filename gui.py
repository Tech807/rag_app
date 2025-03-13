# filepath: d:\temp\app\gui.py
import streamlit as st
from PyPDF2 import PdfReader
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('OPENAI_API_KEY'),  # Use environment variable
)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_completion_from_openai(prompt):
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",  # Optional. Site URL for rankings on openrouter.ai.
            "X-Title": "<YOUR_SITE_NAME>",  # Optional. Site title for rankings on openrouter.ai.
        },
        extra_body={},
        model="qwen/qwq-32b:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content

st.title("PDF Question Answering with RAG")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", pdf_text, height=300)

    question = st.text_input("Ask a question about the PDF")
    if st.button("Get Answer"):
        if question:
            prompt = f"Based on the following text, answer the question: {pdf_text}\n\nQuestion: {question}"
            answer = get_completion_from_openai(prompt)
            st.write("Answer:", answer)
        else:
            st.write("Please enter a question.")
