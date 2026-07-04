'use client';

import { Suspense, useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { motion } from 'framer-motion';
import { Loader2, CheckCircle, XCircle } from 'lucide-react';
import { loginWithGoogle } from '@/lib/auth';

function AuthCallbackInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('Authenticating with Google...');

  useEffect(() => {
    const handleCallback = async () => {
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

        const userInfoResponse = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
          headers: { Authorization: `Bearer ${accessToken}` },
        });

        if (!userInfoResponse.ok) throw new Error('Failed to get user info');
        const userInfo = await userInfoResponse.json();

        await loginWithGoogle(userInfo.email, userInfo.name || userInfo.email.split('@')[0], userInfo.id);

        setStatus('success');
        setMessage(`Welcome ${userInfo.name}! Redirecting...`);
        setTimeout(() => { window.location.href = '/dashboard'; }, 1000);
      } catch {
        setStatus('error');
        setMessage('Authentication failed. Please try again.');
        setTimeout(() => router.push('/login'), 3000);
      }
    };

    handleCallback();
  }, [searchParams, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="bg-white rounded-3xl shadow-2xl p-12 max-w-md w-full text-center">
        {status === 'loading' && (
          <>
            <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: 'linear' }} className="inline-block mb-6">
              <Loader2 className="w-16 h-16 text-blue-500" />
            </motion.div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Signing In</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}
        {status === 'success' && (
          <>
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 200 }} className="inline-block mb-6">
              <CheckCircle className="w-16 h-16 text-green-500" />
            </motion.div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome!</h2>
            <p className="text-gray-600">{message}</p>
          </>
        )}
        {status === 'error' && (
          <>
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: 'spring', stiffness: 200 }} className="inline-block mb-6">
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
    <Suspense fallback={<div className="min-h-screen flex items-center justify-center"><Loader2 className="w-16 h-16 text-blue-500 animate-spin" /></div>}>
      <AuthCallbackInner />
    </Suspense>
  );
}
