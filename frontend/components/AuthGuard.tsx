'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';
import { isAuthenticated } from '@/lib/auth';

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    const publicRoutes = ['/login', '/signup', '/', '/landing', '/auth/callback', '/auth/google/callback', '/terms', '/privacy', '/forgot-password', '/about', '/pricing', '/careers', '/careers/apply'];
    const isPublicRoute = publicRoutes.includes(pathname) || pathname.startsWith('/landing');
    const authed = isAuthenticated();

    if (!authed && !isPublicRoute) {
      router.push(`/login?redirect=${pathname}`);
    } else if (authed && (pathname === '/login' || pathname === '/signup')) {
      router.push('/dashboard');
    }
    setChecked(true);
  }, [pathname, router]);

  if (!checked) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center">
          <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600 font-medium">Loading...</p>
        </motion.div>
      </div>
    );
  }

  return <>{children}</>;
}
