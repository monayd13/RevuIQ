'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Loader2 } from 'lucide-react';

export default function GoogleCallbackPage() {
  const router = useRouter();

  useEffect(() => {
    const hash = window.location.hash || '';
    const search = window.location.search || '';
    router.replace(`/auth/callback${search}${hash}`);
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 flex items-center justify-center">
      <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
    </div>
  );
}
