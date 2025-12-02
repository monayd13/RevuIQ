'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function RootPage() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    const isAuth = localStorage.getItem('isAuthenticated') === 'true';
    
    if (isAuth) {
      router.push('/dashboard');
    } else {
      router.push('/landing');
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
    </div>
  );
}
