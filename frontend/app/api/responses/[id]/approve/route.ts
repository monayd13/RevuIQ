import { proxyBackendRequest } from '@/lib/api';

export async function POST(
  request: Request,
  context: { params: Promise<{ id: string }> }
) {
  const { id } = await context.params;
  const body = await request.text();
  return proxyBackendRequest(`/api/responses/${id}/approve`, {
    method: 'POST',
    body,
  });
}
