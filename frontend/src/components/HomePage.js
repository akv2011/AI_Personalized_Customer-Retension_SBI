import React, { useState } from 'react';
import { 
  Search,
  Menu,
  Shield, 
  MessageCircle,
  X,
  ChevronRight,
  Gift,
  Heart,
  Home,
  Car,
  GraduationCap,
  Phone,
  MapPin,
  Calculator,
  Download,
  CreditCard,
  Star,
  Play,
  Facebook,
  Twitter,
  Linkedin,
  Youtube,
  Instagram,
  Users,
  ArrowRight,
  Globe,
  ChevronLeft,
  UserPlus,
  ChevronDown
} from 'lucide-react';
import ChatInterface from './ChatInterface';

const getDropdownColor = (bgColor) => {
  const colorMap = {
    'bg-red-500': '#ef4444',
    'bg-red-600': '#dc2626',
    'bg-blue-600': '#2563eb',
    'bg-purple-600': '#9333ea',
    'bg-purple-700': '#7e22ce'
  };
  return colorMap[bgColor] || '#2563eb';
};

const HomePage = () => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isLanguageOpen, setIsLanguageOpen] = useState(false);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('English');
  const [isJoinUsOpen, setIsJoinUsOpen] = useState(false);
  const [selectedService, setSelectedService] = useState(null);
  const [hoveredNavItem, setHoveredNavItem] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [focusedNavItem, setFocusedNavItem] = useState(null);
  const navRef = React.useRef(null);
  
  // Handle keyboard navigation
  const handleKeyDown = (e, item) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        setHoveredNavItem(item.name);
        setFocusedNavItem(item.name);
        break;
      case 'Escape':
        e.preventDefault();
        setHoveredNavItem(null);
        setFocusedNavItem(null);
        break;
      case 'ArrowDown':
        e.preventDefault();
        if (hoveredNavItem === item.name) {
          // Focus first dropdown item
          const dropdown = document.querySelector(`[data-dropdown="${item.name}"]`);
          const firstItem = dropdown?.querySelector('a');
          firstItem?.focus();
        }
        break;
      case 'Tab':
        if (hoveredNavItem === item.name && !e.shiftKey) {
          const dropdown = document.querySelector(`[data-dropdown="${item.name}"]`);
          const items = dropdown?.querySelectorAll('a');
          if (items?.length && document.activeElement === items[items.length - 1]) {
            setHoveredNavItem(null);
          }
        }
        break;
    }
  };

  // Auto-slide carousel
  React.useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Close dropdowns when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event) => {
      if (!event.target.closest('.dropdown-container')) {
        setIsLanguageOpen(false);
        setIsLoginOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Close mobile menu when screen size changes
  React.useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth >= 1024) { // lg breakpoint
        setIsMobileMenuOpen(false);
      }
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
    { code: 'gu', name: 'ગુજરાતી', flag: '🇮🇳' },
    { code: 'mr', name: 'मराठी', flag: '🇮🇳' },
    { code: 'ta', name: 'தமிழ்', flag: '🇮🇳' },
    { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
    { code: 'kn', name: 'ಕನ್ನಡ', flag: '🇮🇳' },
    { code: 'bn', name: 'বাংলা', flag: '🇮🇳' }
  ];

  const loginOptions = [
    { 
      name: 'Customer Portal', 
      description: 'View policies, pay premiums, download documents',
      icon: Users,
      url: 'https://customer.sbilife.co.in/'
    },
    { 
      name: 'Agent Portal', 
      description: 'Agent dashboard and tools',
      icon: Shield,
      url: 'https://agent.sbilife.co.in/'
    },
    { 
      name: 'Employee Portal', 
      description: 'Employee access and resources',
      icon: Heart,
      url: 'https://employee.sbilife.co.in/'
    }
  ];

  const joinUsOptions = [
    {
      title: 'Become an Agent',
      description: 'Start your career as a SBI Life insurance agent and help people secure their future.',
      benefits: ['Attractive Commission', 'Training Support', 'Career Growth', 'Flexible Working'],
      icon: Shield,
      cta: 'Apply Now'
    },
    {
      title: 'Career Opportunities',
      description: 'Join our team and be part of India\'s leading life insurance company.',
      benefits: ['Competitive Salary', 'Growth Opportunities', 'Employee Benefits', 'Work-Life Balance'],
      icon: Heart,
      cta: 'View Jobs'
    },
    {
      title: 'Business Partnership',
      description: 'Partner with us to expand your business offerings and serve more customers.',
      benefits: ['Business Growth', 'Support & Training', 'Brand Association', 'Revenue Sharing'],
      icon: Users,
      cta: 'Partner With Us'
    }
  ];

  const serviceDetails = {
    'Nav & Fund Value': {
      title: 'NAV & Fund Performance',
      description: 'Check the latest NAV (Net Asset Value) and fund performance for your ULIP policies.',
      features: ['Real-time NAV updates', 'Fund performance charts', 'Historical data', 'Fund switching options'],
      url: 'https://www.sbilife.co.in/en/nav-fund-performance'
    },
    'Pay Premium': {
      title: 'Premium Payment',
      description: 'Pay your insurance premiums easily and securely online.',
      features: ['Multiple payment options', 'Auto-pay setup', 'Payment history', 'SMS/Email receipts'],
      url: 'https://www.sbilife.co.in/en/pay-premium'
    },
    'Tools & Calculator': {
      title: 'Insurance Calculators',
      description: 'Use our advanced calculators to plan your insurance needs and investments.',
      features: ['Premium calculator', 'ULIP calculator', 'Retirement planner', 'Human Life Value calculator'],
      url: 'https://www.sbilife.co.in/en/tools-calculators'
    },
    'Download Forms': {
      title: 'Forms & Documents',
      description: 'Download important forms and documents for your insurance policies.',
      features: ['Policy forms', 'Claim forms', 'Service request forms', 'Product brochures'],
      url: 'https://www.sbilife.co.in/en/download-centre'
    }
  };
  
  const heroSlides = [
    {
      title: "Apne iraadon ko, smart guarantee do.",
      subtitle: "SBI Life - Smart Platina Supreme ke guaranteed returns se, karo poore apne iraade, apno se kiye sabhi vaade.",
      bgColor: "from-pink-500 via-red-500 to-purple-800",
      image: "https://www.sbilife.co.in/content/dam/sbilife/hero-banner/couple-image.jpg"
    },
    {
      title: "Shield Your Family's Future",
      subtitle: "Comprehensive protection plans that secure your loved ones' financial well-being.",
      bgColor: "from-blue-600 via-blue-700 to-purple-800",
      image: "https://www.sbilife.co.in/content/dam/sbilife/hero-banner/family-protection.jpg"
    },
    {
      title: "Retirement Planning Made Simple",
      subtitle: "Plan today for a worry-free tomorrow with our retirement solutions.",
      bgColor: "from-green-600 via-teal-600 to-blue-800",
      image: "https://www.sbilife.co.in/content/dam/sbilife/hero-banner/retirement-planning.jpg"
    },
    {
      title: "Child's Bright Future Starts Here",
      subtitle: "Give wings to your child's dreams with our education planning solutions.",
      bgColor: "from-orange-500 via-red-500 to-pink-700",
      image: "https://www.sbilife.co.in/content/dam/sbilife/hero-banner/child-education.jpg"
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + heroSlides.length) % heroSlides.length);
  };

  const navigationItems = [
    { 
      name: 'LEARN', 
      href: '#', 
      subtitle: 'Awareness is assurance', 
      bgColor: 'bg-red-500',
      dropdownItems: [
        { title: 'About Life Insurance', href: '#', description: 'Understanding life insurance basics' },
        { title: 'Insurance Guides', href: '#', description: 'Comprehensive guides for better decisions' },
        { title: 'Financial Planning', href: '#', description: 'Plan your financial future' },
        { title: 'Insurance Videos', href: '#', description: 'Learn through our informative videos' },
        { title: 'Insurance Calculators', href: '#', description: 'Calculate your insurance needs' },
        { title: 'Insurance Glossary', href: '#', description: 'Understand insurance terms' }
      ]
    },
    { 
      name: 'PRODUCTS', 
      href: '#', 
      subtitle: 'Plans to Manage Your needs', 
      bgColor: 'bg-red-600',
      dropdownItems: [
        { title: 'Term Insurance', href: '#', description: 'Pure life coverage at affordable rates' },
        { title: 'Savings Plans', href: '#', description: 'Secure your future financially' },
        { title: 'Child Plans', href: '#', description: 'Secure your child\'s education and future' },
        { title: 'Retirement Plans', href: '#', description: 'Plan for a comfortable retirement' },
        { title: 'Health Insurance', href: '#', description: 'Protect against medical expenses' },
        { title: 'ULIP Plans', href: '#', description: 'Investment with insurance benefits' },
        { title: 'Group Insurance', href: '#', description: 'Insurance solutions for organizations' }
      ]
    },
    { 
      name: 'SERVICES', 
      href: '#', 
      subtitle: 'For Existing Customers', 
      bgColor: 'bg-blue-600',
      dropdownItems: [
        { title: 'Pay Premium', href: '#', description: 'Quick and easy premium payment options' },
        { title: 'Policy Services', href: '#', description: 'Access and manage your policies' },
        { title: 'Claims & Maturity', href: '#', description: 'Easy and hassle-free claim process' },
        { title: 'Download Forms', href: '#', description: 'Access all required documentation' },
        { title: 'NAV & Fund Performance', href: '#', description: 'Track your investment performance' },
        { title: 'Branch Locator', href: '#', description: 'Find SBI Life branches near you' }
      ]
    },
    { 
      name: 'ABOUT', 
      href: '#', 
      subtitle: 'SBI Life', 
      bgColor: 'bg-purple-600',
      dropdownItems: [
        { title: 'Company Profile', href: '#', description: 'Know more about SBI Life' },
        { title: 'Board of Directors', href: '#', description: 'Meet our leadership team' },
        { title: 'Financial Information', href: '#', description: 'View our financial performance' },
        { title: 'CSR Initiatives', href: '#', description: 'Our corporate social responsibility' },
        { title: 'Awards & Recognition', href: '#', description: 'Our achievements' },
        { title: 'Career Opportunities', href: '#', description: 'Join our growing team' }
      ]
    },
    { 
      name: 'CONTACT-US', 
      href: '#', 
      subtitle: 'SBI Life', 
      bgColor: 'bg-purple-700',
      dropdownItems: [
        { title: 'Customer Care', href: '#', description: '24x7 support for all your queries' },
        { title: 'Grievance Redressal', href: '#', description: 'Resolution for your concerns' },
        { title: 'Branch Network', href: '#', description: 'Visit our offices across India' },
        { title: 'Feedback', href: '#', description: 'Share your experience with us' },
        { title: 'Contact Information', href: '#', description: 'Reach out to us' }
      ]
    }
  ];

  const secondaryNavItems = [
    'Services',
    'Claims and Maturity', 
    'NRI Corner',
    'Download Centre',
    'NAV & Fund Performance',
    'FAQs'
  ];

  const lifeInsurancePlans = [
    {
      title: "Child Education",
      subtitle: "Child's Future Planning",
      description: "Give wings to your child's dreams by saving today",
      videoUrl: "https://youtu.be/cxs7RDMhAdY",
      link: "/child-plans"
    },
    {
      title: "Care-free Retirement",
      subtitle: "Care-free retirement Life",
      description: "Plan today to enjoy your golden years, worry-free",
      videoUrl: "https://youtu.be/s4oJEo5T9QM",
      link: "/retirement-plans"
    },
    {
      title: "Financial Security",
      subtitle: "Financial Security",
      description: "Ensure your family's financial security and happiness",
      videoUrl: "https://youtu.be/rPjz9MvtE7g",
      link: "/savings-plans"
    },
    {
      title: "Family's Protection",
      subtitle: "Protect Family",
      description: "Secure your family's future with comprehensive protection",
      videoUrl: "https://youtu.be/jn1BeH7GNTA",
      link: "/protection-plans"
    },
    {
      title: "Wealth creation",
      subtitle: "Wealth Creation ULIPs",
      description: "Build wealth for your future with our investment plans",
      videoUrl: "https://youtu.be/5rHQ0ZYhRts",
      link: "/wealth-creation-plans"
    }
  ];

  const quickLinks = [
    'Nav & Fund Value',
    'Pay Premium',
    'Tools & Calculator',
    'Download Forms'
  ];

  const stats = [
    { value: "Over 2,56,473 crores", label: "Claims paid till date*", button: "Make a Claim", buttonColor: "bg-red-600 hover:bg-red-700" },
    { value: "1086", label: "Branches Across India#", button: "Locate us near you", buttonColor: "bg-green-600 hover:bg-green-700" },
    { value: "7,62,63,543", label: "Policy Holders^", button: "Become a customer today", buttonColor: "bg-purple-600 hover:bg-purple-700" }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Top Notification Banner */}
      <div className="bg-red-600 text-white text-center py-2 text-sm">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-center">
          <span className="mr-2">📢</span>
          <span>Important: Beware of fraudulent calls/SMS. SBI Life never asks for OTP/PIN. Report suspicious activity immediately.</span>
          <button className="ml-4 hover:underline">Learn More</button>
        </div>
      </div>

      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Top Bar */}
          <div className="flex justify-between items-center py-2 border-b border-gray-200">
            <div className="flex items-center">
              <img 
                src="/SBI_Logo_original.png" 
                alt="SBI Life"
                className="h-12"
                onError={(e) => {
                  e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='40' viewBox='0 0 120 40'%3E%3Crect width='120' height='40' fill='%23003d82'/%3E%3Ctext x='60' y='25' font-family='Arial' font-size='14' fill='white' text-anchor='middle'%3ESBI Life%3C/text%3E%3C/svg%3E";
                }}
              />
              <img 
                src="/SBI_Logo_25years.png" 
                alt="25 Years"
                className="h-8 ml-2"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
            <div className="flex items-center space-x-6">
              <button 
                className="flex items-center text-sm text-gray-600 hover:text-blue-600"
                onClick={() => setIsJoinUsOpen(true)}
              >
                <UserPlus className="w-4 h-4 mr-1" />
                Join Us
              </button>
              
              {/* Language Selector */}
              <div className="relative dropdown-container">
                <button 
                  className="flex items-center text-sm text-gray-600 hover:text-blue-600"
                  onClick={() => {
                    setIsLanguageOpen(!isLanguageOpen);
                    setIsLoginOpen(false);
                  }}
                >
                  <Globe className="w-4 h-4 mr-1" />
                  <span>{selectedLanguage}</span>
                  <ChevronDown className={`w-4 h-4 ml-1 transition-transform ${isLanguageOpen ? 'rotate-180' : ''}`} />
                </button>
                {isLanguageOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                    <div className="py-2">
                      <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase">Select Language</div>
                      {languages.map((lang) => (
                        <button
                          key={lang.code}
                          className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 flex items-center"
                          onClick={() => {
                            setSelectedLanguage(lang.name);
                            setIsLanguageOpen(false);
                          }}
                        >
                          <span className="mr-2">{lang.flag}</span>
                          <span>{lang.name}</span>
                          {selectedLanguage === lang.name && (
                            <span className="ml-auto text-blue-600">✓</span>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Login Dropdown */}
              <div className="relative dropdown-container">
                <button 
                  className="flex items-center text-sm text-gray-600 hover:text-blue-600"
                  onClick={() => {
                    setIsLoginOpen(!isLoginOpen);
                    setIsLanguageOpen(false);
                  }}
                >
                  Login
                  <ChevronDown className={`w-4 h-4 ml-1 transition-transform ${isLoginOpen ? 'rotate-180' : ''}`} />
                </button>
                {isLoginOpen && (
                  <div className="absolute right-0 mt-2 w-72 bg-white border border-gray-200 rounded-md shadow-lg z-50">
                    <div className="py-2">
                      <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase">Login Options</div>
                      {loginOptions.map((option, index) => (
                        <a
                          key={index}
                          href={option.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 border-b border-gray-100 last:border-b-0"
                        >
                          <div className="flex items-start">
                            <option.icon className="w-5 h-5 text-blue-600 mr-3 mt-0.5" />
                            <div>
                              <div className="font-medium">{option.name}</div>
                              <div className="text-xs text-gray-500 mt-1">{option.description}</div>
                            </div>
                            <ArrowRight className="w-4 h-4 text-gray-400 ml-auto mt-0.5" />
                          </div>
                        </a>
                      ))}
                      <div className="px-4 py-3 border-t border-gray-200">
                        <p className="text-xs text-gray-500">
                          Need help? <a href="#" className="text-blue-600 hover:underline">Contact Support</a>
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Main Navigation */}
          <nav className="py-0" ref={navRef}>
            <div className="flex justify-between items-center">
              {/* Mobile Menu Button */}
              <button
                className="lg:hidden p-2 text-gray-600"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                aria-label="Toggle navigation menu"
                aria-expanded={isMobileMenuOpen}
              >
                {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
              </button>

              {/* Desktop Navigation */}
              <div className="hidden lg:flex relative">
                {navigationItems.map((item, index) => (
                  <div
                    key={item.name}
                    className="group"
                    onMouseEnter={() => !focusedNavItem && setHoveredNavItem(item.name)}
                    onMouseLeave={() => !focusedNavItem && setHoveredNavItem(null)}
                    onKeyDown={(e) => handleKeyDown(e, item)}
                  >
                    <div
                      className={`${item.bgColor} text-white px-6 py-4 text-center group-hover:opacity-100 transition-all duration-200 relative`}
                      style={{ 
                        clipPath: index === navigationItems.length - 1 ? 'none' : 'polygon(0 0, calc(100% - 20px) 0, 100% 50%, calc(100% - 20px) 100%, 0 100%)'
                      }}
                    >
                      <button
                        id={`navitem-${item.name}`}
                        className="block w-full text-left relative focus:outline-none focus:ring-2 focus:ring-white focus:ring-opacity-50"
                        onClick={(e) => {
                          e.preventDefault();
                          setHoveredNavItem(hoveredNavItem === item.name ? null : item.name);
                        }}
                        onKeyDown={(e) => handleKeyDown(e, item)}
                        aria-expanded={hoveredNavItem === item.name}
                        aria-haspopup="true"
                        aria-controls={`dropdown-${item.name}`}
                      >
                        <div className="font-bold text-sm group-hover:transform group-hover:translate-y-[-2px] transition-transform">
                          {item.name}
                          <div className="absolute bottom-[-2px] left-1/2 transform -translate-x-1/2 w-0 h-0.5 bg-white group-hover:w-full transition-all duration-200"></div>
                        </div>
                        <div className="text-xs opacity-90">{item.subtitle}</div>
                      </button>
                    </div>
                    
                    {/* Dropdown Menu */}
                    <div 
                      className={`absolute left-0 w-full bg-white shadow-xl rounded-b-lg overflow-hidden z-50 border-t-2 transition-all duration-300 transform origin-top
                        ${hoveredNavItem === item.name 
                          ? 'opacity-100 translate-y-0 visible' 
                          : 'opacity-0 -translate-y-4 invisible'}`}
                      style={{
                        borderTopColor: hoveredNavItem === item.name 
                          ? getDropdownColor(item.bgColor) 
                          : 'transparent',
                        minWidth: '300px',
                        maxWidth: '400px'
                      }}
                      role="menu"
                      aria-orientation="vertical"
                      aria-labelledby={`navitem-${item.name}`}
                      data-dropdown={item.name}
                    >
                      <div className="p-6">
                        <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                          {item.name}
                          <div className="h-px flex-1 bg-gray-200 ml-4"></div>
                        </h3>
                        <div className="grid gap-2">
                          {item.dropdownItems.map((dropdownItem, idx) => (
                            <a
                              key={idx}
                              href={dropdownItem.href}
                              className="flex items-start p-3 hover:bg-gray-50 rounded-lg group transition-all duration-200"
                            >
                              <div className="relative pl-6">
                                <div className="absolute left-0 top-[10px] w-2 h-2 rounded-full bg-gray-300 group-hover:bg-blue-500 transition-colors"></div>
                                <div>
                                  <div className="font-medium text-gray-900 group-hover:text-blue-600 transition-colors">
                                    {dropdownItem.title}
                                  </div>
                                  <p className="text-sm text-gray-500 mt-0.5 group-hover:text-gray-600 transition-colors">
                                    {dropdownItem.description}
                                  </p>
                                </div>
                              </div>
                              <div className="ml-auto pl-4">
                                <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transform group-hover:translate-x-1 transition-all" />
                              </div>
                            </a>
                          ))}
                        </div>
                      </div>
                      <div className="bg-gray-50 px-6 py-4 border-t border-gray-100">
                        <a 
                          href={item.href} 
                          className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center justify-between group"
                        >
                          <span className="flex items-center">
                            View All {item.name} Resources
                            <ArrowRight className="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" />
                          </span>
                          <span className="text-gray-400 text-xs">{item.dropdownItems.length} items</span>
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex items-center space-x-4">
                <button className="bg-yellow-400 text-black px-6 py-3 rounded-lg font-bold text-sm flex items-center hover:bg-yellow-300 transition-colors">
                  <Globe className="w-4 h-4 mr-2" />
                  Online Plans
                </button>
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search..."
                    className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" />
                </div>
                <button 
                  className="lg:hidden p-2"
                  onClick={() => setIsMenuOpen(!isMenuOpen)}
                >
                  <Menu className="w-6 h-6" />
                </button>
              </div>
            </div>
          </nav>

          {/* Secondary Navigation */}
          <div className="bg-purple-900 -mx-4 px-4 sm:-mx-6 sm:px-6 lg:-mx-8 lg:px-8">
            <div className="flex justify-center space-x-8 py-3 overflow-x-auto">
              {secondaryNavItems.map((item) => (
                <a
                  key={item}
                  href="#"
                  className="text-white hover:text-yellow-400 font-medium text-sm whitespace-nowrap transition-colors"
                >
                  {item}
                </a>
              ))}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className={`relative bg-gradient-to-r ${heroSlides[currentSlide].bgColor} text-white min-h-[500px] flex items-center`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            <div className="space-y-6">
              <h1 className="text-4xl md:text-5xl font-bold leading-tight">
                {heroSlides[currentSlide].title}
              </h1>
              <p className="text-lg md:text-xl text-white opacity-90">
                {heroSlides[currentSlide].subtitle}
              </p>
              <div className="flex space-x-4">
                <button className="bg-white text-blue-900 px-8 py-3 rounded-lg font-bold hover:bg-gray-100 transition-colors">
                  Know More
                </button>
                <button className="border-2 border-white text-white px-8 py-3 rounded-lg font-bold hover:bg-white hover:text-blue-900 transition-colors">
                  Get Quote
                </button>
              </div>
            </div>
            <div className="flex justify-center lg:justify-end">
              <img 
                src={heroSlides[currentSlide].image}
                alt="Insurance"
                className="max-w-md w-full h-auto rounded-lg"
                onError={(e) => {
                  e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300' viewBox='0 0 400 300'%3E%3Crect width='400' height='300' fill='%23f3f4f6'/%3E%3Ctext x='200' y='150' font-family='Arial' font-size='16' fill='%236b7280' text-anchor='middle'%3EInsurance Image%3C/text%3E%3C/svg%3E";
                }}
              />
            </div>
          </div>
        </div>
        
        {/* Navigation Arrows */}
        <button 
          onClick={prevSlide}
          className="absolute left-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center hover:bg-opacity-30 transition-all"
        >
          <ChevronLeft className="w-6 h-6 text-white" />
        </button>
        <button 
          onClick={nextSlide}
          className="absolute right-4 top-1/2 transform -translate-y-1/2 w-12 h-12 bg-white bg-opacity-20 rounded-full flex items-center justify-center hover:bg-opacity-30 transition-all"
        >
          <ChevronRight className="w-6 h-6 text-white" />
        </button>
        
        {/* Slide Indicators */}
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`w-3 h-3 rounded-full transition-all ${
                index === currentSlide ? 'bg-white' : 'bg-white bg-opacity-50'
              }`}
            />
          ))}
        </div>
      </section>

      {/* Product Card Section */}
      <section className="py-8 bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
            <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center space-y-4 lg:space-y-0">
              <div className="flex items-start space-x-4">
                <div className="w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Shield className="w-8 h-8 text-blue-600" />
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900">SBI Life - Smart Platina Supreme</h3>
                  <p className="text-sm text-gray-600 mb-1">UIN : 111N171V01</p>
                  <p className="text-xs text-gray-500">Individual, Non-Linked, Non-Participating, Life Insurance Savings Product</p>
                  <div className="flex items-center mt-2 space-x-4">
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-400 fill-current" />
                      <span className="text-sm text-gray-600 ml-1">Guaranteed Returns</span>
                    </div>
                    <div className="flex items-center">
                      <Gift className="w-4 h-4 text-green-600" />
                      <span className="text-sm text-gray-600 ml-1">Tax Benefits</span>
                    </div>
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="space-y-2">
                  <button className="bg-blue-800 text-white px-8 py-3 rounded-lg font-bold hover:bg-blue-900 transition-colors block">
                    Know More
                  </button>
                  <button className="bg-green-600 text-white px-8 py-3 rounded-lg font-bold hover:bg-green-700 transition-colors block">
                    Buy Online
                  </button>
                </div>
                <div className="text-xs text-gray-500 mt-2">
                  SBI LIFE INSURANCE COMPANY LTD. | IRDAI REGD. NO. 111<br/>
                  CIN: L99999MH2000PLC129113 3G • 4/19/24•VER/B/ENG
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Life Insurance Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-black mb-4">Life Insurance</h1>
            <h2 className="text-2xl text-gray-700">Live your best life today, your tomorrow is secured with us</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
            {lifeInsurancePlans.map((plan, index) => (
              <div key={index} className="bg-white rounded-lg shadow-lg overflow-hidden group hover:shadow-xl transition-all duration-300">
                <div className="relative h-48 bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                  <div className="absolute inset-0 bg-black bg-opacity-20"></div>
                  <button className="relative w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center hover:bg-white transition-all duration-300 group-hover:scale-110">
                    <Play className="w-8 h-8 text-blue-600 ml-1" />
                  </button>
                  <div className="absolute top-4 left-4 text-white">
                    <div className="text-2xl font-bold">0{index + 1}</div>
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">{plan.title}</h3>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center group">
                    Know More 
                    <ArrowRight className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Explore Plans Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Explore With Us – Life Insurance Plans and Guides</h2>
            <p className="text-lg text-gray-600">Discover comprehensive insurance solutions tailored for your life's journey</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden group hover:shadow-xl transition-all duration-300">
              <div className="relative h-56 overflow-hidden">
                <img 
                  src="https://www.sbilife.co.in/content/dam/sbilife/explore-plans/protection-plans.jpg" 
                  alt="Insurance Protection Plan"
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250' viewBox='0 0 400 250'%3E%3Crect width='400' height='250' fill='%23e3f2fd'/%3E%3Cpath d='M180 80 L220 80 L220 120 L260 120 L260 160 L140 160 L140 120 L180 120 Z' fill='%232196f3'/%3E%3Ctext x='200' y='190' font-family='Arial' font-size='14' fill='%232196f3' text-anchor='middle'%3EProtection Plans%3C/text%3E%3C/svg%3E";
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60"></div>
                <div className="absolute bottom-4 left-4 right-4 text-white">
                  <h3 className="text-xl font-bold mb-2">Insurance Protection Plan</h3>
                  <p className="text-sm opacity-90">Secure your family's financial future</p>
                </div>
              </div>
              <div className="p-6">
                <p className="text-gray-600 mb-4 leading-relaxed">Ensure your family's financial security and happiness with comprehensive protection coverage.</p>
                <div className="flex justify-between items-center">
                  <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    View Plans
                  </button>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center">
                    Learn More <ArrowRight className="w-4 h-4 ml-1" />
                  </button>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg overflow-hidden group hover:shadow-xl transition-all duration-300">
              <div className="relative h-56 overflow-hidden">
                <img 
                  src="https://www.sbilife.co.in/content/dam/sbilife/explore-plans/retirement-plans.jpg" 
                  alt="Retirement Benefits"
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250' viewBox='0 0 400 250'%3E%3Crect width='400' height='250' fill='%23fff3e0'/%3E%3Ccircle cx='200' cy='100' r='30' fill='%23ff9800'/%3E%3Cpath d='M170 130 Q200 150 230 130' stroke='%23ff9800' stroke-width='3' fill='none'/%3E%3Ctext x='200' y='190' font-family='Arial' font-size='14' fill='%23ff9800' text-anchor='middle'%3ERetirement Plans%3C/text%3E%3C/svg%3E";
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60"></div>
                <div className="absolute bottom-4 left-4 right-4 text-white">
                  <h3 className="text-xl font-bold mb-2">Retirement Benefits</h3>
                  <p className="text-sm opacity-90">Plan for a worry-free golden age</p>
                </div>
              </div>
              <div className="p-6">
                <p className="text-gray-600 mb-4 leading-relaxed">Plan today to enjoy your golden years, worry-free with our comprehensive retirement solutions.</p>
                <div className="flex justify-between items-center">
                  <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    View Plans
                  </button>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center">
                    Learn More <ArrowRight className="w-4 h-4 ml-1" />
                  </button>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-lg overflow-hidden group hover:shadow-xl transition-all duration-300">
              <div className="relative h-56 overflow-hidden">
                <img 
                  src="https://www.sbilife.co.in/content/dam/sbilife/explore-plans/child-plans.jpg" 
                  alt="Child's Future Planning"
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='250' viewBox='0 0 400 250'%3E%3Crect width='400' height='250' fill='%23e8f5e8'/%3E%3Cpath d='M180 80 L220 80 L220 100 L240 100 L240 140 L160 140 L160 100 L180 100 Z' fill='%234caf50'/%3E%3Ccircle cx='200' cy='120' r='8' fill='%23fff'/%3E%3Ctext x='200' y='180' font-family='Arial' font-size='14' fill='%234caf50' text-anchor='middle'%3EChild Education%3C/text%3E%3Ctext x='200' y='200' font-family='Arial' font-size='14' fill='%234caf50' text-anchor='middle'%3EPlanning%3C/text%3E%3C/svg%3E";
                  }}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent opacity-60"></div>
                <div className="absolute bottom-4 left-4 right-4 text-white">
                  <h3 className="text-xl font-bold mb-2">Child's Future Planning</h3>
                  <p className="text-sm opacity-90">Invest in your child's dreams</p>
                </div>
              </div>
              <div className="p-6">
                <p className="text-gray-600 mb-4 leading-relaxed">Give wings to your child's dreams by saving today for their bright future and education.</p>
                <div className="flex justify-between items-center">
                  <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium">
                    View Plans
                  </button>
                  <button className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center">
                    Learn More <ArrowRight className="w-4 h-4 ml-1" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Additional Insurance Categories */}
          <div className="mt-16">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="text-center group">
                <div className="w-20 h-20 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-200 transition-colors">
                  <Shield className="w-10 h-10 text-blue-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Term Insurance</h4>
                <p className="text-gray-600 text-sm">High coverage at affordable premiums</p>
              </div>
              <div className="text-center group">
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-green-200 transition-colors">
                  <Heart className="w-10 h-10 text-green-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Health Insurance</h4>
                <p className="text-gray-600 text-sm">Comprehensive health coverage</p>
              </div>
              <div className="text-center group">
                <div className="w-20 h-20 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-purple-200 transition-colors">
                  <GraduationCap className="w-10 h-10 text-purple-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Education Plans</h4>
                <p className="text-gray-600 text-sm">Secure your child's education</p>
              </div>
              <div className="text-center group">
                <div className="w-20 h-20 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-orange-200 transition-colors">
                  <Home className="w-10 h-10 text-orange-600" />
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Wealth Creation</h4>
                <p className="text-gray-600 text-sm">Build wealth for the future</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="py-16 bg-gradient-to-r from-blue-900 via-blue-800 to-purple-900 text-white relative overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Our Legacy of Trust</h2>
            <p className="text-xl text-blue-100">Building stronger relationships through reliable service</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            {stats.map((stat, index) => (
              <div key={index} className="bg-white bg-opacity-10 backdrop-blur-sm p-8 rounded-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300">
                <div className="text-5xl font-bold mb-4 text-yellow-400">{stat.value}</div>
                <div className="text-blue-200 text-lg mb-6">{stat.label}</div>
                
                {index === 0 && (
                  <form className="space-y-4">
                    <input 
                      type="text" 
                      placeholder="Enter Policy Number"
                      className="w-full px-4 py-3 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      maxLength="11"
                    />
                    <button className={`${stat.buttonColor} text-white px-6 py-3 rounded-lg font-medium transition-colors w-full`}>
                      {stat.button}
                    </button>
                  </form>
                )}
                
                {index === 1 && (
                  <form className="space-y-4">
                    <input 
                      type="text" 
                      placeholder="Enter City Name"
                      className="w-full px-4 py-3 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      maxLength="40"
                    />
                    <button className={`${stat.buttonColor} text-white px-6 py-3 rounded-lg font-medium transition-colors w-full`}>
                      {stat.button}
                    </button>
                  </form>
                )}
                
                {index === 2 && (
                  <form className="space-y-4">
                    <input 
                      type="text" 
                      placeholder="Enter Mobile Number"
                      className="w-full px-4 py-3 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-yellow-400"
                      maxLength="10"
                    />
                    <button className={`${stat.buttonColor} text-white px-6 py-3 rounded-lg font-medium transition-colors w-full`}>
                      {stat.button}
                    </button>
                  </form>
                )}
              </div>
            ))}
          </div>
          
          {/* Disclaimer Text */}
          <div className="mt-12 text-center text-blue-100 text-sm">
            <p>
              *As per public disclosure (L-7 - Benefits Paid) & Financial Statements (Schedule 4 - Benefits Paid) of the Company, benefits paid since inception upto period ending 31st December 2024.<br />
              <br />
              <sup>#</sup>Network of branches as on period ending 31st December 2024.<br />
              <br />
              ^Includes count of in force and paid-up individual policies along with count of lives covered under various group policies as on period ending 31st December 2024.
            </p>
          </div>
          
          {/* Additional Trust Indicators */}
          <div className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-yellow-400">25+</div>
              <div className="text-blue-200 text-sm">Years of Excellence</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-yellow-400">99.2%</div>
              <div className="text-blue-200 text-sm">Claim Settlement Ratio</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-yellow-400">₹2.5L+</div>
              <div className="text-blue-200 text-sm">Cr. Assets Under Management</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-yellow-400">AAA</div>
              <div className="text-blue-200 text-sm">Credit Rating</div>
            </div>
          </div>
        </div>
      </section>

      {/* Quick Links Section */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Quick Access</h2>
            <p className="text-lg text-gray-600">Fast and convenient services at your fingertips</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickLinks.map((link, index) => (
              <button
                key={index}
                className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 group text-center border-l-4 border-blue-500 hover:border-blue-600"
                onClick={() => setSelectedService(link)}
              >
                <div className="text-blue-600 mb-4 group-hover:scale-110 transition-transform">
                  {index === 0 && <Calculator className="w-12 h-12 mx-auto" />}
                  {index === 1 && <CreditCard className="w-12 h-12 mx-auto" />}
                  {index === 2 && <Calculator className="w-12 h-12 mx-auto" />}
                  {index === 3 && <Download className="w-12 h-12 mx-auto" />}
                </div>
                <h3 className="text-gray-800 group-hover:text-blue-600 font-semibold text-lg mb-2">{link}</h3>
                <p className="text-gray-500 text-sm">
                  {index === 0 && "Check current NAV values and fund performance"}
                  {index === 1 && "Pay your premium quickly and securely online"}
                  {index === 2 && "Calculate premiums and plan your insurance needs"}
                  {index === 3 && "Download forms, brochures and documents"}
                </p>
                <div className="mt-4 opacity-0 group-hover:opacity-100 transition-opacity">
                  <ArrowRight className="w-5 h-5 mx-auto text-blue-600" />
                </div>
              </button>
            ))}
          </div>
          
          {/* Additional Services Row */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg">
              <div className="flex items-center mb-4">
                <Phone className="w-8 h-8 mr-3" />
                <h3 className="text-xl font-bold">Customer Care</h3>
              </div>
              <p className="mb-4">Get instant support for all your queries</p>
              <button className="bg-white text-blue-600 px-4 py-2 rounded font-medium hover:bg-gray-100 transition-colors">
                Call Now: 1800-267-9090
              </button>
            </div>
            
            <div className="bg-gradient-to-r from-green-600 to-teal-600 text-white p-6 rounded-lg">
              <div className="flex items-center mb-4">
                <MapPin className="w-8 h-8 mr-3" />
                <h3 className="text-xl font-bold">Branch Locator</h3>
              </div>
              <p className="mb-4">Find the nearest SBI Life branch</p>
              <button className="bg-white text-green-600 px-4 py-2 rounded font-medium hover:bg-gray-100 transition-colors">
                Find Branch
              </button>
            </div>
            
            <div className="bg-gradient-to-r from-purple-600 to-pink-600 text-white p-6 rounded-lg">
              <div className="flex items-center mb-4">
                <Users className="w-8 h-8 mr-3" />
                <h3 className="text-xl font-bold">Agent Portal</h3>
              </div>
              <p className="mb-4">Access agent tools and resources</p>
              <button className="bg-white text-purple-600 px-4 py-2 rounded font-medium hover:bg-gray-100 transition-colors">
                Agent Login
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Celebrating Life - Customer Testimonials */}
      <section className="py-16 bg-gradient-to-r from-purple-900 to-blue-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">Celebrating Life…</h2>
            <p className="text-xl text-purple-100">Stories of trust and satisfaction from our valued customers</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white bg-opacity-10 backdrop-blur-sm p-6 rounded-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center text-white font-bold text-xl mr-4">
                  RJ
                </div>
                <div>
                  <h4 className="text-xl font-bold">Mr. Rajeev Jain</h4>
                  <p className="text-purple-200 text-sm">Additional Director General, PR, Ministry of Railways, New Delhi</p>
                </div>
              </div>
              <p className="text-purple-100 leading-relaxed">
                "SBI life has been outstanding in providing customer support in my policy payout, guiding at every stage in choosing annuity options & instant response to tweets and emails. What more a customer wants. Well done SBI life insurance."
              </p>
            </div>
            
            <div className="bg-white bg-opacity-10 backdrop-blur-sm p-6 rounded-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center text-white font-bold text-xl mr-4">
                  AR
                </div>
                <div>
                  <h4 className="text-xl font-bold">Ashish Raval</h4>
                  <p className="text-purple-200 text-sm">Software Engineer, Salesforce, Indianapolis, USA</p>
                </div>
              </div>
              <p className="text-purple-100 leading-relaxed">
                "Thank you @SBILifeCares for promptly taking care of my login issue. I'm able to log in and view my policy details now."
              </p>
            </div>
            
            <div className="bg-white bg-opacity-10 backdrop-blur-sm p-6 rounded-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-pink-400 to-red-500 flex items-center justify-center text-white font-bold text-xl mr-4">
                  RI
                </div>
                <div>
                  <h4 className="text-xl font-bold">Rohit Indurkar</h4>
                  <p className="text-purple-200 text-sm">Assistant Manager, Bank of Baroda, Nagpur, Maharashtra</p>
                </div>
              </div>
              <p className="text-purple-100 leading-relaxed">
                "Thank you for your support. It is really good to see, how quickly you had responded for resolution of my concern regarding the deduction of premium. I am happy to be an SBI Life customer!"
              </p>
            </div>
            
            <div className="bg-white bg-opacity-10 backdrop-blur-sm p-6 rounded-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white font-bold text-xl mr-4">
                  AV
                </div>
                <div>
                  <h4 className="text-xl font-bold">Allen Vishwas</h4>
                  <p className="text-purple-200 text-sm">Software Engineer, Mediatek Bangalore</p>
                </div>
              </div>
              <p className="text-purple-100 leading-relaxed">
                "Thank you for your prompt response and resolving my request regarding rectification of my name on the policy held by me."
              </p>
            </div>
            
            <div className="bg-white bg-opacity-10 backdrop-blur-sm p-6 rounded-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-teal-400 to-green-500 flex items-center justify-center text-white font-bold text-xl mr-4">
                  KP
                </div>
                <div>
                  <h4 className="text-xl font-bold">Keval Patel</h4>
                  <p className="text-purple-200 text-sm">Network Engineer, Vadodara, Gujarat</p>
                </div>
              </div>
              <p className="text-purple-100 leading-relaxed">
                "Thank you for your co-operation and help in resolving my query related to change in Nominee in the PMJJBY policy held by me. I am impressed with your service."
              </p>
            </div>
            
            <div className="bg-white bg-opacity-10 backdrop-blur-sm p-6 rounded-lg border border-white border-opacity-20 hover:bg-opacity-20 transition-all duration-300">
              <div className="flex items-center mb-4">
                <div className="w-16 h-16 rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center text-white font-bold text-xl mr-4">
                  RS
                </div>
                <div>
                  <h4 className="text-xl font-bold">Rishabh Sharma</h4>
                  <p className="text-purple-200 text-sm">Marketing Head, Kartar Valves Pvt. Ltd., Jalandhar (Punjab)</p>
                </div>
              </div>
              <p className="text-purple-100 leading-relaxed">
                "I recently visited Jalandhar branch for my policy-related documentation. The customer representative helping me was excellent in his customer handling skills, behaviour, empathy, politeness, other traits, process knowledge, everything was in perfect ratio to my utmost satisfaction."
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-white font-semibold mb-4">INSURANCE PLANS</h3>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Protection Plans</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Savings Plans</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Child Plans</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Retirement Plans</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Wealth Creation Plans</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Group Insurance</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">SERVICES</h3>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">Life Insurance Services</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Claims and Maturity</a></li>
                <li><a href="#" className="hover:text-white transition-colors">NRI Corner</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Download Centre</a></li>
                <li><a href="#" className="hover:text-white transition-colors">NAV & Fund Performance</a></li>
                <li><a href="#" className="hover:text-white transition-colors">FAQs</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">SBI LIFE</h3>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Key Milestones</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Awards</a></li>
                <li><a href="#" className="hover:text-white transition-colors">CSR</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Media Centre</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Investor Relations</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact Us</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">NOTICES</h3>
              <ul className="space-y-2 text-sm">
                <li><a href="#" className="hover:text-white transition-colors">PMJJBJ</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Fengal Cyclone</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Cyclone Remal</a></li>
              </ul>
              
              <div className="mt-8">
                <h4 className="text-white font-semibold mb-4">CONNECT WITH US</h4>
                <div className="flex space-x-4">
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <Facebook className="w-5 h-5" />
                  </a>
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <Twitter className="w-5 h-5" />
                  </a>
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <Linkedin className="w-5 h-5" />
                  </a>
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <Youtube className="w-5 h-5" />
                  </a>
                  <a href="#" className="text-gray-400 hover:text-white transition-colors">
                    <Instagram className="w-5 h-5" />
                  </a>
                </div>
              </div>
            </div>
          </div>
          
          {/* Company Info */}
          <div className="border-t border-gray-800 mt-12 pt-8">
            <div className="text-center mb-6">
              <h4 className="text-white font-semibold mb-2">SBI Life Insurance Company Limited</h4>
              <p className="text-sm mb-2">IRDAI REGISTRATION NO. 111</p>
              <p className="text-xs">Issued on 29th March 2001. Trade logo displayed above belongs to State Bank of India and is used by SBI Life under license.</p>
            </div>
            
            <div className="text-center text-xs">
              <p className="mb-2">
                <strong>REGISTERED & CORPORATE OFFICE:</strong><br />
                SBI Life Insurance Co. Ltd, Natraj, M.V. Road & Western Express Highway Junction, Andheri (East), Mumbai - 400 069.<br />
                CIN: L99999MH2000PLC129113
              </p>
              
              <div className="flex flex-wrap justify-center gap-4 mt-4">
                <a href="#" className="hover:text-white">IRDAI</a>
                <span>|</span>
                <a href="#" className="hover:text-white">Consumer Education Website by IRDAI</a>
                <span>|</span>
                <a href="#" className="hover:text-white">Sitemap</a>
                <span>|</span>
                <a href="#" className="hover:text-white">Life Insurance Council</a>
                <span>|</span>
                <a href="#" className="hover:text-white">SFIN Codes</a>
                <span>|</span>
                <a href="#" className="hover:text-white">Privacy Policy</a>
                <span>|</span>
                <a href="#" className="hover:text-white">Disclaimer</a>
                <span>|</span>
                <a href="#" className="hover:text-white">Do Not Call</a>
              </div>
              
              <p className="mt-4">© 2024 SBI Life Insurance Company Limited. All rights reserved.</p>
            </div>
          </div>
        </div>
      </footer>

      {/* Chatbot Icon */}
      <button
        onClick={() => setIsChatOpen(true)}
        className="fixed bottom-6 right-6 p-4 bg-blue-900 text-white rounded-full shadow-lg hover:bg-blue-800 transition-colors z-40"
      >
        <MessageCircle className="w-6 h-6" />
      </button>

      {/* Floating Online Plans Button */}
      <button className="fixed bottom-6 left-6 bg-yellow-400 text-black px-6 py-3 rounded-full shadow-lg hover:bg-yellow-300 transition-colors z-40 flex items-center font-bold">
        <Globe className="w-5 h-5 mr-2" />
        Buy Online Plans
      </button>

      {/* Chat Interface Modal */}
      {isChatOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-end z-50">
          <div className="bg-white shadow-xl w-full max-w-lg h-screen relative flex flex-col rounded-l-lg">
            <button
              onClick={() => setIsChatOpen(false)}
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 z-10"
            >
              <X className="w-5 h-5" />
            </button>
            <div className="flex-1 overflow-hidden">
              <ChatInterface />
            </div>
          </div>
        </div>
      )}

      {/* Join Us Modal */}
      {isJoinUsOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">Join the SBI Life Family</h2>
              <button
                onClick={() => setIsJoinUsOpen(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="p-6">
              <p className="text-gray-600 mb-8 text-center">
                Discover exciting opportunities to grow with India's leading life insurance company
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {joinUsOptions.map((option, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-6 hover:shadow-lg transition-shadow">
                    <div className="text-center mb-4">
                      <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
                        <option.icon className="w-8 h-8 text-blue-600" />
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 mb-2">{option.title}</h3>
                      <p className="text-gray-600 mb-4">{option.description}</p>
                    </div>
                    <div className="mb-6">
                      <h4 className="font-semibold text-gray-800 mb-2">Benefits:</h4>
                      <ul className="space-y-1">
                        {option.benefits.map((benefit, idx) => (
                          <li key={idx} className="flex items-center text-sm text-gray-600">
                            <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                            {benefit}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <button className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors">
                      {option.cta}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Service Details Modal */}
      {selectedService && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-200 flex justify-between items-center">
              <h2 className="text-2xl font-bold text-gray-900">{serviceDetails[selectedService]?.title}</h2>
              <button
                onClick={() => setSelectedService(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="p-6">
              <p className="text-gray-600 mb-6">{serviceDetails[selectedService]?.description}</p>
              <div className="mb-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Features & Benefits:</h3>
                <ul className="space-y-2">
                  {serviceDetails[selectedService]?.features.map((feature, index) => (
                    <li key={index} className="flex items-center text-gray-600">
                      <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={() => {
                    window.open(serviceDetails[selectedService]?.url, '_blank');
                  }}
                  className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center"
                >
                  <span>Access Service</span>
                  <ArrowRight className="w-4 h-4 ml-2" />
                </button>
                <button
                  onClick={() => setSelectedService(null)}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-50 lg:hidden">
          <div 
            className="fixed top-0 left-0 w-80 h-full bg-white shadow-xl overflow-y-auto"
            role="dialog"
            aria-modal="true"
            aria-label="Navigation menu"
          >
            <div className="p-4">
              <div className="flex justify-between items-center mb-6">
                <img 
                  src="/SBI_Logo_original.png" 
                  alt="SBI Life"
                  className="h-8"
                />
                <button 
                  onClick={() => setIsMobileMenuOpen(false)}
                  className="p-2 text-gray-500 hover:text-gray-700"
                  aria-label="Close menu"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="space-y-2">
                {navigationItems.map((item) => (
                  <div key={item.name} className="border-b border-gray-200 last:border-0">
                    <button 
                      onClick={() => setHoveredNavItem(hoveredNavItem === item.name ? null : item.name)}
                      className="flex items-center justify-between w-full py-3 text-left"
                      aria-expanded={hoveredNavItem === item.name}
                    >
                      <div>
                        <span className="block font-medium text-gray-900">{item.name}</span>
                        <span className="text-xs text-gray-500">{item.subtitle}</span>
                      </div>
                      <ChevronDown 
                        className={`w-5 h-5 text-gray-400 transition-transform ${
                          hoveredNavItem === item.name ? 'rotate-180' : ''
                        }`}
                      />
                    </button>

                    <div
                      className={`${
                        hoveredNavItem === item.name
                          ? 'max-h-[1000px] opacity-100 visible'
                          : 'max-h-0 opacity-0 invisible'
                      } transition-all duration-300 ease-in-out overflow-hidden`}
                    >
                      <div className="py-3 px-4 space-y-3">
                        {item.dropdownItems.map((dropdownItem, idx) => (
                          <a
                            key={idx}
                            href={dropdownItem.href}
                            className="block hover:text-blue-600"
                          >
                            <div className="font-medium text-gray-900">{dropdownItem.title}</div>
                            <div className="text-sm text-gray-500">{dropdownItem.description}</div>
                          </a>
                        ))}
                      </div>
                      <div className="py-3 px-4 bg-gray-50 border-t border-gray-100">
                        <a 
                          href={item.href}
                          className="text-sm text-blue-600 hover:text-blue-700 font-medium flex items-center"
                        >
                          View All {item.name} Resources
                          <ArrowRight className="w-4 h-4 ml-1" />
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Mobile Quick Links */}
              <div className="mt-6 pt-6 border-t border-gray-200">
                <div className="text-xs font-semibold text-gray-500 uppercase mb-4">Quick Links</div>
                <div className="space-y-3">
                  {quickLinks.map((link, index) => (
                    <button
                      key={index}
                      className="flex items-center w-full text-left text-gray-600 hover:text-blue-600"
                      onClick={() => {
                        setSelectedService(link);
                        setIsMobileMenuOpen(false);
                      }}
                    >
                      {index === 0 && <Calculator className="w-4 h-4 mr-3" />}
                      {index === 1 && <CreditCard className="w-4 h-4 mr-3" />}
                      {index === 2 && <Calculator className="w-4 h-4 mr-3" />}
                      {index === 3 && <Download className="w-4 h-4 mr-3" />}
                      {link}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;