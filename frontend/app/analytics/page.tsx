"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

interface SentimentData {
  positive?: number;
  negative?: number;
  neutral?: number;
}

interface EmotionData {
  [key: string]: number;
}

interface Stats {
  total_reviews: number;
  total_businesses: number;
  avg_rating: number;
  positive_reviews: number;
  negative_reviews: number;
  response_rate: number;
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
        `/api/analytics/sentiment-distribution?days=${days}`
      );
      if (sentimentRes.ok) {
        const sentimentJson = await sentimentRes.json();
        setSentimentData(sentimentJson.distribution || {});
      }

      // Fetch emotion distribution
      const emotionRes = await fetch(
        `/api/analytics/emotion-distribution?days=${days}`
      );
      if (emotionRes.ok) {
        const emotionJson = await emotionRes.json();
        setEmotionData(emotionJson.distribution || {});
      }

      // Fetch stats
      const statsRes = await fetch(
        "/api/analytics/stats"
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
    switch (sentiment.toLowerCase()) {
      case "positive":
        return "bg-green-500";
      case "negative":
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
    (sentimentData.positive || 0) +
    (sentimentData.negative || 0) +
    (sentimentData.neutral || 0);

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
            {stats && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Total Reviews</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats.total_reviews || 0}
                  </p>
                </div>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Avg Rating</p>
                  <p className="text-3xl font-bold text-yellow-600">
                    {(stats.avg_rating || 0).toFixed(1)} ⭐
                  </p>
                </div>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Response Rate</p>
                  <p className="text-3xl font-bold text-green-600">
                    {(stats.response_rate || 0).toFixed(0)}%
                  </p>
                </div>
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <p className="text-sm text-gray-600 mb-1">Restaurants</p>
                  <p className="text-3xl font-bold text-blue-600">
                    {stats.total_businesses || 0}
                  </p>
                </div>
              </div>
            )}

            {/* Sentiment Distribution */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold mb-4 text-gray-900">
                Sentiment Distribution
              </h2>
              {totalSentiment > 0 ? (
                <div className="space-y-4">
                  {Object.entries(sentimentData).map(([sentiment, count]) => {
                    const percentage = (count / totalSentiment) * 100;
                    return (
                      <div key={sentiment}>
                        <div className="flex justify-between mb-1">
                          <span className="font-semibold text-gray-900 capitalize">{sentiment}</span>
                          <span className="text-gray-700 font-medium">
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
              <h2 className="text-2xl font-semibold mb-4 text-gray-900">
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

            {/* Review Breakdown */}
            {stats && (
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-semibold mb-4 text-gray-900">
                  Review Breakdown
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <p className="text-sm text-gray-600 mb-2">
                      Positive Reviews
                    </p>
                    <div className="flex items-end space-x-2">
                      <p className="text-3xl font-bold text-green-600">
                        {stats.positive_reviews || 0}
                      </p>
                      <p className="text-gray-600 mb-1">
                        / {stats.total_reviews || 0}
                      </p>
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-500 h-2 rounded-full"
                        style={{
                          width: `${stats.total_reviews ? (stats.positive_reviews / stats.total_reviews * 100) : 0}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div>
                    <p className="text-sm text-gray-600 mb-2">
                      Negative Reviews
                    </p>
                    <div className="flex items-end space-x-2">
                      <p className="text-3xl font-bold text-red-600">
                        {stats.negative_reviews || 0}
                      </p>
                      <p className="text-gray-600 mb-1">
                        / {stats.total_reviews || 0}
                      </p>
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-red-500 h-2 rounded-full"
                        style={{
                          width: `${stats.total_reviews ? (stats.negative_reviews / stats.total_reviews * 100) : 0}%`,
                        }}
                      />
                    </div>
                  </div>

                  <div>
                    <p className="text-sm text-gray-600 mb-2">
                      Response Rate
                    </p>
                    <div className="flex items-end space-x-2">
                      <p className="text-3xl font-bold text-blue-600">
                        {stats.response_rate || 0}%
                      </p>
                    </div>
                    <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-500 h-2 rounded-full"
                        style={{
                          width: `${stats.response_rate || 0}%`,
                        }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
