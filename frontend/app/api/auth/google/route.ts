import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { getBackendApiUrl } from '@/lib/api';

export async function POST(request: Request) {
  try {
    const { email, name, googleId } = await request.json();
    const baseUrl = getBackendApiUrl();
    const password = `google_${googleId}`;

    let res = await fetch(`${baseUrl}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      res = await fetch(`${baseUrl}/api/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, full_name: name }),
      });
    }

    if (!res.ok) {
      return NextResponse.json({ detail: 'Google authentication failed.' }, { status: 401 });
    }

    const data = await res.json();
    const cookieStore = await cookies();
    cookieStore.set('auth_token', data.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 86400,
    });
    cookieStore.set('isAuthenticated', 'true', {
      httpOnly: false,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: 86400,
    });

    return NextResponse.json({ user: data.user });
  } catch {
    return NextResponse.json({ detail: 'Unable to connect to server.' }, { status: 502 });
  }
}
