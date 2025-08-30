import { Link, useLocation } from "react-router-dom";
import { auth } from "../lib/auth";

export default function Nav(){
  const me = auth.get(); const { pathname } = useLocation();
  if (!me) return null;
  const logout = () => { auth.clear(); location.href="/login"; };
  return (
    <div style={{display:"flex",gap:12,justifyContent:"space-between",padding:"10px 16px",borderBottom:"1px solid #eee"}}>
      <div style={{display:"flex",gap:12}}>
        {me.role==="employee" && <Link to="/employee/surveys">My Surveys</Link>}
        {me.role==="admin" && (
          <>
            <Link to="/admin/dashboard">Dashboard</Link>
            <Link to="/admin/surveys">Surveys</Link>
            <Link to="/admin/analytics">Analytics</Link>
          </>
        )}
        <span style={{opacity:.6}}>{pathname}</span>
      </div>
      <div>Hi, {me.name} <button onClick={logout}>Logout</button></div>
    </div>
  );
}
