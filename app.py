import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import Playlist, YouTube


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


prompt_bullet_sum = """
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

class YTSummarizer:
    def __init__(self, url):
        self.url = url
        self.is_playlist = "playlist" in url or "list=" in url
        self.video_links = self.extract_video_links()

    def extract_video_links(self):
        if self.is_playlist:
            try:
                pl = Playlist(self.url)
                return list(pl.video_urls)
            except Exception as e:
                st.error(f"Error loading playlist: {e}")
                return []
        else:
            return [self.url]

    def extract_transcript(self, video_url):
        try:
            video_id = video_url.split("v=")[1].split("&")[0]
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([t["text"] for t in transcript])
            return transcript_text
        except Exception as e:
            st.error(f"Transcript error for {video_url}: {e}")
            return None

    def generate_summary(self, transcript_text, style="bullet"):
        prompt = prompt_bullet_sum if style == "bullet" else prompt_deep_notes
        model = genai.GenerativeModel("gemini-2.0-flash")
        try:
            response = model.generate_content(prompt + transcript_text)
            return response.text
        except Exception as e:
            st.error(f"Error generating summary: {e}")
            return None

    def get_video_thumbnail(self, video_url):
        try:
            video_id = video_url.split("v=")[1].split("&")[0]
            return f"https://img.youtube.com/vi/{video_id}/0.jpg"
        except:
            return None

    

st.title("YouTube Playlist & Video Summarizer")

youtube_url = st.text_input("Enter Youtube Playlist or Video URL")

if youtube_url:
    summarizer = YTSummarizer(youtube_url)

    if not summarizer.is_playlist:
        thumb_url = summarizer.get_video_thumbnail(youtube_url)
        if thumb_url:
            st.image(thumb_url, caption="Youtube Video Thumbnail", use_container_width=True)

    col1, col2 = st.columns([1, 1])
    trigger_summary = False
    trigger_deep_notes = False

    with col1:
        if st.button("🔹 Summarize in Bullet Points", use_container_width=True):
            trigger_summary = True

    with col2:
        if st.button("🔹 Generate Deep Notes", use_container_width=True):
            trigger_deep_notes = True

    if trigger_summary or trigger_deep_notes:
        for idx, video_url in enumerate(summarizer.video_links):
            transcript = summarizer.extract_transcript(video_url)
            if not transcript:
                continue
                
            style = "bullet" if trigger_summary else "deep"
            summary = summarizer.generate_summary(transcript, style)

            st.markdown(f"---\n### 💻 Video [{idx+1}]({video_url})")
            try:
                thumb_url = summarizer.get_video_thumbnail(video_url)
                st.image(thumb_url ,width=320)
            except:
                pass

            if summary:
                header = "point" if style == "bullet" else "Deep"
                if header == "point":
                    st.markdown("#### 🔹 Bullet Point Summary")
                else:
                    st.markdown("#### 🔹 Deep Notes")
                st.write(summary)
                

