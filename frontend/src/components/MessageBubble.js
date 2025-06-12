import React from 'react';
import { User, Bot, AlertCircle, Navigation } from 'lucide-react';

// Enhanced helper function to render formatted text with paragraphs, ordered lists, and nested unordered lists
const renderFormattedContent = (content, isBot) => {
  if (!content) return null;

  // Split content into major sections by double newlines
  const sections = content.split('\n\n');
  const elements = [];

  sections.forEach((section, sectionIndex) => {
    const lines = section.split('\n');
    
    // Check if this section is a numbered section
    const firstLine = lines[0].trim();
    const isNumberedSection = firstLine.match(/^\d+\./);
    
    if (isNumberedSection) {
      // This is a numbered section with bullet points
      const sectionTitle = firstLine;
      const bulletPoints = lines.slice(1).filter(line => line.trim().startsWith('-'));
      
      elements.push(
        <div key={`section-${sectionIndex}`} className="mb-4">
          <h3 className={`font-semibold mb-2 ${isBot ? 'text-gray-800' : 'text-white'}`}>
            {sectionTitle}
          </h3>
          <ul className={`pl-5 space-y-2 ${isBot ? 'text-gray-700' : 'text-white'}`}>
            {bulletPoints.map((point, idx) => (
              <li key={`bullet-${sectionIndex}-${idx}`} className="flex items-start gap-2">
                <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-current flex-shrink-0"/>
                <span className="leading-relaxed">{point.trim().substring(1).trim()}</span>
              </li>
            ))}
          </ul>
        </div>
      );
    } else {
      // Regular text section
      elements.push(
        <p key={`text-${sectionIndex}`} className="mb-4 leading-relaxed">
          {section.trim()}
        </p>
      );
    }
  });

  return elements;
};

const MessageBubble = ({ message, isBot, onShowGuidance }) => {
  const renderSection = (section, index) => {
    switch (section.type) {
      case 'main_response':
        // Use the enhanced helper function
        return (
          <div key={index} className={`${isBot ? "text-gray-800" : "text-white"} text-base flex flex-col`}>
             {renderFormattedContent(section.content, isBot)}
          </div>
        );
     // ... Keep other cases like bullet_points, action_items if they are used elsewhere ...
     case 'bullet_points':
        // This case might become redundant if all lists are handled by main_response
        // Or it could be used for specific, non-nested bullet lists if needed.
        return (
          <div key={index} className="mb-4">
            {/* ... existing bullet_points rendering ... */}
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
             {/* ... existing action_items rendering ... */}
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

  // ... rest of the component remains the same ...
  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'} gap-3`}>
      {/* ... existing icons ... */}
      {isBot && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center flex-shrink-0">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      <div className={`max-w-[80%] space-y-2`}>
        <div
          className={`p-4 rounded-2xl text-base leading-relaxed ${ // Adjusted padding/leading
            isBot
              ? 'bg-white shadow-sm'
              : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
          }`}
        >
          {/* Ensure message.text and message.text.sections exist */}
          {message?.text?.sections?.map((section, index) => renderSection(section, index))}
        </div>
        {/* Cards display for bot messages */}
        {isBot && message.cards && message.cards.length > 0 && (
           // ... existing card rendering ...
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
        
        {/* Smart Swadhan Guidance Button */}
        {isBot && message.showGuidanceButton && onShowGuidance && (
          <button
            onClick={onShowGuidance}
            className="mt-3 px-4 py-2 bg-gradient-to-r from-red-600 to-purple-600 text-white rounded-lg hover:from-red-700 hover:to-purple-700 transition-all flex items-center gap-2 text-sm font-medium"
          >
            <Navigation className="w-4 h-4" />
            Show Visual Navigation Guide
          </button>
        )}
      </div>
       {/* ... existing icons ... */}
       {!isBot && (
        <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center flex-shrink-0">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default MessageBubble;