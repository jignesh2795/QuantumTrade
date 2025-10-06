import { useState } from 'react';
import { useAuth } from '../hooks/useAuth.js';

export default function StrategyPage() {
  const { user } = useAuth();
  const [strategy, setStrategy] = useState('');
  
  if (!user) return <div>Please login to access strategies</div>;
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">AI Strategy</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="col-span-1 bg-white p-4 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Select Strategy</h2>
          
          <div className="space-y-2">
            <button 
              className={`w-full p-2 rounded ${strategy === 'momentum' ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}
              onClick={() => setStrategy('momentum')}
            >
              Momentum Trading
            </button>
            
            <button 
              className={`w-full p-2 rounded ${strategy === 'mean-reversion' ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}
              onClick={() => setStrategy('mean-reversion')}
            >
              Mean Reversion
            </button>
            
            <button 
              className={`w-full p-2 rounded ${strategy === 'arbitrage' ? 'bg-blue-500 text-white' : 'bg-gray-100'}`}
              onClick={() => setStrategy('arbitrage')}
            >
              Arbitrage
            </button>
          </div>
        </div>
        
        <div className="col-span-2 bg-white p-4 rounded-lg shadow">
          {strategy ? (
            <div>
              <h3 className="text-lg font-medium mb-2">{strategy} Strategy</h3>
              <p className="text-gray-600">Configure your {strategy} trading parameters</p>
              {/* Strategy configuration form would go here */}
            </div>
          ) : (
            <p>Select a strategy to configure</p>
          )}
        </div>
      </div>
    </div>
  );
}
