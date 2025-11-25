"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Store, Search, Plus, Trash2, RefreshCw, Eye, Upload } from "lucide-react";

interface Restaurant {
  id: string;
  name: string;
  location: string;
  reviewCount?: number;
  lastFetched?: string;
}

export default function RestaurantsPage() {
  const router = useRouter();
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newRestaurant, setNewRestaurant] = useState({ name: "", location: "", industry: "" });
  const [loading, setLoading] = useState(false);
  const [fetchingId, setFetchingId] = useState<string | null>(null);

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/restaurants");
      if (response.ok) {
        const data = await response.json();
        setRestaurants(
          data.restaurants.map((r: any) => ({
            id: r.id.toString(),
            name: r.name,
            location: r.industry,
            reviewCount: r.review_count,
          }))
        );
      }
    } catch (error) {
      console.error("Error fetching restaurants:", error);
    }
  };

  const addRestaurant = async () => {
    if (newRestaurant.name.trim()) {
      try {
        const response = await fetch("http://localhost:8000/api/restaurants", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: newRestaurant.name,
            industry: newRestaurant.industry || newRestaurant.location || "restaurant",
          }),
        });

        if (response.ok) {
          const data = await response.json();
          await fetchRestaurants();
          setNewRestaurant({ name: "", location: "", industry: "" });
          setShowAddForm(false);
          alert(`✅ Restaurant "${newRestaurant.name}" added successfully!`);
        } else {
          alert("❌ Failed to add restaurant");
        }
      } catch (error) {
        console.error("Error adding restaurant:", error);
        alert("❌ Error connecting to backend");
      }
    }
  };

  const deleteRestaurant = async (id: string) => {
    if (confirm("Are you sure you want to delete this restaurant? This will also delete all its reviews.")) {
      try {
        const response = await fetch(`http://localhost:8000/api/restaurants/${id}`, {
          method: "DELETE",
        });

        if (response.ok) {
          const data = await response.json();
          // Remove from UI
          setRestaurants(restaurants.filter((r) => r.id !== id));
          alert(`✅ ${data.message}`);
        } else {
          alert("❌ Failed to delete restaurant");
        }
      } catch (error) {
        console.error("Error deleting restaurant:", error);
        alert("❌ Error connecting to backend");
      }
    }
  };

  const uploadSampleReviews = async (restaurantId: string) => {
    setFetchingId(restaurantId);
    try {
      const reviewTemplates = [
        { rating: 5, texts: [
          "Amazing food and excellent service! The pasta was absolutely delicious and the staff was very friendly. Will definitely come back!",
          "Outstanding experience! Every dish was perfectly prepared and the ambiance was wonderful. Highly recommend!",
          "Best restaurant in town! The chef really knows what they're doing. Five stars all the way!",
          "Incredible meal from start to finish. The attention to detail was impressive. Can't wait to return!",
          "Absolutely loved everything about this place! Great food, great service, great atmosphere!"
        ]},
        { rating: 4, texts: [
          "Great atmosphere and good food. The only downside was the wait time, but overall a pleasant experience.",
          "Really enjoyed our meal here. Food was tasty and service was good. Would come back again.",
          "Solid restaurant with good portions. A few minor issues but nothing major. Worth visiting.",
          "Nice place with friendly staff. Food was good though not exceptional. Overall satisfied.",
          "Good experience overall. The menu has nice variety and everything we tried was well-prepared."
        ]},
        { rating: 3, texts: [
          "Average experience. Nothing special but nothing terrible either. Food was okay.",
          "It was fine. Not bad but not great. Probably won't rush back but wouldn't avoid it either.",
          "Decent food but overpriced for what you get. Service was acceptable.",
          "Middle of the road restaurant. Some dishes were good, others were mediocre.",
          "Okay place. Met expectations but didn't exceed them. Fair pricing."
        ]},
        { rating: 2, texts: [
          "Disappointed with the service. Food was cold and took forever to arrive. Not worth the price.",
          "Not impressed. The food lacked flavor and the portions were small. Expected better.",
          "Below average experience. Long wait times and the food wasn't fresh. Disappointing.",
          "Had high hopes but was let down. Service was slow and food quality was poor.",
          "Wouldn't recommend. Several issues with our order and staff seemed disorganized."
        ]},
        { rating: 1, texts: [
          "Terrible experience. Food was inedible and service was rude. Never coming back!",
          "Worst restaurant I've been to. Everything was wrong from start to finish. Avoid!",
          "Absolutely awful. Dirty tables, cold food, and terrible service. Health hazard!",
          "Complete disaster. Got food poisoning and the manager was unhelpful. Stay away!",
          "Zero stars if I could. Horrible food, horrible service, horrible everything!"
        ]}
      ];

      const names = ["John Doe", "Jane Smith", "Mike Johnson", "Sarah Williams", "David Brown", 
                     "Emily Davis", "Chris Wilson", "Amanda Taylor", "Robert Martinez", "Lisa Anderson",
                     "James Thomas", "Maria Garcia", "Michael Lee", "Jennifer White", "Daniel Harris"];

      const sampleReviews = [];
      const timestamp = Date.now();
      
      // Generate 15 reviews with varied ratings
      for (let i = 0; i < 15; i++) {
        const template = reviewTemplates[Math.floor(Math.random() * reviewTemplates.length)];
        const text = template.texts[Math.floor(Math.random() * template.texts.length)];
        const name = names[i % names.length];
        const daysAgo = Math.floor(Math.random() * 60); // Random date within last 60 days
        
        sampleReviews.push({
          platform: "google",
          platform_review_id: `sample_${timestamp}_${i}`,
          author_name: name,
          rating: template.rating,
          text: text,
          review_date: new Date(Date.now() - (daysAgo * 86400000)).toISOString(),
        });
      }

      const response = await fetch("http://localhost:8000/api/reviews/bulk", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          business_id: parseInt(restaurantId),
          reviews: sampleReviews,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        await fetchRestaurants();
        alert(
          `✅ Uploaded ${data.created} sample reviews with NLP analysis!\n\nClick "View Analytics" to see insights.`
        );
      } else {
        alert("❌ Failed to upload reviews");
      }
    } catch (error) {
      console.error("Error uploading reviews:", error);
      alert("❌ Error connecting to backend. Make sure it's running on port 8000.");
    } finally {
      setFetchingId(null);
    }
  };

  const fetchGoogleReviews = async (restaurant: Restaurant) => {
    setFetchingId(restaurant.id);
    try {
      const response = await fetch("http://localhost:8000/api/google/fetch-reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          restaurant_name: restaurant.name,
          location: restaurant.location,
          business_id: parseInt(restaurant.id),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          await fetchRestaurants();
          if (data.created > 0) {
            alert(
              `✅ Fetched ${data.created} new reviews from Google Places!\n\n` +
              `${data.skipped > 0 ? `Skipped ${data.skipped} duplicate reviews\n` : ''}` +
              `Click "View Analytics" to see insights.`
            );
          } else if (data.skipped > 0) {
            alert(
              `⚠️ All ${data.skipped} reviews were already in the database (duplicates).\n\n` +
              `Google Places API only returns the same 5 reviews each time.\n` +
              `Try a different restaurant to get new reviews!`
            );
          } else {
            alert(
              `⚠️ No reviews found for this restaurant.\n\n` +
              `This could mean:\n` +
              `1. Restaurant not found on Google Maps\n` +
              `2. Restaurant has no reviews\n` +
              `3. Check the restaurant name spelling`
            );
          }
        } else {
          alert(
            `⚠️ ${data.message}\n\nTo use Google Places API:\n1. Get API key from Google Cloud Console\n2. Add to .env: GOOGLE_PLACES_API_KEY=your_key\n3. Restart backend`
          );
        }
      } else {
        alert("❌ Failed to fetch Google reviews");
      }
    } catch (error) {
      console.error("Error fetching Google reviews:", error);
      alert("❌ Error connecting to backend");
    } finally {
      setFetchingId(null);
    }
  };

  const fetchReviews = async (restaurant: Restaurant) => {
    setFetchingId(restaurant.id);
    try {
      const response = await fetch("http://localhost:8000/api/fetch-reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          business_name: restaurant.name,
          location: restaurant.location,
          platform: "google",
        }),
      });

      if (response.ok) {
        const data = await response.json();
        
        // Update restaurant with review count
        setRestaurants(
          restaurants.map((r) =>
            r.id === restaurant.id
              ? {
                  ...r,
                  reviewCount: data.reviews?.length || 0,
                  lastFetched: new Date().toLocaleString(),
                }
              : r
          )
        );

        alert(
          `✅ Fetched ${data.reviews?.length || 0} reviews for ${restaurant.name}!`
        );
      } else {
        alert("❌ Failed to fetch reviews. Check your API key in .env file.");
      }
    } catch (error) {
      console.error("Error fetching reviews:", error);
      alert("❌ Error connecting to backend. Make sure it's running on port 8000.");
    } finally {
      setFetchingId(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center">
                <Store className="w-10 h-10 mr-3 text-blue-600" />
                Restaurant Management
              </h1>
              <p className="text-gray-600">
                Add restaurants and fetch their reviews from Google Places
              </p>
              <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-800">
                  ℹ️ <strong>Note:</strong> Google Places API returns max 5 reviews per restaurant. 
                  Use "Upload Sample Reviews" to generate 15 diverse reviews for testing!
                </p>
              </div>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setShowAddForm(!showAddForm)}
              className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-xl shadow-lg flex items-center space-x-2"
            >
              <Plus className="w-5 h-5" />
              <span>Add Restaurant</span>
            </motion.button>
          </div>
        </div>

        {/* Add Restaurant Form */}
        {showAddForm && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-xl p-6 mb-6"
          >
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Add New Restaurant
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Restaurant Name *
                </label>
                <input
                  type="text"
                  value={newRestaurant.name}
                  onChange={(e) =>
                    setNewRestaurant({ ...newRestaurant, name: e.target.value })
                  }
                  placeholder="e.g., Olive Garden"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Location (Optional)
                </label>
                <input
                  type="text"
                  value={newRestaurant.location}
                  onChange={(e) =>
                    setNewRestaurant({
                      ...newRestaurant,
                      location: e.target.value,
                    })
                  }
                  placeholder="e.g., New York, NY"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Theme/Category (Optional)
                </label>
                <input
                  type="text"
                  value={newRestaurant.industry}
                  onChange={(e) =>
                    setNewRestaurant({
                      ...newRestaurant,
                      industry: e.target.value,
                    })
                  }
                  placeholder="e.g., Italian, Fast Food, Coffee Shop"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                />
              </div>
            </div>
            <div className="flex space-x-3 mt-4">
              <button
                onClick={addRestaurant}
                className="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
              >
                Add Restaurant
              </button>
              <button
                onClick={() => setShowAddForm(false)}
                className="px-6 py-2 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
            </div>
          </motion.div>
        )}

        {/* Info Card */}
        <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 mb-6">
          <div className="flex items-start space-x-3">
            <div className="text-blue-600 mt-1">ℹ️</div>
            <div>
              <h3 className="font-semibold text-blue-900 mb-1">
                Quick Start Guide:
              </h3>
              <ol className="text-sm text-blue-800 space-y-1">
                <li>1. Add a restaurant using the "Add Restaurant" button</li>
                <li>2. Click "Add Sample Reviews" to upload demo reviews with NLP analysis</li>
                <li>3. Click "View Analytics" to see sentiment, emotions, and insights</li>
                <li>4. All reviews are automatically analyzed using AI (RoBERTa, GoEmotions, etc.)</li>
              </ol>
              <p className="text-sm text-blue-700 mt-2">
                💡 <strong>Tip:</strong> The backend must be running on port 8000. Start it with: <code className="bg-blue-100 px-1 rounded">python backend/restaurant_api.py</code>
              </p>
            </div>
          </div>
        </div>

        {/* Restaurants List */}
        {restaurants.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <Store className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              No restaurants added yet
            </h3>
            <p className="text-gray-500 mb-6">
              Click "Add Restaurant" to get started
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {restaurants.map((restaurant) => (
              <motion.div
                key={restaurant.id}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-1">
                      {restaurant.name}
                    </h3>
                    {restaurant.location && (
                      <p className="text-sm text-gray-500">
                        📍 {restaurant.location}
                      </p>
                    )}
                  </div>
                  <button
                    onClick={() => deleteRestaurant(restaurant.id)}
                    className="text-red-500 hover:text-red-700 transition-colors"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>

                {restaurant.reviewCount !== undefined && (
                  <div className="bg-blue-50 rounded-lg p-3 mb-4">
                    <p className="text-sm text-gray-600">Reviews Fetched</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {restaurant.reviewCount}
                    </p>
                    {restaurant.lastFetched && (
                      <p className="text-xs text-gray-500 mt-1">
                        Last: {restaurant.lastFetched}
                      </p>
                    )}
                  </div>
                )}

                <div className="space-y-2">
                  <button
                    onClick={() => router.push(`/restaurants/${restaurant.id}`)}
                    className="w-full px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all flex items-center justify-center space-x-2"
                  >
                    <Eye className="w-5 h-5" />
                    <span>View Analytics</span>
                  </button>

                  <button
                    onClick={() => fetchGoogleReviews(restaurant)}
                    disabled={fetchingId === restaurant.id}
                    className="w-full px-4 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-all flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {fetchingId === restaurant.id ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span className="text-sm">Fetching...</span>
                      </>
                    ) : (
                      <>
                        <Search className="w-4 h-4" />
                        <span className="text-sm">Fetch from Google</span>
                      </>
                    )}
                  </button>

                  <button
                    onClick={() => uploadSampleReviews(restaurant.id)}
                    disabled={fetchingId === restaurant.id}
                    className="w-full px-4 py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-all flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {fetchingId === restaurant.id ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span className="text-sm">Uploading...</span>
                      </>
                    ) : (
                      <>
                        <Upload className="w-4 h-4" />
                        <span className="text-sm">Add Sample Reviews</span>
                      </>
                    )}
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
