import React, { useState } from 'react';
import { Send, User, Bot, Paperclip, Mic, Sparkles, Circle, FileText, Calendar, Phone, Bell, Settings } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { 
      id: 1, 
      text: "Hi! I'm your SBI Life assistant. I can help you with insurance, investments, and claims processing. What brings you here today?", 
      isBot: true,
      cards: [
        { title: 'Term Insurance', value: '₹1 Cr Cover' },
        { title: 'Health Plans', value: 'Family Coverage' },
        { title: 'Investment', value: 'ULIP Plans' }
      ]
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [isThinking, setIsThinking] = useState(false);

  const handleSend = () => {
    if (inputText.trim()) {
      setMessages([...messages, { id: messages.length + 1, text: inputText, isBot: false }]);
      setInputText('');
      setIsThinking(true);
      setTimeout(() => {
        setMessages(prev => [...prev, { 
          id: prev.length + 1, 
          text: "I understand you're interested in our insurance plans. Here are some options tailored for you:", 
          isBot: true,
          cards: [
            { title: 'Smart Shield', value: 'Protection Plan' },
            { title: 'Health Plus', value: 'Medical Coverage' },
            { title: 'Wealth Max', value: 'Investment Plan' }
          ]
        }]);
        setIsThinking(false);
      }, 1500);
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 shadow-2xl rounded-lg overflow-hidden">
      {/* Top Bar */}
      <div className="bg-gradient-to-r from-blue-900 via-purple-900 to-pink-900 text-white p-2">
        <div className="flex justify-between items-center px-4">
          <div className="flex items-center gap-2">
            <img src="/api/placeholder/32/32" alt="SBI Logo" className="rounded-lg" />
            <span className="text-sm font-medium">SBI Life</span>
          </div>
          <div className="flex items-center gap-3">
            <Bell className="w-4 h-4 hover:text-blue-300 transition-colors cursor-pointer" />
            <Settings className="w-4 h-4 hover:text-blue-300 transition-colors cursor-pointer" />
          </div>
        </div>
      </div>

      {/* Main Banner */}
      <div className="relative h-40 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 overflow-hidden">
        <div className="absolute inset-0">
          {[...Array(40)].map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full mix-blend-overlay animate-pulse"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
                width: `${Math.random() * 40 + 10}px`,
                height: `${Math.random() * 40 + 10}px`,
                backgroundColor: `hsla(${Math.random() * 360}, 70%, 70%, 0.2)`,
                animationDelay: `${Math.random() * 3}s`,
                animationDuration: `${Math.random() * 4 + 2}s`
              }}
            />
          ))}
        </div>
        
        <div className="relative h-full px-6 py-4 flex flex-col justify-between">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-white/10 rounded-lg backdrop-blur-sm">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">AI Assistant</h1>
              <div className="flex items-center gap-2 mt-1">
                <span className="inline-block w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                <span className="text-sm text-blue-100">Online now</span>
              </div>
            </div>
          </div>
          <p className="text-sm text-blue-100 max-w-md">
            Explore insurance plans, manage policies, and get instant support
          </p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white/80 backdrop-blur-md border-b border-blue-100">
        <div className="flex gap-2 p-2 overflow-x-auto">
          {[
            { icon: FileText, label: 'My Policies' },
            { icon: Calendar, label: 'Appointments' },
            { icon: Phone, label: 'Contact Us' },
          ].map((item, index) => (
            <button
              key={index}
              className="flex-shrink-0 flex items-center gap-2 px-4 py-2 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all transform hover:scale-105 hover:shadow-lg"
            >
              <item.icon className="w-4 h-4" />
              <span className="text-sm font-medium whitespace-nowrap">{item.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.map((message) => (
          <div key={message.id} className={`space-y-3 ${message.isBot ? '' : 'flex flex-col items-end'}`}>
            <div className={`flex items-start gap-2 ${message.isBot ? '' : 'flex-row-reverse'}`}>
              <div className={`relative p-4 rounded-2xl max-w-[85%] ${
                message.isBot 
                  ? 'bg-white shadow-lg border border-blue-100' 
                  : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
              }`}>
                <div className="flex items-center gap-2 mb-2">
                  {message.isBot ? (
                    <div className="flex items-center gap-1 bg-blue-100 p-1.5 rounded-full">
                      <Bot className="w-4 h-4 text-blue-600" />
                      <Sparkles className="w-3 h-3 text-yellow-500 animate-pulse" />
                    </div>
                  ) : (
                    <div className="bg-white/20 p-1.5 rounded-full">
                      <User className="w-4 h-4" />
                    </div>
                  )}
                  <span className="text-sm font-medium">
                    {message.isBot ? 'AI Assistant' : 'You'}
                  </span>
                </div>
                <p className="text-sm leading-relaxed">{message.text}</p>
                
                {message.cards && (
                  <div className="mt-4 grid grid-cols-3 gap-2">
                    {message.cards.map((card, idx) => (
                      <div key={idx} 
                        className="p-3 bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg hover:shadow-md transition-all cursor-pointer hover:scale-105"
                      >
                        <h4 className="text-sm font-medium text-blue-700">{card.title}</h4>
                        <p className="text-xs text-blue-600 mt-1">{card.value}</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        
        {isThinking && (
          <div className="flex items-center gap-2 p-4 bg-white/50 rounded-2xl w-fit">
            <Circle className="w-2 h-2 text-blue-600 animate-bounce" />
            <Circle className="w-2 h-2 text-purple-600 animate-bounce delay-100" />
            <Circle className="w-2 h-2 text-pink-600 animate-bounce delay-200" />
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white/90 backdrop-blur-sm p-4 border-t border-blue-100">
        <div className="flex gap-2 items-center">
          <button 
            className="p-3 bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600 rounded-xl hover:from-blue-200 hover:to-purple-200 transition-all transform hover:scale-105"
            aria-label="Attach file"
          >
            <Paperclip className="w-5 h-5" />
          </button>
          
          <div className="flex-1 relative">
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Type your message here..."
              className="w-full px-4 py-3 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white pr-24 transition-all"
            />
            <div className="absolute right-2 top-1/2 -translate-y-1/2 flex gap-1">
              <button
                onClick={() => setIsRecording(!isRecording)}
                className={`p-2 rounded-xl transition-all transform hover:scale-105 ${
                  isRecording 
                    ? 'bg-red-500 text-white animate-pulse' 
                    : 'bg-gradient-to-r from-blue-100 to-purple-100 text-blue-600 hover:from-blue-200 hover:to-purple-200'
                }`}
                aria-label="Voice input"
              >
                <Mic className="w-5 h-5" />
              </button>
              <button
                onClick={handleSend}
                disabled={!inputText.trim()}
                className="p-2 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white rounded-xl hover:from-blue-600 hover:via-purple-600 hover:to-pink-600 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
                aria-label="Send message"
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