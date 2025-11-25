"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CheckCircle, XCircle, Clock, AlertCircle, ThumbsUp, ThumbsDown } from "lucide-react";

interface Review {
  id: number;
  business_id: number;
  author: string;
  rating: number;
  text: string;
  review_date: string;
  sentiment: string;
  sentiment_score: number;
  primary_emotion: string;
  created_at: string;
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
      const response = await fetch("http://localhost:8000/api/reviews/pending");
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
      const response = await fetch("http://localhost:8000/api/reviews/stats");
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
      const response = await fetch(`http://localhost:8000/api/reviews/${reviewId}/approve`, {
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
                        {review.sentiment}
                      </span>
                      <span className="text-2xl">{getEmotionEmoji(review.primary_emotion)}</span>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <span>⭐ {review.rating}/5</span>
                      <span>📅 {new Date(review.review_date).toLocaleDateString()}</span>
                      <span className="capitalize">{review.primary_emotion}</span>
                    </div>
                  </div>
                </div>

                <p className="text-gray-700 mb-6 leading-relaxed">{review.text}</p>

                <div className="flex gap-4">
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
