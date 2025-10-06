import { useEffect, useState } from 'react';
import { useTrades } from '../hooks/useTrades.js';
import TradeCard from '../components/TradeCard.jsx';

export default function DashboardPage() {
  const { trades, loading, error, fetchTrades } = useTrades();
  const [newTrade, setNewTrade] = useState({
    asset: '',
    trade_type: 'BUY',
    amount: 0,
    price: 0
  });
  
  useEffect(() => {
    fetchTrades();
  }, []);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    // TODO: Implement trade creation
  };
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-4">Create New Trade</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block mb-1">Asset</label>
              <input
                type="text"
                value={newTrade.asset}
                onChange={(e) => setNewTrade({...newTrade, asset: e.target.value})}
                className="w-full p-2 border rounded"
                required
              />
            </div>
            
            <div>
              <label className="block mb-1">Trade Type</label>
              <select
                value={newTrade.trade_type}
                onChange={(e) => setNewTrade({...newTrade, trade_type: e.target.value})}
                className="w-full p-2 border rounded"
              >
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
              </select>
            </div>
            
            <div>
              <label className="block mb-1">Amount</label>
              <input
                type="number"
                value={newTrade.amount}
                onChange={(e) => setNewTrade({...newTrade, amount: parseFloat(e.target.value)})}
                className="w-full p-2 border rounded"
                min="0.01"
                step="0.01"
                required
              />
            </div>
            
            <div>
              <label className="block mb-1">Price</label>
              <input
                type="number"
                value={newTrade.price}
                onChange={(e) => setNewTrade({...newTrade, price: parseFloat(e.target.value)})}
                className="w-full p-2 border rounded"
                min="0.01"
                step="0.01"
                required
              />
            </div>
            
            <button
              type="submit"
              className="bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Submit Trade
            </button>
          </form>
        </div>
        
        <div>
          <h2 className="text-xl font-semibold mb-4">Recent Trades</h2>
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
    </div>
  );
}
