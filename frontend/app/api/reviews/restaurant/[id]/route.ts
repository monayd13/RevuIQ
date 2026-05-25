import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    return await proxyBackendRequest(`/api/reviews/restaurant/${id}`);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch reviews' }, { status: 500 });
  }
}
