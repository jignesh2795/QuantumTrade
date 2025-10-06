import { useState } from "react";

function Risk() {
  const [risk, setRisk] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchRisk = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("Fetching risk assessment from backend...");
      const response = await fetch("http://localhost:8000/risk/assess?position_size=1500&account_balance=10000");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Received response:", data);
      setRisk(data);
    } catch (err) {
      console.error("Error fetching risk assessment:", err);
      setError(err.message);
      setRisk({ error: "Failed to fetch risk assessment" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Risk Assessment</h2>
      <button onClick={fetchRisk} disabled={loading}>
        {loading ? "Checking..." : "Check Risk"}
      </button>
      {error && (
        <div style={{ color: "red", marginTop: "1rem" }}>
          Error: {error}
        </div>
      )}
      {risk && (
        <pre style={{ background: "#f5f5f5", padding: "1rem", marginTop: "1rem" }}>
          {JSON.stringify(risk, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default Risk;