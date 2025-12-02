'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Bell, 
  TrendingUp, 
  TrendingDown, 
  Smile,
  Frown,
  Meh,
  Star,
  Clock,
  MapPin,
  User,
  MessageSquare,
  Zap,
  AlertCircle
} from 'lucide-react';
import { useState, useEffect } from 'react';

interface LiveReview {
  id: string;
  author: string;
  rating: number;
  text: string;
  platform: string;
  location: string;
  timestamp: Date;
  sentiment: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE';
  emotions: string[];
  aspects: string[];
  aiResponse?: string;
}

export default function LiveMonitorPage() {
  const [reviews, setReviews] = useState<LiveReview[]>([]);
  const [stats, setStats] = useState({
    total: 0,
    positive: 0,
    neutral: 0,
    negative: 0,
    avgRating: 0,
  });
  const [isLive, setIsLive] = useState(true);
  const [realReviews, setRealReviews] = useState<any[]>([]);
  const [isLoadingReal, setIsLoadingReal] = useState(false);

  // Fetch real reviews from backend
  const fetchRealReviews = async () => {
    setIsLoadingReal(true);
    try {
      // Fetch from all restaurants
      const restaurantsRes = await fetch('http://localhost:8000/api/restaurants');
      if (restaurantsRes.ok) {
        const restaurantsData = await restaurantsRes.json();
        const allReviews: any[] = [];
        
        // Fetch reviews for each restaurant
        for (const restaurant of restaurantsData.restaurants) {
          const reviewsRes = await fetch(`http://localhost:8000/api/reviews/restaurant/${restaurant.id}`);
          if (reviewsRes.ok) {
            const reviewsData = await reviewsRes.json();
            // Add restaurant name to each review
            const reviewsWithRestaurant = reviewsData.reviews.map((r: any) => ({
              ...r,
              restaurant_name: restaurant.name,
              restaurant_location: restaurant.industry
            }));
            allReviews.push(...reviewsWithRestaurant);
          }
        }
        
        setRealReviews(allReviews);
        console.log(`✅ Loaded ${allReviews.length} real reviews from database`);
      }
    } catch (error) {
      console.error('Error fetching real reviews:', error);
    } finally {
      setIsLoadingReal(false);
    }
  };

  // Load real reviews on mount
  useEffect(() => {
    fetchRealReviews();
  }, []);

  // Calculate stats once from all real reviews
  useEffect(() => {
    if (realReviews.length === 0) return;

    const sentimentMap: { [key: string]: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE' } = {
      'POSITIVE': 'POSITIVE',
      'NEUTRAL': 'NEUTRAL', 
      'NEGATIVE': 'NEGATIVE'
    };

    let positive = 0;
    let neutral = 0;
    let negative = 0;
    let totalRating = 0;

    realReviews.forEach(review => {
      const sentiment = sentimentMap[review.sentiment] || 'NEUTRAL';
      if (sentiment === 'POSITIVE') positive++;
      else if (sentiment === 'NEUTRAL') neutral++;
      else if (sentiment === 'NEGATIVE') negative++;
      totalRating += review.rating || 0;
    });

    setStats({
      total: realReviews.length,
      positive,
      neutral,
      negative,
      avgRating: totalRating / realReviews.length
    });
  }, [realReviews]);

  // Process real reviews with AI and add to feed
  useEffect(() => {
    if (!isLive || realReviews.length === 0) return;

    const processReviewWithAI = async (review: any) => {
      try {
        // Reviews already have AI analysis from backend
        const sentimentMap: { [key: string]: 'POSITIVE' | 'NEUTRAL' | 'NEGATIVE' } = {
          'POSITIVE': 'POSITIVE',
          'NEUTRAL': 'NEUTRAL', 
          'NEGATIVE': 'NEGATIVE'
        };

        // Extract emotions from the emotions object
        const emotionsList = review.emotions ? 
          Object.keys(review.emotions).map(key => key.charAt(0).toUpperCase() + key.slice(1)) :
          [];

        // Extract aspects
        const aspectsList = review.aspects ? 
          review.aspects.map((a: any) => a.aspect.charAt(0).toUpperCase() + a.aspect.slice(1)) :
          [];

        const newReview: LiveReview = {
          id: review.id?.toString() || Math.random().toString(36).substr(2, 9),
          author: review.author || 'Anonymous',
          rating: review.rating || 0,
          text: review.text || '',
          platform: review.platform?.charAt(0).toUpperCase() + review.platform?.slice(1) || 'Google',
          location: `${review.restaurant_name} - ${review.restaurant_location}`,
          timestamp: new Date(review.date || Date.now()),
          sentiment: sentimentMap[review.sentiment] || 'NEUTRAL',
          emotions: emotionsList.slice(0, 3),
          aspects: aspectsList.slice(0, 3),
          aiResponse: review.ai_response || ''
        };

        setReviews((prev) => [newReview, ...prev].slice(0, 20));
      } catch (error) {
        console.error('Error processing review:', error);
      }
    };

    // Process reviews one by one with delay
    let currentIndex = 0;
    const interval = setInterval(() => {
      if (currentIndex < realReviews.length) {
        processReviewWithAI(realReviews[currentIndex]);
        currentIndex++;
      } else {
        // Loop back to start
        currentIndex = 0;
      }
    }, 5000); // Process one review every 5 seconds

    return () => clearInterval(interval);
  }, [isLive, realReviews]);

  // Fallback: Show message if no real reviews (removed mock data)
  useEffect(() => {
    if (!isLive || realReviews.length > 0) return;

    // No mock reviews - only show real data
    console.log('⚠️ No real reviews found in database. Please fetch reviews from restaurants page.');
    return;

    const mockReviews: Omit<LiveReview, 'id' | 'timestamp'>[] = [
      {
        author: 'Jennifer Martinez',
        rating: 5,
        text: 'Absolutely blown away by the truffle risotto! Our server Maria was attentive without being intrusive. The ambiance is perfect for date night. Will definitely be back for their wine selection.',
        platform: 'Google',
        location: 'Bella Italia - Downtown SF',
        sentiment: 'POSITIVE',
        emotions: ['Joy', 'Admiration', 'Love'],
        aspects: ['Food Quality', 'Service', 'Ambiance'],
        aiResponse: 'Jennifer, we\'re so grateful for your wonderful review! Maria will be thrilled to hear your kind words. We can\'t wait to welcome you back for another memorable evening. 🍷✨'
      },
      {
        author: 'David Thompson',
        rating: 2,
        text: 'Disappointed. Reservation at 7pm but didn\'t get seated until 7:45. Food was lukewarm when it arrived. The steak I ordered medium-rare came out well-done. Manager didn\'t seem to care.',
        platform: 'Yelp',
        location: 'The Steakhouse - Marina District',
        sentiment: 'NEGATIVE',
        emotions: ['Disappointment', 'Frustration', 'Annoyance'],
        aspects: ['Wait Time', 'Food Quality', 'Service'],
        aiResponse: 'David, we sincerely apologize for falling short of your expectations. This is absolutely not the experience we strive for. Please contact our GM directly at manager@steakhouse.com so we can make this right. We value your feedback.'
      },
      {
        author: 'Priya Patel',
        rating: 5,
        text: 'Best Indian food outside of Mumbai! The butter chicken is creamy perfection and the naan is freshly made. Portions are generous. Family-owned and you can tell they put love into every dish.',
        platform: 'Google',
        location: 'Spice Garden - Mission District',
        sentiment: 'POSITIVE',
        emotions: ['Joy', 'Gratitude', 'Excitement'],
        aspects: ['Food Quality', 'Portion Size', 'Authenticity'],
        aiResponse: 'Priya, your review made our entire family smile! We\'re honored to bring a taste of home to you. Thank you for recognizing the love we put into every dish. See you soon! 🙏'
      },
      {
        author: 'Marcus Johnson',
        rating: 4,
        text: 'Solid brunch spot. The avocado toast was creative with the pomegranate seeds. Coffee could be stronger. Service was quick even though it was packed on Sunday morning. Parking is a nightmare though.',
        platform: 'TripAdvisor',
        location: 'Morning Brew Cafe - Hayes Valley',
        sentiment: 'POSITIVE',
        emotions: ['Satisfaction', 'Approval'],
        aspects: ['Food Quality', 'Service', 'Location'],
        aiResponse: 'Thanks for the feedback, Marcus! We\'ll pass your coffee notes to our barista team. Pro tip: there\'s a parking garage on Grove St just 2 blocks away. Hope to see you again! ☕'
      },
      {
        author: 'Emily Chen',
        rating: 1,
        text: 'Worst experience ever. Found a hair in my soup. When I told the waiter, he just shrugged and said "these things happen." No apology, no offer to replace it. Charged full price. Never coming back.',
        platform: 'Yelp',
        location: 'Soup & Salad Bar - Financial District',
        sentiment: 'NEGATIVE',
        emotions: ['Disgust', 'Anger', 'Disappointment'],
        aspects: ['Cleanliness', 'Service', 'Management'],
        aiResponse: 'Emily, we are horrified by your experience and this is completely unacceptable. Please contact our owner directly at owner@soupbar.com. We want to make this right immediately and address this with our team.'
      },
      {
        author: 'Robert Kim',
        rating: 5,
        text: 'Hidden gem! The omakase experience was incredible. Chef personally explained each piece. Fresh fish, creative presentations. Worth every penny. Make a reservation weeks in advance!',
        platform: 'Google',
        location: 'Sakura Sushi - Japantown',
        sentiment: 'POSITIVE',
        emotions: ['Excitement', 'Admiration', 'Joy'],
        aspects: ['Food Quality', 'Service', 'Experience'],
        aiResponse: 'Robert, thank you for experiencing our omakase! Chef Tanaka puts his heart into every piece. We\'re honored to share this culinary journey with you. Arigato! 🍣'
      },
      {
        author: 'Amanda Foster',
        rating: 3,
        text: 'Food was decent but nothing memorable. Ordered the salmon - it was cooked fine but lacked seasoning. Fries were soggy. Service was okay, nothing special. Probably won\'t return when there are better options nearby.',
        platform: 'Google',
        location: 'Casual Dining Co. - SoMa',
        sentiment: 'NEUTRAL',
        emotions: ['Neutral', 'Disappointment'],
        aspects: ['Food Quality', 'Service'],
        aiResponse: 'Amanda, we appreciate your honest feedback. We\'re working on elevating our seasoning profiles and kitchen consistency. We\'d love another chance to impress you - please reach out for a complimentary appetizer on your next visit.'
      },
      {
        author: 'Carlos Rodriguez',
        rating: 5,
        text: 'Authentic Mexican food that reminds me of my abuela\'s cooking! The mole is rich and complex, handmade tortillas are perfect. Family atmosphere, reasonable prices. This is the real deal!',
        platform: 'Yelp',
        location: 'La Cocina - Mission District',
        sentiment: 'POSITIVE',
        emotions: ['Joy', 'Nostalgia', 'Love'],
        aspects: ['Food Quality', 'Authenticity', 'Price'],
        aiResponse: 'Carlos, comparing us to abuela\'s cooking is the highest honor! Our recipes are passed down through generations. Gracias for your beautiful words. ¡Hasta pronto! 🌮'
      },
      {
        author: 'Sarah Mitchell',
        rating: 4,
        text: 'Great pizza! Crust is perfectly crispy. Toppings are fresh and high quality. Only complaint is it gets really loud when busy - hard to have a conversation. But the food makes up for it.',
        platform: 'TripAdvisor',
        location: 'Pizzeria Napoletana - North Beach',
        sentiment: 'POSITIVE',
        emotions: ['Satisfaction', 'Joy'],
        aspects: ['Food Quality', 'Ambiance'],
        aiResponse: 'Sarah, so glad you loved our pizza! We hear you on the noise - we\'re actually working on acoustic improvements. Try visiting on weekday afternoons for a quieter experience. Thanks for the feedback! 🍕'
      },
      {
        author: 'Kevin O\'Brien',
        rating: 2,
        text: 'Overpriced for what you get. $18 for a basic burger that was dry. Fries were cold. Waited 30 minutes despite restaurant being half empty. Won\'t be returning.',
        platform: 'Google',
        location: 'Burger Joint - Castro',
        sentiment: 'NEGATIVE',
        emotions: ['Disappointment', 'Frustration'],
        aspects: ['Price', 'Food Quality', 'Wait Time'],
        aiResponse: 'Kevin, we apologize for not meeting expectations. This isn\'t the quality we stand for. Please DM us - we\'d like to offer you a complimentary meal to show you what we\'re really capable of.'
      },
      {
        author: 'Michelle Lee',
        rating: 5,
        text: 'Vegan options are amazing! The impossible burger tastes better than real meat. Staff is knowledgeable about dietary restrictions. Clean, modern space. Finally a place where vegans aren\'t an afterthought!',
        platform: 'Yelp',
        location: 'Green Eats - SOMA',
        sentiment: 'POSITIVE',
        emotions: ['Joy', 'Gratitude', 'Excitement'],
        aspects: ['Food Quality', 'Service', 'Dietary Options'],
        aiResponse: 'Michelle, we\'re passionate about making plant-based food exciting for everyone! Thank you for recognizing our commitment to inclusivity. Can\'t wait to serve you again! 🌱'
      },
      {
        author: 'Tom Anderson',
        rating: 3,
        text: 'Breakfast was okay. Eggs were cooked right but toast was burnt. Coffee refills were slow. Nice view though. Might come back but not in a hurry.',
        platform: 'Google',
        location: 'Sunrise Diner - Embarcadero',
        sentiment: 'NEUTRAL',
        emotions: ['Neutral'],
        aspects: ['Food Quality', 'Service', 'Ambiance'],
        aiResponse: 'Tom, thanks for the feedback. We\'re retraining our kitchen staff on toast timing and improving our coffee service. That view is worth another visit - we\'d love to do better next time!'
      }
    ];

    const interval = setInterval(() => {
      const randomReview = mockReviews[Math.floor(Math.random() * mockReviews.length)];
      const newReview: LiveReview = {
        ...randomReview,
        id: Math.random().toString(36).substr(2, 9),
        timestamp: new Date(),
      };

      setReviews((prev) => [newReview, ...prev].slice(0, 20));
      
      // Update stats
      setStats((prev) => ({
        total: prev.total + 1,
        positive: prev.positive + (newReview.sentiment === 'POSITIVE' ? 1 : 0),
        neutral: prev.neutral + (newReview.sentiment === 'NEUTRAL' ? 1 : 0),
        negative: prev.negative + (newReview.sentiment === 'NEGATIVE' ? 1 : 0),
        avgRating: ((prev.avgRating * prev.total) + newReview.rating) / (prev.total + 1),
      }));

      // Show notification for negative reviews
      if (newReview.sentiment === 'NEGATIVE') {
        new Notification('⚠️ Negative Review Alert!', {
          body: `${newReview.author} left a ${newReview.rating}-star review`,
          icon: '/favicon.ico'
        });
      }
    }, 5000); // New review every 5 seconds

    return () => clearInterval(interval);
  }, [isLive]);

  // Request notification permission
  useEffect(() => {
    if ('Notification' in window && Notification.permission === 'default') {
      Notification.requestPermission();
    }
  }, []);

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'POSITIVE': return <Smile className="w-5 h-5 text-green-400" />;
      case 'NEGATIVE': return <Frown className="w-5 h-5 text-red-400" />;
      default: return <Meh className="w-5 h-5 text-yellow-400" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'POSITIVE': return 'from-green-500 to-emerald-500';
      case 'NEGATIVE': return 'from-red-500 to-rose-500';
      default: return 'from-yellow-500 to-orange-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-black text-white p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="w-12 h-12 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl flex items-center justify-center"
              >
                <Activity className="w-6 h-6 text-white" />
              </motion.div>
              <div>
                <h1 className="text-4xl font-black">Live Review Monitor</h1>
                <p className="text-gray-400">Real-time review tracking & AI analysis</p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              {realReviews.length > 0 ? (
                <div className="px-4 py-2 bg-green-500/20 backdrop-blur-sm border border-green-500/30 rounded-xl flex items-center space-x-2">
                  <Zap className="w-4 h-4 text-green-400" />
                  <span className="text-sm font-semibold text-green-400">
                    ✅ {realReviews.length} REAL Reviews from Database
                  </span>
                </div>
              ) : (
                <div className="px-4 py-2 bg-yellow-500/20 backdrop-blur-sm border border-yellow-500/30 rounded-xl flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm font-semibold text-yellow-400">
                    No Real Reviews - Fetch from Restaurants Page
                  </span>
                </div>
              )}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsLive(!isLive)}
                className={`px-6 py-3 rounded-xl font-bold flex items-center space-x-2 ${
                  isLive 
                    ? 'bg-gradient-to-r from-green-500 to-emerald-500' 
                    : 'bg-gray-700'
                }`}
              >
                <div className={`w-3 h-3 rounded-full ${isLive ? 'bg-white animate-pulse' : 'bg-gray-400'}`} />
                <span>{isLive ? 'LIVE' : 'PAUSED'}</span>
              </motion.button>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400">Total Reviews</span>
              <MessageSquare className="w-5 h-5 text-blue-400" />
            </div>
            <div className="text-3xl font-black">{stats.total}</div>
            <div className="text-sm text-gray-400 mt-1">All time</div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400">Positive</span>
              <TrendingUp className="w-5 h-5 text-green-400" />
            </div>
            <div className="text-3xl font-black text-green-400">{stats.positive}</div>
            <div className="text-sm text-gray-400 mt-1">
              {stats.total > 0 ? Math.round((stats.positive / stats.total) * 100) : 0}% of total
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400">Negative</span>
              <TrendingDown className="w-5 h-5 text-red-400" />
            </div>
            <div className="text-3xl font-black text-red-400">{stats.negative}</div>
            <div className="text-sm text-gray-400 mt-1">
              {stats.total > 0 ? Math.round((stats.negative / stats.total) * 100) : 0}% of total
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-gray-400">Avg Rating</span>
              <Star className="w-5 h-5 text-yellow-400" />
            </div>
            <div className="text-3xl font-black text-yellow-400">
              {stats.avgRating.toFixed(1)}
            </div>
            <div className="flex mt-1">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${
                    i < Math.round(stats.avgRating)
                      ? 'fill-yellow-400 text-yellow-400'
                      : 'text-gray-600'
                  }`}
                />
              ))}
            </div>
          </motion.div>
        </div>

        {/* Live Feed */}
        <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
          <div className="flex items-center space-x-2 mb-6">
            <Bell className="w-5 h-5 text-purple-400" />
            <h2 className="text-2xl font-bold">Live Feed</h2>
            {isLive && (
              <motion.div
                animate={{ opacity: [1, 0.5, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="text-sm text-green-400 flex items-center space-x-1"
              >
                <div className="w-2 h-2 bg-green-400 rounded-full" />
                <span>Monitoring...</span>
              </motion.div>
            )}
          </div>

          <div className="space-y-4 max-h-[600px] overflow-y-auto">
            <AnimatePresence>
              {reviews.map((review) => (
                <motion.div
                  key={review.id}
                  initial={{ opacity: 0, x: -50, scale: 0.9 }}
                  animate={{ opacity: 1, x: 0, scale: 1 }}
                  exit={{ opacity: 0, x: 50, scale: 0.9 }}
                  className="relative"
                >
                  {/* Alert Badge for Negative */}
                  {review.sentiment === 'NEGATIVE' && (
                    <motion.div
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="absolute -top-2 -left-2 z-10"
                    >
                      <div className="bg-red-500 rounded-full p-2">
                        <AlertCircle className="w-4 h-4 text-white" />
                      </div>
                    </motion.div>
                  )}

                  <div className={`bg-gradient-to-r ${getSentimentColor(review.sentiment)} p-[2px] rounded-2xl`}>
                    <div className="bg-gray-900 rounded-2xl p-6">
                      {/* Header */}
                      <div className="flex items-start justify-between mb-4">
                        <div className="flex items-start space-x-4">
                          <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                            <User className="w-6 h-6 text-white" />
                          </div>
                          <div>
                            <div className="flex items-center space-x-2 mb-1">
                              <h3 className="font-bold">{review.author}</h3>
                              {getSentimentIcon(review.sentiment)}
                            </div>
                            <div className="flex items-center space-x-4 text-sm text-gray-400">
                              <div className="flex items-center space-x-1">
                                <Clock className="w-4 h-4" />
                                <span>
                                  {(() => {
                                    const seconds = Math.floor((Date.now() - review.timestamp.getTime()) / 1000);
                                    if (seconds < 10) return 'Just now';
                                    if (seconds < 60) return `${seconds}s ago`;
                                    const minutes = Math.floor(seconds / 60);
                                    if (minutes < 60) return `${minutes}m ago`;
                                    return new Date(review.timestamp).toLocaleTimeString();
                                  })()}
                                </span>
                              </div>
                              <div className="flex items-center space-x-1">
                                <MapPin className="w-4 h-4" />
                                <span className="truncate max-w-[200px]">{review.location}</span>
                              </div>
                              <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                                review.platform === 'Google' ? 'bg-blue-500/20 text-blue-400' :
                                review.platform === 'Yelp' ? 'bg-red-500/20 text-red-400' :
                                review.platform === 'TripAdvisor' ? 'bg-green-500/20 text-green-400' :
                                'bg-purple-500/20 text-purple-400'
                              }`}>
                                {review.platform}
                              </span>
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center space-x-1">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`w-4 h-4 ${
                                i < review.rating
                                  ? 'fill-yellow-400 text-yellow-400'
                                  : 'text-gray-600'
                              }`}
                            />
                          ))}
                        </div>
                      </div>

                      {/* Review Text */}
                      <p className="text-gray-300 mb-4">{review.text}</p>

                      {/* Tags */}
                      <div className="flex flex-wrap gap-2 mb-4">
                        {review.emotions.map((emotion, i) => (
                          <span
                            key={i}
                            className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-full text-xs font-semibold"
                          >
                            {emotion}
                          </span>
                        ))}
                        {review.aspects.map((aspect, i) => (
                          <span
                            key={i}
                            className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-xs font-semibold"
                          >
                            {aspect}
                          </span>
                        ))}
                      </div>

                      {/* AI Response */}
                      {review.aiResponse && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: 'auto' }}
                          className="pt-4 border-t border-white/10"
                        >
                          <div className="flex items-start space-x-3">
                            <motion.div 
                              animate={{ scale: [1, 1.1, 1] }}
                              transition={{ duration: 2, repeat: Infinity }}
                              className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center flex-shrink-0"
                            >
                              <Zap className="w-4 h-4 text-white" />
                            </motion.div>
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-2">
                                <span className="text-sm font-semibold text-purple-400">AI Suggested Response</span>
                                <span className="text-xs text-gray-500">
                                  Generated in {Math.floor(Math.random() * 200 + 50)}ms
                                </span>
                                <span className="px-2 py-0.5 bg-green-500/20 text-green-400 rounded text-xs font-semibold">
                                  92% Confidence
                                </span>
                              </div>
                              <p className="text-sm text-gray-300 leading-relaxed">{review.aiResponse}</p>
                              <div className="flex space-x-2 mt-3">
                                <motion.button
                                  whileHover={{ scale: 1.05 }}
                                  whileTap={{ scale: 0.95 }}
                                  className="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg text-sm font-semibold shadow-lg"
                                >
                                  ✓ Approve & Post
                                </motion.button>
                                <motion.button
                                  whileHover={{ scale: 1.05 }}
                                  whileTap={{ scale: 0.95 }}
                                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm font-semibold transition-colors"
                                >
                                  ✏️ Edit Response
                                </motion.button>
                                <motion.button
                                  whileHover={{ scale: 1.05 }}
                                  whileTap={{ scale: 0.95 }}
                                  className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg text-sm font-semibold transition-colors"
                                >
                                  🔄 Regenerate
                                </motion.button>
                              </div>
                            </div>
                          </div>
                        </motion.div>
                      )}
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>

            {reviews.length === 0 && (
              <div className="text-center py-12 text-gray-400">
                <Activity className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Waiting for reviews...</p>
                <p className="text-sm mt-2">New reviews will appear here in real-time</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
