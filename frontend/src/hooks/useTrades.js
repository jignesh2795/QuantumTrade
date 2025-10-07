import { useEffect, useState } from "react";
import { supabase } from "../services/supabaseClient.js";

export function useTrades() {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchTrades = async (limit = 100) => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from("trades")
        .select("*")
        .limit(limit)
        .order("timestamp", { ascending: false });

      if (error) throw error;
      setTrades(data || []);
    } catch (err) {
      setError(err.message);
      setTrades([]);
    } finally {
      setLoading(false);
    }
  };

  const executeTrade = async (asset, tradeType, amount, price) => {
    try {
      const { data, error } = await supabase
        .from("trades")
        .insert([
          {
            asset,
            trade_type: tradeType,
            amount,
            price,
          },
        ])
        .select()
        .single();

      if (error) throw error;

      // Refresh trades
      fetchTrades();
      return data;
    } catch (err) {
      setError(err.message);
      return null;
    }
  };

  // Subscribe to real-time updates
  useEffect(() => {
    const subscription = supabase
      .channel("trades")
      .on(
        "postgres_changes",
        {
          event: "INSERT",
          schema: "public",
          table: "trades",
        },
        (payload) => {
          fetchTrades();
        }
      )
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return {
    trades,
    loading,
    error,
    fetchTrades,
    executeTrade,
  };
}
