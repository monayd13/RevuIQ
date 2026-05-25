import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    return await proxyBackendRequest('/api/reviews/bulk', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add bulk reviews' }, { status: 500 });
  }
}
