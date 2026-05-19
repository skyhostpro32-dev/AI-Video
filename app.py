import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import tempfile
import textwrap

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Video Generator",
    layout="centered"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color:white;
}

h1{
    text-align:center;
    color:#38bdf8;
    font-size:3rem !important;
}

.stButton>button{
    width:100%;
    background:linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
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

st.title("🎬 AI Text To Video Generator")

st.write("Convert text into AI narrated video")

# ---------------- INPUT ----------------

video_text = st.text_area(
    "Enter Video Text",
    height=200
)

language = st.selectbox(
    "Choose Language",
    [
        "en",
        "ta",
        "hi",
        "te",
        "ml",
        "mr",
        "bn"
    ]
)

# ---------------- GENERATE ----------------

if st.button("🚀 Generate Video"):

    if video_text.strip() == "":

        st.warning("Please enter text")

    else:

        with st.spinner("Generating Video..."):

            # ---------------- TEXT TO SPEECH ----------------

            tts = gTTS(
                text=video_text,
                lang=language
            )

            audio_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            tts.save(audio_temp.name)

            # ---------------- AUDIO CLIP ----------------

            audio_clip = AudioFileClip(
                audio_temp.name
            )

            duration = audio_clip.duration

            # ---------------- CREATE IMAGE ----------------

            width = 1280
            height = 720

            image = Image.new(
                "RGB",
                (width, height),
                color=(15, 23, 42)
            )

            draw = ImageDraw.Draw(image)

            try:

                font = ImageFont.truetype(
                    "arial.ttf",
                    45
                )

            except:

                font = ImageFont.load_default()

            wrapped_text = textwrap.fill(
                video_text,
                width=35
            )

            # ---------------- DRAW TEXT ----------------

            draw.text(
                (80, 180),
                wrapped_text,
                fill="white",
                font=font
            )

            # ---------------- SAVE IMAGE ----------------

            image_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".png"
            )

            image.save(image_temp.name)

            # ---------------- CREATE VIDEO ----------------

            video_clip = (
                ImageClip(image_temp.name)
                .set_duration(duration)
                .set_audio(audio_clip)
                .set_fps(24)
            )

            # ---------------- EXPORT ----------------

            output_path = "final_video.mp4"

            video_clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=24
            )

            # ---------------- SHOW VIDEO ----------------

            st.success("✅ Video Generated Successfully!")

            st.video(output_path)

            # ---------------- DOWNLOAD ----------------

            with open(output_path, "rb") as file:

                st.download_button(
                    "⬇ Download Video",
                    file,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
