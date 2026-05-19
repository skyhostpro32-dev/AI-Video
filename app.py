import streamlit as st
from moviepy import (
    AudioFileClip,
    ImageClip
)
from gtts import gTTS
from PIL import Image, ImageDraw
import tempfile

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Text To Video Generator",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

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
    border-radius:10px;
    padding:12px;
    font-size:18px;
    font-weight:bold;
}

textarea{
    font-size:18px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------

st.title("🎬 AI Text To Video Generator")

st.write("Convert text into AI narrated video")

# ---------------- INPUT ----------------

video_text = st.text_area(
    "Enter Video Script",
    height=200
)

voice_language = st.selectbox(
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

# ---------------- GENERATE VIDEO ----------------

if st.button("🚀 Generate Video"):

    if video_text == "":
        st.warning("Please enter text")

    else:

        with st.spinner("Generating AI Video..."):

            # ---------------- TEXT TO SPEECH ----------------

            tts = gTTS(
                text=video_text,
                lang=voice_language
            )

            audio_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            tts.save(audio_file.name)

            # ---------------- CREATE IMAGE ----------------

            width = 1280
            height = 720

            image = Image.new(
                "RGB",
                (width, height),
                color=(15, 23, 42)
            )

            draw = ImageDraw.Draw(image)

            wrapped_text = video_text[:300]

            draw.text(
                (80, 250),
                wrapped_text,
                fill=(255,255,255)
            )

            image_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".png"
            ).name

            image.save(image_path)

            # ---------------- LOAD AUDIO ----------------

            audio_clip = AudioFileClip(audio_file.name)

            duration = audio_clip.duration

            # ---------------- CREATE VIDEO ----------------

            image_clip = ImageClip(image_path)

            image_clip = image_clip.with_duration(duration)

            video_clip = image_clip.with_audio(audio_clip)

            output_path = "final_video.mp4"

            # ---------------- EXPORT VIDEO ----------------

            video_clip.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac"
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
