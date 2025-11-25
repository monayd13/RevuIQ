'use client';

import { motion } from 'framer-motion';
import { 
  BarChart3, 
  TrendingUp, 
  TrendingDown,
  Users,
  Star,
  MessageSquare,
  Calendar,
  ArrowLeft
} from 'lucide-react';
import Link from 'next/link';

export default function AnalyticsPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="backdrop-blur-2xl bg-white/80 border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/dashboard">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                >
                  <ArrowLeft className="w-5 h-5 text-gray-600" />
                </motion.button>
              </Link>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
                <p className="text-sm text-gray-500">Detailed insights and trends</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Time Period Selector */}
        <div className="flex items-center space-x-4 mb-8">
          <button className="px-4 py-2 bg-blue-500 text-white rounded-lg font-medium">Last 7 Days</button>
          <button className="px-4 py-2 bg-white text-gray-700 rounded-lg font-medium hover:bg-gray-50">Last 30 Days</button>
          <button className="px-4 py-2 bg-white text-gray-700 rounded-lg font-medium hover:bg-gray-50">Last 90 Days</button>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Total Reviews', value: '1,284', change: '+12%', trend: 'up', icon: MessageSquare, color: 'blue' },
            { label: 'Avg Rating', value: '4.2', change: '+0.3', trend: 'up', icon: Star, color: 'yellow' },
            { label: 'Response Rate', value: '87%', change: '+5%', trend: 'up', icon: TrendingUp, color: 'green' },
            { label: 'Negative Reviews', value: '23', change: '-8%', trend: 'down', icon: TrendingDown, color: 'red' }
          ].map((stat) => (
            <motion.div
              key={stat.label}
              whileHover={{ y: -4 }}
              className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
            >
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-semibold text-gray-500 uppercase">{stat.label}</span>
                <stat.icon className={`w-5 h-5 text-${stat.color}-500`} />
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-2">{stat.value}</div>
              <div className={`flex items-center space-x-1 text-sm font-medium ${stat.trend === 'up' ? 'text-emerald-600' : 'text-red-600'}`}>
                {stat.trend === 'up' ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
                <span>{stat.change} from last period</span>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Sentiment Trend */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Sentiment Trend</h3>
            <div className="h-64 flex items-end justify-between space-x-2">
              {[65, 72, 68, 80, 75, 82, 78].map((height, i) => (
                <div key={i} className="flex-1 flex flex-col items-center">
                  <div 
                    className="w-full bg-gradient-to-t from-blue-500 to-purple-500 rounded-t-lg transition-all hover:opacity-80"
                    style={{ height: `${height}%` }}
                  ></div>
                  <span className="text-xs text-gray-500 mt-2">Day {i + 1}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Platform Distribution */}
          <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
            <h3 className="text-lg font-bold text-gray-900 mb-6">Platform Distribution</h3>
            <div className="space-y-4">
              {[
                { platform: 'Google', count: 542, percentage: 42, color: 'blue' },
                { platform: 'Yelp', count: 385, percentage: 30, color: 'red' },
                { platform: 'TripAdvisor', count: 257, percentage: 20, color: 'green' },
                { platform: 'Meta', count: 100, percentage: 8, color: 'purple' }
              ].map((item) => (
                <div key={item.platform}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-700">{item.platform}</span>
                    <span className="text-sm text-gray-500">{item.count} reviews</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`bg-${item.color}-500 h-2 rounded-full`}
                      style={{ width: `${item.percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Top Keywords */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 mb-8">
          <h3 className="text-lg font-bold text-gray-900 mb-6">Top Keywords</h3>
          <div className="flex flex-wrap gap-3">
            {[
              { word: 'service', count: 245 },
              { word: 'quality', count: 198 },
              { word: 'fast', count: 167 },
              { word: 'friendly', count: 142 },
              { word: 'clean', count: 128 },
              { word: 'delicious', count: 115 },
              { word: 'expensive', count: 89 },
              { word: 'slow', count: 67 }
            ].map((keyword) => (
              <div
                key={keyword.word}
                className="px-4 py-2 bg-gradient-to-r from-blue-50 to-purple-50 rounded-full border border-blue-200"
              >
                <span className="font-semibold text-gray-900">{keyword.word}</span>
                <span className="text-sm text-gray-600 ml-2">({keyword.count})</span>
              </div>
            ))}
          </div>
        </div>

        {/* Response Time Stats */}
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-6">Response Time Performance</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">2.5h</div>
              <div className="text-sm text-gray-600">Average Response Time</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-emerald-600 mb-2">87%</div>
              <div className="text-sm text-gray-600">Within 24 Hours</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">95%</div>
              <div className="text-sm text-gray-600">Customer Satisfaction</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
