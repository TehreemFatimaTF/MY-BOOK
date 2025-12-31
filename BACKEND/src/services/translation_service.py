import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class TranslationService:
    """
    Service to handle translation using free APIs
    """

    @staticmethod
    def translate_text(text: str, target_lang: str = 'ur') -> Optional[str]:
        """
        Translate text using free translation APIs
        """
        if not text.strip():
            return text

        # Try MyMemory API first (free, no key required)
        try:
            source_lang = 'en'
            target_code = target_lang
            source_code = source_lang

            url = f"https://api.mymemory.translated.net/get?q={text}&langpair={source_code}|{target_code}"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                translated_text = data.get('responseData', {}).get('translatedText', text)
                return translated_text
            else:
                logger.warning(f"MyMemory API failed with status {response.status_code}")
        except Exception as e:
            logger.error(f"MyMemory API error: {e}")

        # Fallback: Return original text if all APIs fail
        return text

    @staticmethod
    def translate_multiple_texts(texts: list, target_lang: str = 'ur') -> list:
        """
        Translate multiple texts
        """
        results = []
        for text in texts:
            translated = TranslationService.translate_text(text, target_lang)
            results.append(translated)
        return results