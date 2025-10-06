import { useEffect, useState } from 'react';
import { useTrades } from '../../hooks/useTrades.js';
import TradeCard from './TradeCard.jsx';

export default function MarketPage() {
  const { trades, loading, error, fetchTrades } = useTrades();
  
  useEffect(() => {
    fetchTrades();
  }, []);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Market</h1>
      
      <div>
        <h2 className="text-xl font-semibold mb-4">Market Trades</h2>
        <div className="space-y-4">
          {trades.length > 0 ? (
            trades.map((trade) => (
              <TradeCard key={trade.id} trade={trade} />
            ))
          ) : (
            <p>No trades yet</p>
          )}
        </div>
      </div>
    </div>
  );
}