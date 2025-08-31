import { useParams } from "react-router-dom";

export default function SurveyResults() {
  const { id } = useParams();
  return (
    <div>
      <h2>Survey Results</h2>
      <p>Summary for survey: {id}</p>
      <ul>
        <li>Participation: 78%</li>
        <li>Sentiment: 62% Positive / 28% Neutral / 10% Negative</li>
        <li>Attrition Risk: 18%</li>
      </ul>
      <p>(Later: link or embed Power BI here)</p>
    </div>
  );
}
