'use client';

import { useState } from 'react';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleReset = (event: React.FormEvent) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 px-6 py-12">
      <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-2xl">
        <h1 className="mb-2 text-2xl font-bold text-gray-900">Reset Password</h1>
        <p className="mb-6 text-gray-600">Enter your account email and we&apos;ll help you reset your password.</p>
        {!submitted ? (
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
              Send Reset Link
            </button>
          </form>
        ) : (
          <div className="rounded-lg bg-blue-50 p-4 text-sm text-blue-700">
            If an account exists for <strong>{email}</strong>, a password reset link has been sent. Please check your inbox.
          </div>
        )}
        <p className="mt-4 text-center text-sm text-gray-500">
          <a href="/login" className="text-blue-600 hover:text-blue-700 font-medium">Back to login</a>
        </p>
      </div>
    </div>
  );
}
