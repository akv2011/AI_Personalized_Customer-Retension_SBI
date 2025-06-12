#!/usr/bin/env python3
"""
Complete Voice Functionality Test
Tests the complete voice workflow: STT -> Chat -> TTS
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:5000"

def test_complete_voice_workflow():
    """Test the complete voice workflow"""
    print("Testing Complete Voice Workflow...")
    print("=" * 60)
    
    # Test 1: Text-to-Speech (TTS)
    print("\n1. Testing Text-to-Speech (Hindi)...")
    tts_data = {
        "text": "नमस्ते! SBI Life Insurance में आपका स्वागत है।",
        "language": "hi"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/speech/text-to-speech", json=tts_data)
        print(f"TTS Response Code: {response.status_code}")
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"TTS Success: Audio data received ({len(audio_data)} bytes)")
            
            # Save audio file for testing
            with open("test_output_hindi.wav", "wb") as f:
                f.write(audio_data)
            print("Audio saved as test_output_hindi.wav")
        else:
            print(f"TTS Error: {response.text}")
    except Exception as e:
        print(f"TTS Exception: {e}")
    
    # Test 2: Text-to-Speech (English)
    print("\n2. Testing Text-to-Speech (English)...")
    tts_data = {
        "text": "Welcome to SBI Life Insurance! How can I help you today?",
        "language": "en"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/speech/text-to-speech", json=tts_data)
        print(f"TTS Response Code: {response.status_code}")
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"TTS Success: Audio data received ({len(audio_data)} bytes)")
            
            # Save audio file for testing
            with open("test_output_english.wav", "wb") as f:
                f.write(audio_data)
            print("Audio saved as test_output_english.wav")
        else:
            print(f"TTS Error: {response.text}")
    except Exception as e:
        print(f"TTS Exception: {e}")
    
    # Test 3: Text-to-Speech (Marathi)
    print("\n3. Testing Text-to-Speech (Marathi)...")
    tts_data = {
        "text": "नमस्कार! SBI Life Insurance मध्ये आपले स्वागत आहे।",
        "language": "mr"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/speech/text-to-speech", json=tts_data)
        print(f"TTS Response Code: {response.status_code}")
        
        if response.status_code == 200:
            audio_data = response.content
            print(f"TTS Success: Audio data received ({len(audio_data)} bytes)")
            
            # Save audio file for testing
            with open("test_output_marathi.wav", "wb") as f:
                f.write(audio_data)
            print("Audio saved as test_output_marathi.wav")
        else:
            print(f"TTS Error: {response.text}")
    except Exception as e:
        print(f"TTS Exception: {e}")
    
    # Test 4: Chatbot (English)
    print("\n4. Testing Chatbot (English)...")
    chat_data = {
        "customer_id": "test_customer_001",
        "user_input_text": "Tell me about Smart Swadhan Supreme policy",
        "language": "en"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=chat_data)
        print(f"Chat Response Code: {response.status_code}")
        
        if response.status_code == 200:
            chat_response = response.json()
            print("Chat Success!")
            print(f"Response: {chat_response.get('response', 'No response')[:200]}...")
        else:
            print(f"Chat Error: {response.text}")
    except Exception as e:
        print(f"Chat Exception: {e}")
    
    # Test 5: Chatbot (Hindi)
    print("\n5. Testing Chatbot (Hindi)...")
    chat_data = {
        "customer_id": "test_customer_002",
        "user_input_text": "स्मार्ट स्वाधन सुप्रीम पॉलिसी के बारे में बताइए",
        "language": "hi"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=chat_data)
        print(f"Chat Response Code: {response.status_code}")
        
        if response.status_code == 200:
            chat_response = response.json()
            print("Chat Success!")
            print(f"Response: {chat_response.get('response', 'No response')[:200]}...")
            
            # Test TTS with the chat response
            print("\n6. Testing TTS with Chat Response (Hindi)...")
            tts_data = {
                "text": chat_response.get('response', 'No response'),
                "language": "hi"
            }
            
            tts_response = requests.post(f"{BASE_URL}/api/speech/text-to-speech", json=tts_data)
            if tts_response.status_code == 200:
                audio_data = tts_response.content
                print(f"TTS Success: Chat response converted to audio ({len(audio_data)} bytes)")
                
                # Save audio file
                with open("test_chat_response_hindi.wav", "wb") as f:
                    f.write(audio_data)
                print("Chat response audio saved as test_chat_response_hindi.wav")
            else:
                print(f"TTS Error: {tts_response.text}")
        else:
            print(f"Chat Error: {response.text}")
    except Exception as e:
        print(f"Chat Exception: {e}")
    
    print("\n" + "=" * 60)
    print("Complete Voice Workflow Testing Finished!")
    print("\nGenerated Audio Files:")
    for filename in ["test_output_hindi.wav", "test_output_english.wav", "test_output_marathi.wav", "test_chat_response_hindi.wav"]:
        if os.path.exists(filename):
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} (not created)")

if __name__ == "__main__":
    test_complete_voice_workflow()
