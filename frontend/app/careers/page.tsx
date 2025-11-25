'use client';

import { motion } from 'framer-motion';
import { Sparkles, Briefcase, Code, Database, Server, Award, TrendingUp, Users, Heart } from 'lucide-react';
import Link from 'next/link';
import { useState } from 'react';

export default function CareersPage() {
  const [selectedJob, setSelectedJob] = useState<string | null>(null);

  const jobs = [
    {
      id: 'backend-intern',
      title: 'Backend Engineer Intern',
      department: 'Engineering',
      location: 'Remote',
      type: 'Unpaid Internship',
      icon: Server,
      color: 'from-blue-500 to-cyan-500',
      description: 'Join our backend team to build scalable APIs and microservices that power RevuIQ\'s AI-driven review management platform.',
      responsibilities: [
        'Develop and maintain RESTful APIs using FastAPI and Python',
        'Work with PostgreSQL databases and optimize queries',
        'Integrate NLP models into production systems',
        'Implement authentication and authorization systems',
        'Write clean, maintainable, and well-documented code',
        'Participate in code reviews and team discussions'
      ],
      requirements: [
        'Currently pursuing a degree in Computer Science or related field',
        'Strong foundation in Python programming',
        'Understanding of REST API design principles',
        'Familiarity with databases (SQL)',
        'Basic knowledge of Git and version control',
        'Eagerness to learn and grow'
      ],
      niceToHave: [
        'Experience with FastAPI or Flask',
        'Knowledge of Docker and containerization',
        'Understanding of cloud platforms (AWS/GCP)',
        'Exposure to microservices architecture'
      ]
    },
    {
      id: 'software-intern',
      title: 'Software Engineering Intern',
      department: 'Engineering',
      location: 'Remote',
      type: 'Unpaid Internship',
      icon: Code,
      color: 'from-purple-500 to-pink-500',
      description: 'Work on full-stack development, building beautiful user interfaces and robust backend systems for our review management platform.',
      responsibilities: [
        'Develop responsive web applications using Next.js and React',
        'Build and integrate backend APIs',
        'Implement new features across the full stack',
        'Collaborate with designers to create intuitive UIs',
        'Write unit and integration tests',
        'Debug and fix issues across the codebase'
      ],
      requirements: [
        'Currently pursuing a degree in Computer Science or related field',
        'Proficiency in JavaScript/TypeScript',
        'Understanding of React and modern web development',
        'Knowledge of HTML, CSS, and responsive design',
        'Problem-solving mindset',
        'Strong communication skills'
      ],
      niceToHave: [
        'Experience with Next.js or similar frameworks',
        'Knowledge of Tailwind CSS',
        'Understanding of state management (Context API, Redux)',
        'Familiarity with RESTful APIs'
      ]
    },
    {
      id: 'data-scientist-intern',
      title: 'Data Scientist Intern',
      department: 'AI/ML',
      location: 'Remote',
      type: 'Unpaid Internship',
      icon: Database,
      color: 'from-emerald-500 to-green-500',
      description: 'Help us improve our NLP models and extract meaningful insights from customer reviews using cutting-edge machine learning techniques.',
      responsibilities: [
        'Fine-tune NLP models for sentiment and emotion analysis',
        'Analyze customer review data to identify trends',
        'Build and evaluate machine learning models',
        'Create data visualizations and reports',
        'Experiment with new NLP techniques and models',
        'Collaborate with engineering team on model deployment'
      ],
      requirements: [
        'Currently pursuing a degree in Data Science, Computer Science, or related field',
        'Strong foundation in Python and data analysis',
        'Understanding of machine learning concepts',
        'Experience with pandas, numpy, and scikit-learn',
        'Knowledge of statistics and data visualization',
        'Analytical and detail-oriented mindset'
      ],
      niceToHave: [
        'Experience with Hugging Face Transformers',
        'Knowledge of PyTorch or TensorFlow',
        'Understanding of NLP concepts (tokenization, embeddings)',
        'Familiarity with Jupyter notebooks'
      ]
    }
  ];

  const perks = [
    {
      icon: Award,
      title: 'Certificate of Completion',
      description: 'Receive an official certificate upon successful completion of your internship'
    },
    {
      icon: TrendingUp,
      title: 'Full-Time Conversion',
      description: 'Outstanding interns may be offered full-time positions based on performance'
    },
    {
      icon: Users,
      title: 'Mentorship Program',
      description: 'Work directly with experienced engineers and data scientists'
    },
    {
      icon: Heart,
      title: 'Hands-on Experience',
      description: 'Work on real-world projects that impact thousands of users'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
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
              <Link href="/about" className="text-gray-600 hover:text-gray-900 font-medium">About</Link>
              <Link href="/careers" className="text-gray-900 font-semibold">Careers</Link>
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
      <section className="pt-32 pb-16 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-50 rounded-full mb-6">
              <Briefcase className="w-4 h-4 text-blue-600" />
              <span className="text-sm font-semibold text-blue-600">Join Our Team</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
              Build the Future of<br />
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Review Management
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Join our mission to help businesses manage their online reputation with AI-powered intelligence.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
          <p className="text-lg text-gray-600 leading-relaxed mb-8">
            At RevuIQ, we're revolutionizing how businesses interact with customer feedback. We combine cutting-edge NLP technology with human expertise to create meaningful connections between businesses and their customers. Our team is passionate about building tools that make a real difference.
          </p>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="bg-gradient-to-br from-blue-50 to-white rounded-xl p-6 border border-blue-100">
              <div className="text-3xl font-bold text-blue-600 mb-2">10K+</div>
              <div className="text-gray-600">Reviews Analyzed Daily</div>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-white rounded-xl p-6 border border-purple-100">
              <div className="text-3xl font-bold text-purple-600 mb-2">500+</div>
              <div className="text-gray-600">Happy Businesses</div>
            </div>
            <div className="bg-gradient-to-br from-emerald-50 to-white rounded-xl p-6 border border-emerald-100">
              <div className="text-3xl font-bold text-emerald-600 mb-2">98%</div>
              <div className="text-gray-600">Satisfaction Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Perks Section */}
      <section className="py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Internship Perks</h2>
            <p className="text-xl text-gray-600">What you'll gain from this experience</p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {perks.map((perk, index) => (
              <motion.div
                key={perk.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -8 }}
                className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100"
              >
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mb-4 shadow-lg shadow-blue-500/30">
                  <perk.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-lg font-bold text-gray-900 mb-2">{perk.title}</h3>
                <p className="text-gray-600 text-sm">{perk.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Job Openings */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Open Positions</h2>
            <p className="text-xl text-gray-600">Internship opportunities to kickstart your career</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {jobs.map((job, index) => (
              <motion.div
                key={job.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -8, scale: 1.02 }}
                className="bg-gradient-to-br from-gray-50 to-white rounded-2xl p-6 shadow-lg border border-gray-200 cursor-pointer"
                onClick={() => setSelectedJob(selectedJob === job.id ? null : job.id)}
              >
                <div className={`w-14 h-14 bg-gradient-to-br ${job.color} rounded-2xl flex items-center justify-center mb-4 shadow-lg`}>
                  <job.icon className="w-7 h-7 text-white" />
                </div>
                
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{job.title}</h3>
                <div className="flex items-center space-x-2 mb-4">
                  <span className="px-3 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-full">
                    {job.department}
                  </span>
                  <span className="px-3 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded-full">
                    {job.location}
                  </span>
                </div>
                
                <p className="text-gray-600 mb-4">{job.description}</p>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-gray-500">{job.type}</span>
                  <button className="text-blue-600 font-semibold hover:text-blue-700">
                    {selectedJob === job.id ? 'Hide Details' : 'View Details →'}
                  </button>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Job Details */}
          {selectedJob && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="bg-white rounded-2xl p-8 shadow-xl border border-gray-200"
            >
              {jobs.filter(j => j.id === selectedJob).map(job => (
                <div key={job.id}>
                  <div className="flex items-start justify-between mb-8">
                    <div>
                      <h3 className="text-3xl font-bold text-gray-900 mb-2">{job.title}</h3>
                      <div className="flex items-center space-x-3">
                        <span className="text-gray-600">{job.department}</span>
                        <span className="text-gray-400">•</span>
                        <span className="text-gray-600">{job.location}</span>
                        <span className="text-gray-400">•</span>
                        <span className="text-orange-600 font-semibold">{job.type}</span>
                      </div>
                    </div>
                    <Link href={`/careers/apply?position=${encodeURIComponent(job.title)}`}>
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-xl shadow-lg"
                      >
                        Apply Now
                      </motion.button>
                    </Link>
                  </div>

                  <div className="grid md:grid-cols-2 gap-8">
                    <div>
                      <h4 className="text-xl font-bold text-gray-900 mb-4">Responsibilities</h4>
                      <ul className="space-y-3">
                        {job.responsibilities.map((item, i) => (
                          <li key={i} className="flex items-start space-x-3">
                            <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                            <span className="text-gray-700">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="text-xl font-bold text-gray-900 mb-4">Requirements</h4>
                      <ul className="space-y-3 mb-6">
                        {job.requirements.map((item, i) => (
                          <li key={i} className="flex items-start space-x-3">
                            <span className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2 flex-shrink-0"></span>
                            <span className="text-gray-700">{item}</span>
                          </li>
                        ))}
                      </ul>

                      <h4 className="text-xl font-bold text-gray-900 mb-4">Nice to Have</h4>
                      <ul className="space-y-3">
                        {job.niceToHave.map((item, i) => (
                          <li key={i} className="flex items-start space-x-3">
                            <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full mt-2 flex-shrink-0"></span>
                            <span className="text-gray-600">{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-100">
                    <h4 className="text-lg font-bold text-gray-900 mb-3">What You'll Gain</h4>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="flex items-center space-x-3">
                        <Award className="w-5 h-5 text-blue-600" />
                        <span className="text-gray-700">Certificate of Completion</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <TrendingUp className="w-5 h-5 text-purple-600" />
                        <span className="text-gray-700">Potential Full-Time Conversion</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Users className="w-5 h-5 text-emerald-600" />
                        <span className="text-gray-700">Expert Mentorship</span>
                      </div>
                      <div className="flex items-center space-x-3">
                        <Heart className="w-5 h-5 text-pink-600" />
                        <span className="text-gray-700">Real-World Experience</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </motion.div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-500 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Start Your Journey?
          </h2>
          <p className="text-xl text-blue-100 mb-10">
            Apply now and join our mission to revolutionize review management with AI.
          </p>
          <Link href="/careers/apply">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-10 py-4 bg-white text-blue-600 font-bold rounded-xl shadow-2xl"
            >
              Apply for an Internship
            </motion.button>
          </Link>
          <p className="mt-6 text-blue-100 text-sm">
            Fill out our online application form
          </p>
        </div>
      </section>
    </div>
  );
}
