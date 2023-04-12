import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)


st.write("# Welcome to the  Green Solution! ♻️")
st.subheader("Making Informed Decisions by Visualizing, Exploring, and Evaluating Renewable Energy Data")


st.sidebar.success("Select a page above.")
st.sidebar.write("[Contact Us](mailto:support@greensolution.com)")

st.markdown(
    """
    Darren McEwan, Isabel Chang, Anjing Bi, Hanh Pham, Edmund Dale, Kelly Seto 
    """
)

with st.columns(3)[1]:
    image = Image.open("images/GT_logo.png")
    image = image.resize((200,200))
    st.image(image)

