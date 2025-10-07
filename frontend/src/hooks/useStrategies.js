import { useEffect, useState } from "react";
import { supabase } from "../services/supabaseClient.js";

export function useStrategies() {
  const [strategies, setStrategies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchStrategies = async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from("strategy_configurations")
        .select("*");

      if (error) throw error;
      setStrategies(data || []);
    } catch (err) {
      setError(err.message);
      setStrategies([]);
    } finally {
      setLoading(false);
    }
  };

  const updateStrategy = async (strategyName, asset, isActive, config) => {
    try {
      // First, try to update existing record
      const { data: updateData, error: updateError } = await supabase
        .from("strategy_configurations")
        .update({
          is_active: isActive,
          config,
        })
        .eq("strategy_name", strategyName)
        .eq("asset", asset)
        .select()
        .single();

      if (updateData) {
        // Update successful, refresh strategies
        fetchStrategies();
        return updateData;
      }

      // If no record was updated, create a new one
      const { data: insertData, error: insertError } = await supabase
        .from("strategy_configurations")
        .insert([
          {
            strategy_name: strategyName,
            asset,
            is_active: isActive,
            config,
          },
        ])
        .select()
        .single();

      if (insertError) throw insertError;

      // Refresh strategies
      fetchStrategies();
      return insertData;
    } catch (err) {
      setError(err.message);
      return null;
    }
  };

  const executeStrategy = async (strategyName, asset, signal, confidence) => {
    try {
      const { data, error } = await supabase
        .from("strategy_executions")
        .insert([
          {
            strategy_name: strategyName,
            asset,
            signal,
            confidence,
          },
        ])
        .select()
        .single();

      if (error) throw error;

      return data;
    } catch (err) {
      setError(err.message);
      return null;
    }
  };

  // Subscribe to real-time updates
  useEffect(() => {
    const subscription = supabase
      .channel("strategies")
      .on(
        "postgres_changes",
        {
          event: "INSERT",
          schema: "public",
          table: "strategy_configurations",
        },
        (payload) => {
          fetchStrategies();
        }
      )
      .on(
        "postgres_changes",
        {
          event: "UPDATE",
          schema: "public",
          table: "strategy_configurations",
        },
        (payload) => {
          fetchStrategies();
        }
      )
      .subscribe();

    return () => {
      subscription.unsubscribe();
    };
  }, []);

  return {
    strategies,
    loading,
    error,
    fetchStrategies,
    updateStrategy,
    executeStrategy,
  };
}
