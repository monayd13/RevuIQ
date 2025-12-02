'use client';

import { motion, useScroll, useTransform, AnimatePresence } from 'framer-motion';
import { 
  Sparkles, 
  Brain, 
  Zap, 
  Shield, 
  TrendingUp, 
  MessageSquare,
  Star,
  ArrowRight,
  CheckCircle2,
  Rocket,
  Globe,
  BarChart3,
  Users,
  Heart,
  Smile,
  Frown,
  Meh
} from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';

export default function LandingPage() {
  const router = useRouter();
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [activeFeature, setActiveFeature] = useState(0);
  const { scrollYProgress } = useScroll();
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);
  const scale = useTransform(scrollYProgress, [0, 0.5], [1, 0.8]);

  // Floating particles effect
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 4 + 2,
    duration: Math.random() * 10 + 10
  }));

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  // Auto-rotate features
  useEffect(() => {
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % 4);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: Brain,
      title: "AI-Powered Analysis",
      description: "Advanced NLP models analyze sentiment, emotions, and key aspects in real-time",
      color: "from-purple-500 to-pink-500",
      stats: "99.2% Accuracy"
    },
    {
      icon: Zap,
      title: "Instant Responses",
      description: "Generate brand-consistent, empathetic replies in milliseconds",
      color: "from-blue-500 to-cyan-500",
      stats: "< 100ms Response"
    },
    {
      icon: Shield,
      title: "Human-in-the-Loop",
      description: "AI suggests, you approve. Maintain full control over your brand voice",
      color: "from-green-500 to-emerald-500",
      stats: "100% Control"
    },
    {
      icon: TrendingUp,
      title: "Smart Analytics",
      description: "Beautiful dashboards reveal trends, patterns, and actionable insights",
      color: "from-orange-500 to-red-500",
      stats: "Real-time Insights"
    }
  ];

  const stats = [
    { value: "10K+", label: "Reviews Analyzed", icon: MessageSquare },
    { value: "99.2%", label: "Accuracy Rate", icon: CheckCircle2 },
    { value: "< 100ms", label: "Response Time", icon: Zap },
    { value: "24/7", label: "AI Monitoring", icon: Shield }
  ];

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Animated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        {/* Gradient Orbs */}
        <motion.div
          className="absolute w-[800px] h-[800px] rounded-full blur-3xl opacity-20"
          style={{
            background: 'radial-gradient(circle, rgba(139,92,246,0.8) 0%, rgba(59,130,246,0.4) 50%, transparent 100%)',
            left: mousePosition.x - 400,
            top: mousePosition.y - 400,
          }}
          animate={{
            scale: [1, 1.2, 1],
            opacity: [0.2, 0.3, 0.2],
          }}
          transition={{
            duration: 4,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
        
        {/* Floating Particles */}
        {particles.map((particle) => (
          <motion.div
            key={particle.id}
            className="absolute rounded-full bg-gradient-to-r from-blue-400 to-purple-400"
            style={{
              width: particle.size,
              height: particle.size,
              left: `${particle.x}%`,
              top: `${particle.y}%`,
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: particle.duration,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        ))}

        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(139,92,246,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(139,92,246,0.03)_1px,transparent_1px)] bg-[size:100px_100px]" />
      </div>

      {/* Hero Section */}
      <motion.section 
        className="relative min-h-screen flex items-center justify-center px-4"
        style={{ opacity, scale }}
      >
        <div className="max-w-7xl mx-auto text-center">
          {/* Logo Animation */}
          <motion.div
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ type: "spring", stiffness: 200, damping: 20 }}
            className="inline-block mb-8"
          >
            <div className="relative">
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-purple-500 to-blue-500 rounded-3xl blur-2xl opacity-50"
                animate={{
                  scale: [1, 1.2, 1],
                  opacity: [0.5, 0.8, 0.5],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut"
                }}
              />
              <div className="relative w-24 h-24 bg-gradient-to-br from-purple-500 via-blue-500 to-cyan-500 rounded-3xl flex items-center justify-center shadow-2xl">
                <Sparkles className="w-12 h-12 text-white" />
              </div>
            </div>
          </motion.div>

          {/* Main Heading */}
          <motion.h1
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="text-7xl md:text-9xl font-black mb-6 bg-gradient-to-r from-white via-purple-200 to-blue-200 bg-clip-text text-transparent"
          >
            RevuIQ
          </motion.h1>

          {/* Animated Subtitle */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="mb-8"
          >
            <p className="text-2xl md:text-4xl font-bold text-gray-300 mb-4">
              AI-Powered Review Management
            </p>
            <p className="text-lg md:text-xl text-gray-400 max-w-3xl mx-auto">
              Transform customer feedback into actionable insights with cutting-edge AI.
              Analyze sentiment, detect emotions, and generate perfect responses instantly.
            </p>
          </motion.div>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.7 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
          >
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: "0 0 40px rgba(139,92,246,0.6)" }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push('/signup')}
              className="group relative px-8 py-4 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl font-bold text-lg overflow-hidden shadow-2xl"
            >
              <motion.div
                className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500"
                initial={{ x: "100%" }}
                whileHover={{ x: 0 }}
                transition={{ duration: 0.3 }}
              />
              <span className="relative flex items-center space-x-2">
                <span>Start Free Trial</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => router.push('/login')}
              className="px-8 py-4 bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl font-bold text-lg hover:bg-white/20 transition-all"
            >
              Sign In
            </motion.button>
          </motion.div>

          {/* Floating Stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.9 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto"
          >
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.5 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.9 + index * 0.1 }}
                whileHover={{ scale: 1.1, y: -5 }}
                className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all"
              >
                <stat.icon className="w-8 h-8 text-purple-400 mb-2 mx-auto" />
                <div className="text-3xl font-black bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                  {stat.value}
                </div>
                <div className="text-sm text-gray-400 mt-1">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center">
            <motion.div
              className="w-1.5 h-3 bg-white rounded-full mt-2"
              animate={{ y: [0, 12, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </div>
        </motion.div>
      </motion.section>

      {/* Features Section */}
      <section className="relative py-32 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-7xl font-black mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
              Superpowers for Your Business
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Harness the power of AI to transform how you manage customer reviews
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: index % 2 === 0 ? -50 : 50 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                whileHover={{ scale: 1.05, rotateY: 5 }}
                className="group relative"
              >
                <div className="absolute inset-0 bg-gradient-to-r opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl"
                  style={{ background: `linear-gradient(to right, ${feature.color})` }}
                />
                <div className="relative bg-white/5 backdrop-blur-sm border border-white/10 rounded-3xl p-8 hover:bg-white/10 transition-all">
                  <div className={`inline-flex p-4 bg-gradient-to-r ${feature.color} rounded-2xl mb-6`}>
                    <feature.icon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold mb-3">{feature.title}</h3>
                  <p className="text-gray-400 mb-4">{feature.description}</p>
                  <div className="inline-flex items-center space-x-2 text-sm font-semibold text-purple-400">
                    <Zap className="w-4 h-4" />
                    <span>{feature.stats}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Interactive Demo Section */}
      <section className="relative py-32 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-7xl font-black mb-6 bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">
              See It In Action
            </h2>
          </motion.div>

          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Mock Review Card */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-6"
            >
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-3xl p-8">
                <div className="flex items-start space-x-4 mb-4">
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                    <Users className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <h4 className="font-bold">Sarah Johnson</h4>
                      <div className="flex">
                        {[...Array(5)].map((_, i) => (
                          <Star key={i} className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                        ))}
                      </div>
                    </div>
                    <p className="text-gray-400 text-sm mb-4">
                      "Amazing service! The food was incredible and the staff went above and beyond. Will definitely come back!"
                    </p>
                    
                    {/* AI Analysis */}
                    <div className="space-y-2">
                      <div className="flex items-center space-x-2">
                        <Smile className="w-5 h-5 text-green-400" />
                        <span className="text-sm text-green-400 font-semibold">Positive Sentiment (98%)</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Heart className="w-5 h-5 text-pink-400" />
                        <span className="text-sm text-pink-400 font-semibold">Emotions: Joy, Gratitude</span>
                      </div>
                      <div className="flex flex-wrap gap-2 mt-3">
                        <span className="px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full text-xs font-semibold">Food Quality</span>
                        <span className="px-3 py-1 bg-purple-500/20 text-purple-400 rounded-full text-xs font-semibold">Service</span>
                        <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-semibold">Staff</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* AI Response */}
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  transition={{ delay: 1 }}
                  className="mt-6 pt-6 border-t border-white/10"
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-500 rounded-full flex items-center justify-center">
                      <Brain className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="font-semibold">AI Generated Response</span>
                        <Sparkles className="w-4 h-4 text-purple-400" />
                      </div>
                      <p className="text-gray-300 text-sm">
                        "Thank you so much for your wonderful review, Sarah! We're thrilled to hear you enjoyed both the food and service. Our team works hard to create memorable experiences, and your kind words mean the world to us. We can't wait to welcome you back soon! 🌟"
                      </p>
                    </div>
                  </div>
                </motion.div>
              </div>
            </motion.div>

            {/* Benefits List */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="space-y-6"
            >
              {[
                { icon: Brain, title: "AI Understands Context", desc: "Advanced NLP analyzes tone, intent, and emotions" },
                { icon: Zap, title: "Instant Analysis", desc: "Get insights in milliseconds, not hours" },
                { icon: MessageSquare, title: "Perfect Responses", desc: "Brand-consistent replies every time" },
                { icon: TrendingUp, title: "Actionable Insights", desc: "Identify trends and improve your business" }
              ].map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: 20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ x: 10 }}
                  className="flex items-start space-x-4 p-4 bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl hover:bg-white/10 transition-all"
                >
                  <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl flex items-center justify-center flex-shrink-0">
                    <item.icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h4 className="font-bold mb-1">{item.title}</h4>
                    <p className="text-sm text-gray-400">{item.desc}</p>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Final CTA */}
      <section className="relative py-32 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500 to-blue-500 rounded-3xl blur-3xl opacity-30" />
            <div className="relative bg-gradient-to-r from-purple-500/20 to-blue-500/20 backdrop-blur-sm border border-white/20 rounded-3xl p-12">
              <Rocket className="w-16 h-16 text-white mx-auto mb-6" />
              <h2 className="text-4xl md:text-6xl font-black mb-6">
                Ready to Transform Your Reviews?
              </h2>
              <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
                Join thousands of businesses using AI to manage customer feedback smarter, faster, and better.
              </p>
              <motion.button
                whileHover={{ scale: 1.05, boxShadow: "0 0 60px rgba(139,92,246,0.8)" }}
                whileTap={{ scale: 0.95 }}
                onClick={() => router.push('/signup')}
                className="px-12 py-5 bg-gradient-to-r from-purple-500 to-blue-500 rounded-2xl font-bold text-xl shadow-2xl hover:shadow-purple-500/50 transition-all"
              >
                Get Started Free →
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative border-t border-white/10 py-12 px-4">
        <div className="max-w-7xl mx-auto text-center text-gray-400">
          <p className="mb-4">© 2025 RevuIQ. Powered by AI. Built with ❤️</p>
          <div className="flex justify-center space-x-6 text-sm">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
