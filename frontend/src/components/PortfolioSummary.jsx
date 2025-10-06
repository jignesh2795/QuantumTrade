import React, { useState, useEffect } from 'react';
import api from '../services/api';

const PortfolioSummary = () => {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPortfolio = async () => {
      try {
        const response = await api.get('/portfolio');
        setPortfolio(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchPortfolio();
  }, []);

  if (loading) return <div>Loading portfolio...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!portfolio) return <div>No portfolio data</div>;

  return (
    <div>
      <h2>Portfolio Summary</h2>
      <p>Total Value: ${portfolio.total_value.toLocaleString()}</p>
      <ul>
        {portfolio.assets.map((asset) => (
          <li key={asset.symbol}>
            {asset.symbol}: {asset.quantity} shares @ ${asset.price} = ${asset.value.toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PortfolioSummary;