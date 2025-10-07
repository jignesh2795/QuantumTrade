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

const PerformanceMetrics = () => {
  const [pnlData, setPnlData] = useState(null);
  const [drawdownData, setDrawdownData] = useState(null);

  // Generate sample performance data
  useEffect(() => {
    // Generate P&L data (last 30 days)
    const generatePnlData = () => {
      const labels = [];
      const data = [];
      let cumulativePnl = 0;

      for (let i = 30; i >= 0; i--) {
        labels.push(`${30 - i}d`);
        const dailyPnl = (Math.random() - 0.5) * 1000; // Random P&L between -500 and 500
        cumulativePnl += dailyPnl;
        data.push(cumulativePnl);
      }

      return {
        labels,
        datasets: [
          {
            label: "Cumulative P&L",
            data,
            borderColor:
              cumulativePnl >= 0 ? "rgb(75, 192, 192)" : "rgb(255, 99, 132)",
            backgroundColor:
              cumulativePnl >= 0
                ? "rgba(75, 192, 192, 0.2)"
                : "rgba(255, 99, 132, 0.2)",
            tension: 0.1,
          },
        ],
      };
    };

    // Generate drawdown data
    const generateDrawdownData = () => {
      const labels = [];
      const data = [];

      for (let i = 30; i >= 0; i--) {
        labels.push(`${30 - i}d`);
        const drawdown = -(Math.random() * 5); // Random drawdown between 0% and -5%
        data.push(drawdown);
      }

      return {
        labels,
        datasets: [
          {
            label: "Drawdown %",
            data,
            borderColor: "rgb(255, 99, 132)",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            tension: 0.1,
          },
        ],
      };
    };

    setPnlData(generatePnlData());
    setDrawdownData(generateDrawdownData());
  }, []);

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  const drawdownOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: function (value) {
            return value + "%";
          },
        },
      },
    },
  };

  return (
    <div className="performance-metrics">
      <h2>Performance Analytics</h2>

      <div className="metrics-charts">
        <div className="chart-container">
          <h3>Portfolio P&L</h3>
          {pnlData ? (
            <Line data={pnlData} options={chartOptions} />
          ) : (
            <div className="chart-placeholder">Loading P&L data...</div>
          )}
        </div>

        <div className="chart-container">
          <h3>Drawdown</h3>
          {drawdownData ? (
            <Line data={drawdownData} options={drawdownOptions} />
          ) : (
            <div className="chart-placeholder">Loading drawdown data...</div>
          )}
        </div>
      </div>

      <div className="key-metrics">
        <div className="metric-card">
          <h4>Sharpe Ratio</h4>
          <p className="metric-value">1.45</p>
          <p className="metric-description">Risk-adjusted return</p>
        </div>

        <div className="metric-card">
          <h4>Max Drawdown</h4>
          <p className="metric-value negative">-3.2%</p>
          <p className="metric-description">Largest peak-to-trough decline</p>
        </div>

        <div className="metric-card">
          <h4>Win Rate</h4>
          <p className="metric-value positive">68%</p>
          <p className="metric-description">Percentage of profitable trades</p>
        </div>

        <div className="metric-card">
          <h4>Profit Factor</h4>
          <p className="metric-value">1.85</p>
          <p className="metric-description">Gross profits / Gross losses</p>
        </div>
      </div>
    </div>
  );
};

export default PerformanceMetrics;
