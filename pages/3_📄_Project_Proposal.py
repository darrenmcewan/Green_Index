import streamlit as st
import base64
st.set_page_config(page_title="Proposal", layout="wide")

original_title = '<h1 style=color:green>Project Proposal</h1>'
st.markdown(original_title, unsafe_allow_html=True)

pdfFileObj = open('pdf/team007proposal.pdf', 'rb')
st.download_button('Download Project Proposal', pdfFileObj, file_name='team007proposal.pdf', mime='pdf')

st.video('https://youtu.be/2jkgdUVbqFc')