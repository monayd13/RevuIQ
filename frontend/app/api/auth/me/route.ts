import { NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { getBackendApiUrl } from '@/lib/api';

export async function GET() {
  try {
    const cookieStore = await cookies();
    const token = cookieStore.get('auth_token')?.value;

    if (!token) {
      return NextResponse.json({ user: null }, { status: 401 });
    }

    const baseUrl = getBackendApiUrl();
    const res = await fetch(`${baseUrl}/api/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!res.ok) {
      return NextResponse.json({ user: null }, { status: 401 });
    }

    const data = await res.json();
    return NextResponse.json({ user: data });
  } catch {
    return NextResponse.json({ user: null }, { status: 502 });
  }
}
