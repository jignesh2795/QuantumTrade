import axios from "axios";
import { useEffect, useState } from "react";

const TradesPage = () => {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchTrades();
  }, [filter]);

  const fetchTrades = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/api/trades/history");
      let tradesData = response.data.trades || [];

      // Apply filter if needed
      if (filter !== "all") {
        tradesData = tradesData.filter(
          (trade) => trade.action === filter.toUpperCase()
        );
      }

      setTrades(tradesData);
    } catch (err) {
      setError("Failed to fetch trade history");
      console.error("Error fetching trades:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "filled":
        return "green";
      case "pending":
        return "orange";
      case "cancelled":
        return "red";
      default:
        return "black";
    }
  };

  if (loading) {
    return <div className="trades-page">Loading trade history...</div>;
  }

  if (error) {
    return <div className="trades-page">Error: {error}</div>;
  }

  return (
    <div className="trades-page">
      <div className="page-header">
        <h1>Trade History</h1>
        <p>View your trading activity and transaction history</p>
      </div>

      <div className="trades-controls">
        <div className="filter-buttons">
          <button
            className={filter === "all" ? "active" : ""}
            onClick={() => handleFilterChange("all")}
          >
            All Trades
          </button>
          <button
            className={filter === "buy" ? "active" : ""}
            onClick={() => handleFilterChange("buy")}
          >
            Buy Orders
          </button>
          <button
            className={filter === "sell" ? "active" : ""}
            onClick={() => handleFilterChange("sell")}
          >
            Sell Orders
          </button>
        </div>
      </div>

      <div className="trades-table">
        {trades.length === 0 ? (
          <p>No trades found</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Action</th>
                <th>Size</th>
                <th>Price</th>
                <th>Value</th>
                <th>Timestamp</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {trades.map((trade) => (
                <tr key={trade.id}>
                  <td>{trade.symbol}</td>
                  <td className={`action ${trade.action.toLowerCase()}`}>
                    {trade.action}
                  </td>
                  <td>{trade.size}</td>
                  <td>${trade.price.toFixed(2)}</td>
                  <td>${(trade.size * trade.price).toFixed(2)}</td>
                  <td>{new Date(trade.timestamp).toLocaleString()}</td>
                  <td style={{ color: getStatusColor(trade.status) }}>
                    {trade.status}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default TradesPage;
