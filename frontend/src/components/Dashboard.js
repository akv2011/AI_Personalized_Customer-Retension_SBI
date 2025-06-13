import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, Area, AreaChart, Legend
} from 'recharts';
import { 
  X, TrendingUp, TrendingDown, DollarSign, Users, Shield, 
  Clock, Award, Target, Activity, PieChart as PieChartIcon,
  BarChart3, Calendar, AlertCircle, CheckCircle, FileText
} from 'lucide-react';

// Mock data for dashboard
const mockDashboardData = {
  overview: {
    totalPolicies: 12,
    totalPremium: 245000,
    activeClaims: 2,
    pendingRenewals: 3,
    customerSatisfaction: 94,
    portfolioValue: 1850000
  },
  monthlyPremiums: [
    { month: 'Jan', amount: 25000, policies: 2 },
    { month: 'Feb', amount: 18000, policies: 1 },
    { month: 'Mar', amount: 32000, policies: 3 },
    { month: 'Apr', amount: 28000, policies: 2 },
    { month: 'May', amount: 35000, policies: 4 },
    { month: 'Jun', amount: 42000, policies: 3 }
  ],
  policyDistribution: [
    { name: 'Term Insurance', value: 45, count: 5, color: '#3B82F6' },
    { name: 'Health Insurance', value: 25, count: 3, color: '#10B981' },
    { name: 'ULIP', value: 20, count: 2, color: '#F59E0B' },
    { name: 'Endowment', value: 10, count: 2, color: '#EF4444' }
  ],
  claimsData: [
    { month: 'Jan', settled: 15, pending: 3, rejected: 1 },
    { month: 'Feb', settled: 22, pending: 5, rejected: 2 },
    { month: 'Mar', settled: 18, pending: 4, rejected: 1 },
    { month: 'Apr', settled: 25, pending: 2, rejected: 3 },
    { month: 'May', settled: 30, pending: 6, rejected: 2 },
    { month: 'Jun', settled: 28, pending: 4, rejected: 1 }
  ],
  recentActivities: [
    { id: 1, type: 'claim', description: 'Health claim approved - ₹15,000', time: '2 hours ago', status: 'success' },
    { id: 2, type: 'renewal', description: 'Term policy renewal reminder', time: '1 day ago', status: 'warning' },
    { id: 3, type: 'payment', description: 'Premium payment received - ₹8,500', time: '3 days ago', status: 'success' },
    { id: 4, type: 'policy', description: 'New ULIP policy activated', time: '5 days ago', status: 'info' },
    { id: 5, type: 'claim', description: 'Motor claim under review', time: '1 week ago', status: 'pending' }
  ],
  performanceMetrics: [
    { metric: 'Customer Retention', value: 96, target: 95, trend: 'up' },
    { metric: 'Claim Settlement Ratio', value: 94, target: 90, trend: 'up' },
    { metric: 'Average Response Time', value: 2.3, target: 3.0, trend: 'down', unit: 'hrs' },
    { metric: 'Policy Renewals', value: 89, target: 85, trend: 'up' }
  ]
};

