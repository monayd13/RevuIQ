import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    return await proxyBackendRequest('/api/google/fetch-reviews', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch Google reviews' }, { status: 500 });
  }
}
