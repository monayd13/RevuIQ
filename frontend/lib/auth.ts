const TOKEN_KEY = 'auth_token';
const USER_KEY = 'userData';

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function getUserData(): Record<string, unknown> | null {
  if (typeof window === 'undefined') return null;
  try {
    const data = localStorage.getItem(USER_KEY);
    return data ? JSON.parse(data) : null;
  } catch {
    return null;
  }
}

export function setAuth(token: string, user: Record<string, unknown>) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  localStorage.setItem('isAuthenticated', 'true');
  // Cookie for middleware (non-httpOnly since set client-side)
  document.cookie = `auth_token=${token}; path=/; max-age=86400; SameSite=Lax`;
  document.cookie = `isAuthenticated=true; path=/; max-age=86400; SameSite=Lax`;
}

export function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem('isAuthenticated');
  document.cookie = 'auth_token=; path=/; max-age=0';
  document.cookie = 'isAuthenticated=; path=/; max-age=0';
}

export function isAuthenticated(): boolean {
  return !!getToken();
}

export function getAuthHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
