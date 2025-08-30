import { useParams, Link } from "react-router-dom";
import { useState } from "react";

export default function TakeSurvey() {
  const { id } = useParams();
  const [rating, setRating] = useState(3);
  const [text, setText] = useState("");

  function submit() {
    alert("Submitted (mock). In real app this will POST to API and trigger agentic worker.");
    history.back();
  }

  return (
    <div style={{ padding:24, maxWidth:800, margin:"0 auto" }}>
      <h2>Employee Satisfaction Survey</h2>
      <p style={{ opacity:.7 }}>Survey ID: {id}</p>

      <div style={{ border:"1px solid #eee", padding:16, borderRadius:8, marginTop:12 }}>
        <p>Q1) Rate your work-life balance</p>
        <div style={{ display:"flex", gap:8 }}>
          {[1,2,3,4,5].map(n => (
            <button key={n}
              onClick={()=>setRating(n)}
              style={{ padding:"6px 10px", background:n===rating?"#e7f0ff":"#f6f6f6" }}>
              {n}
            </button>
          ))}
        </div>
      </div>

      <div style={{ border:"1px solid #eee", padding:16, borderRadius:8, marginTop:12 }}>
        <p>Q2) Any suggestions?</p>
        <textarea rows={4} value={text} onChange={e=>setText(e.target.value)} style={{ width:"100%" }} />
      </div>

      <div style={{ display:"flex", justifyContent:"space-between", marginTop:16 }}>
        <Link to="/employee/surveys">Previous</Link>
        <button onClick={submit}>Submit</button>
      </div>
    </div>
  );
}
