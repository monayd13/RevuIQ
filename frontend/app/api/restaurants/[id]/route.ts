import { NextResponse } from 'next/server';
import { proxyBackendRequest } from '@/lib/api';

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;
    return await proxyBackendRequest(`/api/restaurants/${id}`, {
      method: 'DELETE',
    });
  } catch (error) {
    return NextResponse.json({ error: 'Failed to delete restaurant' }, { status: 500 });
  }
}
