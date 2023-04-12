import streamlit as st
st.set_page_config(page_title="Proposal", layout="wide")

original_title = '<h1 style=color:green>Project Proposal</h1>'
st.markdown(original_title, unsafe_allow_html=True)

pdfFileObj = open('pdf/team007progress.pdf', 'rb')
st.download_button('Download Project Proposal', pdfFileObj, file_name='team007progress.pdf', mime='pdf')

st.video('https://youtu.be/2jkgdUVbqFc')