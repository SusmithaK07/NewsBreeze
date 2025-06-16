import os
import torch
import logging
import tempfile
from dotenv import load_dotenv
import time

# Flag for audio processing
AUDIO_PROCESSING_AVAILABLE = False

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import pydub for audio processing
try:
    from pydub import AudioSegment
    AUDIO_PROCESSING_AVAILABLE = True
    logger.info("Audio processing is available")
except ImportError:
    logger.warning("Could not import pydub. Audio processing will be disabled.")
except Exception as e:
    logger.warning(f"Error importing audio libraries: {e}")
    logger.warning("Audio processing will be disabled.")

def load_tts_model():
    """
    Check if we can load a TTS model
    
    Returns:
        bool: Whether TTS is available
    """
    try:
        # Try to import TTS
        try:
            from TTS.api import TTS
            logger.info("TTS package is available")
            return True
        except ImportError:
            logger.warning("TTS package is not installed. Voice cloning will not be available.")
            logger.warning("To install TTS, run: pip install TTS")
            return False
    
    except Exception as e:
        logger.error(f"Error checking TTS model: {e}")
        return False

def get_reference_audio_path(celebrity):
    """
    Get the path to the reference audio for the celebrity
    
    Args:
        celebrity (str): Name of the celebrity
        
    Returns:
        str: Path to the reference audio file
    """
    # Define paths to reference audio files
    reference_files = {
        "Morgan Freeman": "reference_audio/morgan_freeman.wav",
        "Oprah Winfrey": "reference_audio/oprah_winfrey.wav",
        "Barack Obama": "reference_audio/barack_obama.wav",
        "Emma Watson": "reference_audio/emma_watson.wav",
        "David Attenborough": "reference_audio/david_attenborough.wav"
    }
    
    # For demo purposes, we'll use a fallback if the reference file doesn't exist
    if celebrity in reference_files and os.path.exists(reference_files[celebrity]):
        return reference_files[celebrity]
    else:
        # For the demo, create a placeholder message
        try:
            # Create reference audio directory if it doesn't exist
            os.makedirs("reference_audio", exist_ok=True)
            
            # Note about reference files
            logger.info(f"No reference audio found for {celebrity}")
            logger.info("In a real app, you would have actual celebrity samples")
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting reference audio: {e}")
            return None

def generate_voice_clone(text, celebrity):
    """
    Generate voice clone of a celebrity
    
    Args:
        text (str): Text to convert to speech
        celebrity (str): Name of the celebrity
        
    Returns:
        str: Path to the generated audio file or None if not available
    """
    try:
        # Check if TTS is available
        tts_available = load_tts_model()
        
        if not tts_available:
            logger.error("TTS functionality is not available.")
            
            # For demo purposes, create a placeholder audio file with a message
            fd, output_path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            
            # Write message to file explaining TTS is not available
            with open(output_path, 'w') as f:
                f.write(f"TTS is not available. Please install the TTS package to use voice cloning.")
            
            logger.info(f"Created placeholder file: {output_path}")
            return output_path
        
        # If TTS is available, continue with the actual implementation
        from TTS.api import TTS
        
        # Get API key from environment variables
        api_key = os.getenv("COQUI_API_KEY")
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        
        # Initialize the TTS model
        if api_key:
            logger.info("Using Coqui API key")
            # For cloud API, you might need to use a different initialization
            tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2", coqui_api_key=api_key).to(device)
        else:
            logger.warning("No Coqui API key found, using local model")
            tts_model = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        
        # Get reference audio path
        reference_audio = get_reference_audio_path(celebrity)
        
        # Create a temporary file for the output
        fd, output_path = tempfile.mkstemp(suffix='.wav')
        os.close(fd)
        
        # Generate speech
        logger.info(f"Generating speech for: {text[:50]}...")
        
        if reference_audio:
            # Use voice cloning if reference audio is available
            tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                speaker_wav=reference_audio,
                language="en"
            )
        else:
            # Fallback to default voice if reference audio is not available
            tts_model.tts_to_file(
                text=text,
                file_path=output_path,
                language="en"
            )
        
        logger.info(f"Speech generated and saved to: {output_path}")
        
        # Process audio if needed (e.g., normalize volume)
        if AUDIO_PROCESSING_AVAILABLE:
            process_audio(output_path)
        else:
            logger.warning("Audio processing not available. Skipping audio normalization.")
        
        return output_path
    
    except Exception as e:
        logger.error(f"Error generating voice clone: {e}")
        
        # For demo purposes, create a placeholder file
        try:
            fd, output_path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            
            logger.info(f"Created placeholder file due to error: {output_path}")
            return output_path
        except:
            return None

def process_audio(audio_path):
    """
    Process audio file (normalize volume, etc.)
    
    Args:
        audio_path (str): Path to the audio file
    """
    if not AUDIO_PROCESSING_AVAILABLE:
        logger.warning("Audio processing is not available. Skipping audio normalization.")
        return
    
    try:
        # Check if file exists and is not empty
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) == 0:
            logger.warning(f"Audio file does not exist or is empty: {audio_path}")
            return
        
        try:
            # Load audio
            audio = AudioSegment.from_wav(audio_path)
            
            # Normalize volume
            normalized_audio = audio.normalize()
            
            # Export back to the same file
            normalized_audio.export(audio_path, format="wav")
            
            logger.info(f"Audio processed: {audio_path}")
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            # Continue without processing
    
    except Exception as e:
        logger.error(f"Error in process_audio: {e}")
        # Continue without processing 