"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CheckCircle, XCircle, Clock, AlertCircle, ThumbsUp, ThumbsDown } from "lucide-react";

interface Review {
  id: number;
  platform: string;
  author: string;
  rating: number;
  text: string;
  date: string;
  sentiment: string;
  sentiment_score: number;
  emotions: Record<string, number>;
  aspects: string[];
  ai_response: string;
  approval_status: string;
}

interface Stats {
  total: number;
  pending: number;
  approved: number;
  rejected: number;
}

export default function ReviewApprovalPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [stats, setStats] = useState<Stats>({ total: 0, pending: 0, approved: 0, rejected: 0 });
  const [loading, setLoading] = useState(true);
  const [approving, setApproving] = useState<number | null>(null);

  useEffect(() => {
    fetchPendingReviews();
    fetchStats();
  }, []);

  const fetchPendingReviews = async () => {
    try {
      const response = await fetch("/api/reviews/pending");
      const data = await response.json();
      if (data.success) {
        setReviews(data.reviews);
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch("/api/reviews/stats");
      const data = await response.json();
      if (data.success) {
        setStats(data.stats);
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const handleApproval = async (reviewId: number, isGenuine: boolean, notes: string = "") => {
    setApproving(reviewId);
    try {
      const response = await fetch(`/api/reviews/${reviewId}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          is_genuine: isGenuine,
          approval_notes: notes,
          approved_by: "admin"
        })
      });

      const data = await response.json();
      if (data.success) {
        // Remove from pending list
        setReviews(reviews.filter(r => r.id !== reviewId));
        // Update stats
        fetchStats();
      }
    } catch (error) {
      console.error("Error approving review:", error);
      alert("Failed to process review");
    } finally {
      setApproving(null);
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment?.toUpperCase()) {
      case "POSITIVE": return "text-green-600 bg-green-50";
      case "NEGATIVE": return "text-red-600 bg-red-50";
      default: return "text-gray-600 bg-gray-50";
    }
  };

  const getEmotionEmoji = (emotion: string) => {
    const emotions: { [key: string]: string } = {
      joy: "😊", gratitude: "🙏", love: "❤️",
      anger: "😠", frustration: "😤", disappointment: "😞",
      neutral: "😐", surprise: "😲"
    };
    return emotions[emotion?.toLowerCase()] || "😐";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading reviews...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Review Approval</h1>
          <p className="text-gray-600">Verify and approve reviews before they're included in analytics</p>
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Reviews</p>
                <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
              </div>
              <AlertCircle className="w-12 h-12 text-blue-500" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Pending</p>
                <p className="text-3xl font-bold text-orange-600">{stats.pending}</p>
              </div>
              <Clock className="w-12 h-12 text-orange-500" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Approved</p>
                <p className="text-3xl font-bold text-green-600">{stats.approved}</p>
              </div>
              <CheckCircle className="w-12 h-12 text-green-500" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-xl shadow-lg p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Rejected</p>
                <p className="text-3xl font-bold text-red-600">{stats.rejected}</p>
              </div>
              <XCircle className="w-12 h-12 text-red-500" />
            </div>
          </motion.div>
        </div>

        {/* Reviews List */}
        {reviews.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white rounded-xl shadow-lg p-12 text-center"
          >
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-gray-900 mb-2">All caught up!</h3>
            <p className="text-gray-600">No reviews pending approval</p>
          </motion.div>
        ) : (
          <div className="space-y-6">
            {reviews.map((review, index) => (
              <motion.div
                key={review.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl shadow-lg p-6"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-xl font-bold text-gray-900">{review.author}</h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(review.sentiment)}`}>
                        {review.sentiment?.toUpperCase() || 'NEUTRAL'}
                      </span>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        (review.sentiment_score || 0) > 0.1 ? 'bg-green-50 text-green-700' :
                        (review.sentiment_score || 0) < -0.1 ? 'bg-red-50 text-red-700' :
                        'bg-gray-50 text-gray-700'
                      }`}>
                        {(review.sentiment_score || 0) > 0 ? '+' : ''}{(review.sentiment_score || 0).toFixed(2)}
                        <span className="ml-1 text-xs opacity-75">
                          ({Math.abs(review.sentiment_score || 0) > 0.5 ? 'Strong' : 'Moderate'})
                        </span>
                      </span>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span>⭐ {review.rating}/5</span>
                      <span>📅 {new Date(review.date).toLocaleDateString()}</span>
                      <span className="px-2 py-1 bg-gray-100 rounded text-xs">{review.platform}</span>
                    </div>
                  </div>
                </div>

                <p className="text-gray-700 mb-4 leading-relaxed">{review.text}</p>

                {/* NLP Analysis */}
                <div className="grid grid-cols-2 gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
                  {/* Emotions */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">🎭 Emotions</h4>
                    <div className="flex flex-wrap gap-2">
                      {review.emotions && Object.entries(review.emotions).map(([emotion, score]) => (
                        <span key={emotion} className="px-2 py-1 bg-purple-100 text-purple-700 rounded-full text-xs">
                          {emotion}: {typeof score === 'number' ? score.toFixed(2) : score}
                        </span>
                      ))}
                      {(!review.emotions || Object.keys(review.emotions).length === 0) && (
                        <span className="text-gray-400 text-xs">No emotions detected</span>
                      )}
                    </div>
                  </div>

                  {/* Aspects */}
                  <div>
                    <h4 className="text-sm font-semibold text-gray-700 mb-2">🏷️ Aspects</h4>
                    <div className="flex flex-wrap gap-2">
                      {review.aspects && review.aspects.map((aspect, idx) => {
                        const aspectName = typeof aspect === 'string' 
                          ? aspect 
                          : (aspect as any)?.aspect || JSON.stringify(aspect);
                        return (
                          <span key={idx} className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs capitalize">
                            {aspectName}
                          </span>
                        );
                      })}
                      {(!review.aspects || review.aspects.length === 0) && (
                        <span className="text-gray-400 text-xs">No aspects detected</span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="flex gap-4 mt-4">
                  <button
                    onClick={() => handleApproval(review.id, true, "Verified as genuine review")}
                    disabled={approving === review.id}
                    className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
                  >
                    <ThumbsUp className="w-5 h-5" />
                    {approving === review.id ? "Processing..." : "Approve as Genuine"}
                  </button>
                  <button
                    onClick={() => handleApproval(review.id, false, "Flagged as suspicious or fake")}
                    disabled={approving === review.id}
                    className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
                  >
                    <ThumbsDown className="w-5 h-5" />
                    {approving === review.id ? "Processing..." : "Reject as Fake"}
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
