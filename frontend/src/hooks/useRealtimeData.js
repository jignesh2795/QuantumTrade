import { useEffect, useState } from "react";
import { supabase } from "../supabaseClient";

/**
 * Hook for handling realtime data updates
 */
export function useRealtimeData() {
  const [trades, setTrades] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch initial data
    fetchInitialData();

    // Set up realtime subscription
    const channel = supabase
      .channel("trades")
      .on(
        "postgres_changes",
        {
          event: "INSERT",
          schema: "public",
          table: "trades",
        },
        (payload) => {
          // Add new trade to the list
          setTrades((prevTrades) => [payload.new, ...prevTrades]);
        }
      )
      .subscribe();

    // Cleanup subscription on unmount
    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const fetchInitialData = async () => {
    try {
      setLoading(true);
      // In a real implementation, you would fetch from your backend API
      // For now, we'll use mock data
      const mockTrades = [
        { id: 1, symbol: "AAPL", pnl: 125.5 },
        { id: 2, symbol: "TSLA", pnl: -75.25 },
        { id: 3, symbol: "BTC", pnl: 340.75 },
      ];
      setTrades(mockTrades);
    } catch (error) {
      console.error("Error fetching initial data:", error);
    } finally {
      setLoading(false);
    }
  };

  return { trades, loading };
}
