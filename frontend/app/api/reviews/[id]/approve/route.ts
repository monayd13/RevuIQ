import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function POST(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    const body = await request.json();
    return await proxyBackendRequest(`/api/reviews/${id}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
  } catch (error) {
    return NextResponse.json({ success: false, error: 'Failed to approve review' }, { status: 500 });
  }
}
