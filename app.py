import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import tempfile
import textwrap
import random

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Text to Image Generator",
    layout="centered"
)

# ---------------- UI STYLE ----------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color:white;
}

h1{
    text-align:center;
    color:#38bdf8;
    font-size:3rem !important;
}

.stButton>button{
    width:100%;
    background:linear-gradient(90deg, #22c55e, #06b6d4);
    color:white;
    border:none;
    border-radius:12px;
    padding:12px;
    font-size:18px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🎨 AI Text → Image Generator")
st.write("Enter a prompt and generate AI-style images instantly")

# ---------------- INPUT ----------------

prompt = st.text_area("Enter your image prompt", height=150)

# ---------------- GENERATE ----------------

if st.button("🚀 Generate Image"):

    if prompt.strip() == "":
        st.warning("Please enter a prompt")

    else:
        with st.spinner("Creating image..."):

            # ---------------- CREATE IMAGE ----------------

            width, height = 1024, 1024

            # random gradient background
            color1 = (random.randint(0,50), random.randint(0,50), random.randint(80,150))
            color2 = (random.randint(0,50), random.randint(80,150), random.randint(150,255))

            image = Image.new("RGB", (width, height), color1)
            draw = ImageDraw.Draw(image)

            # simple gradient effect
            for i in range(height):
                r = int(color1[0] + (color2[0] - color1[0]) * (i / height))
                g = int(color1[1] + (color2[1] - color1[1]) * (i / height))
                b = int(color1[2] + (color2[2] - color1[2]) * (i / height))
                draw.line([(0, i), (width, i)], fill=(r, g, b))

            # ---------------- TEXT ----------------

            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            wrapped_text = textwrap.fill(prompt, width=30)

            # center text
            text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            x = (width - text_width) / 2
            y = (height - text_height) / 2

            # shadow
            draw.multiline_text((x+3, y+3), wrapped_text, font=font, fill="black")

            # main text
            draw.multiline_text((x, y), wrapped_text, font=font, fill="white")

            # ---------------- SAVE ----------------

            img_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            image.save(img_file.name)

            # ---------------- SHOW ----------------

            st.success("✅ Image Generated Successfully!")
            st.image(image, caption="Generated AI Image", use_container_width=True)

            # ---------------- DOWNLOAD ----------------

            with open(img_file.name, "rb") as file:
                st.download_button(
                    "⬇ Download Image",
                    data=file,
                    file_name="ai_image.png",
                    mime="image/png"
                )
