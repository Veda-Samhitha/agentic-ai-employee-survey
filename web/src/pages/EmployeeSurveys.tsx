import { Link } from "react-router-dom";

const rows = [
  { id: "q2", title: "Q2 Employee Satisfaction", due: "Jun 15, 2025", status: "Pending" },
  { id: "wlb", title: "Work-Life Balance Assessment", due: "May 30, 2025", status: "Completed" },
  { id: "remote", title: "Remote Work Technology Feedback", due: "Jun 24, 2025", status: "Pending" },
];

export default function EmployeeSurveys() {
  return (
    <div>
      <h2>My Surveys</h2>
      <div style={{ display: "grid", gap: 12 }}>
        {rows.map((s) => (
          <div key={s.id} style={{ border: "1px solid #ddd", padding: 16, borderRadius: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <div style={{ fontWeight: 600 }}>{s.title}</div>
                <div style={{ fontSize: 12, opacity: 0.7 }}>Due: {s.due}</div>
              </div>
              <div>{s.status}</div>
            </div>
            <div style={{ marginTop: 8 }}>
              <Link to={`/employee/surveys/${s.id}/take`}>Take Survey</Link>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
