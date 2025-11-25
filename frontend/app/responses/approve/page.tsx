"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { CheckCircle, XCircle, Clock, Edit2, Send, MessageSquare } from "lucide-react";

interface Review {
  id: number;
  business_id: number;
  author: string;
  rating: number;
  text: string;
  review_date: string;
  sentiment: string;
  ai_response: string;
  response_tone: string;
  human_approved: boolean;
  final_response: string;
  response_posted: boolean;
}

export default function ResponseApprovalPage() {
  const [reviews, setReviews] = useState<Review[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editedResponse, setEditedResponse] = useState("");
  const [approving, setApproving] = useState<number | null>(null);

  useEffect(() => {
    fetchPendingResponses();
  }, []);

  const fetchPendingResponses = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/responses/pending");
      const data = await response.json();
      if (data.success) {
        setReviews(data.reviews);
      }
    } catch (error) {
      console.error("Error fetching responses:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (review: Review) => {
    setEditingId(review.id);
    setEditedResponse(review.ai_response || "");
  };

  const handleApprove = async (reviewId: number, useEdited: boolean = false) => {
    setApproving(reviewId);
    try {
      const response = await fetch(`http://localhost:8000/api/responses/${reviewId}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          approved: true,
          final_response: useEdited ? editedResponse : null,
          approved_by: "admin"
        })
      });

      const data = await response.json();
      if (data.success) {
        setReviews(reviews.filter(r => r.id !== reviewId));
        setEditingId(null);
        setEditedResponse("");
      }
    } catch (error) {
      console.error("Error approving response:", error);
      alert("Failed to approve response");
    } finally {
      setApproving(null);
    }
  };

  const handleReject = async (reviewId: number) => {
    setApproving(reviewId);
    try {
      const response = await fetch(`http://localhost:8000/api/responses/${reviewId}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          approved: false,
          approved_by: "admin"
        })
      });

      const data = await response.json();
      if (data.success) {
        setReviews(reviews.filter(r => r.id !== reviewId));
      }
    } catch (error) {
      console.error("Error rejecting response:", error);
      alert("Failed to reject response");
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

  const getToneColor = (tone: string) => {
    const colors: { [key: string]: string } = {
      professional: "bg-blue-100 text-blue-700",
      friendly: "bg-green-100 text-green-700",
      apologetic: "bg-orange-100 text-orange-700",
      grateful: "bg-purple-100 text-purple-700",
    };
    return colors[tone?.toLowerCase()] || "bg-gray-100 text-gray-700";
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading responses...</p>
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
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Response Approval</h1>
          <p className="text-gray-600">Review and approve AI-generated responses before posting</p>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl shadow-lg p-6 mb-8"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Pending Approvals</p>
              <p className="text-3xl font-bold text-orange-600">{reviews.length}</p>
            </div>
            <Clock className="w-12 h-12 text-orange-500" />
          </div>
        </motion.div>

        {/* Reviews List */}
        {reviews.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="bg-white rounded-xl shadow-lg p-12 text-center"
          >
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h3 className="text-2xl font-bold text-gray-900 mb-2">All caught up!</h3>
            <p className="text-gray-600">No responses pending approval</p>
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
                {/* Original Review */}
                <div className="mb-6 pb-6 border-b border-gray-200">
                  <div className="flex items-center gap-3 mb-3">
                    <h3 className="text-lg font-bold text-gray-900">Customer Review</h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSentimentColor(review.sentiment)}`}>
                      {review.sentiment}
                    </span>
                    <span>⭐ {review.rating}/5</span>
                  </div>
                  <p className="text-gray-700 italic">"{review.text}"</p>
                  <p className="text-sm text-gray-500 mt-2">- {review.author}</p>
                </div>

                {/* AI Response */}
                <div className="mb-6">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <MessageSquare className="w-5 h-5 text-purple-600" />
                      <h3 className="text-lg font-bold text-gray-900">AI-Generated Response</h3>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${getToneColor(review.response_tone)}`}>
                        {review.response_tone || "professional"}
                      </span>
                    </div>
                    {editingId !== review.id && (
                      <button
                        onClick={() => handleEdit(review)}
                        className="flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium"
                      >
                        <Edit2 className="w-4 h-4" />
                        Edit
                      </button>
                    )}
                  </div>

                  {editingId === review.id ? (
                    <div>
                      <textarea
                        value={editedResponse}
                        onChange={(e) => setEditedResponse(e.target.value)}
                        className="w-full p-4 border-2 border-purple-300 rounded-lg focus:border-purple-500 focus:outline-none min-h-[150px] text-gray-700"
                        placeholder="Edit the AI response..."
                      />
                      <div className="flex gap-3 mt-3">
                        <button
                          onClick={() => handleApprove(review.id, true)}
                          disabled={approving === review.id}
                          className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium"
                        >
                          Save & Approve
                        </button>
                        <button
                          onClick={() => {
                            setEditingId(null);
                            setEditedResponse("");
                          }}
                          className="px-4 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-lg font-medium"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
                      <p className="text-gray-700 leading-relaxed">{review.ai_response}</p>
                    </div>
                  )}
                </div>

                {/* Action Buttons */}
                {editingId !== review.id && (
                  <div className="flex gap-4">
                    <button
                      onClick={() => handleApprove(review.id, false)}
                      disabled={approving === review.id}
                      className="flex-1 bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
                    >
                      <CheckCircle className="w-5 h-5" />
                      {approving === review.id ? "Processing..." : "Approve & Post"}
                    </button>
                    <button
                      onClick={() => handleReject(review.id)}
                      disabled={approving === review.id}
                      className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
                    >
                      <XCircle className="w-5 h-5" />
                      {approving === review.id ? "Processing..." : "Reject Response"}
                    </button>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
