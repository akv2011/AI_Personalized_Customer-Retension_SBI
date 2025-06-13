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
        Detect language based on character patterns and script analysis
        """
        if not text or len(text.strip()) < 3:
            return 'en'  # Default to English for very short text
        
        # Count characters by script type
        dekanagari_count = 0
        tamil_count = 0
        english_count = 0
        
        for char in text:
            # Devanagari script (Hindi, Marathi, Sanskrit)
            if '\u0900' <= char <= '\u097F':
                dekanagari_count += 1
            # Tamil script
            elif '\u0B80' <= char <= '\u0BFF':
                tamil_count += 1
            # English alphabet
            elif char.isalpha():
                english_count += 1
        
        total_chars = dekanagari_count + tamil_count + english_count
        
        if total_chars == 0:
            return 'en'
        
        # Calculate percentages
        dekanagari_pct = dekanagari_count / total_chars if total_chars > 0 else 0
        tamil_pct = tamil_count / total_chars if total_chars > 0 else 0
        english_pct = english_count / total_chars if total_chars > 0 else 0
        
        # If more than 30% of characters are in a specific script, consider it that language
        if dekanagari_pct > 0.3:
            return 'hi'  # Default to Hindi for Devanagari script
        elif tamil_pct > 0.3:
            return 'ta'
        elif english_pct > 0.7:
            return 'en'
        else:
            # If mixed or unclear, default to English
            return 'en'
    
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