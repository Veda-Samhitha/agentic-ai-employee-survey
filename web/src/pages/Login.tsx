import { useState } from "react";
import { auth } from "../lib/auth";
import type { Role } from "../lib/auth";

export default function Login() {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState<Role>("employee");

  function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    auth.set({ token: "demo", name: email || "User", role });
    location.href = role === "employee" ? "/employee/surveys" : "/admin/dashboard";
  }

  return (
    <div style={{ display: "grid", placeItems: "center", height: "100vh" }}>
      <form onSubmit={onSubmit} style={{ width: 340 }}>
        <h2>Welcome Back</h2>
        <input
          placeholder="you@company.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ width: "100%", padding: 8, margin: "8px 0" }}
        />
        <select
          value={role}
          onChange={(e) => setRole(e.target.value as Role)}
          style={{ width: "100%", padding: 8, margin: "8px 0" }}
        >
          <option value="employee">Employee</option>
          <option value="admin">Admin (HR/Exec)</option>
        </select>
        <button style={{ width: "100%", padding: 10 }}>Login</button>
      </form>
    </div>
  );
}