const Dashboard = ({ isVisible, onClose, currentUser }) => {
  const [activeTab, setActiveTab] = useState('overview');
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    if (isVisible) {
      // Simulate API call
      setTimeout(() => {
        setDashboardData(mockDashboardData);
      }, 500);
    }
  }, [isVisible]);

  if (!isVisible) return null;

  const StatCard = ({ title, value, icon: Icon, trend, color = 'blue' }) => (
    <div className={`bg-gradient-to-br from-${color}-50 to-${color}-100 p-6 rounded-2xl shadow-lg border border-${color}-200`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
          {trend && (
            <div className={`flex items-center mt-2 ${trend === 'up' ? 'text-green-600' : 'text-red-600'}`}>
              {trend === 'up' ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
              <span className="text-sm ml-1">
                {trend === 'up' ? '+12%' : '-3%'} from last month
              </span>
            </div>
          )}
        </div>
        <div className={`p-3 bg-${color}-500 rounded-full`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
      </div>
    </div>
  );

  const MetricCard = ({ metric, value, target, trend, unit = '%' }) => (
    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{metric}</p>
          <p className="text-2xl font-bold text-gray-900">{value}{unit}</p>
          <p className="text-xs text-gray-500">Target: {target}{unit}</p>
        </div>
        <div className={`p-2 rounded-full ${trend === 'up' ? 'bg-green-100' : trend === 'down' ? 'bg-red-100' : 'bg-gray-100'}`}>
          {trend === 'up' ? (
            <TrendingUp className="w-4 h-4 text-green-600" />
          ) : trend === 'down' ? (
            <TrendingDown className="w-4 h-4 text-red-600" />
          ) : (
            <Activity className="w-4 h-4 text-gray-600" />
          )}
        </div>
      </div>
    </div>
  );

  const ActivityItem = ({ activity }) => {
    const getStatusColor = (status) => {
      switch (status) {
        case 'success': return 'text-green-600 bg-green-100';
        case 'warning': return 'text-yellow-600 bg-yellow-100';
        case 'pending': return 'text-blue-600 bg-blue-100';
        case 'info': return 'text-purple-600 bg-purple-100';
        default: return 'text-gray-600 bg-gray-100';
      }
    };

    const getStatusIcon = (status) => {
      switch (status) {
        case 'success': return <CheckCircle className="w-4 h-4" />;
        case 'warning': return <AlertCircle className="w-4 h-4" />;
        case 'pending': return <Clock className="w-4 h-4" />;
        default: return <Activity className="w-4 h-4" />;
      }
    };

    return (
      <div className="flex items-center gap-3 p-3 hover:bg-gray-50 rounded-lg transition-colors">
        <div className={`p-2 rounded-full ${getStatusColor(activity.status)}`}>
          {getStatusIcon(activity.status)}
        </div>
        <div className="flex-1">
          <p className="font-medium text-gray-900">{activity.description}</p>
          <p className="text-sm text-gray-500">{activity.time}</p>
        </div>
      </div>
    );
  };

  if (!dashboardData) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 shadow-2xl">
          <div className="flex items-center gap-3">
            <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
            <span className="text-lg font-medium">Loading Dashboard...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-7xl h-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">SBI Life Dashboard</h1>
              <p className="text-blue-100 mt-1">
                Welcome back, {currentUser?.name || 'User'}! Here's your personalized overview.
              </p>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-white/20 rounded-full transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white border-b border-gray-200 px-6">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview', icon: BarChart3 },
              { id: 'policies', label: 'Policies', icon: Shield },
              { id: 'claims', label: 'Claims', icon: FileText },
              { id: 'performance', label: 'Performance', icon: Target }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto max-h-[calc(100vh-200px)]">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Overview Stats */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                  title="Total Policies"
                  value={dashboardData.overview.totalPolicies}
                  icon={Shield}
                  trend="up"
                  color="blue"
                />
                <StatCard
                  title="Total Premium"
                  value={`₹${(dashboardData.overview.totalPremium / 1000).toFixed(1)}K`}
                  icon={DollarSign}
                  trend="up"
                  color="green"
                />
                <StatCard
                  title="Active Claims"
                  value={dashboardData.overview.activeClaims}
                  icon={Clock}
                  color="yellow"
                />
                <StatCard
                  title="Portfolio Value"
                  value={`₹${(dashboardData.overview.portfolioValue / 100000).toFixed(1)}L`}
                  icon={TrendingUp}
                  trend="up"
                  color="purple"
                />
              </div>

              {/* Charts Row */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Monthly Premiums Chart */}
                <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Premiums</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <AreaChart data={dashboardData.monthlyPremiums}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="month" />
                      <YAxis />
                      <Tooltip formatter={(value) => [`₹${value}`, 'Premium']} />
                      <Area type="monotone" dataKey="amount" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.3} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>

                {/* Policy Distribution Chart */}
                <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Policy Distribution</h3>
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={dashboardData.policyDistribution}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {dashboardData.policyDistribution.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Recent Activities */}
              <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activities</h3>
                <div className="space-y-2">
                  {dashboardData.recentActivities.map((activity) => (
                    <ActivityItem key={activity.id} activity={activity} />
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'policies' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {dashboardData.policyDistribution.map((policy, index) => (
                  <div key={index} className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="font-medium text-gray-900">{policy.name}</p>
                        <p className="text-sm text-gray-500">{policy.count} policies</p>
                      </div>
                      <div className="w-4 h-4 rounded-full" style={{ backgroundColor: policy.color }}></div>
                    </div>
                    <div className="mt-2">
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="h-2 rounded-full"
                          style={{ backgroundColor: policy.color, width: `${policy.value}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Policy Performance</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={dashboardData.monthlyPremiums}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="policies" fill="#3B82F6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'claims' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <StatCard
                  title="Claims Settled"
                  value="142"
                  icon={CheckCircle}
                  trend="up"
                  color="green"
                />
                <StatCard
                  title="Pending Claims"
                  value="8"
                  icon={Clock}
                  color="yellow"
                />
                <StatCard
                  title="Settlement Ratio"
                  value="94.2%"
                  icon={Award}
                  trend="up"
                  color="blue"
                />
              </div>
              
              <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Claims Trend</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={dashboardData.claimsData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="settled" stroke="#10B981" strokeWidth={2} />
                    <Line type="monotone" dataKey="pending" stroke="#F59E0B" strokeWidth={2} />
                    <Line type="monotone" dataKey="rejected" stroke="#EF4444" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {activeTab === 'performance' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {dashboardData.performanceMetrics.map((metric, index) => (
                  <MetricCard
                    key={index}
                    metric={metric.metric}
                    value={metric.value}
                    target={metric.target}
                    trend={metric.trend}
                    unit={metric.unit || '%'}
                  />
                ))}
              </div>
              
              <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Overview</h3>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={dashboardData.performanceMetrics}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="metric" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#3B82F6" />
                    <Bar dataKey="target" fill="#10B981" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
