import os
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable for the summarizer
summarizer = None

def load_summarizer():
    """
    Load the summarization model
    
    Returns:
        pipeline: Hugging Face summarization pipeline
    """
    global summarizer
    
    try:
        if summarizer is None:
            logger.info("Loading summarization model...")
            
            # Get API key from environment variables
            api_key = os.getenv("HUGGINGFACE_API_KEY")
            
            # Use Falconsai/text_summarization model
            model_name = "Falconsai/text_summarization"
            
            # Load tokenizer and model with API key if available
            if api_key:
                logger.info("Using Hugging Face API key")
                tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=api_key)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name, use_auth_token=api_key)
            else:
                logger.warning("No Hugging Face API key found, trying to download models anonymously")
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            # Create summarization pipeline
            summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
            
            logger.info("Summarization model loaded successfully.")
        
        return summarizer
    
    except Exception as e:
        logger.error(f"Error loading summarization model: {e}")
        return None

def summarize_text(text, max_length=150, min_length=30):
    """
    Summarize text using Hugging Face's summarization pipeline
    
    Args:
        text (str): Text to summarize
        max_length (int): Maximum length of summary
        min_length (int): Minimum length of summary
        
    Returns:
        str: Summarized text
    """
    try:
        # Check if text is too short
        if len(text.split()) < min_length:
            return text
        
        # Load summarizer if not already loaded
        sum_pipeline = load_summarizer()
        
        if sum_pipeline is None:
            logger.error("Failed to load summarizer.")
            return text
        
        # Truncate input text if it's too long
        max_input_length = 1024  # Most models have a limit
        tokenizer = sum_pipeline.tokenizer
        
        # Tokenize and truncate if necessary
        tokens = tokenizer.encode(text, truncation=True, max_length=max_input_length)
        truncated_text = tokenizer.decode(tokens, skip_special_tokens=True)
        
        # Generate summary
        summary = sum_pipeline(
            truncated_text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        
        # Extract summary text
        if summary and len(summary) > 0:
            return summary[0]['summary_text']
        else:
            return text
    
    except Exception as e:
        logger.error(f"Error summarizing text: {e}")
        return text 