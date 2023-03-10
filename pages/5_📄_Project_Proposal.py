import streamlit as st
import base64

pdfFileObj = open('pdf/team007proposal.pdf', 'rb')
st.download_button('Download Project Proposal', pdfFileObj, file_name='team007proposal.pdf', mime='pdf')

st.video('https://youtu.be/2jkgdUVbqFc')