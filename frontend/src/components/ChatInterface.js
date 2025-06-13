import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Paperclip, Mic, MicOff, Circle, FileText, Calendar, Phone, Bell, Settings, Globe, Search, Navigation, Volume2, LogOut, MessageSquarePlus, BarChart3 } from 'lucide-react';
import MessageBubble from './MessageBubble';
import SmartSwadhanGuidance from './SmartSwadhanGuidance';
import MockAuth from './MockAuth';
import Dashboard from './Dashboard';

const ChatInterface = () => {
  // Authentication state
  const [currentUser, setCurrentUser] = useState(null);
  // Show/hide login modal
  const [showLoginModal, setShowLoginModal] = useState(false);
  // Loading state for chat history
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  // Show/hide new chat confirmation
  const [showNewChatConfirm, setShowNewChatConfirm] = useState(false);
  // Show/hide dashboard
  const [showDashboard, setShowDashboard] = useState(false);
  
  // Authentication handlers
  const handleLogin = (userSession) => {
    setCurrentUser(userSession);
    setShowLoginModal(false);
    // Clear current messages and load personalized welcome message
    setMessages([
      {
        id: 1,
        text: {
          sections: [
            {
              type: 'main_response',
              content: `Welcome back, ${userSession.name}! I'm your SBI Life assistant with access to your personalized chat history. I can help you with insurance, investments, and claims processing based on your previous interactions. What would you like to discuss today?`
            }
          ]
        },
        isBot: true,
        cards: [
          { title: 'Term Insurance', value: '₹1 Cr Cover' },
          { title: 'Health Plans', value: 'Family Coverage' },
          { title: 'Investment', value: 'ULIP Plans' },
        ],
      },
    ]);
    
    // Load user's chat history from localStorage
    loadUserChatHistory(userSession.customerId);
  };

  const handleLogout = () => {
    setCurrentUser(null);
    // Reset to default welcome message
    setMessages([
      {
        id: 1,
        text: {
          sections: [
            {
              type: 'main_response',
              content: "Hi! I'm your SBI Life assistant. Please login to access personalized chat with your interaction history."
            }
          ]
        },
        isBot: true,
        cards: [
          { title: 'Term Insurance', value: '₹1 Cr Cover' },
          { title: 'Health Plans', value: 'Family Coverage' },
          { title: 'Investment', value: 'ULIP Plans' },
        ],
      },
    ]);
  };

  const handleNewChat = () => {
    if (!currentUser) return;
    setShowNewChatConfirm(true);
  };

  const confirmNewChat = () => {
    // Clear current messages and show new chat welcome message
    setMessages([
      {
        id: 1,
        text: {
          sections: [
            {
              type: 'main_response',
              content: `Hello ${currentUser.name}! Starting a fresh conversation. Your previous chat history has been cleared. How can I help you today?`
            }
          ]
        },
        isBot: true,
        cards: [
          { title: 'Term Insurance', value: '₹1 Cr Cover' },
          { title: 'Health Plans', value: 'Family Coverage' },
          { title: 'Investment', value: 'ULIP Plans' },
        ],
      },
    ]);
    
    // Clear chat history from localStorage
    localStorage.removeItem(`sbi_chat_history_${currentUser.customerId}`);
    
    // Reset any ongoing processes
    setInputText('');
    setIsThinking(false);
    setIsVoiceMode(false);
    stopListening();
    
    // Close confirmation dialog
    setShowNewChatConfirm(false);
  };

  const handleDashboard = () => {
    if (!currentUser) {
      setShowLoginModal(true);
      return;
    }
    setShowDashboard(true);
  };

  // Add this at the beginning of the component to show login modal on load
  useEffect(() => {
    // Check if user is not logged in, then show login modal automatically
    if (!currentUser) {
      setShowLoginModal(true);
    }
  }, [currentUser]);

  // Initialize messages state
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: {
        sections: [
          {
            type: 'main_response',
            content: "Hi! I'm your SBI Life assistant. I can help you with insurance, investments, and claims processing. What brings you here today?"
          }
        ]
      },
      isBot: true,
      cards: [
        { title: 'Term Insurance', value: '₹1 Cr Cover' },
        { title: 'Health Plans', value: 'Family Coverage' },
        { title: 'Investment', value: 'ULIP Plans' },
      ],
    },
  ]);
  
  // Load and save chat history for the logged-in user
  const loadUserChatHistory = (customerId) => {
    setIsLoadingHistory(true);
    try {
      const savedHistory = localStorage.getItem(`sbi_chat_history_${customerId}`);
      if (savedHistory) {
        const parsedHistory = JSON.parse(savedHistory);
        if (Array.isArray(parsedHistory) && parsedHistory.length > 0) {
          setMessages(parsedHistory);
        }
      }
      setTimeout(() => setIsLoadingHistory(false), 500); // Small delay to show loading state
    } catch (error) {
      console.error('Error loading chat history:', error);
      setIsLoadingHistory(false);
    }
  };

  const saveUserChatHistory = (customerId, messages) => {
    try {
      localStorage.setItem(`sbi_chat_history_${customerId}`, JSON.stringify(messages));
    } catch (error) {
      console.error('Error saving chat history:', error);
    }
  };

  // Save chat history whenever messages change and user is logged in
  useEffect(() => {
    if (currentUser && messages.length > 1) {
      saveUserChatHistory(currentUser.customerId, messages);
    }
  }, [messages, currentUser]);
  
  const [inputText, setInputText] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [isExaSearchActive, setIsExaSearchActive] = useState(false);
  const [showSmartSwadhanGuidance, setShowSmartSwadhanGuidance] = useState(false);
  const [currentGuidanceQuery, setCurrentGuidanceQuery] = useState('');
  
  // Enhanced Voice States
  const [isVoiceMode, setIsVoiceMode] = useState(false); // Toggle for continuous voice mode
  const [isListening, setIsListening] = useState(false); // Currently listening
  const [isSpeaking, setIsSpeaking] = useState(false); // Currently speaking response
  const [voiceTimeout, setVoiceTimeout] = useState(null);
  
  const fileInputRef = useRef(null);
  const recognitionRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const silenceTimerRef = useRef(null);
  const audioChunksRef = useRef([]);

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिंदी' },
    { code: 'gu', name: 'ગુજરાતી' },
    { code: 'mr', name: 'मराठी' },
    { code: 'ta', name: 'தமிழ்' },
    { code: 'te', name: 'తెలుగు' },
    { code: 'kn', name: 'ಕನ್ನಡ' },
    { code: 'bn', name: 'বাংলা' },
    { code: 'ml', name: 'മലയാളം' },
    { code: 'or', name: 'ଓଡ଼ିଆ' },
    { code: 'pa', name: 'ਪੰਜਾਬੀ' },
    { code: 'as', name: 'অসমীয়া' },
    { code: 'ur', name: 'اردو' },
    { code: 'sa', name: 'संस्कृत' },
    { code: 'ne', name: 'नेपाली' },
    { code: 'si', name: 'සිංහල' },
    { code: 'my', name: 'မြန်မာ' },
    { code: 'sd', name: 'سنڌي' },
    { code: 'ks', name: 'کٲشُر' },
    { code: 'do', name: 'डोगरी' },
    { code: 'mni', name: 'ꯃꯩꯇꯩꯂꯣꯟ' },
    { code: 'kok', name: 'कोंकणी' }
  ];

  // Initialize speech recognition and media recorder
  useEffect(() => {
    initializeSpeechCapabilities();
    return () => {
      cleanup();
    };
  }, []);

  const cleanup = () => {
    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current);
    }
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
  };

  const initializeSpeechCapabilities = async () => {
    // Initialize media recorder for backend STT
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Check for supported audio formats and use the best one
      let options = {};
      if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
        options = { mimeType: 'audio/webm;codecs=opus' };
      } else if (MediaRecorder.isTypeSupported('audio/webm')) {
        options = { mimeType: 'audio/webm' };
      } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
        options = { mimeType: 'audio/mp4' };
      } else if (MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')) {
        options = { mimeType: 'audio/ogg;codecs=opus' };
      }
      
      const recorder = new MediaRecorder(stream, options);
      mediaRecorderRef.current = recorder;
      
      console.log('MediaRecorder initialized with mimeType:', recorder.mimeType);
      
      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };
      
      recorder.onstop = async () => {
        if (audioChunksRef.current.length > 0) {
          // Use the actual MediaRecorder mimeType instead of forcing 'audio/wav'
          const audioBlob = new Blob(audioChunksRef.current, { type: recorder.mimeType });
          await sendAudioToBackend(audioBlob, recorder.mimeType);
          audioChunksRef.current = [];
        }
      };
    } catch (err) {
      console.warn('Media recorder not available, using browser speech recognition:', err);
    }

    // Initialize browser speech recognition as fallback
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      const recognition = recognitionRef.current;
      
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = getLanguageCode(selectedLanguage);

      recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        if (finalTranscript) {
          setInputText(finalTranscript.trim());
          // Note: In voice mode, message will be sent when user manually stops recording
        } else if (interimTranscript) {
          setInputText(interimTranscript);
        }
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        if (isVoiceMode && event.error !== 'no-speech') {
          // Restart recognition in voice mode unless it's a no-speech error
          setTimeout(() => {
            if (isVoiceMode) {
              startListening();
            }
          }, 1000);
        }
      };

      recognition.onend = () => {
        if (isVoiceMode && !isSpeaking) {
          // Restart listening in voice mode
          setTimeout(() => {
            if (isVoiceMode) {
              startListening();
            }
          }, 500);
        }
        setIsListening(false);
      };
    }
  };

  const getLanguageCode = (lang) => {
    const langMap = {
      'en': 'en-US',
      'hi': 'hi-IN',
      'mr': 'mr-IN'
    };
    return langMap[lang] || 'en-US';
  };

  const sendAudioToBackend = async (audioBlob, mimeType) => {
    try {
      const formData = new FormData();
      
      // Determine file extension based on mimeType
      let filename = 'audio.webm'; // default
      if (mimeType && mimeType.includes('webm')) {
        filename = 'audio.webm';
      } else if (mimeType && mimeType.includes('mp4')) {
        filename = 'audio.mp4';
      } else if (mimeType && mimeType.includes('ogg')) {
        filename = 'audio.ogg';
      }
      
      formData.append('audio', audioBlob, filename);
      formData.append('language', selectedLanguage);
      formData.append('mimeType', mimeType || 'audio/webm');

      console.log('Sending audio to backend:', {
        size: audioBlob.size,
        type: audioBlob.type,
        filename: filename,
        mimeType: mimeType
      });

      const response = await fetch('http://127.0.0.1:5000/api/speech/speech-to-text', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.transcription) {
          // Show transcribed text in input field
          setInputText(data.transcription);
          
          // If in voice mode, auto-send after a short delay
          if (isVoiceMode) {
            if (silenceTimerRef.current) {
              clearTimeout(silenceTimerRef.current);
            }
            silenceTimerRef.current = setTimeout(() => {
              if (data.transcription.trim()) {
                handleAutoSend(data.transcription.trim());
              }
            }, 1500);
          }
        } else {
          console.error('Transcription failed:', data.error);
        }
      } else {
        console.error('STT API error:', response.status);
      }
    } catch (error) {
      console.error('Error sending audio to backend:', error);
    }
  };

  const startListening = () => {
    if (!isListening) {
      setIsListening(true);
      
      // Try media recorder first
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'inactive') {
        audioChunksRef.current = [];
        mediaRecorderRef.current.start(1000); // Record in 1-second chunks
      } 
      // Fallback to browser speech recognition
      else if (recognitionRef.current) {
        try {
          recognitionRef.current.lang = getLanguageCode(selectedLanguage);
          recognitionRef.current.start();
        } catch (error) {
          console.error('Error starting speech recognition:', error);
          setIsListening(false);
        }
      }
    }
  };

  const stopListening = () => {
    setIsListening(false);
    
    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current);
    }
    
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
    }
    
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  };

  // Toggle voice mode on/off
  const handleVoiceToggle = () => {
    if (isVoiceMode) {
      // Turn off voice mode
      setIsVoiceMode(false);
      stopListening();
      console.log('Voice mode: OFF');
    } else {
      // Turn on voice mode
      setIsVoiceMode(true);
      startListening();
      console.log('Voice mode: ON - Listening continuously...');
    }
  };

  // Auto-send function for voice mode
  const handleAutoSend = async (text) => {
    // Authentication guard
    if (!currentUser) {
      setShowLoginModal(true);
      return;
    }

    if (!text.trim() || isThinking) return;

    console.log('Auto-sending:', text);
    
    // Close voice toggle after auto-sending
    if (isVoiceMode) {
      setIsVoiceMode(false);
      stopListening();
      console.log('Voice mode: OFF (auto-closed after send)');
    }
    
    const userMessage = {
      id: messages.length + 1,
      text: {
        sections: [
          {
            type: 'main_response',
            content: text
          }
        ]
      },
      isBot: false
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsThinking(true);
    
    // Stop listening while processing
    stopListening();

    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_id: currentUser ? currentUser.customerId : 'USER_FRONTEND_TEST',
          user_input_text: text,
          language: selectedLanguage
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const responseText = data.response || "I apologize, but I couldn't process that request.";
        
        const botMessage = {
          id: messages.length + 2,
          text: {
            sections: [
              {
                type: 'main_response',
                content: responseText
              }
            ]
          },
          isBot: true,
        };

        setMessages(prev => [...prev, botMessage]);
        
        // Don't speak response anymore since voice mode is closed
        // User can manually click speaker icon if they want TTS
      }
    } catch (error) {
      console.error('Error in auto-send:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: {
          sections: [
            {
              type: 'main_response',
              content: "Sorry, I couldn't process your request. Please try again."
            }
          ]
        },
        isBot: true,
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsThinking(false);
      // Voice mode is already closed, no need to restart listening
    }
  };

  // Speak response function
  const speakResponse = async (text) => {
    setIsSpeaking(true);
    
    try {
      const response = await fetch('http://127.0.0.1:5000/api/speech/text-to-speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: text,
          language: selectedLanguage
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.audio_base64) {
          // Convert base64 to audio blob
          const audioData = atob(data.audio_base64);
          const audioArray = new Uint8Array(audioData.length);
          for (let i = 0; i < audioData.length; i++) {
            audioArray[i] = audioData.charCodeAt(i);
          }
          const audioBlob = new Blob([audioArray], { type: 'audio/wav' });
          const audioUrl = URL.createObjectURL(audioBlob);
          const audio = new Audio(audioUrl);
          
          audio.onended = () => {
            URL.revokeObjectURL(audioUrl);
            setIsSpeaking(false);
            
            // Resume listening after speaking in voice mode
            if (isVoiceMode) {
              setTimeout(() => {
                if (isVoiceMode) {
                  startListening();
                }
              }, 500);
            }
          };
          
          await audio.play();
        } else {
          throw new Error('No audio data received');
        }
      } else {
        throw new Error('Backend TTS failed');
      }
    } catch (error) {
      console.error('Error with TTS:', error);
      // Fallback to browser speech synthesis
      fallbackTextToSpeech(text);
    }
  };

  const fallbackTextToSpeech = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = getLanguageCode(selectedLanguage);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      
      utterance.onend = () => {
        setIsSpeaking(false);
        if (isVoiceMode) {
          setTimeout(() => {
            if (isVoiceMode) {
              startListening();
            }
          }, 500);
        }
      };
      
      speechSynthesis.speak(utterance);
    } else {
      setIsSpeaking(false);
      if (isVoiceMode) {
        setTimeout(() => {
          if (isVoiceMode) {
            startListening();
          }
        }, 500);
      }
    }
  };

  // Regular send function (for manual sending)
  const handleSend = async () => {
    // Authentication guard
    if (!currentUser) {
      setShowLoginModal(true);
      return;
    }

    if (inputText.trim() && !isThinking) {
      // Close voice toggle when manually sending a message
      if (isVoiceMode) {
        setIsVoiceMode(false);
        stopListening();
        console.log('Voice mode: OFF (auto-closed on send)');
      }
      
      const currentInputText = inputText;
      const userMessage = {
        id: messages.length + 1,
        text: {
          sections: [
            {
              type: 'main_response',
              content: currentInputText
            }
          ]
        },
        isBot: false
      };
      
      setMessages(prev => [...prev, userMessage]);
      setInputText('');
      setIsThinking(true);

      try {
        const endpoint = isExaSearchActive ? 'http://127.0.0.1:5000/gemini_search' : 'http://127.0.0.1:5000/chat';
        const body = isExaSearchActive
          ? JSON.stringify({ query: currentInputText })
          : JSON.stringify({
              customer_id: currentUser ? currentUser.customerId : 'USER_FRONTEND_TEST',
              user_input_text: currentInputText,
              language: selectedLanguage
            });

        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: body,
        });

        if (response.ok) {
          const data = await response.json();
          const responseText = data.response || "I apologize, but I couldn't process that request.";
          
          // Check if backend indicates visual guidance should be shown
          if (data.show_visual_guidance) {
            console.log("Backend triggered visual guidance, opening SmartSwadhanGuidance modal");
            setCurrentGuidanceQuery(currentInputText);
            setShowSmartSwadhanGuidance(true);
          }
          
          const botMessage = {
            id: messages.length + 2,
            text: {
              sections: [
                {
                  type: 'main_response',
                  content: responseText
                }
              ]
            },
            isBot: true,
            showGuidanceButton: data.show_visual_guidance || false, // Add guidance button if backend indicates
          };

          setMessages(prev => [...prev, botMessage]);
        } else {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
      } catch (error) {
        console.error('Error in handleSend:', error);
        setMessages(prev => [...prev, {
          id: prev.length + 1,
          text: {
            sections: [
              {
                type: 'main_response',
                content: `Error: Could not connect or process response. Details: ${error.message}`
              }
            ]
          },
          isBot: true,
          isError: true
        }]);
      } finally {
        setIsThinking(false);
      }
    }
  };

  // File upload handling
  const handlePaperclipClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Selected file:', file.name);
      event.target.value = null;
    }
  };

  const handleExaSearchToggle = () => {
    setIsExaSearchActive(prev => !prev);
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 shadow-2xl rounded-lg overflow-hidden">
      {/* Header with language selector */}
      <div className="bg-gradient-to-b from-purple-900 to-pink-500 text-white p-3">
        <div className="flex justify-between items-center px-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center p-1">
              <svg viewBox="0 0 100 100" className="w-full h-full">
                <circle cx="50" cy="50" r="50" fill="#0056A5" />
                <rect x="48" y="30" width="4" height="40" fill="white" />
                <circle cx="50" cy="25" r="5" fill="white" />
              </svg>
            </div>
            <span className="text-lg font-semibold">SBI Life</span>
          </div>
          <div className="flex items-center gap-4">
            {/* Language Selector */}
            <div className="relative group">
              <button className="flex items-center gap-2 hover:bg-white/10 p-2 rounded-lg transition-colors">
                <Globe className="w-5 h-5" />
                <span className="text-sm">{languages.find(l => l.code === selectedLanguage)?.name}</span>
              </button>
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all transform origin-top-right scale-95 group-hover:scale-100 z-50 max-h-80 overflow-y-auto language-dropdown-scroll">
                {languages.map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => setSelectedLanguage(lang.code)}
                    className="w-full text-left px-4 py-2 text-gray-700 hover:bg-blue-50 first:rounded-t-lg last:rounded-b-lg"
                  >
                    {lang.name}
                  </button>
                ))}
              </div>
            </div>
            
            {/* Voice Mode Status */}
            {isVoiceMode && (
              <div className="flex items-center gap-2 bg-white/20 px-3 py-1 rounded-full">
                <div className={`w-2 h-2 rounded-full ${isListening ? 'bg-red-400 animate-pulse' : isSpeaking ? 'bg-green-400 animate-pulse' : 'bg-yellow-400'}`}></div>
                <span className="text-xs">
                  {isListening ? 'Listening...' : isSpeaking ? 'Speaking...' : 'Voice Mode'}
                </span>
              </div>
            )}
            
            {/* User/Login Button */}
            {currentUser ? (
              <div className="flex items-center gap-2">
                <span className="text-xs text-white overflow-hidden whitespace-nowrap overflow-ellipsis max-w-[80px]">
                  {currentUser.name}
                </span>
                <button 
                  onClick={handleDashboard} 
                  title="Open Dashboard" 
                  className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center hover:bg-blue-600 transition-colors"
                >
                  <BarChart3 className="w-4 h-4 text-white" />
                </button>
                <button 
                  onClick={handleNewChat} 
                  title="Start New Chat" 
                  className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center hover:bg-green-600 transition-colors"
                >
                  <MessageSquarePlus className="w-4 h-4 text-white" />
                </button>
                <button 
                  onClick={handleLogout} 
                  title="Logout" 
                  className="w-8 h-8 rounded-full bg-red-500 flex items-center justify-center hover:bg-red-600 transition-colors"
                >
                  <LogOut className="w-4 h-4 text-white" />
                </button>
              </div>
            ) : (
              <button 
                onClick={() => setShowLoginModal(true)} 
                title="Login" 
                className="w-8 h-8 rounded-full bg-white flex items-center justify-center"
              >
                <User className="w-5 h-5 text-purple-600" />
              </button>
            )}
            
            <Bell className="w-5 h-5 hover:text-blue-300 transition-colors cursor-pointer" />
            <Settings className="w-5 h-5 hover:text-blue-300 transition-colors cursor-pointer" />
          </div>
        </div>
      </div>

      {/* AI Assistant Banner */}
      <div className="relative bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-6">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="relative z-10 text-center text-white">
          <h2 className="text-2xl font-bold mb-2">AI-Powered SBI Life Assistant</h2>
          <p className="text-blue-100">Get personalized insurance guidance in your preferred language</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white/80 backdrop-blur-md border-b border-blue-100 p-3">
        <div className="flex justify-center space-x-4 text-sm">
          {currentUser && (
            <button 
              onClick={handleNewChat}
              className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 rounded-lg hover:from-green-200 hover:to-emerald-200 transition-all"
            >
              <MessageSquarePlus className="w-4 h-4" />
              New Chat
            </button>
          )}
          <button className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-700 rounded-lg hover:from-blue-200 hover:to-purple-200 transition-all">
            <FileText className="w-4 h-4" />
            Claims
          </button>
          <button className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 rounded-lg hover:from-purple-200 hover:to-pink-200 transition-all">
            <Calendar className="w-4 h-4" />
            Renewals
          </button>
          <button className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-pink-100 to-blue-100 text-pink-700 rounded-lg hover:from-pink-200 hover:to-blue-200 transition-all">
            <Phone className="w-4 h-4" />
            Support
          </button>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {isLoadingHistory ? (
          <div className="flex items-center justify-center p-8">
            <div className="flex items-center gap-3">
              <Circle className="w-3 h-3 text-blue-600 animate-bounce" />
              <Circle className="w-3 h-3 text-purple-600 animate-bounce delay-100" />
              <Circle className="w-3 h-3 text-pink-600 animate-bounce delay-200" />
              <span className="text-sm text-gray-600 ml-2">Loading your chat history...</span>
            </div>
          </div>
        ) : (
          messages.map((message) => (
            <MessageBubble 
              key={message.id} 
              message={message} 
              isBot={message.isBot}
              onShowGuidance={() => setShowSmartSwadhanGuidance(true)}
              onSpeak={(text) => speakResponse(text)}
              selectedLanguage={selectedLanguage}
            />
          ))
        )}

        {isThinking && (
          <div className="flex items-center gap-2 p-4 bg-white/50 rounded-xl w-fit">
            <Circle className="w-2 h-2 text-blue-600 animate-bounce" />
            <Circle className="w-2 h-2 text-purple-600 animate-bounce delay-100" />
            <Circle className="w-2 h-2 text-pink-600 animate-bounce delay-200" />
            <span className="text-sm text-gray-600 ml-2">Thinking...</span>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white/90 backdrop-blur-sm p-4 border-t border-blue-100">
        <div className="flex gap-3 items-center">
          {/* File Upload */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: 'none' }}
            accept="image/*,application/pdf,.doc,.docx,.txt"
          />
          <button
            onClick={handlePaperclipClick}
            disabled={!currentUser}
            title={!currentUser ? "Please login to upload files" : "Upload file"}
            className="p-3 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600 rounded-xl hover:from-blue-200 hover:to-purple-200 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Paperclip className="w-5 h-5" />
          </button>

          <div className="flex-1 relative">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder={
                !currentUser ? "Please login to start chatting..." :
                selectedLanguage === 'en' ? "Type your message here..." : 
                selectedLanguage === 'hi' ? "अपना संदेश यहां टाइप करें..." :
                "आपला संदेश इथे टाइप करा..."
              }
              className="w-full px-4 py-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white pr-32 transition-all"
              disabled={!currentUser || (isVoiceMode && isListening)}
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-2">
              {/* Voice Toggle Button */}
              <button
                onClick={handleVoiceToggle}
                disabled={!currentUser}
                title={!currentUser ? "Please login to use voice mode" : isVoiceMode ? "Turn off voice mode" : "Turn on voice mode"}
                className={`p-2 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
                  isVoiceMode
                    ? 'bg-red-500 text-white shadow-lg'
                    : 'bg-gradient-to-r from-green-100 to-blue-100 text-green-600 hover:from-green-200 hover:to-blue-200'
                }`}
              >
                {isVoiceMode ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
              </button>

              {/* Exa Search Toggle */}
              <button
                onClick={handleExaSearchToggle}
                disabled={!currentUser}
                title={!currentUser ? "Please login to use web search" : isExaSearchActive ? "Disable Exa Web Search" : "Enable Exa Web Search"}
                className={`p-2 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed ${
                  isExaSearchActive
                    ? 'bg-blue-500 text-white'
                    : 'bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600'
                }`}
              >
                <Search className="w-5 h-5" />
              </button>

              {/* Send Button */}
              <button
                onClick={handleSend}
                disabled={!currentUser || !inputText.trim() || isVoiceMode}
                className="p-2 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white rounded-xl hover:opacity-90 transition-all disabled:opacity-50"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
        
        {/* Voice Mode Instructions */}
        {isVoiceMode && (
          <div className="mt-3 p-3 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200">
            <div className="flex items-center gap-2 text-sm text-green-700">
              <div className={`w-2 h-2 rounded-full ${isListening ? 'bg-red-500 animate-pulse' : isSpeaking ? 'bg-green-500 animate-pulse' : 'bg-yellow-500'}`}></div>
              <span className="font-medium">
                {isListening ? 'Listening for your voice...' : 
                 isSpeaking ? 'Speaking response...' : 
                 'Voice mode active - waiting...'}
              </span>
            </div>
            <p className="text-xs text-gray-600 mt-1">
              Speak naturally. I'll automatically send your message and respond in {languages.find(l => l.code === selectedLanguage)?.name}.
            </p>
          </div>
        )}
      </div>
      
      {/* Smart Swadhan Guidance Modal */}
      <SmartSwadhanGuidance 
        isVisible={showSmartSwadhanGuidance}
        onClose={() => setShowSmartSwadhanGuidance(false)}
        userQuery={currentGuidanceQuery}
      />
      
      {/* Authentication Modal */}
      <MockAuth 
        isVisible={showLoginModal}
        onLogin={handleLogin}
        onClose={() => setShowLoginModal(false)}
      />
      
      {/* New Chat Confirmation Modal */}
      {showNewChatConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4 p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center">
                <MessageSquarePlus className="w-5 h-5 text-orange-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Start New Chat</h3>
                <p className="text-sm text-gray-600">This will clear your current conversation</p>
              </div>
            </div>
            
            <p className="text-gray-700 mb-6">
              Are you sure you want to start a new chat? This will permanently delete your current conversation history for this session.
            </p>
            
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowNewChatConfirm(false)}
                className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmNewChat}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Start New Chat
              </button>
            </div>
          </div>
        </div>
      )}
      
      {/* Dashboard Modal */}
      <Dashboard 
        isVisible={showDashboard}
        onClose={() => setShowDashboard(false)}
        currentUser={currentUser}
      />
    </div>
  );
};

export default ChatInterface;
