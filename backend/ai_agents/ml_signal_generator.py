"""
ML Signal Generator
Uses machine learning to generate trading signals
Phase 3: Simple XGBoost model
"""
from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
from backend.ai_agents.base_agent import BaseAgent, Signal
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

# Try to import ML libraries
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    logger.warning("⚠️  scikit-learn not available - ML features disabled")


class MLSignalGenerator(BaseAgent):
    """
    ML Signal Generator
    
    Uses machine learning to detect trading opportunities
    Phase 3: Random Forest classifier
    Phase 7: Deep learning models
    """
    
    def __init__(self):
        super().__init__(name="MLSignal", agent_type="ml_generator")
        
        self.model = None
        self.scaler = None
        self.is_trained = False
        self.feature_names = []
        
        if ML_AVAILABLE:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
            logger.info("✅ ML Signal Generator initialized with Random Forest")
        else:
            logger.warning("⚠️  ML libraries not available - using rule-based fallback")
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate ML-based trading signal
        
        Args:
            data: Market data with features
            
        Returns:
            Trading signal with confidence
        """
        self.update_timestamp()
        
        if not ML_AVAILABLE or not self.is_trained:
            # Fallback to rule-based
            return self._rule_based_signal(data)
        
        # Extract features
        features = self._extract_features(data)
        
        if features is None:
            return {
                "agent": self.name,
                "action": "hold",
                "confidence": 0.0,
                "reason": "Insufficient data for prediction"
            }
        
        # Make prediction
        X = self.scaler.transform([features])
        prediction = self.model.predict(X)[0]
        probabilities = self.model.predict_proba(X)[0]
        
        # Map prediction to action
        action_map = {0: "sell", 1: "hold", 2: "buy"}
        action = action_map[prediction]
        confidence = probabilities[prediction]
        
        logger.info(
            f"🤖 MLSignal: {action.upper()} | "
            f"Confidence: {confidence:.2%} | "
            f"Probs: {probabilities}"
        )
        
        return {
            "agent": self.name,
            "action": action,
            "confidence": confidence,
            "reason": f"ML prediction (Random Forest)",
            "probabilities": {
                "sell": probabilities[0],
                "hold": probabilities[1],
                "buy": probabilities[2]
            }
        }
    
    def _extract_features(self, data: Dict[str, Any]) -> Optional[List[float]]:
        """
        Extract features from market data
        
        Features:
        - Price momentum (returns over multiple periods)
        - Volatility
        - Volume
        - Technical indicators
        """
        candles = data.get('candles', [])
        
        if len(candles) < 20:
            return None
        
        closes = np.array([c.close for c in candles])
        volumes = np.array([c.volume for c in candles])
        
        features = []
        
        # Returns over different periods
        for period in [1, 5, 10, 20]:
            if len(closes) >= period:
                returns = (closes[-1] - closes[-period]) / closes[-period]
                features.append(returns)
        
        # Volatility
        if len(closes) >= 20:
            returns = np.diff(closes) / closes[:-1]
            volatility = np.std(returns[-20:])
            features.append(volatility)
        
        # Volume trend
        if len(volumes) >= 10:
            volume_ma = np.mean(volumes[-10:])
            volume_ratio = volumes[-1] / volume_ma if volume_ma > 0 else 1.0
            features.append(volume_ratio)
        
        # RSI-like indicator
        if len(closes) >= 14:
            gains = []
            losses = []
            for i in range(1, 14):
                change = closes[-i] - closes[-i-1]
                if change > 0:
                    gains.append(change)
                else:
                    losses.append(abs(change))
            
            avg_gain = np.mean(gains) if gains else 0.01
            avg_loss = np.mean(losses) if losses else 0.01
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            features.append(rsi / 100)  # Normalize to 0-1
        
        return features
    
    def _rule_based_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback rule-based signal"""
        candles = data.get('candles', [])
        
        if len(candles) < 20:
            return {
                "agent": self.name,
                "action": "hold",
                "confidence": 0.0,
                "reason": "Insufficient data"
            }
        
        closes = [c.close for c in candles]
        
        # Simple momentum
        short_ma = np.mean(closes[-5:])
        long_ma = np.mean(closes[-20:])
        
        if short_ma > long_ma * 1.01:
            action = "buy"
            confidence = 0.6
            reason = "Bullish momentum (rule-based)"
        elif short_ma < long_ma * 0.99:
            action = "sell"
            confidence = 0.6
            reason = "Bearish momentum (rule-based)"
        else:
            action = "hold"
            confidence = 0.5
            reason = "Neutral momentum (rule-based)"
        
        return {
            "agent": self.name,
            "action": action,
            "confidence": confidence,
            "reason": reason
        }
    
    def train(self, historical_data: pd.DataFrame):
        """
        Train the ML model on historical data
        
        Args:
            historical_data: DataFrame with features and labels
        """
        if not ML_AVAILABLE:
            logger.warning("Cannot train - ML libraries not available")
            return
        
        logger.info("🎓 Training ML Signal Generator...")
        
        X = historical_data[self.feature_names].values
        y = historical_data['label'].values  # 0=sell, 1=hold, 2=buy
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Get feature importance
        importances = self.model.feature_importances_
        for name, importance in zip(self.feature_names, importances):
            logger.info(f"  {name}: {importance:.3f}")
        
        logger.info("✅ ML model trained successfully")
    
    def get_status(self) -> Dict[str, Any]:
        """Get ML Signal Generator status"""
        return {
            "name": self.name,
            "type": self.agent_type,
            "active": self.is_active,
            "last_update": self.last_update.isoformat(),
            "ml_available": ML_AVAILABLE,
            "is_trained": self.is_trained,
            "model_type": "RandomForest" if ML_AVAILABLE else "RuleBased"
        }