import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader 
from rake_nltk import Rake
rake_nltk_var=Rake()
from PyPDF2 import PdfReader

st.set_page_config(layout="wide")
@st.cache_resource
def summary_text(text):
    summary=Summary()
    text=(text)
    result=summary(text)
    return result
 #Extract text from pdf file using pypdf2
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader=PdfReader(f)
        page=reader.pages[0]
        text=page.extract_text()
    return text    



choice = st.sidebar.selectbox("Select your choice",["Extract Images From PDF","Summarize PDF & Extract Keywords"])

if choice== "Extract Images From PDF":
    st.subheader("Image Extraction ")
    input_file=st.file_uploader("Upload your file",type=["pdf"])
    if input_file is not None:
        if st.button("Extract Images and summarize"):
            with open("doc_file.pdf","wb") as f:
                f.write(input_file.getbuffer())
            col1,col2=st.columns([1,1])
            with col1:
                result=extract_text_from_pdf("doc_file.pdf")
                st.markdown("*summarize Document*")
                summary_result=summary_text(result)
                st.success(summary_result)
            with col2:
                with open("doc_file.pdf","wb") as f:
                 f.write(input_file.getbuffer())
            reader=PdfReader("doc_file.pdf")
            st.markdown("*Images are stored in the local folders*")    
            page=reader.pages[0]
            for i in page.images:
                with open(i.name,'wb') as f:
                 f.write(i.data)

elif choice=="Summarize PDF & Extract Keywords":
    st.subheader("Summarize PDF")
    input_file=st.file_uploader("Upload your file",type=["pdf"])
    if input_file is not None:
        if st.button("Summarize PDF"):
            with open("doc_file.pdf","wb") as f:
                f.write(input_file.getbuffer())
            col1,col2=st.columns([1,1])
            with col1:
                result=extract_text_from_pdf("doc_file.pdf")
                st.markdown("*Your Summarized text*")
                summary_result=summary_text(result)
                st.success(summary_result)
            with col2:
                st.markdown("**The Extracted Keywords:**")
                rake_nltk_var.extract_keywords_from_text(summary_result)
                keyword_extracted=rake_nltk_var.get_ranked_phrases()
                st.success(keyword_extracted)