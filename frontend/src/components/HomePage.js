import React, { useState } from 'react';
import { 
  CreditCard, 
  Shield, 
  PieChart, 
  Users, 
  Bell, 
  MessageCircle,
  X,
  ChevronRight,
  Gift,
  Briefcase,
  Heart,
  Home,
  Car,
  GraduationCap
} from 'lucide-react';
import ChatInterface from './ChatInterface';

const HomePage = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);

  const dashboardCards = [
    { title: 'My Policies', icon: Shield, value: '3 Active', color: 'bg-blue-500' },
    { title: 'Premium Due', icon: CreditCard, value: '₹25,000', color: 'bg-purple-500' },
    { title: 'Claims Status', icon: PieChart, value: '1 Pending', color: 'bg-green-500' },
    { title: 'Family Members', icon: Users, value: '4 Covered', color: 'bg-pink-500' },
  ];

  const products = [
    { name: 'Term Life Insurance', icon: Shield, desc: 'Secure your family\'s future' },
    { name: 'Health Insurance', icon: Heart, desc: 'Comprehensive health coverage' },
    { name: 'Home Insurance', icon: Home, desc: 'Protect your dream home' },
    { name: 'Motor Insurance', icon: Car, desc: 'Complete vehicle protection' },
    { name: 'Education Plan', icon: GraduationCap, desc: 'Secure your child\'s future' },
    { name: 'Retirement Plan', icon: Gift, desc: 'Plan for peaceful retirement' },
  ];

  const quickLinks = [
    'Pay Premium Online',
    'Download Policy Document',
    'Update Contact Details',
    'Raise a Claim',
    'Track Application Status',
    'Contact Us'
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-blue-900 rounded-lg flex items-center justify-center p-1">
                <svg viewBox="0 0 100 100" className="w-full h-full">
                  <circle cx="50" cy="50" r="50" fill="#0056A5" />
                  <rect x="48" y="30" width="4" height="40" fill="white" />
                  <circle cx="50" cy="25" r="5" fill="white" />
                </svg>
              </div>
              <h1 className="ml-3 text-2xl font-semibold text-gray-900">SBI Life Insurance</h1>
            </div>
            <div className="flex items-center space-x-4">
              <button className="p-2 text-gray-400 hover:text-gray-500 relative">
                <Bell className="w-6 h-6" />
                <span className="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-400 ring-2 ring-white"></span>
              </button>
              <div className="h-8 w-8 rounded-full bg-blue-900 text-white flex items-center justify-center">
                US
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Hero Banner */}
        <div className="relative rounded-xl overflow-hidden bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8 md:p-12">
          <div className="relative z-10">
            <h2 className="text-3xl font-bold mb-4">Welcome to SBI Life Insurance</h2>
            <p className="text-lg mb-6">Secure your family's future with India's most trusted life insurance provider</p>
            <button className="bg-white text-blue-600 px-6 py-2 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
              Explore Plans
            </button>
          </div>
          <div className="absolute inset-0 bg-black opacity-20"></div>
        </div>

        {/* Dashboard Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {dashboardCards.map((card, index) => (
            <div key={index} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-all cursor-pointer">
              <div className={`inline-flex p-3 rounded-lg ${card.color} text-white mb-4`}>
                <card.icon className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-medium text-gray-900">{card.title}</h3>
              <p className="mt-2 text-xl font-semibold text-gray-700">{card.value}</p>
            </div>
          ))}
        </div>

        {/* Product Categories */}
        <div className="bg-white rounded-xl shadow-sm p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Our Products</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product, index) => (
              <div key={index} className="group p-6 rounded-lg border border-gray-200 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer">
                <div className="flex items-start space-x-4">
                  <div className="p-3 rounded-lg bg-blue-50 text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                    <product.icon className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-1">{product.name}</h3>
                    <p className="text-gray-600">{product.desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Two Column Section */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Recent Activity */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
              <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">View All</button>
            </div>
            <div className="space-y-4">
              {[
                { text: 'Premium paid for Term Insurance Policy', time: '2 hours ago', status: 'success' },
                { text: 'New family member added to Health Insurance', time: '1 day ago', status: 'pending' },
                { text: 'Policy document downloaded', time: '3 days ago', status: 'success' },
                { text: 'Address update requested', time: '5 days ago', status: 'pending' },
              ].map((activity, index) => (
                <div key={index} className="flex justify-between items-center border-b pb-4">
                  <div className="flex items-center space-x-3">
                    <div className={`w-2 h-2 rounded-full ${activity.status === 'success' ? 'bg-green-400' : 'bg-yellow-400'}`}></div>
                    <p className="text-gray-600">{activity.text}</p>
                  </div>
                  <span className="text-sm text-gray-400">{activity.time}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div className="bg-white rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Links</h2>
            <div className="grid grid-cols-1 gap-4">
              {quickLinks.map((link, index) => (
                <button
                  key={index}
                  className="flex justify-between items-center p-4 rounded-lg border border-gray-200 hover:border-blue-500 hover:bg-blue-50 transition-all text-left"
                >
                  <span className="text-gray-700">{link}</span>
                  <ChevronRight className="w-5 h-5 text-gray-400" />
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Promotional Banner */}
        <div className="grid md:grid-cols-2 gap-6">
          <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-6 text-white">
            <h3 className="text-xl font-semibold mb-2">Special Offer!</h3>
            <p className="mb-4">Get up to 15% discount on new term life insurance policies</p>
            <button className="bg-white text-purple-600 px-4 py-2 rounded-lg font-medium hover:bg-purple-50 transition-colors">
              Learn More
            </button>
          </div>
          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl p-6 text-white">
            <h3 className="text-xl font-semibold mb-2">Download Our App</h3>
            <p className="mb-4">Manage your policies on the go with our mobile app</p>
            <button className="bg-white text-blue-600 px-4 py-2 rounded-lg font-medium hover:bg-blue-50 transition-colors">
              Get App
            </button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-white font-semibold mb-4">About SBI Life</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white">Company Overview</a></li>
                <li><a href="#" className="hover:text-white">Board of Directors</a></li>
                <li><a href="#" className="hover:text-white">Financial Reports</a></li>
                <li><a href="#" className="hover:text-white">Careers</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Products</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white">Term Life Insurance</a></li>
                <li><a href="#" className="hover:text-white">Health Insurance</a></li>
                <li><a href="#" className="hover:text-white">Investment Plans</a></li>
                <li><a href="#" className="hover:text-white">Child Plans</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Customer Service</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white">Contact Us</a></li>
                <li><a href="#" className="hover:text-white">Grievance Redressal</a></li>
                <li><a href="#" className="hover:text-white">Branch Locator</a></li>
                <li><a href="#" className="hover:text-white">FAQs</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Connect With Us</h3>
              <ul className="space-y-2">
                <li><a href="#" className="hover:text-white">1800-267-9090</a></li>
                <li><a href="#" className="hover:text-white">info@sbilife.co.in</a></li>
                <li className="pt-4">
                  <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Contact Support
                  </button>
                </li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-12 pt-8 text-sm text-center">
            <p>© 2025 SBI Life Insurance Company Ltd. All Rights Reserved.</p>
          </div>
        </div>
      </footer>

      {/* Chatbot Icon */}
      <button
        onClick={() => setIsChatOpen(true)}
        className="fixed bottom-6 right-6 p-4 bg-blue-900 text-white rounded-full shadow-lg hover:bg-blue-800 transition-colors"
      >
        <MessageCircle className="w-6 h-6" />
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
    </div>
  );
};

export default HomePage;