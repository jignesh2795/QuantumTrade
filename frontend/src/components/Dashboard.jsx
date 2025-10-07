import { useEffect, useState } from "react";

export default function Dashboard() {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrades();
  }, []);

  const fetchTrades = async () => {
    try {
      setLoading(true);
      // In a real implementation, you would fetch from your backend API
      // For now, we'll use mock data
      const mockTrades = [
        { id: 1, symbol: "AAPL", pnl: 125.5 },
        { id: 2, symbol: "TSLA", pnl: -75.25 },
        { id: 3, symbol: "BTC", pnl: 340.75 },
      ];
      setTrades(mockTrades);
    } catch (error) {
      console.error("Error fetching trades:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="p-4">Loading dashboard...</div>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Live Trading Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {trades.map((trade) => (
          <div key={trade.id} className="bg-white p-4 rounded-lg shadow">
            <h2 className="text-lg font-semibold">{trade.symbol}</h2>
            <p
              className={`text-lg ${
                trade.pnl >= 0 ? "text-green-600" : "text-red-600"
              }`}
            >
              ${trade.pnl.toFixed(2)}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
