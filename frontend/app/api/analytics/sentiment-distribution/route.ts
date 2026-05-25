import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const days = searchParams.get('days') || '30';
    
    return await proxyBackendRequest(`/api/analytics/sentiment-distribution?days=${days}`);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch sentiment distribution' }, { status: 500 });
  }
}
