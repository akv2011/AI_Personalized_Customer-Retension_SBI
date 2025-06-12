#!/usr/bin/env python3
"""
Simple manual recording test with Ctrl+C control
"""

import sys
import os
sys.path.append('/home/Arun/Desktop/Hack/AI_Personalized_Customer-Retension_SBI/backend/src')

from utils.speech_service import get_speech_service

def test_manual_recording():
    """Test manual recording with Ctrl+C control"""
    print("🎙️ Manual Voice Recording Test")
    print("=" * 50)
    print("• Press Ctrl+C to stop recording and transcribe")
    print("• Speak clearly into your microphone")
    print("• Test works with all languages")
    print("=" * 50)
    
    service = get_speech_service()
    
    while True:
        # Get language choice
        print("\nChoose language:")
        print("1. English (ElevenLabs STT)")
        print("2. Hindi (ElevenLabs STT)")  
        print("3. Marathi (Google STT)")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '4':
            print("Goodbye!")
            break
        
        language_map = {
            '1': 'english',
            '2': 'hindi', 
            '3': 'marathi'
        }
        
        language = language_map.get(choice)
        if not language:
            print("Invalid choice, please try again.")
            continue
        
        print(f"\n🗣️ Recording in {language.title()}...")
        print("Start speaking now, press Ctrl+C when done!")
        print("-" * 40)
        
        try:
            result = service.record_with_pyaudio(language)
            
            print(f"\n📊 Results:")
            print(f"Success: {result['success']}")
            print(f"Language: {language.title()}")
            print(f"Service: {result.get('service', 'Unknown')}")
            
            if result['success']:
                print(f"✅ Transcription: '{result['transcription']}'")
                print(f"Duration: {result.get('audio_duration', 'N/A'):.1f}s")
                print(f"Confidence: {result.get('confidence', 'N/A')}")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
                temp_file = result.get('temp_file')
                if temp_file:
                    print(f"Audio file saved for debugging: {temp_file}")
            
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\n⚠️ Recording interrupted before starting")
        except Exception as e:
            print(f"\n❌ Test error: {e}")

if __name__ == "__main__":
    test_manual_recording()
