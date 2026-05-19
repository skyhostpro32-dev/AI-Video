import streamlit as st
from moviepy.editor import ImageClip, AudioFileClip
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
import tempfile
import textwrap
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Video Generator",
    layout="centered"
)

# ---------------- CSS ----------------

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
    background:linear-gradient(90deg, #06b6d4, #3b82f6);
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

video_text = st.text_area("Enter Video Text", height=200)

language = st.selectbox(
    "Choose Language",
    ["en", "ta", "hi", "te", "ml", "mr", "bn"]
)

# ---------------- GENERATE ----------------

if st.button("🚀 Generate Video"):

    if video_text.strip() == "":
        st.warning("Please enter text")

    else:
        with st.spinner("Generating Video..."):

            # ---------------- TEXT TO SPEECH ----------------
            tts = gTTS(text=video_text, lang=language)

            audio_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(audio_file.name)

            audio_clip = AudioFileClip(audio_file.name)
            duration = audio_clip.duration

            # ---------------- CREATE IMAGE ----------------
            width, height = 1280, 720

            image = Image.new("RGB", (width, height), color=(15, 23, 42))
            draw = ImageDraw.Draw(image)

            try:
                font = ImageFont.truetype("arial.ttf", 45)
            except:
                font = ImageFont.load_default()

            wrapped_text = textwrap.fill(video_text, width=35)

            draw.text(
                (80, 250),
                wrapped_text,
                fill="white",
                font=font
            )

            image_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            image.save(image_file.name)

            # ---------------- CREATE VIDEO ----------------
            video_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name

            video_clip = (
                ImageClip(image_file.name)
                .set_duration(duration)
                .set_audio(audio_clip)
                .set_fps(24)
            )

            video_clip.write_videofile(
                video_path,
                codec="libx264",
                audio_codec="aac",
                fps=24,
                temp_audiofile="temp-audio.m4a",
                remove_temp=True,
                verbose=False,
                logger=None
            )

            # ---------------- SHOW VIDEO ----------------
            st.success("✅ Video Generated Successfully!")

            with open(video_path, "rb") as f:
                video_bytes = f.read()
                st.video(video_bytes)

            # ---------------- DOWNLOAD ----------------
            with open(video_path, "rb") as file:
                st.download_button(
                    "⬇ Download Video",
                    data=file,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )

            # ---------------- CLEANUP ----------------
            audio_clip.close()
