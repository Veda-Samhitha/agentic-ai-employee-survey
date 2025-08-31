import { Link } from "react-router-dom";

const rows = [
  { id: "q2", title: "Q2 Employee Satisfaction" },
  { id: "wlb", title: "Work-Life Balance Assessment" },
  { id: "remote", title: "Remote Work Technology Feedback" },
];

export default function AdminSurveys() {
  return (
    <div>
      <h2>Surveys</h2>
      <p>
        <Link to="/admin/surveys/new">+ Create Survey</Link>
      </p>
      <ul>
        {rows.map((r) => (
          <li key={r.id}>
            {r.title} — <Link to={`/admin/surveys/${r.id}/results`}>Results</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
