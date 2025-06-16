import streamlit as st
import os
import tempfile
import logging
from utils.news_fetcher import fetch_news
from utils.summarizer import summarize_text
from utils.voice_generator import generate_voice_clone, load_tts_model

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="NewsBreeze",
    page_icon="📰",
    layout="wide"
)

# App title and description
st.title("NewsBreeze 📰🔊")
st.markdown("### Your Celebrity-Powered Audio News Reader")

# Check if TTS is available
tts_available = load_tts_model()

# Sidebar for news sources and voices
st.sidebar.header("Settings")

# News sources
news_sources = {
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Reuters": "http://feeds.reuters.com/reuters/topNews",
    "The Guardian": "https://www.theguardian.com/world/rss",
    "The New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
}

selected_source = st.sidebar.selectbox(
    "Select News Source",
    list(news_sources.keys())
)

# Celebrity voices
celebrity_voices = [
    "Morgan Freeman",
    "Oprah Winfrey",
    "Barack Obama",
    "Emma Watson",
    "David Attenborough"
]

selected_voice = st.sidebar.selectbox(
    "Select Celebrity Voice",
    celebrity_voices
)

# Display TTS status
if not tts_available:
    st.sidebar.warning("""
    ⚠️ TTS package is not installed. Voice cloning is not available.
    
    To enable voice cloning, install the TTS package:
    ```
    pip install TTS
    ```
    """)

# Fetch and display news
if st.sidebar.button("Fetch Latest News"):
    with st.spinner("Fetching news..."):
        try:
            news_items = fetch_news(news_sources[selected_source])
            
            if news_items:
                st.session_state.news_items = news_items
                st.success(f"Successfully fetched {len(news_items)} news items!")
            else:
                st.error("Failed to fetch news. Please try again later.")
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            st.error(f"Error fetching news: {str(e)}")

# Display news items
if 'news_items' in st.session_state:
    for i, item in enumerate(st.session_state.news_items[:10]):  # Limit to 10 news items
        with st.expander(f"{i+1}. {item['title']}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                if 'summary' not in item:
                    with st.spinner("Generating summary..."):
                        try:
                            item['summary'] = summarize_text(item['description'])
                        except Exception as e:
                            logger.error(f"Error generating summary: {e}")
                            item['summary'] = item['description']
                            st.warning("Failed to generate summary. Using original text.")
                        
                st.markdown(f"**Original:** {item['description']}")
                st.markdown(f"**Summary:** {item['summary']}")
                st.markdown(f"[Read more]({item['link']})", unsafe_allow_html=True)
            
            with col2:
                audio_button = st.button(f"🔊 Play with {selected_voice}'s voice", key=f"play_{i}")
                
                if audio_button:
                    with st.spinner(f"Generating audio with {selected_voice}'s voice..."):
                        try:
                            audio_file = generate_voice_clone(item['summary'], selected_voice)
                            if audio_file and os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
                                st.audio(audio_file, format='audio/wav')
                            else:
                                st.error("Failed to generate audio. Please check if TTS package is installed.")
                        except Exception as e:
                            logger.error(f"Error generating audio: {e}")
                            st.error(f"Error generating audio: {str(e)}")
else:
    st.info("Click on 'Fetch Latest News' to get started.")

# Footer
st.markdown("---")
st.markdown("NewsBreeze | Powered by Hugging Face and Coqui XTTS-v2") 