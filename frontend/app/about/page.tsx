'use client';

import { motion } from 'framer-motion';
import { Sparkles, Target, Users, Zap, Heart, Shield } from 'lucide-react';
import Link from 'next/link';

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Navigation */}
      <motion.nav
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="fixed top-0 left-0 right-0 z-50 backdrop-blur-2xl bg-white/80 border-b border-gray-200"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <Link href="/home" className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/30">
                <Sparkles className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold text-gray-900">RevuIQ</span>
            </Link>
            
            <div className="hidden md:flex items-center space-x-8">
              <Link href="/home#features" className="text-gray-600 hover:text-gray-900 font-medium">Features</Link>
              <Link href="/pricing" className="text-gray-600 hover:text-gray-900 font-medium">Pricing</Link>
              <Link href="/about" className="text-gray-900 font-semibold">About</Link>
              <Link href="/careers" className="text-gray-600 hover:text-gray-900 font-medium">Careers</Link>
            </div>

            <div className="flex items-center space-x-4">
              <Link href="/login">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-6 py-2.5 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-xl shadow-lg shadow-blue-500/50"
                >
                  Get Started
                </motion.button>
              </Link>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              About RevuIQ
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We're on a mission to help businesses manage their online reputation with the power of artificial intelligence.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
            >
              <h2 className="text-4xl font-bold text-gray-900 mb-6">
                Our Mission
              </h2>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                RevuIQ was born from a simple observation: businesses struggle to keep up with customer reviews across multiple platforms. We saw an opportunity to leverage AI and NLP to automate this process while maintaining the human touch.
              </p>
              <p className="text-lg text-gray-600 leading-relaxed">
                Our goal is to empower businesses of all sizes to understand their customers better, respond faster, and build stronger relationships through intelligent review management.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl p-12 text-white"
            >
              <div className="space-y-8">
                <div>
                  <div className="text-5xl font-bold mb-2">10K+</div>
                  <div className="text-blue-100">Reviews Analyzed Daily</div>
                </div>
                <div>
                  <div className="text-5xl font-bold mb-2">500+</div>
                  <div className="text-blue-100">Happy Businesses</div>
                </div>
                <div>
                  <div className="text-5xl font-bold mb-2">98%</div>
                  <div className="text-blue-100">Customer Satisfaction</div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-gray-50 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Our Values
            </h2>
            <p className="text-xl text-gray-600">
              The principles that guide everything we do
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Target,
                title: 'Customer First',
                description: 'We build features that solve real problems for real businesses. Your success is our success.',
                color: 'from-blue-500 to-cyan-500'
              },
              {
                icon: Shield,
                title: 'Trust & Transparency',
                description: 'We believe in ethical AI. Human oversight ensures every response maintains your brand voice.',
                color: 'from-purple-500 to-pink-500'
              },
              {
                icon: Zap,
                title: 'Innovation',
                description: 'We continuously improve our NLP models to provide the most accurate insights and responses.',
                color: 'from-orange-500 to-amber-500'
              }
            ].map((value, index) => (
              <motion.div
                key={value.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -8 }}
                className="bg-white rounded-2xl p-8 shadow-lg"
              >
                <div className={`w-14 h-14 bg-gradient-to-br ${value.color} rounded-2xl flex items-center justify-center mb-6 shadow-lg`}>
                  <value.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{value.title}</h3>
                <p className="text-gray-600 leading-relaxed">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Powered by Advanced NLP
            </h2>
            <p className="text-xl text-gray-600">
              State-of-the-art technology stack
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: 'Sentiment Analysis', tech: 'RoBERTa Transformers' },
              { name: 'Emotion Detection', tech: 'GoEmotions Model' },
              { name: 'Response Generation', tech: 'Flan-T5' },
              { name: 'Aspect Extraction', tech: 'Custom NER' }
            ].map((item, index) => (
              <motion.div
                key={item.name}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gradient-to-br from-gray-50 to-white rounded-xl p-6 border border-gray-200"
              >
                <h4 className="font-semibold text-gray-900 mb-2">{item.name}</h4>
                <p className="text-sm text-gray-600">{item.tech}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-gradient-to-br from-blue-50 to-purple-50 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Built by Experts
          </h2>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
            Our team combines expertise in AI, NLP, and customer experience to deliver the best review management solution.
          </p>
          
          <div className="flex justify-center space-x-4">
            <div className="px-6 py-3 bg-white rounded-xl shadow-lg">
              <div className="text-2xl font-bold text-gray-900">AI/ML Engineers</div>
            </div>
            <div className="px-6 py-3 bg-white rounded-xl shadow-lg">
              <div className="text-2xl font-bold text-gray-900">NLP Specialists</div>
            </div>
            <div className="px-6 py-3 bg-white rounded-xl shadow-lg">
              <div className="text-2xl font-bold text-gray-900">UX Designers</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-500 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold text-white mb-6">
            Join us on our mission
          </h2>
          <p className="text-xl text-blue-100 mb-10">
            Start managing your reviews with intelligence today.
          </p>
          <Link href="/login">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-10 py-4 bg-white text-blue-600 font-bold rounded-xl shadow-2xl"
            >
              Get Started Free
            </motion.button>
          </Link>
        </div>
      </section>
    </div>
  );
}
