import { useContext, useState } from 'react';
import { supabase } from '../services/supabaseClient.js';

export function usePortfolio() {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const fetchPortfolio = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('portfolio')
        .select('*');
      
      if (error) throw error;
      setPortfolio(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return {
    portfolio,
    loading,
    error,
    fetchPortfolio
  };
}
