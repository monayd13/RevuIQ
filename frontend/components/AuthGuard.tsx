'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

export default function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    // Check authentication status
    const checkAuth = () => {
      const authStatus = localStorage.getItem('isAuthenticated');
      const isAuth = authStatus === 'true';
      setIsAuthenticated(isAuth);

      // Public routes
      const publicRoutes = ['/login', '/signup', '/'];
      const isPublicRoute = publicRoutes.includes(pathname);

      // Redirect logic
      if (!isAuth && !isPublicRoute) {
        router.push(`/login?redirect=${pathname}`);
      } else if (isAuth && (pathname === '/login' || pathname === '/signup')) {
        router.push('/dashboard');
      }
    };

    checkAuth();
  }, [pathname, router]);

  // Show loading while checking auth
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <Loader2 className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600 font-medium">Loading...</p>
        </motion.div>
      </div>
    );
  }

  return <>{children}</>;
}
