import React, { useState, useEffect } from 'react';
import { 
  ChevronRight, 
  Globe, 
  Menu, 
  FileText, 
  Calculator, 
  ShoppingCart, 
  Download, 
  Phone,
  CheckCircle,
  ArrowRight,
  Eye,
  MousePointer
} from 'lucide-react';

const SmartSwadhanGuidance = ({ isVisible, onClose, userQuery = "" }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [guidanceData, setGuidanceData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isAutoPlay, setIsAutoPlay] = useState(false);
  const [scrapingMode, setScrapingMode] = useState('');
  const [processingTime, setProcessingTime] = useState(0);

  // Fetch guidance data when component becomes visible OR when userQuery changes
  useEffect(() => {
    if (isVisible) {
      // Always fetch fresh data when query changes or component becomes visible
      fetchGuidanceData();
    }
  }, [isVisible, userQuery]); // Added userQuery as dependency

  // Reset current step when userQuery changes
  useEffect(() => {
    if (userQuery) {
      setCurrentStep(0);
      setGuidanceData(null); // Clear previous data
    }
  }, [userQuery]);

  // Auto-play functionality
  useEffect(() => {
    if (isAutoPlay && guidanceData && currentStep < guidanceData.total_steps - 1) {
      const timer = setTimeout(() => {
        setCurrentStep(prev => prev + 1);
      }, 3000); // 3 seconds per step
      return () => clearTimeout(timer);
    }
  }, [isAutoPlay, currentStep, guidanceData]);

  const fetchGuidanceData = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/smart_swadhan_guidance', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          query: userQuery || 'Guide me to SBI Life product' 
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Guidance data received:', data);
      setGuidanceData(data);
      setScrapingMode(data.mode || 'unknown');
      setProcessingTime(data.processing_time || 0);
    } catch (error) {
      console.error('Error fetching guidance data:', error);
      // Set fallback data in case of error
      setGuidanceData(getFallbackGuidanceData());
    } finally {
      setLoading(false);
    }
  };

  const getFallbackGuidanceData = () => ({
    success: true,
    total_steps: 6,
    navigation_steps: [
      {
        step: 1,
        title: "SBI Life Homepage",
        description: "Starting at the SBI Life homepage with the main navigation menu",
        visual_elements: [
          "SBI Life logo with 25 years celebration",
          "Navigation menu: LEARN, PRODUCTS, SERVICES, ABOUT, CONTACT US",
          "Main banner with insurance messaging",
          "Online Plans button prominently displayed"
        ]
      },
      {
        step: 2,
        title: "Products Menu",
        description: "Hovering over PRODUCTS shows dropdown options",
        visual_elements: [
          "Individual Life Insurance Plans option",
          "Group Insurance Plans option",
          "Dropdown menu with various plan categories"
        ]
      },
      {
        step: 3,
        title: "Individual Plans Categories",
        description: "Viewing individual plan categories",
        visual_elements: [
          "Online Plans", "Saving Plans", "Protection Plans",
          "Wealth Creation with Insurance", "Retirement Plans", "Child Plans"
        ]
      },
      {
        step: 4,
        title: "Smart Swadhan Supreme Found",
        description: "Locating Smart Swadhan Supreme in product listings",
        visual_elements: [
          "SBI Life - Smart Swadhan Supreme (highlighted)",
          "Other products listed alongside"
        ]
      },
      {
        step: 5,
        title: "Product Details Page",
        description: "Comprehensive Smart Swadhan Supreme information",
        visual_elements: [
          "Product title and UIN", "Key features", "Benefits overview",
          "Calculate Premium button", "Buy Online button"
        ]
      },
      {
        step: 6,
        title: "Ready to Proceed",
        description: "All information available for next steps",
        visual_elements: [
          "Calculate Premium", "Buy Online", "Download Brochure", "Talk to Advisor"
        ]
      }
    ],
    product_summary: `🏆 **SBI Life - Smart Swadhan Supreme**

📋 **Product Details:**
• UIN: 111N140V02
• Type: Individual, Non-Linked, Non-Participating Life Insurance Savings Product

🎯 **Key Features:**
• Life insurance protection for family security
• Return of total premium paid at policy maturity
• Affordable premium structure
• Tax benefits under current tax laws`,
    recommended_actions: [
      "Calculate Premium for personalized quote",
      "Download Brochure for detailed information",
      "Talk to Advisor for consultation",
      "Buy Online for immediate purchase"
    ]
  });

  const getStepIcon = (stepNumber) => {
    const icons = [
      <Globe className="w-6 h-6" />,
      <Menu className="w-6 h-6" />,
      <FileText className="w-6 h-6" />,
      <Eye className="w-6 h-6" />,
      <FileText className="w-6 h-6" />,
      <CheckCircle className="w-6 h-6" />
    ];
    return icons[stepNumber - 1] || <ChevronRight className="w-6 h-6" />;
  };

  const getCurrentStepData = () => {
    if (!guidanceData || !guidanceData.navigation_steps) return null;
    return guidanceData.navigation_steps[currentStep];
  };

  const handleNextStep = () => {
    if (guidanceData && currentStep < guidanceData.total_steps - 1) {
      setCurrentStep(prev => prev + 1);
    }
  };

  const handlePrevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const toggleAutoPlay = () => {
    setIsAutoPlay(!isAutoPlay);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-red-600 to-purple-600 text-white p-6">
          <div className="flex justify-between items-center">
            <div>
              <h2 className="text-2xl font-bold">SBI Life Product - Navigation Guide</h2>
              {scrapingMode && (
                <div className="flex items-center mt-2 space-x-4">
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    scrapingMode === 'real_time_scraping' 
                      ? 'bg-green-500 text-white' 
                      : 'bg-blue-500 text-white'
                  }`}>
                    {scrapingMode === 'real_time_scraping' ? '🌐 Live Scraping' : '⚡ Fast Simulation'}
                  </span>
                  {processingTime > 0 && (
                    <span className="text-sm opacity-90">
                      ⏱️ {processingTime.toFixed(2)}s
                    </span>
                  )}
                </div>
              )}
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
            >
              ✕
            </button>
          </div>
          
          {/* Progress Bar */}
          {guidanceData && (
            <div className="mt-4">
              <div className="flex justify-between text-sm mb-2">
                <span>Step {currentStep + 1} of {guidanceData.total_steps}</span>
                <span>{Math.round(((currentStep + 1) / guidanceData.total_steps) * 100)}%</span>
              </div>
              <div className="w-full bg-white bg-opacity-30 rounded-full h-2">
                <div 
                  className="bg-white h-2 rounded-full transition-all duration-300"
                  style={{ width: `${((currentStep + 1) / guidanceData.total_steps) * 100}%` }}
                ></div>
              </div>
            </div>
          )}
        </div>

        <div className="flex h-[60vh]">
          {/* Left Side - Step Navigation */}
          <div className="w-1/3 bg-gray-50 p-4 overflow-y-auto">
            <h3 className="font-semibold text-lg mb-4">Navigation Steps</h3>
            
            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-red-600 mx-auto"></div>
                <p className="mt-2 text-gray-600">Loading guidance...</p>
              </div>
            ) : (
              guidanceData?.navigation_steps?.map((step, index) => (
                <div
                  key={index}
                  className={`flex items-center p-3 mb-2 rounded-lg cursor-pointer transition-all ${
                    index === currentStep
                      ? 'bg-red-100 border-l-4 border-red-600'
                      : index < currentStep
                      ? 'bg-green-50 border-l-4 border-green-500'
                      : 'bg-white border-l-4 border-gray-200 hover:bg-gray-100'
                  }`}
                  onClick={() => setCurrentStep(index)}
                >
                  <div className={`mr-3 ${
                    index === currentStep ? 'text-red-600' : 
                    index < currentStep ? 'text-green-600' : 'text-gray-400'
                  }`}>
                    {getStepIcon(step.step)}
                  </div>
                  <div className="flex-1">
                    <h4 className="font-medium text-sm">{step.title}</h4>
                    <p className="text-xs text-gray-600 mt-1 line-clamp-2">
                      {step.description}
                    </p>
                  </div>
                  {index < currentStep && (
                    <CheckCircle className="w-5 h-5 text-green-600 ml-2" />
                  )}
                </div>
              ))
            )}
          </div>

          {/* Right Side - Step Details */}
          <div className="w-2/3 p-6 overflow-y-auto">
            {loading ? (
              <div className="text-center py-16">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Preparing your guidance...</p>
              </div>
            ) : (
              getCurrentStepData() && (
                <div>
                  <div className="flex items-center mb-4">
                    <div className="bg-red-600 text-white p-2 rounded-full mr-3">
                      {getStepIcon(getCurrentStepData().step)}
                    </div>
                    <h3 className="text-xl font-bold">{getCurrentStepData().title}</h3>
                  </div>

                  <p className="text-gray-700 mb-6 leading-relaxed">
                    {getCurrentStepData().description}
                  </p>

                  {/* Visual Elements */}
                  {getCurrentStepData().visual_elements && (
                    <div className="mb-6">
                      <h4 className="font-semibold mb-3 flex items-center">
                        <Eye className="w-4 h-4 mr-2" />
                        What You'll See:
                      </h4>
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <ul className="space-y-2">
                          {getCurrentStepData().visual_elements.map((element, index) => (
                            <li key={index} className="flex items-start">
                              <ArrowRight className="w-4 h-4 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                              <span className="text-sm">{element}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                  {/* Next Action */}
                  {getCurrentStepData().next_action && (
                    <div className="bg-yellow-50 p-4 rounded-lg mb-6">
                      <h4 className="font-semibold mb-2 flex items-center">
                        <MousePointer className="w-4 h-4 mr-2" />
                        Next Action:
                      </h4>
                      <p className="text-sm">{getCurrentStepData().next_action}</p>
                    </div>
                  )}

                  {/* Product Data (for final step) */}
                  {currentStep === (guidanceData?.total_steps - 1) && guidanceData?.product_summary && (
                    <div className="bg-green-50 p-4 rounded-lg mb-6">
                      <h4 className="font-semibold mb-3">Product Information:</h4>
                      <div className="text-sm whitespace-pre-line">
                        {guidanceData.product_summary}
                      </div>
                    </div>
                  )}
                </div>
              )
            )}
          </div>
        </div>

        {/* Footer Controls */}
        <div className="bg-gray-50 p-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleAutoPlay}
              className={`px-4 py-2 rounded-lg transition-colors ${
                isAutoPlay 
                  ? 'bg-red-600 text-white' 
                  : 'bg-white border border-gray-300 text-gray-700 hover:bg-gray-50'
              }`}
            >
              {isAutoPlay ? 'Pause Auto-Play' : 'Start Auto-Play'}
            </button>
            
            <span className="text-sm text-gray-600">
              Click steps to jump around or use auto-play
            </span>
            
            {guidanceData?.note && (
              <span className="text-xs text-gray-500 max-w-xs truncate">
                💡 {guidanceData.note}
              </span>
            )}
          </div>

          <div className="flex space-x-2">
            <button
              onClick={handlePrevStep}
              disabled={currentStep === 0}
              className="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            
            <button
              onClick={handleNextStep}
              disabled={!guidanceData || currentStep >= guidanceData.total_steps - 1}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
            
            {currentStep === (guidanceData?.total_steps - 1) && (
              <button
                onClick={onClose}
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 ml-2"
              >
                Complete ✓
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SmartSwadhanGuidance;
