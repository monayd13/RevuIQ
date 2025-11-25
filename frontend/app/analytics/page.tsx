"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface SentimentData {
  POSITIVE?: number;
  NEGATIVE?: number;
  NEUTRAL?: number;
}

interface EmotionData {
  [key: string]: number;
}

interface Stats {
  response_stats: {
    total_reviews: number;
    approved_responses: number;
    posted_responses: number;
    pending_reviews: number;
    approval_rate: number;
    post_rate: number;
  };
  average_rating: number;
}

export default function AnalyticsPage() {
  const router = useRouter();
  const [sentimentData, setSentimentData] = useState<SentimentData>({});
  const [emotionData, setEmotionData] = useState<EmotionData>({});
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);

  useEffect(() => {
    fetchAnalytics();
  }, [days]);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      // Fetch sentiment distribution
      const sentimentRes = await fetch(
        `http://localhost:8000/api/analytics/sentiment-distribution?days=${days}`
      );
      if (sentimentRes.ok) {
        const sentimentJson = await sentimentRes.json();
        setSentimentData(sentimentJson.distribution || {});
      }

      // Fetch emotion distribution
      const emotionRes = await fetch(
        `http://localhost:8000/api/analytics/emotion-distribution?days=${days}`
      );
      if (emotionRes.ok) {
        const emotionJson = await emotionRes.json();
        setEmotionData(emotionJson.distribution || {});
      }

      // Fetch stats
      const statsRes = await fetch(
        "http://localhost:8000/api/analytics/stats"
      );
      if (statsRes.ok) {
        const statsJson = await statsRes.json();
        setStats(statsJson);
      }
    } catch (error) {
      console.error("Failed to fetch analytics:", error);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case "POSITIVE":
        return "bg-green-500";
      case "NEGATIVE":
        return "bg-red-500";
      default:
        return "bg-gray-500";
    }
  };

  const getEmotionEmoji = (emotion: string) => {
    const emojis: Record<string, string> = {
      joy: "😊",
      anger: "😠",
      disappointment: "😞",
      gratitude: "🙏",
      frustration: "😤",
    };
    return emojis[emotion] || "😐";
  };

  const totalSentiment =
    (sentimentData.POSITIVE || 0) +
    (sentimentData.NEGATIVE || 0) +
    (sentimentData.NEUTRAL || 0);

  const totalEmotions = Object.values(emotionData).reduce(
    (sum, count) => sum + count,
    0
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-100 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            📊 Analytics Dashboard
          </h1>
          <p className="text-gray-600">
            Review insights and performance metrics
          </p>
        </div>

        {/* Time Period Selector */}
        <div className="bg-white rounded-lg shadow-lg p-4 mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Time Period
          </label>
          <div className="flex space-x-2">
            {[7, 30, 90].map((d) => (
              <button
                key={d}
                onClick={() => setDays(d)}
                className={`px-4 py-2 rounded-lg font-semibold transition-colors ${
                  days === d
                    ? "bg-blue-600 text-white"
                    : "bg-gray-200 text-gray-700 hover:bg-gray-300"
                }`}
              >
                {d} Days
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading analytics...</p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Stats Overview */}
            {stats && stats.response_stats && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Total Reviews</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats.response_stats?.total_reviews || 0}
                  </p>
                </div>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Avg Rating</p>
                  <p className="text-3xl font-bold text-yellow-600">
                    {(stats.average_rating || 0).toFixed(1)} ⭐
                  </p>
                </div>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Approval Rate</p>
                  <p className="text-3xl font-bold text-green-600">
                    {(stats.response_stats?.approval_rate || 0).toFixed(0)}%
                  </p>
                </div>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Posted</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {stats.response_stats?.posted_responses || 0}
                  </p>
                </div>
              </div>
            )}

            {/* Sentiment Distribution */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold mb-4">
                Sentiment Distribution
              </h2>
              {totalSentiment > 0 ? (
                <div className="space-y-4">
                  {Object.entries(sentimentData).map(([sentiment, count]) => {
                    const percentage = (count / totalSentiment) * 100;
                    return (
                      <div key={sentiment}>
                        <div className="flex justify-between mb-1">
                          <span className="font-semibold">{sentiment}</span>
                          <span className="text-gray-600">
                            {count} ({percentage.toFixed(1)}%)
                          </span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-4">
                          <div
                            className={`h-4 rounded-full ${getSentimentColor(
                              sentiment
                            )}`}
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">
                  No sentiment data available for this period
                </p>
              )}
            </div>

            {/* Emotion Distribution */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold mb-4">
                Emotion Distribution
              </h2>
              {totalEmotions > 0 ? (
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  {Object.entries(emotionData).map(([emotion, count]) => {
                    const percentage = (count / totalEmotions) * 100;
                    return (
                      <div
                        key={emotion}
                        className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-4 text-center"
                      >
                        <div className="text-4xl mb-2">
                          {getEmotionEmoji(emotion)}
                        </div>
                        <p className="font-semibold capitalize">{emotion}</p>
                        <p className="text-2xl font-bold text-purple-600">
                          {count}
                        </p>
                        <p className="text-sm text-gray-600">
                          {percentage.toFixed(1)}%
                        </p>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="text-gray-500 text-center py-8">
                  No emotion data available for this period
                </p>
              )}
            </div>

            {/* Response Performance */}
            {stats && stats.response_stats && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-semibold mb-4">
                  Response Performance
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <p className="text-sm text-gray-600 mb-2">
                      Approved Responses
                    </p>
                    <div className="flex items-end space-x-2">
                      <p className="text-3xl font-bold text-green-600">
                        {stats.response_stats?.approved_responses || 0}
                      </p>
                      <p className="text-gray-600 mb-1">
                        / {stats.response_stats?.total_reviews || 0}
                      </p>
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{
                          width: `${stats.response_stats?.approval_rate || 0}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div>
                    <p className="text-sm text-gray-600 mb-2">
                      Posted Responses
                    </p>
                    <div className="flex items-end space-x-2">
                      <p className="text-3xl font-bold text-blue-600">
                        {stats.response_stats?.posted_responses || 0}
                      </p>
                      <p className="text-gray-600 mb-1">
                        / {stats.response_stats?.total_reviews || 0}
                      </p>
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full"
                        style={{
                          width: `${stats.response_stats?.post_rate || 0}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div>
                    <p className="text-sm text-gray-600 mb-2">
                      Pending Approval
                    </p>
                    <div className="flex items-end space-x-2">
                      <p className="text-3xl font-bold text-orange-600">
                        {stats.response_stats?.pending_reviews || 0}
                      </p>
                      <p className="text-gray-600 mb-1">reviews</p>
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-orange-500 h-2 rounded-full"
                        style={{
                          width: `${
                            stats.response_stats?.pending_reviews 
                              ? (stats.response_stats.pending_reviews / 
                                 (stats.response_stats.total_reviews + stats.response_stats.pending_reviews) * 100)
                              : 0
                          }%`,
                        }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Quick Actions */}
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
              <h2 className="text-2xl font-semibold mb-4">Quick Actions</h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button 
                  onClick={() => router.push('/restaurants')}
                  className="bg-white text-blue-600 py-3 px-6 rounded-lg font-semibold hover:bg-blue-50 transition-colors flex items-center justify-center gap-2"
                >
                  📥 Manage Restaurants
                </button>
                <button 
                  onClick={() => router.push('/reviews/approve')}
                  className="bg-white text-purple-600 py-3 px-6 rounded-lg font-semibold hover:bg-purple-50 transition-colors flex items-center justify-center gap-2"
                >
                  ✅ Approve Reviews
                </button>
                <button 
                  onClick={() => router.push('/responses/approve')}
                  className="bg-white text-green-600 py-3 px-6 rounded-lg font-semibold hover:bg-green-50 transition-colors flex items-center justify-center gap-2"
                >
                  💬 Approve Responses
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
