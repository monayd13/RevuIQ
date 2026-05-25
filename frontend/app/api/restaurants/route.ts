import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function GET() {
  try {
    return await proxyBackendRequest('/api/restaurants');
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch restaurants' }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    return await proxyBackendRequest('/api/restaurants', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add restaurant' }, { status: 500 });
  }
}
