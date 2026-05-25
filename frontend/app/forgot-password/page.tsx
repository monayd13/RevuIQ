'use client';

import { useState } from 'react';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  const handleReset = (event: React.FormEvent) => {
    event.preventDefault();
    const users = JSON.parse(localStorage.getItem('revuiq_users') || '[]');
    const user = users.find((item: { email?: string; provider?: string }) => item.email === email && item.provider === 'email');

    if (!user) {
      setMessage('No email/password account exists for that email. Google users should continue with Google.');
      return;
    }

    setMessage('Password reset is available in local account storage only for this deployment. Please create a new account or contact the site owner to reset stored credentials.');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 px-6 py-12">
      <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-2xl">
        <h1 className="mb-2 text-2xl font-bold text-gray-900">Reset Password</h1>
        <p className="mb-6 text-gray-600">Enter your account email to check reset options.</p>
        <form onSubmit={handleReset} className="space-y-4">
          <input
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-gray-900 outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="you@example.com"
            required
          />
          <button className="w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" type="submit">
            Check Reset Options
          </button>
        </form>
        {message && <p className="mt-4 rounded-lg bg-blue-50 p-3 text-sm text-blue-700">{message}</p>}
      </div>
    </div>
  );
}
