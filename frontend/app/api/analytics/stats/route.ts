import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function GET() {
  try {
    return await proxyBackendRequest('/api/analytics/stats');
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch stats' }, { status: 500 });
  }
}
