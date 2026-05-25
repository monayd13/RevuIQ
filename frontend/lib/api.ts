import { NextResponse } from 'next/server';

export function getBackendApiUrl() {
  return process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
}

export function missingBackendResponse() {
  return NextResponse.json(
    {
      error: 'Backend API URL is not configured',
      message: 'Set BACKEND_API_URL or NEXT_PUBLIC_API_URL to your deployed backend URL.',
    },
    { status: 503 }
  );
}

export async function proxyBackendRequest(path: string, init?: RequestInit) {
  const baseUrl = getBackendApiUrl();

  if (process.env.NODE_ENV === 'production' && baseUrl.includes('localhost')) {
    return missingBackendResponse();
  }

  const response = await fetch(`${baseUrl}${path}`, init);
  const contentType = response.headers.get('content-type');
  const data = contentType?.includes('application/json') ? await response.json() : await response.text();

  return NextResponse.json(data, { status: response.status });
}
