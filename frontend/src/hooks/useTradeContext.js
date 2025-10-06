import { createContext, useContext, useState } from 'react';
import { supabase } from '../services/supabaseClient.js';

export const TradeContext = createContext();

export function TradeProvider({ children }) {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const fetchTrades = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('trades')
        .select('*')
        .order('timestamp', { ascending: false });
      
      if (error) throw error;
      setTrades(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  const createTrade = async (tradeData) => {
    try {
      const { data, error } = await supabase
        .from('trades')
        .insert(tradeData)
        .select();
      
      if (error) throw error;
      setTrades([data[0], ...trades]);
      return data[0];
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };
  
  const value = {
    trades,
    loading,
    error,
    fetchTrades,
    createTrade
  };
  
  return (
    <TradeContext.Provider value={value}>
      {children}
    </TradeContext.Provider>
  );
}

export function useTrade() {
  return useContext(TradeContext);
}
