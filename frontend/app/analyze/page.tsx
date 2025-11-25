"use client";

import { useState } from "react";

interface AnalysisResult {
  success: boolean;
  sentiment: {
    label: string;
    score: number;
    polarity: number;
    subjectivity: number;
  };
  emotions: {
    primary_emotion: string;
    confidence: number;
    all_emotions: Record<string, number>;
  };
  ai_response: {
    response: string;
    tone: string;
    confidence: number;
  };
  timestamp: string;
}

export default function AnalyzePage() {
  const [reviewText, setReviewText] = useState("");
  const [businessName, setBusinessName] = useState("Your Business");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");

  const analyzeReview = async () => {
    if (!reviewText.trim()) {
      setError("Please enter a review to analyze");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: reviewText,
          business_name: businessName,
        }),
      });

      if (!response.ok) {
        throw new Error("Analysis failed");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Failed to analyze review. Make sure the backend is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const getSentimentColor = (label: string) => {
    switch (label) {
      case "POSITIVE":
        return "text-green-600 bg-green-50";
      case "NEGATIVE":
        return "text-red-600 bg-red-50";
      default:
        return "text-gray-600 bg-gray-50";
    }
  };

  const getEmotionEmoji = (emotion: string) => {
    const emojis: Record<string, string> = {
      joy: "😊",
      anger: "😠",
      disappointment: "😞",
      gratitude: "🙏",
      frustration: "😤",
      neutral: "😐",
    };
    return emojis[emotion] || "😐";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🧠 RevuIQ Review Analyzer
          </h1>
          <p className="text-gray-600">
            AI-Powered Sentiment Analysis & Response Generation
          </p>
        </div>

        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4">Analyze a Review</h2>

          <div className="mb-4">
            <label className="block text-sm font-bold text-gray-900 mb-2">
              Business Name
            </label>
            <input
              type="text"
              value={businessName}
              onChange={(e) => setBusinessName(e.target.value)}
              className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 font-medium"
              placeholder="Your Business Name"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm font-bold text-gray-900 mb-2">
              Customer Review
            </label>
            <textarea
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900 font-medium"
              rows={4}
              placeholder="It was okay, nothing special but not bad either."
            />
          </div>

          <button
            onClick={analyzeReview}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? "Analyzing..." : "Analyze Review"}
          </button>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </div>

        {/* Results Section */}
        {result && (
          <div className="space-y-6">
            {/* Sentiment Card */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4">
                📊 Sentiment Analysis
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-bold text-gray-900 mb-2">Overall Sentiment</p>
                  <span
                    className={`inline-block px-4 py-2 rounded-full font-bold text-base ${getSentimentColor(
                      result.sentiment.label
                    )}`}
                  >
                    {result.sentiment.label}
                  </span>
                </div>
                <div>
                  <p className="text-sm font-bold text-gray-900 mb-2">Confidence</p>
                  <div className="flex items-center">
                    <div className="flex-1 bg-gray-200 rounded-full h-4 mr-2">
                      <div
                        className="bg-blue-600 h-4 rounded-full"
                        style={{
                          width: `${result.sentiment.score * 100}%`,
                        }}
                      />
                    </div>
                    <span className="text-base font-bold text-gray-900">
                      {(result.sentiment.score * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
                <div>
                  <p className="text-sm font-bold text-gray-900 mb-2">Polarity</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {result.sentiment.polarity.toFixed(2)}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-bold text-gray-900 mb-2">Subjectivity</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {result.sentiment.subjectivity.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>

            {/* Emotion Card */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4">💭 Emotion Detection</h3>
              <div className="flex items-center space-x-4 mb-4">
                <span className="text-5xl">
                  {getEmotionEmoji(result.emotions.primary_emotion)}
                </span>
                <div>
                  <p className="text-2xl font-semibold capitalize">
                    {result.emotions.primary_emotion}
                  </p>
                  <p className="text-sm text-gray-600">
                    Confidence: {(result.emotions.confidence * 100).toFixed(0)}%
                  </p>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-2">
                {Object.entries(result.emotions.all_emotions).map(
                  ([emotion, score]) => (
                    <div
                      key={emotion}
                      className="bg-gray-50 rounded-lg p-2 text-center"
                    >
                      <p className="text-xs text-gray-600 capitalize">
                        {emotion}
                      </p>
                      <p className="text-sm font-semibold">{score}</p>
                    </div>
                  )
                )}
              </div>
            </div>

            {/* AI Response Card */}
            <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-4">
                ✍️ AI-Generated Response
              </h3>
              <div className="bg-white rounded-lg p-4 mb-4">
                <p className="text-gray-800 leading-relaxed">
                  {result.ai_response.response}
                </p>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600">
                  Tone:{" "}
                  <span className="font-semibold capitalize">
                    {result.ai_response.tone}
                  </span>
                </span>
                <span className="text-gray-600">
                  Confidence:{" "}
                  <span className="font-semibold">
                    {(result.ai_response.confidence * 100).toFixed(0)}%
                  </span>
                </span>
              </div>
              <button className="mt-4 w-full bg-purple-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-purple-700 transition-colors">
                Copy Response
              </button>
            </div>
          </div>
        )}

        {/* Sample Reviews */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-semibold mb-4">📝 Try Sample Reviews</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              "The coffee was amazing and the staff was so friendly!",
              "Service was terrible and the food was cold.",
              "It was okay, nothing special but not bad either.",
            ].map((sample, idx) => (
              <button
                key={idx}
                onClick={() => setReviewText(sample)}
                className="text-left p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
              >
                <p className="text-sm text-gray-700">{sample}</p>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
