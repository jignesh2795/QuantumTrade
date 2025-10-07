import axios from "axios";
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MarketDataPage = () => {
  const [symbols, setSymbols] = useState([
    "BTC-USD",
    "ETH-USD",
    "AAPL",
    "GOOGL",
  ]);
  const [selectedSymbol, setSelectedSymbol] = useState("BTC-USD");
  const [marketData, setMarketData] = useState([]);
  const [livePrice, setLivePrice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMarketData();
    const interval = setInterval(fetchLivePrice, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, [selectedSymbol]);

  const fetchMarketData = async () => {
    try {
      setLoading(true);
      const response = await axios.get(
        `/api/market/historical/${selectedSymbol}?days=30`
      );
      setMarketData(response.data.data || []);
    } catch (err) {
      setError("Failed to fetch market data");
      console.error("Error fetching market data:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchLivePrice = async () => {
    try {
      const response = await axios.get(`/api/market/price/${selectedSymbol}`);
      setLivePrice(response.data);
    } catch (err) {
      console.error("Error fetching live price:", err);
    }
  };

  const handleSymbolChange = (symbol) => {
    setSelectedSymbol(symbol);
  };

  // Prepare chart data
  const chartData = {
    labels: marketData.map((data) =>
      new Date(data.timestamp).toLocaleDateString()
    ),
    datasets: [
      {
        label: `${selectedSymbol} Price`,
        data: marketData.map((data) => data.close_price),
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        tension: 0.1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: `${selectedSymbol} Historical Price`,
      },
    },
  };

  return (
    <div className="market-data-page">
      <div className="page-header">
        <h1>Market Data</h1>
        <p>Real-time and historical market information</p>
      </div>

      <div className="market-controls">
        <div className="symbol-selector">
          <label>Symbol: </label>
          <select
            value={selectedSymbol}
            onChange={(e) => handleSymbolChange(e.target.value)}
          >
            {symbols.map((symbol) => (
              <option key={symbol} value={symbol}>
                {symbol}
              </option>
            ))}
          </select>
        </div>

        {livePrice && (
          <div className="live-price">
            <h3>Live Price: ${livePrice.price.toFixed(2)}</h3>
            <p>Updated: {new Date(livePrice.timestamp).toLocaleTimeString()}</p>
          </div>
        )}
      </div>

      {loading ? (
        <div>Loading market data...</div>
      ) : error ? (
        <div>Error: {error}</div>
      ) : (
        <div className="market-chart">
          <Line data={chartData} options={chartOptions} />
        </div>
      )}

      <div className="market-table">
        <h2>Recent Market Data</h2>
        {marketData.length === 0 ? (
          <p>No market data available</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Open</th>
                <th>High</th>
                <th>Low</th>
                <th>Close</th>
                <th>Volume</th>
              </tr>
            </thead>
            <tbody>
              {marketData
                .slice(-10)
                .reverse()
                .map((data) => (
                  <tr key={data.id}>
                    <td>{new Date(data.timestamp).toLocaleDateString()}</td>
                    <td>${data.open_price.toFixed(2)}</td>
                    <td>${data.high_price.toFixed(2)}</td>
                    <td>${data.low_price.toFixed(2)}</td>
                    <td>${data.close_price.toFixed(2)}</td>
                    <td>{data.volume.toLocaleString()}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default MarketDataPage;
