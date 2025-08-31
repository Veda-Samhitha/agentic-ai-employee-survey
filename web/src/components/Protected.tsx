import { Navigate } from "react-router-dom";
import { auth } from "../lib/auth";
import type { Role } from "../lib/auth";
import Layout from "./Layout";

export default function Protected({
  children,
  allow,
}: {
  children: React.ReactNode;
  allow?: Role[];
}) {
  const session = auth.get();
  if (!session) return <Navigate to="/login" replace />;
  if (allow && !allow.includes(session.role)) return <Navigate to="/login" replace />;
  return <Layout>{children}</Layout>;
}
