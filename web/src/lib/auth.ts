export type Role = "employee" | "admin";
export type Session = { token: string; name: string; role: Role };

export const auth = {
  get(): Session | null {
    const raw = localStorage.getItem("auth");
    return raw ? (JSON.parse(raw) as Session) : null;
  },
  set(s: Session) {
    localStorage.setItem("auth", JSON.stringify(s));
  },
  clear() {
    localStorage.removeItem("auth");
  },
};

