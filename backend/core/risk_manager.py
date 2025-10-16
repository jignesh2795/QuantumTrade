"""
Risk Management System - Guard Agent (Basic Version)
"""
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class RiskManager:
    """
    Guard Agent - Protects capital and enforces risk limits
    
    Features:
    - Position sizing
    - Daily loss limits
    - Stop-loss enforcement
    - Max drawdown protection
    """
    
    def __init__(
        self,
        initial_capital: float,
        max_position_size: float = 0.1,
        max_daily_loss: float = 0.02,
        max_drawdown: float = 0.10,
        stop_loss_pct: float = 0.02,
        take_profit_pct: float = 0.04
    ):
        self.initial_capital = initial_capital
        self.max_position_size = max_position_size
        self.max_daily_loss = max_daily_loss
        self.max_drawdown = max_drawdown
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        
        # Tracking
        self.daily_start_capital = initial_capital
        self.daily_pnl = 0.0
        self.peak_capital = initial_capital
        self.current_drawdown = 0.0
        self.last_reset = datetime.utcnow()
        self.circuit_breaker_triggered = False
        
        logger.info(
            f"🛡️  Risk Manager initialized | "
            f"Max Position: {max_position_size*100:.1f}%, "
            f"Max Daily Loss: {max_daily_loss*100:.1f}%, "
            f"Stop Loss: {stop_loss_pct*100:.1f}%"
        )
    
    def reset_daily_metrics(self, current_capital: float):
        """Reset daily metrics at start of new trading day"""
        now = datetime.utcnow()
        if (now - self.last_reset).days >= 1:
            self.daily_start_capital = current_capital
            self.daily_pnl = 0.0
            self.last_reset = now
            self.circuit_breaker_triggered = False
            logger.info(f"📅 Daily metrics reset | Starting capital: ${current_capital:,.2f}")
    
    def update_metrics(self, current_capital: float):
        """Update risk metrics"""
        # Update peak capital for drawdown calculation
        if current_capital > self.peak_capital:
            self.peak_capital = current_capital
        
        # Calculate current drawdown
        if self.peak_capital > 0:
            self.current_drawdown = (self.peak_capital - current_capital) / self.peak_capital
        
        # Calculate daily P&L
        self.daily_pnl = current_capital - self.daily_start_capital
    
    def can_trade(self, current_capital: float) -> Tuple[bool, str]:
        """
        Check if trading is allowed based on risk limits
        
        Returns:
            (can_trade: bool, reason: str)
        """
        # Reset daily metrics if needed
        self.reset_daily_metrics(current_capital)
        
        # Update current metrics
        self.update_metrics(current_capital)
        
        # Check circuit breaker
        if self.circuit_breaker_triggered:
            return False, "Circuit breaker triggered - trading halted for today"
        
        # Check daily loss limit (only if limit is set > 0)
        if self.max_daily_loss > 0:
            daily_loss = self.daily_pnl / self.daily_start_capital if self.daily_start_capital > 0 else 0
            if daily_loss < -self.max_daily_loss:
                self.circuit_breaker_triggered = True
                logger.warning(
                    f"🚨 CIRCUIT BREAKER TRIGGERED | "
                    f"Daily loss: {daily_loss*100:.2f}% exceeds limit: {self.max_daily_loss*100:.2f}%"
                )
                return False, f"Daily loss limit exceeded: {daily_loss*100:.2f}%"
        
        # Check max drawdown (only if limit is set > 0)
        if self.max_drawdown > 0:
            if self.current_drawdown > self.max_drawdown:
                self.circuit_breaker_triggered = True
                logger.warning(
                    f"🚨 CIRCUIT BREAKER TRIGGERED | "
                    f"Drawdown: {self.current_drawdown*100:.2f}% exceeds limit: {self.max_drawdown*100:.2f}%"
                )
                return False, f"Max drawdown exceeded: {self.current_drawdown*100:.2f}%"
        
        return True, "Risk checks passed"
    
    def calculate_position_size(
        self,
        available_capital: float,
        current_price: float,
        volatility: float = 0.02
    ) -> float:
        """
        Calculate safe position size
        
        Args:
            available_capital: Available cash
            current_price: Current asset price
            volatility: Estimated volatility (default 2%)
            
        Returns:
            Position size (quantity)
        """
        # Base position size
        max_position_value = available_capital * self.max_position_size
        
        # Adjust for volatility (higher volatility = smaller position)
        volatility_factor = max(0.5, 1 - (volatility * 10))
        adjusted_value = max_position_value * volatility_factor
        
        # Calculate quantity
        quantity = adjusted_value / current_price
        
        logger.debug(
            f"💰 Position sizing | "
            f"Max value: ${max_position_value:.2f}, "
            f"Volatility: {volatility*100:.2f}%, "
            f"Adjusted: ${adjusted_value:.2f}, "
            f"Quantity: {quantity:.6f}"
        )
        
        return quantity
    
    def calculate_stop_loss(self, entry_price: float, side: str) -> float:
        """Calculate stop-loss price"""
        if side.lower() == "buy":
            return entry_price * (1 - self.stop_loss_pct)
        else:  # sell
            return entry_price * (1 + self.stop_loss_pct)
    
    def calculate_take_profit(self, entry_price: float, side: str) -> float:
        """Calculate take-profit price"""
        if side.lower() == "buy":
            return entry_price * (1 + self.take_profit_pct)
        else:  # sell
            return entry_price * (1 - self.take_profit_pct)
    
    def should_close_position(
        self,
        entry_price: float,
        current_price: float,
        side: str,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None
    ) -> Tuple[bool, str]:
        """
        Check if position should be closed based on stop-loss or take-profit
        
        Returns:
            (should_close: bool, reason: str)
        """
        if side.lower() == "buy":
            # Check stop-loss
            if stop_loss and current_price <= stop_loss:
                return True, f"Stop-loss hit: ${current_price:.2f} <= ${stop_loss:.2f}"
            
            # Check take-profit
            if take_profit and current_price >= take_profit:
                return True, f"Take-profit hit: ${current_price:.2f} >= ${take_profit:.2f}"
        
        else:  # sell/short position
            # Check stop-loss
            if stop_loss and current_price >= stop_loss:
                return True, f"Stop-loss hit: ${current_price:.2f} >= ${stop_loss:.2f}"
            
            # Check take-profit
            if take_profit and current_price <= take_profit:
                return True, f"Take-profit hit: ${current_price:.2f} <= ${take_profit:.2f}"
        
        return False, "Position within risk parameters"
    
    def get_risk_report(self) -> Dict:
        """Get current risk metrics report"""
        return {
            "daily_pnl": self.daily_pnl,
            "daily_pnl_pct": (self.daily_pnl / self.daily_start_capital * 100) if self.daily_start_capital > 0 else 0,
            "current_drawdown": self.current_drawdown,
            "current_drawdown_pct": self.current_drawdown * 100,
            "circuit_breaker_active": self.circuit_breaker_triggered,
            "max_daily_loss_pct": self.max_daily_loss * 100,
            "max_drawdown_pct": self.max_drawdown * 100,
            "peak_capital": self.peak_capital
        }