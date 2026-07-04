'use client';

import { LogOut } from 'lucide-react';
import { motion } from 'framer-motion';
import { logout } from '@/lib/auth';

export default function LogoutButton({ className = '' }: { className?: string }) {
  const handleLogout = async () => {
    await logout();
    window.location.href = '/login';
  };

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={handleLogout}
      className={`flex items-center space-x-2 px-4 py-2 bg-red-50 hover:bg-red-100 text-red-600 rounded-lg transition-colors ${className}`}
    >
      <LogOut className="w-4 h-4" />
      <span className="font-medium">Logout</span>
    </motion.button>
  );
}
