import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

st.set_page_config(page_title="AI Image Generator")

st.title("🎨 Real AI Text → Image Generator")

prompt = st.text_area("Enter Prompt")

@st.cache_resource
def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float32
    )
    pipe = pipe.to("cpu")   # change to "cuda" if GPU available
    return pipe

pipe = load_model()

if st.button("Generate Image"):

    if prompt.strip() == "":
        st.warning("Enter prompt")
    else:
        with st.spinner("Generating AI Image..."):

            image = pipe(prompt).images[0]

            st.success("Done!")
            st.image(image, use_container_width=True)

            image.save("output.png")

            with open("output.png", "rb") as f:
                st.download_button(
                    "Download Image",
                    f,
                    file_name="ai_image.png",
                    mime="image/png"
                )
