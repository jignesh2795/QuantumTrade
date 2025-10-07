import { useEffect, useState } from "react";
import { supabase } from "../services/supabaseClient.js";

export function usePortfolio() {
  const [portfolio, setPortfolio] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPortfolio = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase.from("portfolio").select("*");

      if (error) throw error;
      setPortfolio(data || []);
    } catch (err) {
      setError(err.message);
      setPortfolio([]);
    } finally {
      setLoading(false);
    }
  };

  const updatePortfolio = async (asset, quantity, avgPrice) => {
    try {
      // First, try to update existing record
      const { data: updateData, error: updateError } = await supabase
        .from("portfolio")
        .update({
          quantity,
          avg_price: avgPrice,
        })
        .eq("asset", asset)
        .select()
        .single();

      if (updateData) {
        // Update successful, refresh portfolio
        fetchPortfolio();
        return updateData;
      }

      // If no record was updated, create a new one
      const { data: insertData, error: insertError } = await supabase
        .from("portfolio")
        .insert([
          {
            asset,
            quantity,
            avg_price: avgPrice,
          },
        ])
        .select()
        .single();

      if (insertError) throw insertError;

      // Refresh portfolio
      fetchPortfolio();
      return insertData;
    } catch (err) {
      setError(err.message);
      return null;
    }
  };

  // Subscribe to real-time updates
  useEffect(() => {
    const subscription = supabase
      .channel("portfolio")
      .on(
        "postgres_changes",
        {
          event: "INSERT",
          schema: "public",
          table: "portfolio",
        },
        (payload) => {
          fetchPortfolio();
        }
      )
      .on(
        "postgres_changes",
        {
          event: "UPDATE",
          schema: "public",
          table: "portfolio",
        },
        (payload) => {
          fetchPortfolio();
        }
      )
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return {
    portfolio,
    loading,
    error,
    fetchPortfolio,
    updatePortfolio,
  };
}
