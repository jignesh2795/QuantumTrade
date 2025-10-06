import { createContext, useContext, useState } from 'react';
import { supabase } from '../services/supabaseClient.js';

export const AIContext = createContext();

export function AIProvider({ children }) {
  const [strategies, setStrategies] = useState([]);
  const [selectedStrategy, setSelectedStrategy] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const fetchStrategies = async () => {
    setLoading(true);
    try {
      // In a real app, this would fetch from your backend
      const mockStrategies = [
        { id: 1, name: 'momentum', description: 'Momentum trading strategy' },
        { id: 2, name: 'mean-reversion', description: 'Mean reversion strategy' },
        { id: 3, name: 'arbitrage', description: 'Arbitrage strategy' }
      ];
      setStrategies(mockStrategies);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const selectStrategy = (strategy) => {
    setSelectedStrategy(strategy);
  };
  
  const value = {
    strategies,
    selectedStrategy,
    loading,
    error,
    fetchStrategies,
    selectStrategy
  };
  
  return (
    <AIContext.Provider value={value}>
      {children}
    </AIContext.Provider>
  );
}

export function useAI() {
  return useContext(AIContext);
}
