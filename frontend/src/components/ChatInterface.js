import React, { useState } from 'react';
import { Send, User, Bot, Paperclip, Mic, Circle, FileText, Calendar, Phone, Bell, Settings, Globe } from 'lucide-react';
import MessageBubble from './MessageBubble';

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

  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिंदी' },
    { code: 'ta', name: 'தமிழ்' }
  ];

  const handleSend = async () => {
    if (inputText.trim()) {
      const userMessage = {
        id: messages.length + 1,
        text: {
          sections: [
            {
              type: 'main_response',
              content: inputText
            }
          ]
        },
        isBot: false
      };
      setMessages([...messages, userMessage]);
      setInputText('');
      setIsThinking(true);

      try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            customer_id: 'USER_FRONTEND_TEST',
            user_input_text: inputText,
            language: selectedLanguage // Add language parameter
          }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();

        const botText = data.rag_response?.formatted_response || {
          sections: [
            {
              type: 'main_response',
              content: "I apologize, but I couldn't process that request."
            }
          ]
        };

        setMessages((prev) => [
          ...prev,
          {
            id: prev.length + 1,
            text: botText,
            isBot: true,
          },
        ]);
      } catch (error) {
        console.error('Chat error:', error);
        setMessages((prev) => [
          ...prev,
          {
            id: prev.length + 1,
            text: {
              sections: [
                {
                  type: 'main_response',
                  content: "I'm sorry, but I'm having trouble connecting right now. Please try again later."
                }
              ]
            },
            isBot: true,
          },
        ]);
      } finally {
        setIsThinking(false);
      }
    }
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
          <MessageBubble key={message.id} message={message} isBot={message.isBot} />
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
          <button className="p-3 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600 rounded-xl hover:from-blue-200 hover:to-purple-200 transition-all">
            <Paperclip className="w-5 h-5" />
          </button>

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
              <button
                onClick={() => setIsRecording(!isRecording)}
                className={`p-2 rounded-xl transition-all ${
                  isRecording
                    ? 'bg-red-500 text-white animate-pulse'
                    : 'bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600'
                }`}
              >
                <Mic className="w-5 h-5" />
              </button>
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
    </div>
  );
};

export default ChatInterface;