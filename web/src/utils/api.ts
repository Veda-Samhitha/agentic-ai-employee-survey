// web/src/utils/api.ts
const API = import.meta.env.VITE_API_URL; // <-- from .env.production

export async function api(path: string, init?: RequestInit) {
  const res = await fetch(`${API}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    ...init,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}
