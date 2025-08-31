export default function AdminDashboard() {
  return (
    <div>
      <h2>HR Dashboard</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 12 }}>
        <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 8 }}>Participation %</div>
        <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 8 }}>Avg Sentiment</div>
        <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 8 }}>Attrition Risk</div>
      </div>
    </div>
  );
}
