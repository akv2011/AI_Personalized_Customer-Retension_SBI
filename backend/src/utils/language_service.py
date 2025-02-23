# backend/src/utils/language_service.py

from typing import Dict, Optional
from deep_translator import GoogleTranslator

class LanguageService:
    def __init__(self):
        self.supported_languages = {
            'en': 'english',
            'ta': 'tamil',
            'hi': 'hindi'
        }
    
    def detect_language(self, text: str) -> str:
        """
        Since deep-translator doesn't have language detection,
        we'll rely on the language parameter from the frontend
        """
        return 'en'  # Default to English if not specified
    
    def translate_to_english(self, text: str, source_lang: str = 'auto') -> str:
        """Translate any supported language to English"""
        try:
            if source_lang == 'en':
                return text
                
            translator = GoogleTranslator(source=source_lang, target='en')
            return translator.translate(text)
        except Exception as e:
            print(f"Error translating to English: {e}")
            return text
    
    def translate_from_english(self, text: str, target_lang: str) -> str:
        """Translate English text to target language"""
        try:
            if target_lang == 'en':
                return text
                
            translator = GoogleTranslator(source='en', target=target_lang)
            return translator.translate(text)
        except Exception as e:
            print(f"Error translating from English: {e}")
            return text

    def get_supported_languages(self) -> Dict[str, str]:
        """Return dictionary of supported languages"""
        return self.supported_languages