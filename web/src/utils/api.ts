// Simple, typed API client for the Employee Survey app (Vite + TS)
// Reads the API base from Vercel/Env: VITE_API_URL=https://employee-survey-api.onrender.com

export const API_BASE =
  (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, '') ??
  '';

type Json = Record<string, unknown> | Array<unknown> | null;

const TOKEN_KEY = 'auth_token';

export function setAuthToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}
export function getAuthToken() {
  return localStorage.getItem(TOKEN_KEY);
}
export function clearAuthToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request<T = unknown>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  if (!API_BASE) {
    throw new Error('VITE_API_URL is not set');
  }

  const headers = new Headers(init.headers || {});
  const token = getAuthToken();
  if (token) headers.set('Authorization', `Bearer ${token}`);
  if (!headers.has('Content-Type') && init.body) {
    headers.set('Content-Type', 'application/json');
  }
  headers.set('Accept', 'application/json');

  const res = await fetch(`${API_BASE}${path}`, { ...init, headers });

  // 204 No Content
  if (res.status === 204) return undefined as unknown as T;

  let data: Json;
  try {
    data = (await res.json()) as Json;
  } catch {
    // Fallback when server returns plain text or empty
    data = null;
  }

  if (!res.ok) {
    const detail =
      (data && typeof data === 'object' && 'detail' in data && (data as any).detail) ||
      `${res.status} ${res.statusText}`;
    throw new Error(String(detail));
  }

  return data as T;
}

/* ======================
   Public API functions
   ====================== */

export type LoginResponse = {
  token: string;
  name?: string;
  role?: string;
};

// 1) Login with demo/issued token carried in Authorization header
export async function loginWithToken(token: string) {
  setAuthToken(token);
  const out = await request<LoginResponse>('/auth/login', { method: 'POST' });
  if (out?.token) setAuthToken(out.token);
  return out;
}

// 2) Login with credentials (if your API supports it)
export async function loginWithCredentials(email: string, password: string) {
  const out = await request<LoginResponse>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  if (out?.token) setAuthToken(out.token);
  return out;
}

/* Surveys (admin) */
export type Survey = {
  id: number;
  title: string;
  description?: string;
  anonymous?: boolean;
};

export async function listSurveys() {
  return request<Survey[]>('/admin/surveys');
}

export async function createSurvey(input: {
  title: string;
  description?: string;
  anonymous?: boolean;
}) {
  return request<Survey>('/admin/surveys', {
    method: 'POST',
    body: JSON.stringify(input),
  });
}

/* Questions & Responses */
export type Question = {
  id: number;
  qtype: 'likert' | 'text' | 'mcq' | string | null;
  text: string;
};

export async function getQuestions(sid: number) {
  return request<Question[]>(`/surveys/${sid}/questions`);
}

export type AnswerIn = {
  question_id: number;
  value_text?: string | null;
  value_numeric?: number | null;
};

export async function submitResponses(sid: number, answers: AnswerIn[]) {
  return request<{ response_id: number; count: number }>(
    `/surveys/${sid}/responses`,
    {
      method: 'POST',
      body: JSON.stringify(answers),
    },
  );
}

/* Health */
export async function health() {
  return request<{ status: string }>('/health');
}
