from fastapi import APIRouter, HTTPException, Query
from typing import List
from pydantic import BaseModel
import logging

from src.services.translation_service import TranslationService

logger = logging.getLogger(__name__)
router = APIRouter()

class TranslationRequest(BaseModel):
    text: str
    target_lang: str = "ur"

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    target_lang: str

class BulkTranslationRequest(BaseModel):
    texts: List[str]
    target_lang: str = "ur"

class BulkTranslationResponse(BaseModel):
    original_texts: List[str]
    translated_texts: List[str]
    target_lang: str

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate a single text to the target language
    """
    try:
        translated_text = TranslationService.translate_text(
            request.text,
            request.target_lang
        )

        return TranslationResponse(
            original_text=request.text,
            translated_text=translated_text,
            target_lang=request.target_lang
        )
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail="Translation failed")

@router.post("/translate-bulk", response_model=BulkTranslationResponse)
async def translate_bulk_texts(request: BulkTranslationRequest):
    """
    Translate multiple texts to the target language
    """
    try:
        translated_texts = TranslationService.translate_multiple_texts(
            request.texts,
            request.target_lang
        )

        return BulkTranslationResponse(
            original_texts=request.texts,
            translated_texts=translated_texts,
            target_lang=request.target_lang
        )
    except Exception as e:
        logger.error(f"Bulk translation error: {e}")
        raise HTTPException(status_code=500, detail="Bulk translation failed")

# Health check endpoint
@router.get("/translate/health")
async def translation_health():
    """
    Health check for translation service
    """
    return {"status": "ok", "service": "translation"}