import React from 'react';
import { User, Bot, AlertCircle } from 'lucide-react';

const MessageBubble = ({ message, isBot }) => {
  const renderSection = (section, index) => {
    switch (section.type) {
      case 'main_response':
        return (
          <div key={index} className={`${isBot ? "text-gray-800" : "text-white"} mb-4`}>
            <p className="text-lg">{section.content}</p>
          </div>
        );
      case 'bullet_points':
        return (
          <div key={index} className="mb-4">
            <div className="flex items-center gap-2 mb-3">
              <AlertCircle className={`w-5 h-5 ${isBot ? "text-blue-600" : "text-white"}`} />
              <h3 className={`font-semibold ${isBot ? "text-gray-700" : "text-white"}`}>
                Available Options
              </h3>
            </div>
            <ul className={`space-y-3 ${isBot ? "text-gray-700" : "text-white"}`}>
              {section.points.map((point, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="mt-2 w-1.5 h-1.5 rounded-full bg-current flex-shrink-0" />
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          </div>
        );
      case 'action_items':
        return (
          <div key={index} className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center gap-2 mb-3">
              <div className={`w-2 h-6 rounded-sm ${isBot ? "bg-blue-600" : "bg-white"}`} />
              <h3 className={`font-semibold ${isBot ? "text-gray-700" : "text-white"}`}>
                Recommended Actions
              </h3>
            </div>
            <ul className={`space-y-3 ${isBot ? "text-gray-700" : "text-white"}`}>
              {section.items.map((item, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span className="mt-2 w-1.5 h-1.5 rounded-full bg-current flex-shrink-0" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} gap-3`}>
      {isBot && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center flex-shrink-0">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      
      <div className={`max-w-[80%] space-y-2`}>
        <div
          className={`p-5 rounded-2xl ${
            isBot
              ? 'bg-white shadow-sm'
              : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
          }`}
        >
          {message.text.sections.map((section, index) => renderSection(section, index))}
        </div>

        {/* Cards display for bot messages */}
        {isBot && message.cards && message.cards.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 mt-3">
            {message.cards.map((card, index) => (
              <div
                key={index}
                className="p-3 bg-white/80 backdrop-blur-sm rounded-xl border border-blue-100 hover:shadow-md transition-all cursor-pointer"
              >
                <h3 className="text-sm font-medium text-gray-700">{card.title}</h3>
                <p className="text-sm text-blue-600 font-semibold mt-1">{card.value}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {!isBot && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center flex-shrink-0">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default MessageBubble;