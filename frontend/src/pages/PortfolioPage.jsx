import axios from "axios";
import { useEffect, useState } from "react";

const PortfolioPage = () => {
  const [positions, setPositions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPositions();
  }, []);

  const fetchPositions = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/api/portfolio/positions");
      setPositions(response.data.positions || []);
    } catch (err) {
      setError("Failed to fetch portfolio positions");
      console.error("Error fetching positions:", err);
    } finally {
      setLoading(false);
    }
  };

  const calculateTotalValue = () => {
    return positions.reduce((total, position) => {
      return total + position.size * position.current_price;
    }, 0);
  };

  const calculatePnL = () => {
    return positions.reduce((total, position) => {
      return (
        total + (position.current_price - position.avg_price) * position.size
      );
    }, 0);
  };

  if (loading) {
    return <div className="portfolio-page">Loading portfolio data...</div>;
  }

  if (error) {
    return <div className="portfolio-page">Error: {error}</div>;
  }

  return (
    <div className="portfolio-page">
      <div className="page-header">
        <h1>Portfolio</h1>
        <p>Manage your trading positions and track performance</p>
      </div>

      <div className="portfolio-summary">
        <div className="summary-card">
          <h3>Total Value</h3>
          <p className="value">${calculateTotalValue().toFixed(2)}</p>
        </div>
        <div className="summary-card">
          <h3>Profit/Loss</h3>
          <p
            className={`value ${calculatePnL() >= 0 ? "positive" : "negative"}`}
          >
            ${calculatePnL().toFixed(2)}
          </p>
        </div>
        <div className="summary-card">
          <h3>Positions</h3>
          <p className="value">{positions.length}</p>
        </div>
      </div>

      <div className="positions-table">
        <h2>Current Positions</h2>
        {positions.length === 0 ? (
          <p>No open positions</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Symbol</th>
                <th>Size</th>
                <th>Avg Price</th>
                <th>Current Price</th>
                <th>P&L</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {positions.map((position) => (
                <tr key={position.id}>
                  <td>{position.symbol}</td>
                  <td>{position.size}</td>
                  <td>${position.avg_price.toFixed(2)}</td>
                  <td>${position.current_price.toFixed(2)}</td>
                  <td
                    className={
                      (position.current_price - position.avg_price) *
                        position.size >=
                      0
                        ? "positive"
                        : "negative"
                    }
                  >
                    $
                    {(
                      (position.current_price - position.avg_price) *
                      position.size
                    ).toFixed(2)}
                  </td>
                  <td>
                    ${(position.size * position.current_price).toFixed(2)}
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

export default PortfolioPage;
