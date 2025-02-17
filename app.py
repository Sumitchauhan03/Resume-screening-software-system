import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import time

load_dotenv()  ## load all our environment variables

genai.configure(api_key="AIzaSyBP65KKgEc6iL69wWX7zvIAg-xQOHVX9xk")

# function to instantiate model and get response
def get_gemini_response(input):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(input)
    return response.text

# function to extract text from pdf
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page_n in range(len(reader.pages)):
        page = reader.pages[page_n]
        text += str(page.extract_text())
    
    return text

# Prompt template

input_prompt = """
Hey act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst
and bit data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide best assistance
for improving the resumes. Assign the percentage matching based on JD (Job Description)
and the missing keywords with high accuracy.

I want the response in json structure like
{
    "JD Match": "%",
    "Missing Keywords": [],
    "Profile Summary": ""
}
"""

# Streamlit app
st.title("Resume Screening Software (ATS)")
col1, col2 = st.columns([1, 3])  # Create two columns
with col1:
    st.image("ats_image.jpg", width=150)  # Add a smaller image on the left
with col2:
    st.subheader("Match Your Resume Against the Job Description")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload your Resume", type="pdf", help="Please upload the pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response([input_prompt, "Job Description\n" + jd, "Resume \n" + text])
        bar = st.progress(50)
        time.sleep(3)
        bar.progress(100)
        st.json(response)

