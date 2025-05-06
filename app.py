import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
load_dotenv()



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """
    You are the Youtube video summarizer, 
    Given the transcript of a Youtube video,
    summarize the content in concise **bullet points**,
    each capturing a key idea or topic discussed.
    Format the output with bullet points.
    one per line, using dashes or asterisks.
"""

prompt_deep_notes = """
    You are a Youtube video summarizer.
    Given the transcript of a Youtube video, 
    provide a deep and detailed explanation of the content in a well-structured format. 
    Include context, elaboration of key points, and logical flow. 
    The summary should be comprehensive, 
    like notes one would take during a lecture.
"""


def extract_transcript_text(yt_video_url):
    try:
        video_id = yt_video_url.split("v=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t["text"] for t in transcript])
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None


def generate(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text


st.title("Youtube Playlist Videos Summarizer")
youtub_link = st.text_input("Enter Youtube Playlist or Video URL")

if youtub_link:
    try:
        video_id = youtub_link.split("v=")[1]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", caption="Youtube Video Thumbnail", use_container_width=True)
    except IndexError:
        st.error("Invalid Youtube URL. Please enter a valid URL.")


col1, col2 = st.columns([1, 1])
trigger_summary = False
trigger_deep_notes = False


with col1:
    if st.button("🔹 Summarize in Bullet Points", use_container_width=True):
        trigger_summary = True

with col2:
    if st.button("🔹 Generate Deep Notes", use_container_width=True):
        trigger_deep_notes = True

# Row 4: Full width output, not inside column
if youtub_link and (trigger_summary or trigger_deep_notes):
    transcript_text = extract_transcript_text(youtub_link)
    if transcript_text:
        if trigger_summary:
            with st.spinner("Generating point-wise summary..."):
                summary = generate(transcript_text, prompt)
            st.markdown("## 🔹 Point-wise Summary")
            st.write(summary)

        if trigger_deep_notes:
            with st.spinner("Generating detailed notes..."):
                notes = generate(transcript_text, prompt_deep_notes)
            st.markdown("## 🔹 Deep Notes")
            st.write(notes)
    else:
        st.error("Transcript not available.")

