import { NextResponse } from 'next/server';
import { headers } from 'next/headers';

export function getBackendApiUrl() {
  return process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
}

export function missingBackendResponse() {
  return NextResponse.json(
    { error: 'Backend API URL is not configured' },
    { status: 503 }
  );
}

export async function proxyBackendRequest(path: string, init?: RequestInit) {
  const baseUrl = getBackendApiUrl();

  if (process.env.NODE_ENV === 'production' && baseUrl.includes('localhost')) {
    return missingBackendResponse();
  }

  // Forward Authorization header from the incoming request
  const incomingHeaders = await headers();
  const authorization = incomingHeaders.get('authorization');

  const mergedHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(init?.headers as Record<string, string> || {}),
  };
  if (authorization) {
    mergedHeaders['Authorization'] = authorization;
  }

  const response = await fetch(`${baseUrl}${path}`, { ...init, headers: mergedHeaders });
  const contentType = response.headers.get('content-type');
  const data = contentType?.includes('application/json') ? await response.json() : await response.text();

  return NextResponse.json(data, { status: response.status });
}
