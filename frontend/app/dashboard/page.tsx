'use client';

import { motion } from 'framer-motion';
import { 
  BarChart3, 
  MessageSquare, 
  TrendingUp, 
  Store,
  Sparkles,
  Star,
  ThumbsUp,
  AlertCircle,
  RefreshCw,
  ArrowRight,
  Shield,
  Activity,
  Zap
} from 'lucide-react';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

interface Stats {
  total_reviews: number;
  total_restaurants: number;
  response_stats: {
    total_reviews: number;
    approved_responses: number;
    posted_responses: number;
    approval_rate: number;
    post_rate: number;
  };
  average_rating: number;
}

interface SentimentDistribution {
  POSITIVE: number;
  NEUTRAL: number;
  NEGATIVE: number;
}

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
};

export default function DashboardPage() {
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [sentiment, setSentiment] = useState<SentimentDistribution | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch overall stats
      const statsRes = await fetch('http://localhost:8000/api/analytics/stats');
      if (statsRes.ok) {
        const data = await statsRes.json();
        setStats(data);
      }

      // Fetch sentiment distribution
      const sentimentRes = await fetch('http://localhost:8000/api/analytics/sentiment-distribution?days=30');
      if (sentimentRes.ok) {
        const data = await sentimentRes.json();
        setSentiment(data.distribution);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentPercentage = (count: number, total: number) => {
    return total > 0 ? Math.round((count / total) * 100) : 0;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const totalSentimentReviews = sentiment 
    ? sentiment.POSITIVE + sentiment.NEUTRAL + sentiment.NEGATIVE 
    : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <motion.header 
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="bg-white/80 backdrop-blur-xl border-b border-gray-200 sticky top-0 z-50"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <motion.div 
                whileHover={{ scale: 1.05 }}
                className="w-11 h-11 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-lg"
              >
                <span className="text-white font-bold text-xl">R</span>
              </motion.div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">RevuIQ</h1>
                <p className="text-xs text-gray-500">AI Review Management</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/live-monitor">
                <motion.button 
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-4 py-2 bg-gradient-to-r from-purple-500 to-blue-500 text-white rounded-lg text-sm font-semibold flex items-center space-x-2 shadow-lg"
                >
                  <Activity className="w-4 h-4" />
                  <span>Live Monitor</span>
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                </motion.button>
              </Link>
              <Link href="/restaurants">
                <motion.button 
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Restaurants
                </motion.button>
              </Link>
              <Link href="/analytics">
                <motion.button 
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-900 transition-colors"
                >
                  Analytics
                </motion.button>
              </Link>
              <motion.button 
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={fetchData}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                title="Refresh data"
              >
                <RefreshCw className="w-5 h-5 text-gray-600" />
              </motion.button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h2 className="text-5xl font-bold text-gray-900 mb-3 tracking-tight">
            Dashboard
          </h2>
          <p className="text-xl text-gray-600">Real-time insights from your restaurant reviews</p>
        </motion.div>

        {/* NEW AI Features Banner */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="mb-8 bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-600 rounded-3xl p-8 shadow-2xl relative overflow-hidden"
        >
          {/* Animated background */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
          </div>
          
          <div className="relative z-10">
            <div className="flex items-center space-x-3 mb-4">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              >
                <Zap className="w-8 h-8 text-yellow-300" />
              </motion.div>
              <span className="px-3 py-1 bg-white/20 backdrop-blur-sm rounded-full text-white text-sm font-semibold">
                NEW AI FEATURES
              </span>
            </div>
            
            <h3 className="text-3xl font-black text-white mb-3">
              🧠 Advanced Deep Learning & NLP Powered!
            </h3>
            <p className="text-white/90 text-lg mb-6 max-w-3xl">
              RevuIQ now uses 5 state-of-the-art transformer models + 4 custom deep learning networks for the most accurate review analysis in the industry!
            </p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                <div className="text-2xl font-bold text-white mb-1">92%</div>
                <div className="text-white/80 text-sm">Sentiment Accuracy</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                <div className="text-2xl font-bold text-white mb-1">28</div>
                <div className="text-white/80 text-sm">Emotions Detected</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4">
                <div className="text-2xl font-bold text-white mb-1">&lt;300ms</div>
                <div className="text-white/80 text-sm">Analysis Speed</div>
              </div>
            </div>
            
            <div className="flex flex-wrap gap-3">
              <Link href="/live-monitor">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-6 py-3 bg-white text-purple-600 rounded-xl font-bold shadow-lg flex items-center space-x-2"
                >
                  <Activity className="w-5 h-5" />
                  <span>Try Live Monitor</span>
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => window.open('/DEEP_LEARNING_NLP_MCP.md', '_blank')}
                className="px-6 py-3 bg-white/20 backdrop-blur-sm text-white rounded-xl font-bold border-2 border-white/30"
              >
                Learn More
              </motion.button>
            </div>
          </div>
        </motion.div>

        {/* Stats Cards */}
        <motion.div 
          variants={container}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
        >
          {/* Total Reviews */}
          <motion.div 
            variants={item}
            whileHover={{ y: -8, scale: 1.02 }}
            className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Total Reviews</h3>
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center shadow-lg">
                <MessageSquare className="w-6 h-6 text-white" />
              </div>
            </div>
            <p className="text-4xl font-bold text-gray-900 mb-2">
              {stats?.total_reviews || 0}
            </p>
            <p className="text-sm text-gray-500">Across all restaurants</p>
          </motion.div>

          {/* Average Rating */}
          <motion.div 
            variants={item}
            whileHover={{ y: -8, scale: 1.02 }}
            className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Avg Rating</h3>
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center shadow-lg">
                <Star className="w-6 h-6 text-white" />
              </div>
            </div>
            <div className="flex items-baseline space-x-2 mb-2">
              <p className="text-4xl font-bold text-gray-900">
                {stats?.average_rating.toFixed(1) || '0.0'}
              </p>
              <span className="text-gray-400">/5</span>
            </div>
            <div className="flex items-center space-x-1">
              {[1, 2, 3, 4, 5].map((star) => (
                <Star
                  key={star}
                  className={`w-4 h-4 ${
                    star <= Math.round(stats?.average_rating || 0)
                      ? 'text-yellow-400 fill-yellow-400'
                      : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
          </motion.div>

          {/* Response Rate */}
          <motion.div 
            variants={item}
            whileHover={{ y: -8, scale: 1.02 }}
            className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Response Rate</h3>
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center shadow-lg">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
            </div>
            <p className="text-4xl font-bold text-gray-900 mb-2">
              {Math.round(stats?.response_stats.approval_rate || 0)}%
            </p>
            <p className="text-sm text-gray-500">
              {stats?.response_stats.approved_responses || 0} AI responses generated
            </p>
          </motion.div>

          {/* Total Restaurants */}
          <motion.div 
            variants={item}
            whileHover={{ y: -8, scale: 1.02 }}
            className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100"
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide">Restaurants</h3>
              <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center shadow-lg">
                <Store className="w-6 h-6 text-white" />
              </div>
            </div>
            <p className="text-4xl font-bold text-gray-900 mb-2">
              {stats?.total_restaurants || 0}
            </p>
            <p className="text-sm text-gray-500">Active locations</p>
          </motion.div>
        </motion.div>

        {/* Sentiment Distribution */}
        {sentiment && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl p-8 shadow-lg mb-8 border border-gray-100"
          >
            <h3 className="text-2xl font-bold text-gray-900 mb-6">Sentiment Distribution (Last 30 Days)</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Positive */}
              <div className="text-center">
                <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <ThumbsUp className="w-10 h-10 text-green-600" />
                </div>
                <p className="text-3xl font-bold text-green-600 mb-1">{sentiment.POSITIVE}</p>
                <p className="text-sm text-gray-500 mb-2">Positive Reviews</p>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-green-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${getSentimentPercentage(sentiment.POSITIVE, totalSentimentReviews)}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  {getSentimentPercentage(sentiment.POSITIVE, totalSentimentReviews)}%
                </p>
              </div>

              {/* Neutral */}
              <div className="text-center">
                <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <AlertCircle className="w-10 h-10 text-gray-600" />
                </div>
                <p className="text-3xl font-bold text-gray-600 mb-1">{sentiment.NEUTRAL}</p>
                <p className="text-sm text-gray-500 mb-2">Neutral Reviews</p>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-gray-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${getSentimentPercentage(sentiment.NEUTRAL, totalSentimentReviews)}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  {getSentimentPercentage(sentiment.NEUTRAL, totalSentimentReviews)}%
                </p>
              </div>

              {/* Negative */}
              <div className="text-center">
                <div className="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-10 h-10 text-red-600 rotate-180" />
                </div>
                <p className="text-3xl font-bold text-red-600 mb-1">{sentiment.NEGATIVE}</p>
                <p className="text-sm text-gray-500 mb-2">Negative Reviews</p>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className="bg-red-600 h-2 rounded-full transition-all duration-500"
                    style={{ width: `${getSentimentPercentage(sentiment.NEGATIVE, totalSentimentReviews)}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  {getSentimentPercentage(sentiment.NEGATIVE, totalSentimentReviews)}%
                </p>
              </div>
            </div>
          </motion.div>
        )}

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
        >
          {/* View Restaurants */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            onClick={() => router.push('/restaurants')}
            className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl p-8 shadow-lg cursor-pointer text-white"
          >
            <Store className="w-12 h-12 mb-4" />
            <h3 className="text-2xl font-bold mb-2">Manage Restaurants</h3>
            <p className="text-blue-100 mb-4">
              Add restaurants, fetch Google reviews, and view detailed analytics
            </p>
            <div className="flex items-center space-x-2 text-white font-semibold">
              <span>Go to Restaurants</span>
              <ArrowRight className="w-5 h-5" />
            </div>
          </motion.div>

          {/* Approve Reviews */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            onClick={() => router.push('/reviews/approve')}
            className="bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl p-8 shadow-lg cursor-pointer text-white"
          >
            <Shield className="w-12 h-12 mb-4" />
            <h3 className="text-2xl font-bold mb-2">Approve Reviews</h3>
            <p className="text-orange-100 mb-4">
              Verify and approve reviews to ensure authenticity
            </p>
            <div className="flex items-center space-x-2 text-white font-semibold">
              <span>Review Approvals</span>
              <ArrowRight className="w-5 h-5" />
            </div>
          </motion.div>

          {/* Approve Responses */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            onClick={() => router.push('/responses/approve')}
            className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl p-8 shadow-lg cursor-pointer text-white"
          >
            <MessageSquare className="w-12 h-12 mb-4" />
            <h3 className="text-2xl font-bold mb-2">Approve Responses</h3>
            <p className="text-indigo-100 mb-4">
              Review and approve AI-generated responses before posting
            </p>
            <div className="flex items-center space-x-2 text-white font-semibold">
              <span>Review Responses</span>
              <ArrowRight className="w-5 h-5" />
            </div>
          </motion.div>

          {/* View Analytics */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            onClick={() => router.push('/analytics')}
            className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl p-8 shadow-lg cursor-pointer text-white"
          >
            <BarChart3 className="w-12 h-12 mb-4" />
            <h3 className="text-2xl font-bold mb-2">View Analytics</h3>
            <p className="text-green-100 mb-4">
              Deep dive into sentiment trends, emotions, and customer insights
            </p>
            <div className="flex items-center space-x-2 text-white font-semibold">
              <span>Go to Analytics</span>
              <ArrowRight className="w-5 h-5" />
            </div>
          </motion.div>
        </motion.div>
      </main>
    </div>
  );
}
