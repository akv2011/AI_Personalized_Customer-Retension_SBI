#!/usr/bin/env python3
"""
Test the improved speech service with PyAudio recording method
"""

import sys
import os
sys.path.append('/home/Arun/Desktop/Hack/AI_Personalized_Customer-Retension_SBI/backend/src')

from utils.speech_service import get_speech_service

def test_pyaudio_recording():
    """Test the new PyAudio recording method"""
    print("🎙️ Testing Improved Voice Recording with PyAudio")
    print("=" * 60)
    
    service = get_speech_service()
    
    # Test different languages
    languages = ['english', 'hindi', 'marathi']
    
    for language in languages:
        print(f"\n🗣️ Testing {language.title()} STT...")
        print(f"Speak in {language} now...")
        
        result = service.record_with_pyaudio(language)
        
        print(f"Success: {result['success']}")
        if result['success']:
            print(f"Transcription: '{result['transcription']}'")
            print(f"Service: {result.get('service', 'unknown')}")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        
        print("-" * 40)
        
        # Ask if user wants to continue
        if language != languages[-1]:
            input(f"Press Enter to test {languages[languages.index(language) + 1]}...")

if __name__ == "__main__":
    test_pyaudio_recording()
