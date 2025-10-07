import { supabase } from "../supabaseClient";

/**
 * Supabase Service for QuantumTrade Platform
 * Handles all Supabase database operations
 */

// User authentication
export const authenticateUser = async (email, password) => {
  try {
    // In a real implementation, you would use Supabase Auth
    // This is a simplified version for local development
    const { data, error } = await supabase
      .from("users")
      .select("*")
      .eq("email", email)
      .single();

    if (error) throw error;
    return data;
  } catch (error) {
    console.error("Error authenticating user:", error);
    return null;
  }
};

// Trades operations
export const getTrades = async (userId, limit = 100) => {
  try {
    const { data, error } = await supabase
      .from("trades")
      .select("*")
      .eq("user_id", userId)
      .limit(limit)
      .order("timestamp", { ascending: false });

    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error("Error fetching trades:", error);
    return [];
  }
};

export const executeTrade = async (userId, asset, tradeType, amount, price) => {
  try {
    const { data, error } = await supabase
      .from("trades")
      .insert([
        {
          user_id: userId,
          asset,
          trade_type: tradeType,
          amount,
          price,
        },
      ])
      .select()
      .single();

    if (error) throw error;
    return data;
  } catch (error) {
    console.error("Error executing trade:", error);
    return null;
  }
};

// Portfolio operations
export const getPortfolio = async (userId) => {
  try {
    const { data, error } = await supabase
      .from("portfolio")
      .select("*")
      .eq("user_id", userId);

    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error("Error fetching portfolio:", error);
    return [];
  }
};

export const updatePortfolio = async (userId, asset, quantity, avgPrice) => {
  try {
    // First, try to update existing record
    const { data: updateData, error: updateError } = await supabase
      .from("portfolio")
      .update({
        quantity,
        avg_price: avgPrice,
      })
      .eq("user_id", userId)
      .eq("asset", asset)
      .select()
      .single();

    if (updateData) {
      return updateData;
    }

    // If no record was updated, create a new one
    const { data: insertData, error: insertError } = await supabase
      .from("portfolio")
      .insert([
        {
          user_id: userId,
          asset,
          quantity,
          avg_price: avgPrice,
        },
      ])
      .select()
      .single();

    if (insertError) throw insertError;
    return insertData;
  } catch (error) {
    console.error("Error updating portfolio:", error);
    return null;
  }
};

// Strategy operations
export const getStrategyConfigurations = async (userId) => {
  try {
    const { data, error } = await supabase
      .from("strategy_configurations")
      .select("*")
      .eq("user_id", userId);

    if (error) throw error;
    return data || [];
  } catch (error) {
    console.error("Error fetching strategy configurations:", error);
    return [];
  }
};

export const updateStrategyConfiguration = async (
  userId,
  strategyName,
  asset,
  isActive,
  config
) => {
  try {
    // First, try to update existing record
    const { data: updateData, error: updateError } = await supabase
      .from("strategy_configurations")
      .update({
        is_active: isActive,
        config,
      })
      .eq("user_id", userId)
      .eq("strategy_name", strategyName)
      .eq("asset", asset)
      .select()
      .single();

    if (updateData) {
      return updateData;
    }

    // If no record was updated, create a new one
    const { data: insertData, error: insertError } = await supabase
      .from("strategy_configurations")
      .insert([
        {
          user_id: userId,
          strategy_name: strategyName,
          asset,
          is_active: isActive,
          config,
        },
      ])
      .select()
      .single();

    if (insertError) throw insertError;
    return insertData;
  } catch (error) {
    console.error("Error updating strategy configuration:", error);
    return null;
  }
};

export const createStrategyExecution = async (
  userId,
  strategyName,
  asset,
  signal,
  confidence
) => {
  try {
    const { data, error } = await supabase
      .from("strategy_executions")
      .insert([
        {
          user_id: userId,
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
  } catch (error) {
    console.error("Error creating strategy execution:", error);
    return null;
  }
};

// Real-time subscriptions
export const subscribeToTrades = (userId, callback) => {
  return supabase
    .channel("trades")
    .on(
      "postgres_changes",
      {
        event: "INSERT",
        schema: "public",
        table: "trades",
        filter: `user_id=eq.${userId}`,
      },
      (payload) => {
        callback(payload.new);
      }
    )
    .subscribe();
};

export const subscribeToPortfolio = (userId, callback) => {
  return supabase
    .channel("portfolio")
    .on(
      "postgres_changes",
      {
        event: "INSERT",
        schema: "public",
        table: "portfolio",
        filter: `user_id=eq.${userId}`,
      },
      (payload) => {
        callback(payload.new);
      }
    )
    .on(
      "postgres_changes",
      {
        event: "UPDATE",
        schema: "public",
        table: "portfolio",
        filter: `user_id=eq.${userId}`,
      },
      (payload) => {
        callback(payload.new);
      }
    )
    .subscribe();
};
