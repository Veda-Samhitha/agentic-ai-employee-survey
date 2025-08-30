import { Link } from "react-router-dom";
import { surveys } from "../services/mock";

export default function AdminSurveys() {
  return (
    <div style={{ padding:24 }}>
      <h2>Surveys</h2>
      <Link to="/admin/surveys/new">+ Create Survey</Link>
      <ul>
        {surveys.map(s => (
          <li key={s.id}>
            {s.title} — <Link to={`/admin/surveys/${s.id}/results`}>Results</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
