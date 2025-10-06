import { useState } from "react";

function Portfolio() {
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPositions = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("Fetching positions from backend...");
      const response = await fetch("http://localhost:8000/portfolio/list");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Received response:", data);
      setPositions(data.positions || []);
    } catch (err) {
      console.error("Error fetching positions:", err);
      setError(err.message);
      setPositions([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Portfolio</h2>
      <button onClick={fetchPositions} disabled={loading}>
        {loading ? "Loading..." : "Load Positions"}
      </button>
      {error && (
        <div style={{ color: "red", marginTop: "1rem" }}>
          Error: {error}
        </div>
      )}
      <pre style={{ background: "#f5f5f5", padding: "1rem", marginTop: "1rem" }}>
        {JSON.stringify(positions, null, 2)}
      </pre>
    </div>
  );
}

export default Portfolio;