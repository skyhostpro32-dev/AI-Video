import streamlit as st
from moviepy import (
    AudioFileClip,
    ImageClip
)
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
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
    border-radius:12px;
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

            audio_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            tts.save(audio_temp.name)

            # ---------------- CREATE IMAGE ----------------

            width = 1280
            height = 720

            image = Image.new(
                "RGB",
                (width, height),
                color=(15, 23, 42)
            )

            draw = ImageDraw.Draw(image)

            # Optional Font

            try:
                font = ImageFont.truetype(
                    "arial.ttf",
                    45
                )

            except:
                font = ImageFont.load_default()

            # Wrap Text

            wrapped_text = ""

            words = video_text.split()

            line = ""

            for word in words:

                if len(line + word) < 35:
                    line += word + " "

                else:
                    wrapped_text += line + "\n\n"
                    line = word + " "

            wrapped_text += line

            # Draw Text

            draw.text(
                (80, 180),
                wrapped_text,
                fill=(255,255,255),
                font=font
            )

            # Save Image

            image_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".png"
            )

            image.save(image_temp.name)

            # ---------------- AUDIO CLIP ----------------

            audio_clip = AudioFileClip(
                audio_temp.name
            )

            duration = audio_clip.duration

            # ---------------- IMAGE CLIP ----------------

            image_clip = ImageClip(
                image_temp.name
            )

            image_clip = image_clip.resized(
                width=1280
            )

            image_clip = image_clip.with_duration(
                duration
            )

            image_clip = image_clip.with_fps(24)

            # ---------------- FINAL VIDEO ----------------

            final_video = image_clip.with_audio(
                audio_clip
            )

            output_path = "final_video.mp4"

            # ---------------- EXPORT VIDEO ----------------

            final_video.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=24
            )

            # ---------------- SUCCESS ----------------

            st.success(
                "✅ Video Generated Successfully!"
            )

            # ---------------- SHOW VIDEO ----------------

            video_file = open(
                output_path,
                "rb"
            )

            video_bytes = video_file.read()

            st.video(video_bytes)

            # ---------------- DOWNLOAD ----------------

            with open(output_path, "rb") as file:

                st.download_button(
                    "⬇ Download Video",
                    file,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
