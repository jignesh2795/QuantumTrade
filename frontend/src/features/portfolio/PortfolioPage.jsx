import { useEffect, useState } from 'react';
import { usePortfolio } from '../../hooks/usePortfolio.js';
import PortfolioCard from './PortfolioCard.jsx';

export default function PortfolioPage() {
  const { portfolio, loading, error, fetchPortfolio } = usePortfolio();
  
  useEffect(() => {
    fetchPortfolio();
  }, []);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Portfolio</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {portfolio.length > 0 ? (
          portfolio.map((asset) => (
            <PortfolioCard key={asset.asset} asset={asset} />
          ))
        ) : (
          <p>No assets in portfolio</p>
        )}
      </div>
    </div>
  );
}