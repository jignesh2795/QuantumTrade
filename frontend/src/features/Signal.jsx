import { useState } from "react";

function Signal() {
  const [signal, setSignal] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSignal = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("Fetching signal from backend...");
      const response = await fetch("http://localhost:8000/strategy/signal?symbol=BTC-USD");
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Received response:", data);
      setSignal(data);
    } catch (err) {
      console.error("Error fetching signal:", err);
      setError(err.message);
      setSignal({ error: "Failed to fetch signal" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Trading Signal</h2>
      <button onClick={fetchSignal} disabled={loading}>
        {loading ? "Fetching..." : "Get Signal"}
      </button>
      {error && (
        <div style={{ color: "red", marginTop: "1rem" }}>
          Error: {error}
        </div>
      )}
      {signal && (
        <pre style={{ marginTop: "1rem", background: "#f5f5f5", padding: "1rem" }}>
          {JSON.stringify(signal, null, 2)}
        </pre>
      )}
    </div>
  );
}

export default Signal;