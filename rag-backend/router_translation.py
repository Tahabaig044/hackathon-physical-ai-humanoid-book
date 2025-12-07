from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging

router = APIRouter(prefix="/translate", tags=["translation"])

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "ur"  # Default to Urdu

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str

# Mock translation function - in a real implementation, this would call a translation API
def mock_translate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Mock translation function - in a real implementation, this would integrate with
    a translation service like Google Translate API, Microsoft Translator, etc.
    """
    # For this mock implementation, we'll just return a placeholder
    # In a real implementation, you would call an actual translation service
    if target_lang.lower() == 'ur' and source_lang.lower() == 'en':
        # This is just a placeholder - in reality, you'd use a proper translation API
        return f"MOCK TRANSLATION: {text}"
    else:
        return text  # Return original text if not English to Urdu

@router.post("/", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text from source language to target language
    """
    try:
        # Validate language codes
        supported_languages = ["en", "ur"]  # English and Urdu
        if request.source_lang not in supported_languages or request.target_lang not in supported_languages:
            raise HTTPException(status_code=400, detail="Unsupported language code. Supported: en, ur")

        # Perform translation (mock implementation)
        translated_text = mock_translate(
            request.text,
            request.source_lang,
            request.target_lang
        )

        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in translation: {e}")
        raise HTTPException(status_code=500, detail="Translation service error")

# Alternative endpoint for batch translation
class BatchTranslationRequest(BaseModel):
    texts: list[str]
    source_lang: str = "en"
    target_lang: str = "ur"

class BatchTranslationResponse(BaseModel):
    translations: list[TranslationResponse]

@router.post("/batch", response_model=BatchTranslationResponse)
async def translate_batch(request: BatchTranslationRequest):
    """
    Translate multiple texts from source language to target language
    """
    try:
        translations = []
        for text in request.texts:
            translated_text = mock_translate(text, request.source_lang, request.target_lang)
            translations.append(
                TranslationResponse(
                    original_text=text,
                    translated_text=translated_text,
                    source_lang=request.source_lang,
                    target_lang=request.target_lang
                )
            )

        return BatchTranslationResponse(translations=translations)
    except Exception as e:
        logging.error(f"Error in batch translation: {e}")
        raise HTTPException(status_code=500, detail="Batch translation service error")