import { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth.js';
import { useTrades } from '../hooks/useTrades.js';
import { usePortfolio } from '../hooks/usePortfolio.js';

export default function AnalyticsPage() {
  const { user } = useAuth();
  const { trades } = useTrades();
  const { portfolio } = usePortfolio();
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    if (user && trades && portfolio) {
      setLoading(false);
    }
  }, [user, trades, portfolio]);
  
  if (!user) return <div>Please login to view analytics</div>;
  if (loading) return <div>Loading analytics...</div>;
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Analytics Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Performance Metrics</h2>
          <div className="space-y-4">
            <div>
              <h3 className="font-medium">Total Portfolio Value</h3>
              <p className="text-2xl font-bold">
                ${portfolio.reduce((sum, asset) => sum + (asset.quantity * asset.avg_price), 0).toFixed(2)}
              </p>
            </div>
            
            <div>
              <h3 className="font-medium">Total Trades</h3>
              <p className="text-2xl font-bold">{trades.length}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Asset Allocation</h2>
          {/* Chart would be rendered here */}
          <div className="h-64 bg-gray-100 flex items-center justify-center">
            <p>Asset allocation chart will appear here</p>
          </div>
        </div>
      </div>
    </div>
  );
}
