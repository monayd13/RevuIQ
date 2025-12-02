'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle2, XCircle, AlertCircle, Info, X } from 'lucide-react';
import { useEffect, useState } from 'react';

export type NotificationType = 'success' | 'error' | 'warning' | 'info';

interface NotificationProps {
  type: NotificationType;
  message: string;
  duration?: number;
  onClose?: () => void;
}

const icons = {
  success: CheckCircle2,
  error: XCircle,
  warning: AlertCircle,
  info: Info,
};

const colors = {
  success: {
    bg: 'from-green-500 to-emerald-500',
    border: 'border-green-400',
    icon: 'text-green-100',
  },
  error: {
    bg: 'from-red-500 to-rose-500',
    border: 'border-red-400',
    icon: 'text-red-100',
  },
  warning: {
    bg: 'from-yellow-500 to-orange-500',
    border: 'border-yellow-400',
    icon: 'text-yellow-100',
  },
  info: {
    bg: 'from-blue-500 to-cyan-500',
    border: 'border-blue-400',
    icon: 'text-blue-100',
  },
};

export default function AnimatedNotification({
  type,
  message,
  duration = 5000,
  onClose,
}: NotificationProps) {
  const [isVisible, setIsVisible] = useState(true);
  const Icon = icons[type];
  const color = colors[type];

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(() => onClose?.(), 300);
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: -50, scale: 0.3 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, scale: 0.5, transition: { duration: 0.2 } }}
          className="fixed top-4 right-4 z-50"
        >
          <motion.div
            className={`relative bg-gradient-to-r ${color.bg} rounded-2xl shadow-2xl border-2 ${color.border} overflow-hidden`}
            whileHover={{ scale: 1.05 }}
          >
            {/* Animated Background */}
            <motion.div
              className="absolute inset-0 bg-white/10"
              animate={{
                x: ['-100%', '100%'],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'linear',
              }}
            />

            <div className="relative flex items-center space-x-4 p-4 pr-12">
              <motion.div
                animate={{
                  rotate: [0, 10, -10, 0],
                  scale: [1, 1.1, 1],
                }}
                transition={{
                  duration: 0.5,
                  repeat: 3,
                }}
              >
                <Icon className={`w-6 h-6 ${color.icon}`} />
              </motion.div>
              <p className="text-white font-semibold">{message}</p>
              <button
                onClick={() => {
                  setIsVisible(false);
                  setTimeout(() => onClose?.(), 300);
                }}
                className="absolute top-3 right-3 text-white/80 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Progress Bar */}
            <motion.div
              className="h-1 bg-white/30"
              initial={{ width: '100%' }}
              animate={{ width: '0%' }}
              transition={{ duration: duration / 1000, ease: 'linear' }}
            />
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// Notification Manager Hook
export function useNotification() {
  const [notifications, setNotifications] = useState<Array<{
    id: string;
    type: NotificationType;
    message: string;
  }>>([]);

  const addNotification = (type: NotificationType, message: string) => {
    const id = Math.random().toString(36).substr(2, 9);
    setNotifications((prev) => [...prev, { id, type, message }]);
  };

  const removeNotification = (id: string) => {
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  return {
    notifications,
    addNotification,
    removeNotification,
    success: (message: string) => addNotification('success', message),
    error: (message: string) => addNotification('error', message),
    warning: (message: string) => addNotification('warning', message),
    info: (message: string) => addNotification('info', message),
  };
}
