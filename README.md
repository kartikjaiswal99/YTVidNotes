
---

# 🎥 YouTube Playlist & Video Summarizer

This Streamlit web app summarizes YouTube videos or playlists using Google Gemini 2.0 Flash. It can generate:
-  Bullet point summaries
-  Deep, lecture-style notes

Supports both individual video URLs and full playlists.

---

##  Features

-  Extracts transcripts from YouTube videos
-  Uses Gemini 2.0 Flash for intelligent summarization
-  Supports two summarization styles: Bullet points & Detailed notes
- 🎞 Displays video thumbnails and clickable links
-  Handles playlists (up to 15 or 30 videos in free tier)

---

##  Tech Stack

- **Python**
- **Streamlit**
- **Gemini 2.0 Flash (via Google Generative AI API)**
- **YouTubeTranscriptAPI**
- **pytube**

---

##  Demo

[![Demo Video](https://img.youtube.com/vi/80zEu0DP95Q/0.jpg)](https://youtu.be/80zEu0DP95Q)

▶️ **[Watch the demo on YouTube](https://youtu.be/80zEu0DP95Q)**

---

## 🧪 How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/kartikjaiswal99/Youtube-Playlist-Video-Summarizer.git
   cd Youtube-Playlist-Video-Summarizer

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:

   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

---

## 📌 Limitations

* The free Gemini tier supports limited tokens and \~15 videos in a playlist.
* Long videos may hit transcript or token limits.

---

## 📬 Contact

Created by **Kartik Jaiswal** – feel free to reach out for suggestions or improvements!

