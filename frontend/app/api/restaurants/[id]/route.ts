import { proxyBackendRequest } from '@/lib/api';

export async function DELETE(
  request: Request,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  return proxyBackendRequest(`/api/restaurants/${id}`, {
    method: 'DELETE',
  });
}
