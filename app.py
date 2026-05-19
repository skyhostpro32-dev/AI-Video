import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("🎨 AI Image Generator")

prompt = st.text_area("Enter Prompt")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}

def generate_image(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return Image.open(BytesIO(response.content))

if st.button("Generate"):

    if prompt.strip() == "":
        st.warning("Enter prompt")
    else:
        with st.spinner("Generating..."):
            image = generate_image(prompt)
            st.image(image, use_container_width=True)
