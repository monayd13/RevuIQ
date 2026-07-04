export function isAuthenticated(): boolean {
  if (typeof document === 'undefined') return false;
  return document.cookie.includes('isAuthenticated=true');
}

export function getUserDataFromCookie(): Record<string, unknown> | null {
  if (typeof document === 'undefined') return null;
  try {
    const match = document.cookie.match(/(?:^|;\s*)userData=([^;]*)/);
    return match ? JSON.parse(decodeURIComponent(match[1])) : null;
  } catch {
    return null;
  }
}

export async function loginWithCredentials(email: string, password: string) {
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Login failed');
  if (data.user) {
    document.cookie = `userData=${encodeURIComponent(JSON.stringify(data.user))}; path=/; max-age=86400; SameSite=Lax`;
  }
  return data;
}

export async function signupWithCredentials(payload: { email: string; password: string; full_name: string; business_name?: string }) {
  const res = await fetch('/api/auth/signup', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Signup failed');
  if (data.user) {
    document.cookie = `userData=${encodeURIComponent(JSON.stringify(data.user))}; path=/; max-age=86400; SameSite=Lax`;
  }
  return data;
}

export async function loginWithGoogle(email: string, name: string, googleId: string) {
  const res = await fetch('/api/auth/google', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, name, googleId }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Google login failed');
  if (data.user) {
    document.cookie = `userData=${encodeURIComponent(JSON.stringify(data.user))}; path=/; max-age=86400; SameSite=Lax`;
  }
  return data;
}

export async function logout() {
  await fetch('/api/auth/logout', { method: 'POST' });
  document.cookie = 'userData=; path=/; max-age=0';
}

export async function fetchCurrentUser() {
  try {
    const res = await fetch('/api/auth/me');
    if (!res.ok) return null;
    const data = await res.json();
    return data.user;
  } catch {
    return null;
  }
}
