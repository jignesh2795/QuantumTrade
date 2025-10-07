import axios from "axios";
import { useEffect, useState } from "react";

// Components
import PriceChart from "../MarketData/PriceChart";
import PortfolioSummary from "../Portfolio/PortfolioSummary";
import TradeHistory from "../Trading/TradeHistory";

const Dashboard = () => {
  const [portfolioData, setPortfolioData] = useState(null);
  const [marketData, setMarketData] = useState(null);
  const [tradeHistory, setTradeHistory] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState("BTC-USD");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch dashboard data
  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        // Fetch portfolio summary
        const portfolioRes = await axios.get("/api/portfolio/summary");
        setPortfolioData(portfolioRes.data);

        // Fetch market data
        const marketRes = await axios.get("/api/market/data", {
          params: { symbol: selectedSymbol, days: 30 },
        });
        setMarketData(marketRes.data);

        // Fetch recent trades
        const tradesRes = await axios.get("/api/trades/history", {
          params: { days: 7 },
        });
        setTradeHistory(tradesRes.data.trades);

        setIsLoading(false);
      } catch (err) {
        console.error("Error fetching dashboard data:", err);
        setError("Failed to load dashboard data");
        setIsLoading(false);
      }
    };

    fetchData();

    // Set up real-time updates
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, [selectedSymbol]);

  const handleSymbolChange = (e) => {
    setSelectedSymbol(e.target.value);
  };

  if (isLoading && !portfolioData) {
    return (
      <div className="dashboard loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Trading Dashboard</h1>
        <div className="dashboard-controls">
          <select value={selectedSymbol} onChange={handleSymbolChange}>
            <option value="BTC-USD">BTC/USD</option>
            <option value="ETH-USD">ETH/USD</option>
            <option value="AAPL">AAPL</option>
            <option value="GOOGL">GOOGL</option>
            <option value="TSLA">TSLA</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
          <button onClick={() => window.location.reload()}>Retry</button>
        </div>
      )}

      <div className="dashboard-grid">
        {/* Portfolio Summary */}
        <div className="dashboard-card portfolio-summary">
          <h2>Portfolio Overview</h2>
          <PortfolioSummary summary={portfolioData} />
        </div>

        {/* Market Data Chart */}
        <div className="dashboard-card market-chart">
          <h2>Market Data</h2>
          {marketData ? (
            <PriceChart symbol={selectedSymbol} initialData={marketData.data} />
          ) : (
            <div className="chart-placeholder">Loading chart...</div>
          )}
        </div>

        {/* Recent Trades */}
        <div className="dashboard-card trade-history">
          <h2>Recent Trades</h2>
          <TradeHistory trades={tradeHistory} />
        </div>

        {/* Performance Metrics */}
        <div className="dashboard-card performance-metrics">
          <h2>Performance Metrics</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <h3>Total Return</h3>
              <p className="metric-value positive">+12.5%</p>
            </div>
            <div className="metric-card">
              <h3>Sharpe Ratio</h3>
              <p className="metric-value">1.45</p>
            </div>
            <div className="metric-card">
              <h3>Max Drawdown</h3>
              <p className="metric-value negative">-3.2%</p>
            </div>
            <div className="metric-card">
              <h3>Win Rate</h3>
              <p className="metric-value positive">68%</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
