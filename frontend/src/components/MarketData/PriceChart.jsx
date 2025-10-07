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
import { useEffect, useRef, useState } from "react";
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

const PriceChart = ({ symbol, initialData = [] }) => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: `${symbol || "Asset"} Price`,
        data: [],
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        tension: 0.1,
      },
    ],
  });

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const chartRef = useRef(null);

  // Initialize with provided data
  useEffect(() => {
    if (initialData && initialData.length > 0) {
      const labels = initialData.map((_, index) => `Point ${index + 1}`);
      const prices = initialData.map(
        (item) => item.close_price || item.price || 0
      );

      setChartData({
        labels: labels,
        datasets: [
          {
            label: `${symbol || "Asset"} Price`,
            data: prices,
            borderColor: "rgb(75, 192, 192)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            tension: 0.1,
          },
        ],
      });
    }
  }, [initialData, symbol]);

  // Simulate real-time data updates
  useEffect(() => {
    if (!symbol) return;

    const interval = setInterval(() => {
      // In a real app, this would fetch from an API
      // For demo purposes, we'll simulate price movements
      setChartData((prevData) => {
        const newData = [...prevData.datasets[0].data];
        const newLabels = [...prevData.labels];

        // Generate a new price point (simulate market movement)
        const lastPrice =
          newData.length > 0 ? newData[newData.length - 1] : 100;
        const change = (Math.random() - 0.5) * 2; // Random change between -1 and 1
        const newPrice = Math.max(0, lastPrice + change);

        // Add new data point
        newData.push(newPrice);
        newLabels.push(`T+${newData.length}`);

        // Keep only the last 50 data points for performance
        if (newData.length > 50) {
          newData.shift();
          newLabels.shift();
        }

        return {
          labels: newLabels,
          datasets: [
            {
              ...prevData.datasets[0],
              data: newData,
            },
          ],
        };
      });
    }, 2000); // Update every 2 seconds

    return () => clearInterval(interval);
  }, [symbol]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: `${symbol || "Asset"} Real-time Price Chart`,
      },
    },
    scales: {
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: "Price (USD)",
        },
      },
      x: {
        title: {
          display: true,
          text: "Time",
        },
      },
    },
    animation: {
      duration: 300,
    },
  };

  if (error) {
    return <div className="error-message">Error loading chart: {error}</div>;
  }

  return (
    <div className="price-chart-container">
      <div style={{ height: "400px" }}>
        <Line ref={chartRef} data={chartData} options={options} />
      </div>
    </div>
  );
};

export default PriceChart;
