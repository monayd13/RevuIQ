import { proxyBackendRequest } from '@/lib/api';

export async function GET(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  const { searchParams } = new URL(request.url);
  const days = searchParams.get('days') || '30';
  return proxyBackendRequest(`/api/analytics/restaurant/${id}?days=${days}`);
}
