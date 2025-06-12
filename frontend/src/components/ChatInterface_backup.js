import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Paperclip, Mic, Circle, FileText, Calendar, Phone, Bell, Settings, Globe, Search, Navigation } from 'lucide-react'; // Added Search and Navigation icons
import MessageBubble from './MessageBubble';
import SmartSwadhanGuidance from './SmartSwadhanGuidance';

const ChatInterface = () => {
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
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isThinking, setIsThinking] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [isGeminiSearchActive, setIsGeminiSearchActive] = useState(false); // <-- New state for Gemini Search toggle
  const [showSmartSwadhanGuidance, setShowSmartSwadhanGuidance] = useState(false); // <-- New state for guidance modal
  const [currentGuidanceQuery, setCurrentGuidanceQuery] = useState(''); // <-- Store the query that triggered guidance
  const fileInputRef = useRef(null); // Ref for file input
  const recognitionRef = useRef(null); // Ref for SpeechRecognition instance

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिंदी' },
    { code: 'ta', name: 'தமிழ்' }
  ];

  const handleSend = async () => {
    if (inputText.trim() && !isThinking) {
      const currentInputText = inputText; // Capture current input
      const userMessage = {
        id: messages.length + 1,
        text: {
          sections: [
            {
              type: 'main_response',
              content: currentInputText // Use captured input
            }
          ]
        },
        isBot: false
      };
      setMessages((prev) => [...prev, userMessage]); // Use functional update
      setInputText('');
      setIsThinking(true);

      console.log("Attempting to send message:", currentInputText); // Log 1: Before fetch
      console.log("Gemini Search Active:", isGeminiSearchActive); // Log if Gemini Search is active

      // Check if user is asking about SBI Life product guidance (extended for all products)
      const sbiProductKeywords = [
        // Smart Swadhan Products
        'smart swadhan supreme', 'smart swadhan neo', 'smart swadhan',
        'swadhan supreme', 'swadhan neo', 'swadhan',
        
        // Saral Products
        'saral swadhan supreme', 'saral swadhan', 'saral jeevan bima', 'saral jeevan',
        
        // eShield Products
        'eshield next', 'e-shield next', 'eshield insta', 'e-shield insta', 'eshield', 'e-shield',
        
        // Smart Shield Products
        'smart shield premier', 'smart shield', 'shield premier',
        
        // General guidance keywords
        'guide me to', 'show me', 'navigate to', 'find', 'where is', 
        'how to find', 'product page', 'scheme', 'plan'
      ];
      
      // Check if the query contains any SBI product + guidance keywords combination
      const productMentioned = sbiProductKeywords.some(keyword => 
        currentInputText.toLowerCase().includes(keyword.toLowerCase())
      );
      
      const guidanceRequested = [
        'guide', 'show', 'navigate', 'find', 'where', 'how', 'page', 'help'
      ].some(keyword => currentInputText.toLowerCase().includes(keyword));
      
      const isSBIProductGuidanceQuery = productMentioned && (guidanceRequested || 
        currentInputText.toLowerCase().includes('live scrape') ||
        currentInputText.toLowerCase().includes('real time') ||
        currentInputText.toLowerCase().includes('guidance')
      );

      if (isSBIProductGuidanceQuery) {
        console.log("SBI Life product guidance detected, showing visual guide for:", currentInputText);
        setCurrentGuidanceQuery(currentInputText);
        setShowSmartSwadhanGuidance(true);
        setIsThinking(false);
        
        // Add a message indicating guidance is being shown
        const guidanceMessage = {
          id: messages.length + 2,
          text: {
            sections: [
              {
                type: 'main_response',
                content: "🎯 I'll show you exactly how to navigate to your requested SBI Life product! Opening visual step-by-step guidance..."
              }
            ]
          },
          isBot: true,
          showGuidanceButton: true
        };
        setMessages((prev) => [...prev, guidanceMessage]);
        return;
      }

      try {
        // <-- Modified fetch logic -->
        const endpoint = isGeminiSearchActive ? 'http://127.0.0.1:5000/gemini_search' : 'http://127.0.0.1:5000/chat';
        const body = isGeminiSearchActive
          ? JSON.stringify({ query: currentInputText })
          : JSON.stringify({
              customer_id: 'USER_FRONTEND_TEST',
              user_input_text: currentInputText, // Use captured input text
              language: selectedLanguage
            });

        const response = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: body,
        });
        // <-- End modified fetch logic -->

        console.log("Received response status:", response.status, response.statusText); // Log 2: After fetch, before checks

        if (!response.ok) {
          // Log the error response text if possible
          const errorText = await response.text().catch(() => "Could not read error response body");
          console.error("Fetch error response text:", errorText);
          throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
        }

        console.log("Attempting to parse JSON response..."); // Log 3: Before response.json()
        const data = await response.json();
        console.log("Received data from backend:", JSON.stringify(data, null, 2)); // Log 4: After successful JSON parsing

        // --- CHANGE HERE ---
        // Check if data.response exists and is a non-empty string
        const mainResponseContent = typeof data.response === 'string' && data.response.trim() ? data.response.trim() : null;

        let botText;
        if (mainResponseContent) {
          // If we have a valid response string, format it correctly
          botText = {
            sections: [
              {
                type: 'main_response',
                content: mainResponseContent
              }
            ]
          };
        } else {
           // Otherwise, use the fallback message
           console.warn("Backend response did not contain a valid 'response' string. Using fallback."); // Add a warning
           botText = {
            sections: [
              {
                type: 'main_response',
                content: isGeminiSearchActive ? "Sorry, I couldn't find relevant search results." : "I apologize, but I couldn't process that request."
              }
            ]
          };
        }
        // --- END CHANGE ---

        console.log("Parsed botText:", JSON.stringify(botText, null, 2)); // Log 5: After parsing botText

        setMessages((prev) => [
          ...prev,
          {
            id: prev.length + 1,
            text: botText, // Use the correctly structured botText
            isBot: true,
          },
        ]);
      } catch (error) {
        // Log 6: Catch block - Make sure this logs any error encountered
        console.error('!!! Critical Error in handleSend !!!:', error);
        console.error('Error name:', error.name);
        console.error('Error message:', error.message);
        // Optionally log stack trace if available
        if (error.stack) {
            console.error('Error stack:', error.stack);
        }

        // Display a user-friendly error message in the chat
        setMessages((prev) => [
          ...prev,
          {
            id: prev.length + 1,
            text: { sections: [{ type: 'main_response', content: `Error: Could not connect or process response. Details: ${error.message}` }] }, // Show error message in chat
            isBot: true,
            isError: true // Optional: Add flag for styling error messages
          },
        ]);
      } finally {
        console.log("Setting isThinking to false."); // Log 7: Finally block
        setIsThinking(false);
      }
    }
  };

  // --- NEW: File Upload Handling ---
  const handlePaperclipClick = () => {
    fileInputRef.current.click(); // Trigger hidden file input
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      console.log('Selected file:', file.name);
      // TODO: Implement actual file upload logic (e.g., send to backend)
      // Reset file input value so the same file can be selected again
      event.target.value = null;
    }
  };
  // --- END NEW: File Upload Handling ---


  // --- ENHANCED: Voice Input Handling with Backend Integration ---
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);

  useEffect(() => {
    // Initialize media recorder for backend STT
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          const recorder = new MediaRecorder(stream);
          setMediaRecorder(recorder);
          
          recorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
              setAudioChunks(prev => [...prev, event.data]);
            }
          };
          
          recorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            await sendAudioToBackend(audioBlob);
            setAudioChunks([]);
          };
        })
        .catch(err => {
          console.error('Error accessing microphone:', err);
          // Fallback to browser Speech Recognition
          initializeBrowserSpeechRecognition();
        });
    } else {
      // Fallback to browser Speech Recognition
      initializeBrowserSpeechRecognition();
    }
  }, []);

  const initializeBrowserSpeechRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.warn("Speech Recognition API not supported in this browser.");
      return;
    }

    recognitionRef.current = new SpeechRecognition();
    const recognition = recognitionRef.current;
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = getLanguageCode(selectedLanguage);

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      console.log("Browser voice input transcript:", transcript);
      setInputText(transcript);
      setIsRecording(false);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsRecording(false);
    };

    recognition.onend = () => {
      if (isRecording) {
        console.log("Recognition ended unexpectedly.");
        setIsRecording(false);
      }
    };
  };

  const getLanguageCode = (lang) => {
    const langMap = {
      'en': 'en-US',
      'hi': 'hi-IN',
      'mr': 'mr-IN'
    };
    return langMap[lang] || 'en-US';
  };

  const sendAudioToBackend = async (audioBlob) => {
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.wav');
      formData.append('language', selectedLanguage);

      const response = await fetch('http://127.0.0.1:5000/speech-to-text', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.text) {
          setInputText(data.text);
          console.log("Backend STT result:", data.text);
        } else {
          console.error("STT failed:", data.error);
          // Fallback to browser recognition
          if (recognitionRef.current) {
            handleBrowserSpeechRecognition();
          }
        }
      }
    } catch (error) {
      console.error('Error sending audio to backend:', error);
      // Fallback to browser recognition
      if (recognitionRef.current) {
        handleBrowserSpeechRecognition();
      }
    } finally {
      setIsRecording(false);
    }
  };

  const handleBrowserSpeechRecognition = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.lang = getLanguageCode(selectedLanguage);
        recognitionRef.current.start();
      } catch (error) {
        console.error("Error starting browser speech recognition:", error);
        setIsRecording(false);
      }
    }
  };

  const handleMicClick = () => {
    if (isRecording) {
      // Stop recording
      if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
      } else if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsRecording(false);
      console.log("Stopping voice recognition...");
    } else {
      // Start recording
      setIsRecording(true);
      console.log("Starting voice recognition...");
      
      // Try backend STT first (for Hindi/English with ElevenLabs, Marathi with free)
      if (mediaRecorder && mediaRecorder.state === 'inactive') {
        setAudioChunks([]);
        mediaRecorder.start();
      } else {
        // Fallback to browser recognition
        handleBrowserSpeechRecognition();
      }
    }
  };

  // Text-to-Speech function
  const speakText = async (text, language = selectedLanguage) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/text-to-speech', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: text,
          language: language
        })
      });

      if (response.ok) {
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        
        audio.onended = () => {
          URL.revokeObjectURL(audioUrl);
        };
        
        audio.play().catch(err => {
          console.error('Error playing audio:', err);
          // Fallback to browser speech synthesis
          fallbackTextToSpeech(text, language);
        });
      } else {
        // Fallback to browser speech synthesis
        fallbackTextToSpeech(text, language);
      }
    } catch (error) {
      console.error('Error with backend TTS:', error);
      // Fallback to browser speech synthesis
      fallbackTextToSpeech(text, language);
    }
  };

  const fallbackTextToSpeech = (text, language) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = getLanguageCode(language);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      speechSynthesis.speak(utterance);
    }
  };
  // --- END ENHANCED: Voice Input Handling ---

  // <-- New handler for Gemini Search button -->
  const handleGeminiSearchToggle = () => {
    setIsGeminiSearchActive(prev => !prev);
    console.log("Gemini Search toggled:", !isGeminiSearchActive);
  };
  // <-- End new handler -->

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
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all transform origin-top-right scale-95 group-hover:scale-100 z-50">
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
            <Bell className="w-5 h-5 hover:text-blue-300 transition-colors cursor-pointer" />
            <Settings className="w-5 h-5 hover:text-blue-300 transition-colors cursor-pointer" />
          </div>
        </div>
      </div>

      {/* Rest of the component remains the same */}
      {/* AI Assistant Banner */}
      <div className="relative bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-6">
        {/* ... existing banner code ... */}
      </div>

      {/* Quick Actions */}
      <div className="bg-white/80 backdrop-blur-md border-b border-blue-100 p-3">
        {/* ... existing quick actions code ... */}
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((message) => (
          <MessageBubble 
            key={message.id} 
            message={message} 
            isBot={message.isBot}
            onShowGuidance={() => setShowSmartSwadhanGuidance(true)}
          />
        ))}

        {isThinking && (
          <div className="flex items-center gap-2 p-4 bg-white/50 rounded-xl w-fit">
            <Circle className="w-2 h-2 text-blue-600 animate-bounce" />
            <Circle className="w-2 h-2 text-purple-600 animate-bounce delay-100" />
            <Circle className="w-2 h-2 text-pink-600 animate-bounce delay-200" />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white/90 backdrop-blur-sm p-4 border-t border-blue-100">
        <div className="flex gap-3 items-center">
          {/* --- MODIFIED: Paperclip Button --- */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: 'none' }} // Hide the default input
            accept="image/*,application/pdf,.doc,.docx,.txt" // Example file types
          />
          <button
            onClick={handlePaperclipClick} // Use new handler
            className="p-3 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600 rounded-xl hover:from-blue-200 hover:to-purple-200 transition-all"
          >
            <Paperclip className="w-5 h-5" />
          </button>
          {/* --- END MODIFIED: Paperclip Button --- */}

          <div className="flex-1 relative">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder={selectedLanguage === 'en' ? "Type your message here..." : 
                          selectedLanguage === 'hi' ? "अपना संदेश यहां टाइप करें..." :
                          "இங்கே உங்கள் செய்தியை தட்டச்சு செய்யவும்..."}
              className="w-full px-4 py-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white pr-24 transition-all"
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-2">
              {/* --- MODIFIED: Mic Button --- */}
              <button
                onClick={handleMicClick} // Use new handler
                className={`p-2 rounded-xl transition-all ${
                  isRecording
                    ? 'bg-red-500 text-white animate-pulse'
                    : 'bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600'
                }`}
              >
                <Mic className="w-5 h-5" />
              </button>
              {/* --- END MODIFIED: Mic Button --- */}

              {/* <-- New Gemini Search Toggle Button --> */}
              <button
                onClick={handleGeminiSearchToggle}
                title={isGeminiSearchActive ? "Disable Gemini Search" : "Enable Gemini Search"}
                className={`p-2 rounded-xl transition-all ${
                  isGeminiSearchActive
                    ? 'bg-blue-500 text-white' // Style when active
                    : 'bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600' // Style when inactive
                }`}
              >
                <Search className="w-5 h-5" />
              </button>
              {/* <-- End New Gemini Search Toggle Button --> */}

              <button
                onClick={handleSend}
                disabled={!inputText.trim()}
                className="p-2 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white rounded-xl hover:opacity-90 transition-all disabled:opacity-50"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      {/* Smart Swadhan Guidance Modal */}
      <SmartSwadhanGuidance 
        isVisible={showSmartSwadhanGuidance}
        onClose={() => setShowSmartSwadhanGuidance(false)}
        userQuery={currentGuidanceQuery}
      />
    </div>
  );
};

export default ChatInterface;