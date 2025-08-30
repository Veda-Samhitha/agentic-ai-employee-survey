import { Link } from "react-router-dom";
import { surveys } from "../services/mock";

export default function EmployeeSurveys() {
  return (
    <div style={{ padding:24 }}>
      <h2>My Surveys</h2>
      <div style={{ display:"grid", gap:12 }}>
        {surveys.map(s => (
          <div key={s.id} style={{ border:"1px solid #ddd", padding:16, borderRadius:8 }}>
            <div style={{ display:"flex", justifyContent:"space-between" }}>
              <div>
                <div style={{ fontWeight:600 }}>{s.title}</div>
                <div style={{ fontSize:12, opacity:.7 }}>Due: {s.due}</div>
              </div>
              <div>{s.status}</div>
            </div>
            <div style={{ marginTop:8 }}>
              <Link to={`/employee/surveys/${s.id}/take`}>Take Survey</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
