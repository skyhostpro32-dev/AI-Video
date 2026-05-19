import streamlit as st
from moviepy.editor import (
    TextClip,
    ColorClip,
    CompositeVideoClip,
    AudioFileClip
)
from gtts import gTTS
import tempfile

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

st.write("Generate AI narrated videos")

# ---------------- INPUT ----------------

video_text = st.text_area(
    "Enter Video Text",
    height=200
)

language = st.selectbox(
    "Language",
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

            # ---------------- AUDIO ----------------

            tts = gTTS(
                text=video_text,
                lang=language
            )

            audio_temp = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp3"
            )

            tts.save(audio_temp.name)

            audio_clip = AudioFileClip(
                audio_temp.name
            )

            duration = audio_clip.duration

            # ---------------- BACKGROUND ----------------

            background = ColorClip(
                size=(1280,720),
                color=(15,23,42),
                duration=duration
            )

            # ---------------- TEXT ----------------

            text_clip = TextClip(
                video_text,
                fontsize=50,
                color="white",
                size=(1000,None),
                method="caption"
            )

            text_clip = (
                text_clip
                .set_position("center")
                .set_duration(duration)
            )

            # ---------------- FINAL VIDEO ----------------

            final_video = CompositeVideoClip(
                [background, text_clip]
            )

            final_video = final_video.set_audio(
                audio_clip
            )

            # ---------------- EXPORT ----------------

            output_path = "final_video.mp4"

            final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac"
            )

            # ---------------- SHOW VIDEO ----------------

            st.success("✅ Video Generated!")

            st.video(output_path)

            # ---------------- DOWNLOAD ----------------

            with open(output_path, "rb") as file:

                st.download_button(
                    "⬇ Download Video",
                    file,
                    file_name="ai_video.mp4",
                    mime="video/mp4"
                )
