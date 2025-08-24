from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import logging
from pydantic import BaseModel
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="Langchain Translation Server",
    version="1.0",
    description="A beautiful translation API server using Langchain and Groq"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List of available Groq models
WORKING_MODELS = [
    "llama3-8b-8192",
    "llama3-70b-8192", 
    "gemma2-9b-it",
]

# Language mapping with emojis
LANGUAGE_MAP = {
    "English": {"code": "en", "emoji": "🇺🇸"},
    "French": {"code": "fr", "emoji": "🇫🇷"},
    "Hindi": {"code": "hi", "emoji": "🇮🇳"},
    "Spanish": {"code": "es", "emoji": "🇪🇸"},
    "German": {"code": "de", "emoji": "🇩🇪"},
    "Italian": {"code": "it", "emoji": "🇮🇹"},
    "Portuguese": {"code": "pt", "emoji": "🇵🇹"},
    "Dutch": {"code": "nl", "emoji": "🇳🇱"},
    "Russian": {"code": "ru", "emoji": "🇷🇺"},
    "Arabic": {"code": "ar", "emoji": "🇸🇦"},
    "Chinese": {"code": "zh", "emoji": "🇨🇳"},
    "Japanese": {"code": "ja", "emoji": "🇯🇵"},
    "Korean": {"code": "ko", "emoji": "🇰🇷"},
    "Turkish": {"code": "tr", "emoji": "🇹🇷"},
    "Greek": {"code": "el", "emoji": "🇬🇷"}
}

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Translation server is running"}

# Get available models
@app.get("/models")
async def get_models():
    return {"models": WORKING_MODELS}

# Get available languages
@app.get("/languages")
async def get_languages():
    return {"languages": list(LANGUAGE_MAP.keys())}

# Check if Groq API key is available
@app.get("/check_groq")
async def check_groq():
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        return {"status": "error", "message": "GROQ_API_KEY not found in environment variables"}
    
    try:
        test_model = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key, timeout=10)
        prompt = ChatPromptTemplate.from_template("Say hello in French")
        chain = prompt | test_model | StrOutputParser()
        result = chain.invoke({})
        return {
            "status": "success", 
            "message": "Groq API is working",
            "working_models": WORKING_MODELS,
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Groq API test failed: {str(e)}",
        }

# Translation request model
class TranslationRequest(BaseModel):
    text: str
    language: str
    model: Optional[str] = "llama3-8b-8192"

# Mock translator for fallback
def mock_translator(text, language):
    """Mock translator for when Groq API fails"""
    translations = {
        "English": f"English translation: {text}",
        "French": f"Traduction française: {text}",
        "Hindi": f"हिंदी अनुवाद: {text}",
        "Spanish": f"Traducción española: {text}",
        "German": f"Deutsche Übersetzung: {text}",
        "Italian": f"Traduzione italiana: {text}",
        "Portuguese": f"Tradução portuguesa: {text}",
        "Dutch": f"Nederlandse vertaling: {text}",
        "Russian": f"Русский перевод: {text}",
        "Arabic": f"الترجمة العربية: {text}",
        "Chinese": f"中文翻译: {text}",
        "Japanese": f"日本語訳: {text}",
        "Korean": f"한국어 번역: {text}",
        "Turkish": f"Türkçe çeviri: {text}",
        "Greek": f"Ελληνική μετάφραση: {text}"
    }
    return translations.get(language, f"Translation to {language}: {text}")

# Main translation endpoint
@app.post("/translate")
async def translate_text(request: TranslationRequest):
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    # Validate input
    if not request.text or not request.text.strip():
        return {
            "output": "Error: Text is required",
            "status": "error", 
            "message": "Text is required",
            "model_used": "none",
            "source": "validation"
        }
    
    if request.language not in LANGUAGE_MAP:
        return {
            "output": f"Error: Language '{request.language}' not supported",
            "status": "error", 
            "message": f"Language '{request.language}' not supported",
            "model_used": "none",
            "source": "validation"
        }
    
    # Validate model selection
    if request.model not in WORKING_MODELS:
        request.model = "llama3-8b-8192"
    
    # Try Groq API first
    if groq_api_key:
        try:
            # Initialize model
            model = ChatGroq(model=request.model, groq_api_key=groq_api_key, timeout=30)
            
            # Create prompt template
            prompt_template = ChatPromptTemplate.from_messages([
                ('system', "You are a professional translator. Translate the following text into {language}. Provide only the translation without any additional text, explanations, or notes. Ensure the translation is accurate and natural sounding:"),
                ('user', '{text}')
            ])
            
            # Create chain
            chain = prompt_template | model | StrOutputParser()
            
            # Invoke the chain
            result = chain.invoke({"language": request.language, "text": request.text})
            
            return {
                "output": result, 
                "status": "success", 
                "model_used": request.model,
                "language": request.language,
                "source": "groq_api"
            }
            
        except Exception as e:
            logger.error(f"Groq API translation error: {e}")
            # Fall through to mock translator
    
    # Fallback to mock translator
    try:
        mock_result = mock_translator(request.text, request.language)
        return {
            "output": mock_result, 
            "status": "partial_success", 
            "model_used": "mock_translator",
            "language": request.language,
            "source": "mock_translator",
            "message": "Groq API unavailable, using mock translator"
        }
    except Exception as e:
        logger.error(f"Mock translator error: {e}")
        return {
            "output": f"Error: All translation methods failed - {str(e)}",
            "status": "error", 
            "message": f"All translation methods failed: {str(e)}",
            "model_used": "none",
            "source": "error"
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")