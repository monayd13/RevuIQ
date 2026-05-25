import { proxyBackendRequest } from '@/lib/api';

export async function GET() {
  return proxyBackendRequest('/api/analytics/stats');
}
