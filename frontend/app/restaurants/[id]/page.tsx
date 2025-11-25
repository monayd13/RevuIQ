"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  Star,
  TrendingUp,
  MessageSquare,
  BarChart3,
  RefreshCw,
} from "lucide-react";

interface Review {
  id: number;
  author: string;
  rating: number;
  text: string;
  date: string;
  sentiment: string;
  sentiment_score: number;
  emotions: Record<string, number>;
  aspects: Array<{ aspect: string; sentiment: string }>;
  ai_response: string;
}

interface Analytics {
  total_reviews: number;
  average_rating: number;
  sentiment_distribution: {
    POSITIVE: number;
    NEUTRAL: number;
    NEGATIVE: number;
  };
  top_emotions: Record<string, number>;
  top_aspects: Record<string, number>;
  rating_distribution: {
    "5_star": number;
    "4_star": number;
    "3_star": number;
    "2_star": number;
    "1_star": number;
  };
}

interface Restaurant {
  id: number;
  name: string;
  industry: string;
  stats: {
    total_reviews: number;
    average_rating: number;
    sentiment_distribution: {
      POSITIVE: number;
      NEUTRAL: number;
      NEGATIVE: number;
    };
  };
}

export default function RestaurantDetailPage() {
  const params = useParams();
  const router = useRouter();
  const restaurantId = params.id as string;

  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(365);

  useEffect(() => {
    fetchData();
  }, [restaurantId, days]);

  const fetchData = async () => {
    setLoading(true);
    try {
      // Fetch restaurant details
      const restaurantRes = await fetch(
        `http://localhost:8000/api/restaurants/${restaurantId}`
      );
      if (restaurantRes.ok) {
        const data = await restaurantRes.json();
        setRestaurant(data.restaurant);
      }

      // Fetch reviews
      const reviewsRes = await fetch(
        `http://localhost:8000/api/reviews/restaurant/${restaurantId}`
      );
      if (reviewsRes.ok) {
        const data = await reviewsRes.json();
        setReviews(data.reviews || []);
      }

      // Fetch analytics
      const analyticsRes = await fetch(
        `http://localhost:8000/api/analytics/restaurant/${restaurantId}?days=${days}`
      );
      if (analyticsRes.ok) {
        const data = await analyticsRes.json();
        setAnalytics(data);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "POSITIVE":
        return "text-green-600 bg-green-50";
      case "NEGATIVE":
        return "text-red-600 bg-red-50";
      default:
        return "text-gray-600 bg-gray-50";
    }
  };

  const getSentimentBadge = (sentiment: string) => {
    switch (sentiment) {
      case "POSITIVE":
        return "😊 Positive";
      case "NEGATIVE":
        return "😞 Negative";
      default:
        return "😐 Neutral";
    }
  };

  const getEmotionEmoji = (emotion: string) => {
    const emojis: Record<string, string> = {
      joy: "😊",
      anger: "😠",
      disappointment: "😞",
      gratitude: "🙏",
      frustration: "😤",
      admiration: "😍",
      love: "❤️",
      excitement: "🤩",
      sadness: "😢",
      surprise: "😲",
    };
    return emojis[emotion] || "😐";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading restaurant data...</p>
        </div>
      </div>
    );
  }

  if (!restaurant) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-gray-600">Restaurant not found</p>
          <button
            onClick={() => router.push("/restaurants")}
            className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Back to Restaurants
          </button>
        </div>
      </div>
    );
  }

  const totalSentiment =
    (analytics?.sentiment_distribution?.POSITIVE || 0) +
    (analytics?.sentiment_distribution?.NEUTRAL || 0) +
    (analytics?.sentiment_distribution?.NEGATIVE || 0);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => router.push("/restaurants")}
            className="flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Restaurants
          </button>

          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2">
                {restaurant.name}
              </h1>
              <p className="text-gray-600 capitalize">{restaurant.industry}</p>
            </div>

            <div className="flex space-x-2">
              {[7, 30, 90, 365].map((d) => (
                <button
                  key={d}
                  onClick={() => setDays(d)}
                  disabled={loading}
                  className={`px-4 py-2 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
                    days === d
                      ? "bg-blue-600 text-white"
                      : "bg-white text-gray-700 hover:bg-gray-100"
                  }`}
                >
                  {loading && days === d ? (
                    <RefreshCw className="w-4 h-4 animate-spin inline mr-1" />
                  ) : null}
                  {d === 365 ? 'All Time' : `${d} Days`}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-gray-600">Total Reviews</p>
              <MessageSquare className="w-5 h-5 text-blue-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">
              {analytics?.total_reviews || 0}
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-2xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-gray-600">Average Rating</p>
              <Star className="w-5 h-5 text-yellow-500" />
            </div>
            <p className="text-3xl font-bold text-yellow-600">
              {analytics?.average_rating ? analytics.average_rating.toFixed(1) : "0.0"} ⭐
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-2xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-gray-600">Positive Reviews</p>
              <TrendingUp className="w-5 h-5 text-green-600" />
            </div>
            <p className="text-3xl font-bold text-green-600">
              {analytics?.sentiment_distribution?.POSITIVE || 0}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {totalSentiment > 0
                ? `${((analytics?.sentiment_distribution?.POSITIVE || 0) / totalSentiment * 100).toFixed(0)}%`
                : "0%"}
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-2xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <p className="text-sm text-gray-600">Negative Reviews</p>
              <BarChart3 className="w-5 h-5 text-red-600" />
            </div>
            <p className="text-3xl font-bold text-red-600">
              {analytics?.sentiment_distribution?.NEGATIVE || 0}
            </p>
            <p className="text-xs text-gray-500 mt-1">
              {totalSentiment > 0
                ? `${((analytics?.sentiment_distribution?.NEGATIVE || 0) / totalSentiment * 100).toFixed(0)}%`
                : "0%"}
            </p>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Sentiment Distribution */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Sentiment Analysis
            </h2>
            {totalSentiment > 0 ? (
              <div className="space-y-4">
                {Object.entries(analytics?.sentiment_distribution || {}).map(
                  ([sentiment, count]) => {
                    const percentage = (count / totalSentiment) * 100;
                    return (
                      <div key={sentiment}>
                        <div className="flex justify-between mb-2">
                          <span className="font-semibold text-gray-700">
                            {getSentimentBadge(sentiment)}
                          </span>
                          <span className="text-gray-600">
                            {count} ({percentage.toFixed(1)}%)
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div
                            className={`h-3 rounded-full ${
                              sentiment === "POSITIVE"
                                ? "bg-green-500"
                                : sentiment === "NEGATIVE"
                                ? "bg-red-500"
                                : "bg-gray-500"
                            }`}
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  }
                )}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">
                No sentiment data available
              </p>
            )}
          </div>

          {/* Top Emotions */}
          <div className="bg-white rounded-2xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Top Emotions Detected
            </h2>
            {analytics?.top_emotions &&
            Object.keys(analytics.top_emotions).length > 0 ? (
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(analytics.top_emotions).map(
                  ([emotion, score]) => (
                    <div
                      key={emotion}
                      className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 text-center"
                    >
                      <div className="text-4xl mb-2">
                        {getEmotionEmoji(emotion)}
                      </div>
                      <p className="font-semibold capitalize text-gray-800">
                        {emotion}
                      </p>
                      <p className="text-sm text-gray-600">
                        Score: {(score * 100).toFixed(0)}%
                      </p>
                    </div>
                  )
                )}
              </div>
            ) : (
              <p className="text-gray-500 text-center py-8">
                No emotion data available
              </p>
            )}
          </div>
        </div>

        {/* Top Aspects */}
        {analytics?.top_aspects &&
          Object.keys(analytics.top_aspects).length > 0 && (
            <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Most Mentioned Topics
              </h2>
              <div className="flex flex-wrap gap-3">
                {Object.entries(analytics.top_aspects).map(
                  ([aspect, count]) => (
                    <div
                      key={aspect}
                      className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full font-semibold"
                    >
                      {aspect} ({count})
                    </div>
                  )
                )}
              </div>
            </div>
          )}

        {/* Reviews List */}
        <div className="bg-white rounded-2xl shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Recent Reviews ({reviews.length})
          </h2>

          {reviews.length > 0 ? (
            <div className="space-y-6">
              {reviews.map((review) => (
                <motion.div
                  key={review.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="border-b border-gray-200 pb-6 last:border-0"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <p className="font-semibold text-gray-900">
                        {review.author}
                      </p>
                      <div className="flex items-center space-x-2 mt-1">
                        <div className="flex">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`w-4 h-4 ${
                                i < review.rating
                                  ? "text-yellow-500 fill-yellow-500"
                                  : "text-gray-300"
                              }`}
                            />
                          ))}
                        </div>
                        <span className="text-sm text-gray-500">
                          {new Date(review.date).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-semibold ${getSentimentColor(
                        review.sentiment
                      )}`}
                    >
                      {getSentimentBadge(review.sentiment)}
                    </span>
                  </div>

                  <p className="text-gray-700 mb-3">{review.text}</p>

                  {/* Emotions */}
                  {review.emotions && Object.keys(review.emotions).length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-3">
                      {Object.entries(review.emotions)
                        .sort(([, a], [, b]) => b - a)
                        .slice(0, 3)
                        .map(([emotion, score]) => (
                          <span
                            key={emotion}
                            className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded-full"
                          >
                            {getEmotionEmoji(emotion)} {emotion} (
                            {(score * 100).toFixed(0)}%)
                          </span>
                        ))}
                    </div>
                  )}

                  {/* AI Response */}
                  {review.ai_response && (
                    <div className="mt-4 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                      <p className="text-sm font-semibold text-blue-900 mb-2">
                        🤖 AI-Generated Response:
                      </p>
                      <p className="text-sm text-gray-700">
                        {review.ai_response}
                      </p>
                    </div>
                  )}
                </motion.div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">
              No reviews available for this restaurant
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
