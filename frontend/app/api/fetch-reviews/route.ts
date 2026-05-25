import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const query = new URLSearchParams({
      business_name: body.business_name || body.restaurant_name || '',
      location: body.location || '',
      platform: body.platform || 'yelp',
    });

    return await proxyBackendRequest(`/api/fetch-reviews?${query.toString()}`, {
      method: 'POST',
    });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch reviews' }, { status: 500 });
  }
}
