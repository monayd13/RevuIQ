import { proxyBackendRequest } from '@/lib/api';

export async function POST(request: Request) {
  const body = await request.json();
  return proxyBackendRequest('/api/reviews/bulk', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}
