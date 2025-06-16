# NewsBreeze 📰🔊

A modern Streamlit application that transforms news reading into an immersive audio experience by fetching the latest headlines, summarizing them with AI, and reading them aloud using celebrity voice cloning technology.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0+-red.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![Coqui TTS](https://img.shields.io/badge/Coqui-XTTS--v2-green.svg)

## ✨ Features

- **Real-time News Aggregation**: Fetches latest headlines from major news sources via RSS feeds
- **AI-Powered Summarization**: Condenses news articles using Hugging Face's text summarization model
- **Celebrity Voice Cloning**: Reads summaries aloud using Coqui's XTTS-v2 voice cloning technology
- **Clean User Interface**: Intuitive Streamlit UI for seamless user experience
- **Multiple News Sources**: BBC, CNN, Reuters, The Guardian, and The New York Times

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **News Fetching**: Feedparser, BeautifulSoup4
- **Text Summarization**: Hugging Face Transformers (Falconsai/text_summarization)
- **Voice Generation**: Coqui XTTS-v2 (Text-to-Speech with voice cloning)
- **Audio Processing**: PyDub

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd NewsBreeze
   ```

2. **Set up a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **API Keys (Optional but Recommended)**

   Create a `.env` file in the root directory:
   ```
   # Hugging Face API key
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   
   # Coqui TTS API key (if using their cloud service)
   COQUI_API_KEY=your_coqui_api_key_here
   ```
   
   Obtain API keys from:
   - [Hugging Face](https://huggingface.co/settings/tokens)
   - [Coqui TTS](https://coqui.ai/)

   > Note: The application will work without API keys but may have rate limitations or slower performance.

6. **Launch the application**
   ```bash
   streamlit run app.py
   ```

7. **Access the web interface**
   
   Open your browser and navigate to `http://localhost:8501`

## 💡 Usage Guide

1. **Select a News Source**: Choose from the dropdown menu in the sidebar
2. **Fetch Latest News**: Click the "Fetch Latest News" button
3. **Browse Headlines**: Expand any headline to view the original article and AI-generated summary
4. **Choose a Voice**: Select a celebrity voice from the sidebar options
5. **Listen to News**: Click the "Play" button next to any summary to hear it read aloud in the selected voice

## 📋 Available News Sources

- BBC News
- CNN
- Reuters
- The Guardian
- The New York Times

## 🎤 Available Celebrity Voices

- Morgan Freeman
- Oprah Winfrey
- Barack Obama
- Emma Watson
- David Attenborough

## ⚠️ First Run Notice

The first run may take some time as the models are downloaded. Subsequent runs will be faster as models are cached.

## 🧩 Project Structure

```
NewsBreeze/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this file)
├── utils/
│   ├── __init__.py        # Package initializer
│   ├── news_fetcher.py    # RSS feed parser and content fetcher
│   ├── summarizer.py      # Text summarization using HuggingFace
│   └── voice_generator.py # Voice cloning using Coqui XTTS-v2
└── reference_audio/       # Directory for celebrity voice samples (create this)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the web framework
- [Hugging Face](https://huggingface.co/) for the text summarization model
- [Coqui](https://coqui.ai/) for the XTTS-v2 voice cloning technology 