import React, { useState } from 'react';
import { Send, User, Bot, Paperclip, Mic, Circle, FileText, Calendar, Phone, Bell, Settings } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hi! I'm your SBI Life assistant. I can help you with insurance, investments, and claims processing. What brings you here today?",
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

  const handleSend = async () => {
    if (inputText.trim()) {
      setMessages([...messages, { id: messages.length + 1, text: inputText, isBot: false }]);
      setInputText('');
      setIsThinking(true);

      try {
        const response = await fetch('http://127.0.0.1:5000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            customer_id: 'USER_FRONTEND_TEST',
            user_input_text: inputText,
          }),
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();
        setMessages((prev) => [
          ...prev,
          {
            id: prev.length + 1,
            text: data.rag_response?.rag_response || "I apologize, but I couldn't process that request.",
            isBot: true,
          },
        ]);
      } catch (error) {
        console.error('Chat error:', error);
        setMessages((prev) => [
          ...prev,
          {
            id: prev.length + 1,
            text: "I'm sorry, but I'm having trouble connecting right now. Please try again later.",
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
      {/* Header with corrected logo and gradient */}
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
            <Bell className="w-5 h-5 hover:text-blue-300 transition-colors cursor-pointer" />
            <Settings className="w-5 h-5 hover:text-blue-300 transition-colors cursor-pointer" />
          </div>
        </div>
      </div>

      {/* AI Assistant Banner */}
      <div className="relative bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 p-6">
        <div className="flex items-center gap-4 mb-4">
          <div className="p-3 bg-white/10 rounded-lg backdrop-blur-sm">
            <Bot className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white mb-1">AI Assistant</h1>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              <span className="text-sm text-blue-100">Online now</span>
            </div>
          </div>
        </div>
        <p className="text-lg text-white/90 max-w-md">
          Explore insurance plans, manage policies, and get instant support
        </p>
      </div>

      {/* Quick Actions */}
      <div className="bg-white/80 backdrop-blur-md border-b border-blue-100 p-3">
        <div className="flex gap-3 overflow-x-auto px-2">
          {[
            { icon: FileText, label: 'My Policies' },
            { icon: Calendar, label: 'Appointments' },
            { icon: Phone, label: 'Contact Us' },
          ].map((item, index) => (
            <button
              key={index}
              className="flex items-center gap-2 px-5 py-2.5 bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all transform hover:scale-105 hover:shadow-lg"
            >
              <item.icon className="w-5 h-5" />
              <span className="text-sm font-medium whitespace-nowrap">{item.label}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex w-full ${message.isBot ? 'justify-start' : 'justify-end'}`}
          >
            <div
              className={`inline-flex max-w-[85%] ${
                message.isBot ? 'flex-row' : 'flex-row-reverse'
              }`}
            >
              <div
                className={`flex items-start gap-3 ${
                  message.isBot ? 'flex-row' : 'flex-row-reverse'
                }`}
              >
                <div
                  className={`p-4 rounded-2xl ${
                    message.isBot
                      ? 'bg-white shadow-lg'
                      : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                  } min-w-[100px] max-w-[500px]`}
                >
                  <div className="flex items-center gap-2 mb-2">
                    {message.isBot ? (
                      <>
                        <Bot className="w-5 h-5 text-blue-600" />
                        <span className="font-medium">AI Assistant</span>
                      </>
                    ) : (
                      <>
                        <User className="w-5 h-5" />
                        <span className="font-medium">You</span>
                      </>
                    )}
                  </div>
                  <p className="text-sm leading-relaxed break-words">{message.text}</p>

                  {message.cards && (
                    <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-3">
                      {message.cards.map((card, idx) => (
                        <div
                          key={idx}
                          className="bg-gradient-to-br from-blue-100 to-purple-100 hover:from-blue-200 hover:to-purple-200 rounded-lg p-1"
                        >
                          <div className="bg-white rounded-lg p-4 h-full">
                            <p className="text-sm font-medium text-blue-900">{card.title}</p>
                            <p className="text-lg font-bold text-blue-700 mt-2">{card.value}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
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
              placeholder="Type your message here..."
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