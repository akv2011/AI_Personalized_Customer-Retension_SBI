#!/usr/bin/env python3
"""
Test script for voice endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_speech_to_text():
    """Test speech-to-text endpoint"""
    print("Testing Speech-to-Text endpoint...")
    
    # Create a simple test audio file (silent audio for testing)
    import io
    import wave
    
    # Create a simple silent WAV file for testing
    with io.BytesIO() as buffer:
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(44100)  # 44.1 kHz
            wav_file.writeframes(b'\x00' * 44100)  # 1 second of silence
        
        buffer.seek(0)
        audio_data = buffer.read()
    
    files = {'audio': ('test.wav', audio_data, 'audio/wav')}
    data = {'language': 'en'}
    
    try:
        response = requests.post(f"{BASE_URL}/api/speech/speech-to-text", files=files, data=data)
        print(f"STT Response: {response.status_code}")
        if response.status_code == 200:
            print(f"STT Result: {response.json()}")
        else:
            print(f"STT Error: {response.text}")
    except Exception as e:
        print(f"STT Request failed: {e}")

def test_text_to_speech():
    """Test text-to-speech endpoint"""
    print("\nTesting Text-to-Speech endpoint...")
    
    data = {
        'text': 'Hello, this is a test message.',
        'language': 'en'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/speech/text-to-speech", json=data)
        print(f"TTS Response: {response.status_code}")
        if response.status_code == 200:
            print(f"TTS Success: Audio data received ({len(response.content)} bytes)")
        else:
            print(f"TTS Error: {response.text}")
    except Exception as e:
        print(f"TTS Request failed: {e}")

def test_chatbot_endpoint():
    """Test chatbot endpoint"""
    print("\nTesting Chatbot endpoint...")
    
    data = {
        'message': 'Tell me about Smart Swadhan Supreme',
        'language': 'en'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/chat", json=data)
        print(f"Chat Response: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Chat Success: {result.get('response', 'No response')[:100]}...")
        else:
            print(f"Chat Error: {response.text}")
    except Exception as e:
        print(f"Chat Request failed: {e}")

if __name__ == "__main__":
    print("Testing Voice Endpoints...")
    print("=" * 50)
    
    test_text_to_speech()
    test_speech_to_text()
    test_chatbot_endpoint()
    
    print("\n" + "=" * 50)
    print("Voice endpoint testing completed!")
