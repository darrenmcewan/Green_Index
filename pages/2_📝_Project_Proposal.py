import streamlit as st
import base64

st.set_page_config(page_title="Project Proposal", page_icon="🌍")

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")

pdfFileObj = open('pdf/team007proposal.pdf', 'rb')
st.download_button('Download Proposal', pdfFileObj, file_name='team007proposal.pdf', mime='pdf')

pdf_file = 'pdf/team007proposal.pdf'
with open(pdf_file, "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')

pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
st.markdown(pdf_display, unsafe_allow_html=True)
st.write('📧: gburdell@gatech.edu')