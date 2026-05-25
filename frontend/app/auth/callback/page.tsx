'use client';

import { Suspense, useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';

function AuthCallbackInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error' | 'name_input'>('loading');
  const [message, setMessage] = useState('Authenticating with Google...');
  const [userName, setUserName] = useState('');
  const [authCode, setAuthCode] = useState('');

  useEffect(() => {
    const handleCallback = async () => {
      // Get access token from URL hash (for response_type=token)
      const hash = window.location.hash.substring(1);
      const params = new URLSearchParams(hash);
      const accessToken = params.get('access_token');
      const error = params.get('error') || searchParams.get('error');

      if (error) {
        setStatus('error');
        setMessage('Authentication cancelled or failed.');
        setTimeout(() => router.push('/login'), 3000);
        return;
      }

      if (!accessToken) {
        setStatus('error');
        setMessage('No access token received.');
        setTimeout(() => router.push('/login'), 3000);
        return;
      }

      try {
        setMessage('Loading your profile...');
        
        // Get user info from Google using the access token
        const userInfoResponse = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (!userInfoResponse.ok) {
          throw new Error('Failed to get user info');
        }

        const userInfo = await userInfoResponse.json();

        // Store Google user in database (if not already exists)
        const usersDB = localStorage.getItem('revuiq_users');
        const users = usersDB ? JSON.parse(usersDB) : [];
        
        let existingUser = users.find((u: any) => u.email === userInfo.email);
        
        if (!existingUser) {
          // Create new Google user account
          const newUser = {
            id: userInfo.id,
            name: userInfo.name || userInfo.email.split('@')[0],
            email: userInfo.email,
            picture: userInfo.picture,
            company: '',
            provider: 'google',
            googleId: userInfo.id,
            createdAt: new Date().toISOString()
          };
          users.push(newUser);
          localStorage.setItem('revuiq_users', JSON.stringify(users));
          existingUser = newUser;
        }

        // Store authentication data with real user info
        localStorage.setItem('isAuthenticated', 'true');
        localStorage.setItem('userData', JSON.stringify({
          name: existingUser.name,
          email: existingUser.email,
          picture: existingUser.picture,
          company: existingUser.company || '',
          provider: 'google'
        }));

        setStatus('success');
        setMessage(`Welcome ${existingUser.name}! Redirecting...`);
        
        setTimeout(() => {
          router.push('/dashboard');
        }, 1500);

      } catch (err) {
        console.error('Authentication error:', err);
        setStatus('error');
        setMessage('Authentication failed. Please try again.');
        setTimeout(() => router.push('/login'), 3000);
      }
    };

    handleCallback();
  }, [searchParams, router]);

  const handleNameSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!userName.trim()) return;

    // Store authentication data with user's name
    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('userData', JSON.stringify({
      name: userName,
      email: 'user@gmail.com', // In production, get from Google API
      company: '',
      provider: 'google',
      authCode: authCode
    }));

    setStatus('success');
    setMessage('Successfully signed in! Redirecting...');
    
    setTimeout(() => {
      router.push('/dashboard');
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="bg-white rounded-3xl shadow-2xl p-12 max-w-md w-full text-center"
      >
        {status === 'loading' && (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="inline-block mb-6"
            >
              <Loader2 className="w-16 h-16 text-blue-500" />
            </motion.div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Signing In</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}

        {status === 'success' && (
          <>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200 }}
              className="inline-block mb-6"
            >
              <CheckCircle className="w-16 h-16 text-green-500" />
            </motion.div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome!</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}

        {status === 'name_input' && (
          <>
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Welcome!</h2>
            <p className="text-gray-600 mb-6">Please enter your name to complete signup</p>
            <form onSubmit={handleNameSubmit} className="space-y-4">
              <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                placeholder="Enter your name"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                required
                autoFocus
              />
              <button
                type="submit"
                className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-xl hover:shadow-lg transition-all"
              >
                Continue
              </button>
            </form>
          </>
        )}

        {status === 'error' && (
          <>
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 200 }}
              className="inline-block mb-6"
            >
              <XCircle className="w-16 h-16 text-red-500" />
            </motion.div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Oops!</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}
      </motion.div>
    </div>
  );
}

export default function AuthCallbackPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-16 h-16 text-blue-500 animate-spin" />
      </div>
    }>
      <AuthCallbackInner />
    </Suspense>
  );
}
