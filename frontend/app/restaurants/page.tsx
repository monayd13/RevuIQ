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
      const response = await fetch("/api/restaurants");
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
        const response = await fetch("/api/restaurants", {
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
        const response = await fetch(`/api/restaurants/${id}`, {
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
          "Came here for my anniversary and it exceeded all expectations! The ribeye steak was cooked to perfection - medium rare just like I asked. Our server Maria was attentive without being intrusive. The chocolate lava cake for dessert was divine. Already planning our next visit!",
          "This place is a hidden gem! I ordered the seafood linguine and it tasted like I was dining in Italy. Fresh ingredients, generous portions, and the chef even came out to ask how everything was. The wine selection is impressive too. Highly recommend the Chianti!",
          "Best brunch spot in the city! Their avocado toast with poached eggs is Instagram-worthy AND delicious. The cold brew coffee is smooth and not bitter at all. Atmosphere is cozy with great music. Waited 20 minutes but it was totally worth it. Will be back every weekend!",
          "My family and I celebrated my daughter's graduation here. The private dining room was perfect, and they even decorated it with balloons! Every single dish from the tasting menu was exceptional. The manager personally thanked us for coming. This is what hospitality looks like!",
          "I'm usually picky about sushi but this place changed my mind! The salmon nigiri melts in your mouth and the dragon roll is a work of art. Chef Ken explained each piece to us. Prices are reasonable for the quality. Bringing all my friends here!"
        ]},
        { rating: 4, texts: [
          "Really solid experience overall. The burger was juicy and cooked well, fries were crispy. Only complaint is it took 15 minutes longer than expected during lunch rush. Staff apologized and gave us free dessert though, which was nice. Would definitely return!",
          "Great neighborhood spot! Love their outdoor patio seating. The margherita pizza had a perfect crispy crust. Service was friendly but a bit slow when we needed refills. Still, the food quality makes up for it. Good value for money.",
          "Took my vegetarian friend here and she loved the options! I had the grilled chicken which was tender and well-seasoned. The only reason I'm not giving 5 stars is the noise level - it's pretty loud inside. But the food is consistently good!",
          "Nice ambiance with dim lighting and soft jazz music. The filet mignon was excellent, though the sides were just okay. Our waiter gave great wine recommendations. A bit pricey but you're paying for the experience. Perfect for date night!",
          "Impressed with their gluten-free menu! As someone with celiac disease, I appreciate restaurants that take allergies seriously. The GF pasta tasted just like regular pasta. Portions could be slightly bigger but overall very satisfied. Will recommend to my support group!"
        ]},
        { rating: 3, texts: [
          "It's okay for a quick bite. The sandwich was decent but nothing memorable. Service was fast which is good for lunch breaks. Prices are fair. Not bad, not amazing - just average. There are better options nearby but this works in a pinch.",
          "Mixed feelings about this place. The appetizers were great - loved the calamari! But my main course (chicken parmesan) was lukewarm and the cheese wasn't fully melted. Dessert saved the meal. Might give them another chance on a different day.",
          "Atmosphere is nice but the food didn't wow me. Had the salmon which was a bit dry. My partner's pasta was better. Service was professional but not particularly warm. For the price point, I expected more. It's not terrible, just underwhelming.",
          "Came here based on a friend's recommendation but I don't see the hype. Food was edible but lacked seasoning. Had to ask for salt and pepper. The portions are generous though. Maybe I ordered the wrong thing? Might try their specials next time.",
          "Decent spot for casual dining. The menu has variety which is nice. My salad was fresh but the dressing was bland. Coffee was weak. It's convenient for the area but I probably won't go out of my way to come back. Three stars seems fair."
        ]},
        { rating: 2, texts: [
          "Pretty disappointed. Waited 45 minutes for our food only to get cold fries and a burger that was overcooked. Asked them to remake it but the replacement wasn't much better. Server seemed overwhelmed. The place was understaffed. Not sure I'll give them another shot.",
          "The photos online look nothing like what we got. My 'gourmet' pizza looked sad and tasted worse. Crust was soggy in the middle. My wife's salad had wilted lettuce. We complained and they took 10% off the bill but that doesn't fix the quality issue. Very let down.",
          "Hygiene concerns here. Saw a server touch food with bare hands. Tables weren't properly cleaned - ours was sticky. The bathroom was out of soap. Food was mediocre at best. For $60 for two people, this is unacceptable. Health department should check this place.",
          "Ordered delivery and it arrived an hour late and cold. The container was leaking sauce everywhere. Called to complain and they were dismissive. The food itself was bland and portions were smaller than expected. Save your money and order from somewhere else.",
          "Service was incredibly slow and inattentive. Had to flag down our server multiple times for water refills. Food was underseasoned and presentation was sloppy. For these prices, I expect way better. The manager didn't even acknowledge our complaints. Won't be returning."
        ]},
        { rating: 1, texts: [
          "Absolutely the worst dining experience I've had in years. Found a HAIR in my pasta halfway through eating. When I showed the server, they just shrugged and offered to remake it. No apology, no discount. I lost my appetite completely. This is disgusting and unacceptable!",
          "AVOID AT ALL COSTS! Got severe food poisoning after eating here. Spent the entire next day sick. The chicken tasted off but I thought I was being paranoid. Called to report it and they denied any responsibility. I'm contacting the health department. This place is dangerous!",
          "Rude, unprofessional staff and terrible food. Our server rolled her eyes when we asked questions about the menu. The steak was so tough I couldn't cut it. Manager refused to comp anything and argued with us. Walked out and paid for drinks only. Never again!",
          "This place should be shut down. Dirty kitchen visible from dining area, flies buzzing around, and the smell was off-putting. We left before ordering. How is this place still operating? Seriously concerning. I'm reporting this to the authorities. Do NOT eat here!",
          "Worst $100 I've ever spent. Everything was wrong - wrong orders, wrong temperatures, wrong attitude from staff. The 'fresh' fish smelled fishy (not in a good way). Overpriced garbage. The chef should be embarrassed. Save yourself the money and disappointment. ZERO STARS if I could!"
        ]}
      ];

      const names = ["Alex Chen", "Priya Patel", "Marcus Johnson", "Sofia Rodriguez", "Jamal Williams", 
                     "Emma Thompson", "Kai Nakamura", "Olivia Martinez", "Liam O'Brien", "Zara Ahmed",
                     "Diego Santos", "Aisha Khan", "Noah Kim", "Isabella Rossi", "Ethan Taylor",
                     "Maya Singh", "Lucas Brown", "Chloe Nguyen", "Ryan Murphy", "Amara Okafor"];

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

      const response = await fetch("/api/reviews/bulk", {
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
      const response = await fetch("/api/google/fetch-reviews", {
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
      const response = await fetch("/api/fetch-reviews", {
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
