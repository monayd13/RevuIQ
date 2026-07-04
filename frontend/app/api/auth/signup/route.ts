import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { getBackendApiUrl } from '@/lib/api';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const baseUrl = getBackendApiUrl();

    const res = await fetch(`${baseUrl}/api/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await res.json();
    if (!res.ok) {
      return NextResponse.json(data, { status: res.status });
    }

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
