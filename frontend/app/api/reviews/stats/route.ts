import { proxyBackendRequest } from '@/lib/api';

export async function GET() {
  return proxyBackendRequest('/api/reviews/stats');
}
