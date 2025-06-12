import React, { useState } from 'react';
import { X, User, Lock } from 'lucide-react';

const MockAuth = ({ isVisible, onLogin, onClose }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Mock user database
  const mockUsers = {
    'arun': { 
      password: 'password123', 
      name: 'Arun Kumar', 
      customerId: 'CUST_ARUN_001' 
    },
    'aravind': { 
      password: 'password123', 
      name: 'Aravind Singh', 
      customerId: 'CUST_ARAVIND_002' 
    },
    'priya': { 
      password: 'password123', 
      name: 'Priya Sharma', 
      customerId: 'CUST_PRIYA_003' 
    },
    'sran': { 
      password: 'password123', 
      name: 'Sran Krishnan', 
      customerId: 'CUST_SRAN_004' 
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    // Simulate network delay
    setTimeout(() => {
      const user = mockUsers[username.toLowerCase()];
      
      if (!user) {
        setError('Invalid username. Try: arun, aravind, priya, or sran');
        setIsLoading(false);
        return;
      }

      if (user.password !== password) {
        setError('Invalid password. Use: password123');
        setIsLoading(false);
        return;
      }

      // Successful login
      const userSession = {
        username: username.toLowerCase(),
        name: user.name,
        customerId: user.customerId
      };

      onLogin(userSession);
      
      // Reset form
      setUsername('');
      setPassword('');
      setIsLoading(false);
    }, 800);
  };

  const handleDemoLogin = (demoUsername) => {
    setUsername(demoUsername);
    setPassword('password123');
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-900">SBI Life Login</h2>
              <p className="text-sm text-gray-600">Access your personalized assistant</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter username"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter password"
                required
              />
            </div>
          </div>

          {error && (
            <div className="text-red-600 text-sm bg-red-50 p-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        {/* Demo Accounts */}
        <div className="px-6 pb-6 border-t bg-gray-50">
          <h3 className="text-sm font-medium text-gray-700 mb-3 mt-4">Demo Accounts</h3>
          <div className="grid grid-cols-2 gap-2">
            {Object.entries(mockUsers).map(([username, user]) => (
              <button
                key={username}
                onClick={() => handleDemoLogin(username)}
                className="text-left p-2 text-xs bg-white border border-gray-200 rounded hover:bg-blue-50 hover:border-blue-300 transition-colors"
              >
                <div className="font-medium text-gray-900">{user.name}</div>
                <div className="text-gray-500">@{username}</div>
              </button>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Click any demo account and use password: <code className="bg-gray-200 px-1 rounded">password123</code>
          </p>
        </div>
      </div>
    </div>
  );
};

export default MockAuth;