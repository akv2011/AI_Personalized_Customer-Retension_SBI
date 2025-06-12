"""
Comprehensive Speech Service for SBI Life Customer Retention
- ElevenLabs for Hindi and English (TTS + STT)
- Free solutions for Marathi (gTTS + speech_recognition)
"""

import os
import logging
import io
import tempfile
import requests
import json
from typing import Optional, Dict, Any, Union
from pathlib import Path

# Free TTS/STT imports
try:
    import pyttsx3
    import gtts
    import speech_recognition as sr
    import pygame
    from pydub import AudioSegment
    from pydub.playback import play
except ImportError as e:
    logging.warning(f"Some speech libraries not installed: {e}")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpeechService:
    """Unified Speech Service with ElevenLabs and Free alternatives"""
    
    def __init__(self):
        # ElevenLabs configuration
        self.elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
        self.elevenlabs_base_url = "https://api.elevenlabs.io/v1"
        
        # Language configuration
        self.language_config = {
            'hindi': {
                'code': 'hi',
                'gtts_lang': 'hi',
                'use_elevenlabs': True,  # Keep ElevenLabs for TTS only
                'elevenlabs_voice_id': 'pNInz6obpgDQGcFmaJgB',  # Default Hindi voice
                'elevenlabs_model': 'eleven_multilingual_v2',
                'speech_recognition_lang': 'hi-IN',
                'use_google_stt': True  # Force Google STT for all languages
            },
            'english': {
                'code': 'en',
                'gtts_lang': 'en',
                'use_elevenlabs': True,  # Keep ElevenLabs for TTS only
                'elevenlabs_voice_id': 'EXAVITQu4vr4xnSDxMaL',  # Default English voice
                'elevenlabs_model': 'eleven_turbo_v2',
                'speech_recognition_lang': 'en-US',
                'use_google_stt': True  # Force Google STT for all languages
            },
            'marathi': {
                'code': 'mr',
                'gtts_lang': 'mr',
                'use_elevenlabs': False,  # Use Google TTS for Marathi
                'speech_recognition_lang': 'mr-IN',
                'use_google_stt': True  # Force Google STT for all languages
            }
        }
        
        # Initialize free TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            self.setup_pyttsx3()
        except Exception as e:
            logger.warning(f"Could not initialize pyttsx3: {e}")
            self.tts_engine = None
        
        # Initialize speech recognition
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.calibrate_microphone()
        except Exception as e:
            logger.warning(f"Could not initialize speech recognition: {e}")
            self.recognizer = None
            self.microphone = None
    
    def setup_pyttsx3(self):
        """Configure pyttsx3 TTS engine"""
        if self.tts_engine:
            # Set properties
            self.tts_engine.setProperty('rate', 150)  # Speed
            self.tts_engine.setProperty('volume', 0.9)  # Volume
            
            # Try to set a voice
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
    
    def calibrate_microphone(self):
        """Calibrate microphone for better recognition"""
        if self.recognizer and self.microphone:
            try:
                with self.microphone as source:
                    logger.info("Calibrating microphone for ambient noise...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                    logger.info("Microphone calibrated successfully")
            except Exception as e:
                logger.warning(f"Microphone calibration failed: {e}")
    
    # ==================== TEXT TO SPEECH ====================
    
    def text_to_speech(self, text: str, language: str = 'english', save_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert text to speech using appropriate service based on language
        
        Args:
            text: Text to convert to speech
            language: Language ('hindi', 'english', 'marathi')
            save_path: Optional path to save audio file
            
        Returns:
            Dict with success status and audio data/path
        """
        try:
            lang_config = self.language_config.get(language.lower())
            if not lang_config:
                raise ValueError(f"Unsupported language: {language}")
            
            if lang_config['use_elevenlabs'] and self.elevenlabs_api_key:
                return self._elevenlabs_tts(text, lang_config, save_path)
            else:
                return self._free_tts(text, lang_config, save_path)
                
        except Exception as e:
            logger.error(f"TTS error for {language}: {e}")
            return {
                'success': False,
                'error': str(e),
                'language': language
            }
    
    def _elevenlabs_tts(self, text: str, lang_config: Dict, save_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate speech using ElevenLabs API"""
        try:
            url = f"{self.elevenlabs_base_url}/text-to-speech/{lang_config['elevenlabs_voice_id']}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_api_key
            }
            
            data = {
                "text": text,
                "model_id": lang_config['elevenlabs_model'],
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5,
                    "style": 0.0,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            # Save or return audio data
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return {
                    'success': True,
                    'audio_path': save_path,
                    'service': 'elevenlabs',
                    'language': lang_config['code']
                }
            else:
                return {
                    'success': True,
                    'audio_data': response.content,
                    'service': 'elevenlabs',
                    'language': lang_config['code']
                }
                
        except Exception as e:
            logger.error(f"ElevenLabs TTS error: {e}")
            # Fallback to free TTS
            return self._free_tts(text, lang_config, save_path)
    
    def _free_tts(self, text: str, lang_config: Dict, save_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate speech using free TTS (gTTS or pyttsx3)"""
        try:
            # Try gTTS first (requires internet)
            try:
                from gtts import gTTS
                tts = gTTS(text=text, lang=lang_config['gtts_lang'], slow=False)
                
                if save_path:
                    tts.save(save_path)
                    return {
                        'success': True,
                        'audio_path': save_path,
                        'service': 'gtts',
                        'language': lang_config['code']
                    }
                else:
                    # Save to temporary file and return data
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                        tts.save(temp_file.name)
                        with open(temp_file.name, 'rb') as f:
                            audio_data = f.read()
                        os.unlink(temp_file.name)
                        
                        return {
                            'success': True,
                            'audio_data': audio_data,
                            'service': 'gtts',
                            'language': lang_config['code']
                        }
                        
            except Exception as gtts_error:
                logger.warning(f"gTTS failed: {gtts_error}, trying pyttsx3")
                
                # Fallback to pyttsx3 (offline)
                if self.tts_engine:
                    if save_path:
                        self.tts_engine.save_to_file(text, save_path)
                        self.tts_engine.runAndWait()
                    else:
                        # For pyttsx3, we can only play directly
                        self.tts_engine.say(text)
                        self.tts_engine.runAndWait()
                    
                    return {
                        'success': True,
                        'audio_path': save_path if save_path else None,
                        'service': 'pyttsx3',
                        'language': lang_config['code']
                    }
                else:
                    raise Exception("No TTS engine available")
                    
        except Exception as e:
            logger.error(f"Free TTS error: {e}")
            return {
                'success': False,
                'error': str(e),
                'service': 'free_tts',
                'language': lang_config['code']
            }
    
    # ==================== SPEECH TO TEXT ====================
    
    def speech_to_text(self, audio_source: Union[str, bytes], language: str = 'english') -> Dict[str, Any]:
        """
        Convert speech to text using Google STT for all languages (working reliably)
        
        Args:
            audio_source: Audio file path or audio bytes
            language: Language ('hindi', 'english', 'marathi')
            
        Returns:
            Dict with transcription and confidence
        """
        try:
            lang_config = self.language_config.get(language.lower())
            if not lang_config:
                raise ValueError(f"Unsupported language: {language}")
            
            # Use Google STT for all languages since it's working well
            return self._free_stt(audio_source, lang_config)
                
        except Exception as e:
            logger.error(f"STT error for {language}: {e}")
            return {
                'success': False,
                'error': str(e),
                'language': language
            }
    
    def _elevenlabs_stt(self, audio_source: Union[str, bytes], lang_config: Dict) -> Dict[str, Any]:
        """Transcribe speech using ElevenLabs API"""
        try:
            url = f"{self.elevenlabs_base_url}/speech-to-text"
            
            headers = {
                "xi-api-key": self.elevenlabs_api_key
            }
            
            # Prepare and convert audio data
            audio_data = None
            temp_file_path = None
            
            try:
                if isinstance(audio_source, str):
                    # Convert audio file to proper format
                    temp_file_path = self._convert_audio_for_stt(audio_source)
                    with open(temp_file_path, 'rb') as f:
                        audio_data = f.read()
                    filename = "audio.mp3"  # ElevenLabs prefers MP3
                else:
                    # Convert bytes to proper format
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                        temp_file.write(audio_source)
                        temp_source_path = temp_file.name
                    
                    temp_file_path = self._convert_audio_for_stt(temp_source_path)
                    with open(temp_file_path, 'rb') as f:
                        audio_data = f.read()
                    filename = "audio.mp3"
                
                files = {
                    'audio': (filename, audio_data, 'audio/mpeg')
                }
                
                # ElevenLabs STT doesn't need model_id for basic transcription
                response = requests.post(url, headers=headers, files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        'success': True,
                        'transcription': result.get('text', ''),
                        'confidence': 0.9,  # ElevenLabs doesn't provide confidence
                        'service': 'elevenlabs',
                        'language': lang_config['code']
                    }
                else:
                    logger.error(f"ElevenLabs STT HTTP error: {response.status_code} - {response.text}")
                    raise Exception(f"HTTP {response.status_code}: {response.text}")
                    
            finally:
                # Clean up temporary files
                if temp_file_path and os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                if isinstance(audio_source, bytes) and 'temp_source_path' in locals() and os.path.exists(temp_source_path):
                    os.unlink(temp_source_path)
            
        except Exception as e:
            logger.error(f"ElevenLabs STT error: {e}")
            # Fallback to free STT
            return self._free_stt(audio_source, lang_config)
    
    def _free_stt(self, audio_source: Union[str, bytes], lang_config: Dict) -> Dict[str, Any]:
        """Transcribe speech using free STT (speech_recognition with Google)"""
        try:
            if not self.recognizer:
                raise Exception("Speech recognition not available")
            
            # Convert audio to WAV format for speech_recognition
            wav_file = self._convert_to_wav(audio_source)
            
            try:
                # Transcribe using speech_recognition
                with sr.AudioFile(wav_file) as source:
                    # Adjust for ambient noise
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = self.recognizer.record(source)
                
                # Try Google Speech Recognition (free)
                try:
                    speech_lang = lang_config.get('speech_recognition_lang', lang_config['code'])
                    transcription = self.recognizer.recognize_google(audio, language=speech_lang)
                    
                    return {
                        'success': True,
                        'transcription': transcription,
                        'confidence': 0.8,  # Google doesn't provide confidence
                        'service': 'google_speech',
                        'language': lang_config['code']
                    }
                    
                except sr.UnknownValueError:
                    return {
                        'success': False,
                        'error': 'Could not understand audio',
                        'service': 'google_speech',
                        'language': lang_config['code']
                    }
                except sr.RequestError as e:
                    logger.error(f"Google Speech Recognition error: {e}")
                    
                    # Fallback to offline recognition if available
                    try:
                        transcription = self.recognizer.recognize_sphinx(audio)
                        return {
                            'success': True,
                            'transcription': transcription,
                            'confidence': 0.6,
                            'service': 'sphinx',
                            'language': lang_config['code']
                        }
                    except Exception as sphinx_error:
                        logger.warning(f"Sphinx STT also failed: {sphinx_error}")
                        raise Exception("All STT services failed")
                        
            finally:
                # Clean up temporary WAV file
                if isinstance(audio_source, bytes) and os.path.exists(wav_file):
                    os.unlink(wav_file)
            
        except Exception as e:
            logger.error(f"Free STT error: {e}")
            return {
                'success': False,
                'error': str(e),
                'service': 'free_stt',
                'language': lang_config['code']
            }
    
    # ==================== LIVE RECORDING ====================
    
    def record_from_microphone(self, duration: int = 5, language: str = 'english') -> Dict[str, Any]:
        """
        Record audio from microphone and transcribe
        
        Args:
            duration: Recording duration in seconds
            language: Language for transcription
            
        Returns:
            Dict with transcription result
        """
        try:
            if not self.recognizer or not self.microphone:
                raise Exception("Microphone not available")
            
            logger.info(f"Recording for {duration} seconds...")
            
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record audio
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            
            logger.info("Recording completed, transcribing...")
            
            # Convert to audio data
            audio_data = audio.get_wav_data()
            
            # Transcribe
            result = self.speech_to_text(audio_data, language)
            result['recording_duration'] = duration
            
            return result
            
        except Exception as e:
            logger.error(f"Microphone recording error: {e}")
            return {
                'success': False,
                'error': str(e),
                'recording_duration': duration
            }
    
    def record_with_pyaudio(self, language: str = 'english') -> Dict[str, Any]:
        """
        Record audio using PyAudio with manual stop (Ctrl+C only)
        
        Args:
            language: Language for transcription
            
        Returns:
            Dict with transcription result
        """
        try:
            import pyaudio
            import wave
            from io import BytesIO
            
            # Audio settings (same as your working script)
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            CHUNK = 1024
            
            # Initialize audio
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                              input=True, frames_per_buffer=CHUNK)
            
            logger.info("🎙️ Recording... Press Ctrl+C to stop and transcribe.")
            
            frames = []
            
            try:
                while True:
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                    
                    # Show progress every 2 seconds
                    if len(frames) % (2 * RATE // CHUNK) == 0:
                        duration = len(frames) * CHUNK / RATE
                        logger.info(f"Recording... {duration:.1f}s (Press Ctrl+C to stop)")
                        
            except KeyboardInterrupt:
                logger.info("✅ Recording stopped by user")
            
            stream.stop_stream()
            stream.close()
            audio.terminate()
            
            if not frames:
                return {
                    'success': False,
                    'error': 'No audio recorded',
                    'language': language
                }
            
            duration = len(frames) * CHUNK / RATE
            logger.info(f"📝 Recording complete ({duration:.1f}s), transcribing...")
            
            # Save to temporary file for debugging
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_path = temp_file.name
            
            # Create WAV file
            wf = wave.open(temp_path, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            logger.info(f"Audio saved to: {temp_path}")
            
            # Transcribe using the speech service
            result = self.speech_to_text(temp_path, language)
            result['recording_method'] = 'pyaudio'
            result['audio_duration'] = duration
            result['temp_file'] = temp_path
            
            # Keep temp file for debugging if transcription fails
            if result['success']:
                try:
                    os.unlink(temp_path)
                except:
                    pass
            else:
                logger.info(f"Transcription failed. Audio file kept at: {temp_path}")
            
            return result
            
        except Exception as e:
            logger.error(f"PyAudio recording error: {e}")
            return {
                'success': False,
                'error': str(e),
                'language': language,
                'recording_method': 'pyaudio'
            }

    # ==================== UTILITY METHODS ====================
    
    def _convert_audio_for_stt(self, audio_path: str) -> str:
        """Convert audio to format suitable for ElevenLabs STT (supports WebM, MP4, OGG, WAV, MP3)"""
        try:
            logger.info(f"Converting audio file: {audio_path}")
            
            # Load audio using pydub (supports WebM, MP4, OGG, WAV, MP3)
            audio = AudioSegment.from_file(audio_path)
            
            # Convert to format suitable for ElevenLabs (MP3, 16kHz, mono)
            audio = audio.set_frame_rate(16000).set_channels(1)
            
            # Generate temporary path for converted file
            import tempfile
            temp_fd, temp_path = tempfile.mkstemp(suffix='_converted.mp3')
            os.close(temp_fd)  # Close the file descriptor, pydub will create new file
            
            # Export as MP3 for ElevenLabs STT
            audio.export(temp_path, format="mp3", bitrate="64k")
            
            logger.info(f"Audio converted successfully: {audio_path} -> {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"Audio conversion error for {audio_path}: {e}")
            # Try to continue with original file
            return audio_path

    def _convert_to_wav(self, audio_source: Union[str, bytes]) -> str:
        """Convert audio to WAV format for speech_recognition (supports WebM, MP4, OGG, WAV, MP3)"""
        try:
            logger.info(f"Converting audio to WAV format, source type: {type(audio_source)}")
            
            if isinstance(audio_source, str):
                logger.info(f"Loading audio from file: {audio_source}")
                # Load from file - pydub can handle WebM, MP4, OGG, WAV, MP3
                audio = AudioSegment.from_file(audio_source)
            else:
                logger.info(f"Loading audio from bytes, size: {len(audio_source)} bytes")
                # Load from bytes
                audio = AudioSegment.from_file(io.BytesIO(audio_source))
            
            # Convert to proper WAV format (16kHz, mono, 16-bit)
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            
            # Save to temporary file
            import tempfile
            temp_fd, temp_path = tempfile.mkstemp(suffix='.wav')
            os.close(temp_fd)  # Close the file descriptor, pydub will create new file
            
            audio.export(temp_path, format="wav")
            
            logger.info(f"Audio converted to WAV successfully: {temp_path}")
            return temp_path
                
        except Exception as e:
            logger.error(f"WAV conversion error: {e}")
            raise e

    def play_audio(self, audio_source: Union[str, bytes]) -> bool:
        """Play audio from file path or bytes"""
        try:
            if isinstance(audio_source, str):
                # Play from file
                pygame.mixer.init()
                pygame.mixer.music.load(audio_source)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                return True
            else:
                # Play from bytes using pydub
                audio_segment = AudioSegment.from_mp3(io.BytesIO(audio_source))
                play(audio_segment)
                return True
                
        except Exception as e:
            logger.error(f"Audio playback error: {e}")
            return False
    
    def get_available_voices(self, language: str = 'english') -> Dict[str, Any]:
        """Get available voices for a language"""
        try:
            lang_config = self.language_config.get(language.lower())
            if not lang_config:
                return {'success': False, 'error': 'Unsupported language'}
            
            if lang_config['use_elevenlabs'] and self.elevenlabs_api_key:
                # Get ElevenLabs voices
                url = f"{self.elevenlabs_base_url}/voices"
                headers = {"xi-api-key": self.elevenlabs_api_key}
                
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                
                voices_data = response.json()
                return {
                    'success': True,
                    'voices': voices_data.get('voices', []),
                    'service': 'elevenlabs'
                }
            else:
                # Get local voices
                if self.tts_engine:
                    voices = self.tts_engine.getProperty('voices')
                    voice_list = [{'id': v.id, 'name': v.name} for v in voices] if voices else []
                    return {
                        'success': True,
                        'voices': voice_list,
                        'service': 'local'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'No TTS engine available'
                    }
                    
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def test_speech_services(self) -> Dict[str, Any]:
        """Test all speech services"""
        results = {
            'tts_tests': {},
            'stt_tests': {},
            'overall_status': 'unknown'
        }
        
        test_text = {
            'hindi': 'नमस्ते, मैं SBI Life का सहायक हूं',
            'english': 'Hello, I am your SBI Life assistant',
            'marathi': 'नमस्कार, मी तुमचा SBI Life सहायक आहे'
        }
        
        # Test TTS for each language
        for lang, text in test_text.items():
            try:
                result = self.text_to_speech(text, lang)
                results['tts_tests'][lang] = {
                    'success': result['success'],
                    'service': result.get('service', 'unknown'),
                    'error': result.get('error')
                }
            except Exception as e:
                results['tts_tests'][lang] = {
                    'success': False,
                    'error': str(e)
                }
        
        # Check if at least one service works
        working_services = sum(1 for test in results['tts_tests'].values() if test['success'])
        
        if working_services == 3:
            results['overall_status'] = 'all_working'
        elif working_services > 0:
            results['overall_status'] = 'partial_working'
        else:
            results['overall_status'] = 'not_working'
        
        return results

# Singleton instance
_speech_service = None

def get_speech_service() -> SpeechService:
    """Get singleton speech service instance"""
    global _speech_service
    if _speech_service is None:
        _speech_service = SpeechService()
    return _speech_service

# Convenience functions
def speak_text(text: str, language: str = 'english', save_path: Optional[str] = None) -> Dict[str, Any]:
    """Quick text-to-speech function"""
    service = get_speech_service()
    return service.text_to_speech(text, language, save_path)

def transcribe_audio(audio_source: Union[str, bytes], language: str = 'english') -> Dict[str, Any]:
    """Quick speech-to-text function"""
    service = get_speech_service()
    return service.speech_to_text(audio_source, language)

def record_and_transcribe(duration: int = 5, language: str = 'english') -> Dict[str, Any]:
    """Quick record and transcribe function"""
    service = get_speech_service()
    return service.record_from_microphone(duration, language)

if __name__ == "__main__":
    # Test the speech service
    service = SpeechService()
    
    print("Testing Speech Service...")
    test_results = service.test_speech_services()
    
    print("\n=== TTS Test Results ===")
    for lang, result in test_results['tts_tests'].items():
        status = "✓" if result['success'] else "✗"
        service_name = result.get('service', 'unknown')
        print(f"{status} {lang.title()}: {service_name}")
        if not result['success']:
            print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print(f"\nOverall Status: {test_results['overall_status']}")
