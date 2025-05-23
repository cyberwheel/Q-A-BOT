import streamlit as st
import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io
import os

st.set_page_config(page_title="PDF OCR App", layout="wide")
st.title("📄 PDF OCR App")

st.markdown("""
Upload one or more PDF files below. The app will extract text from each page using OCR.
**Note**: Only English language is supported.
""")

uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"Processing: {uploaded_file.name}")
        with st.spinner("Extracting text..."):
            try:
                # Read PDF file
                pdf_bytes = uploaded_file.read()
                pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                text_output = ""

                for page_num in range(len(pdf_doc)):
                    page = pdf_doc.load_page(page_num)
                    pix = page.get_pixmap()
                    img = Image.open(io.BytesIO(pix.tobytes()))
                    text = pytesseract.image_to_string(img, lang="eng")
                    text_output += f"\n--- Page {page_num + 1} ---\n{text}"

                st.text_area("Extracted Text", text_output, height=300)
                st.download_button(
                    label="Download Text",
                    data=text_output,
                    file_name=f"{uploaded_file.name}_extracted.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"An error occurred while processing {uploaded_file.name}: {e}")
