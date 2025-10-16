"""
Optima - Optimization Agent
Continuously optimizes strategy parameters
"""
from typing import Dict, Any, List
import numpy as np
from backend.ai_agents.base_agent import BaseAgent
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class OptimaOptimizer(BaseAgent):
    """
    Optima - Optimization Agent
    
    Responsibilities:
    - Strategy parameter optimization
    - Performance tracking
    - A/B testing
    - Walk-forward optimization
    """
    
    def __init__(self):
        super().__init__(name="Optima", agent_type="optimizer")
        self.performance_history = []
        self.parameter_tests = {}
        self.best_parameters = {}
        self.optimization_cycles = 0
    
    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze performance and suggest optimizations
        
        Args:
            data: Performance metrics, current parameters
            
        Returns:
            Optimization recommendations
        """
        self.update_timestamp()
        
        current_performance = data.get('performance', {})
        current_params = data.get('parameters', {})
        
        # Record performance
        self._record_performance(current_performance, current_params)
        
        # Check if optimization is needed
        needs_optimization = self._should_optimize()
        
        if needs_optimization:
            # Generate optimization suggestions
            suggestions = self._generate_optimization_suggestions(
                current_params,
                current_performance
            )
            
            logger.info(
                f"🤖 Optima: Optimization cycle {self.optimization_cycles} | "
                f"Suggestions: {len(suggestions)}"
            )
            
            return {
                "agent": self.name,
                "needs_optimization": True,
                "suggestions": suggestions,
                "confidence": 0.75,
                "current_performance": current_performance
            }
        
        return {
            "agent": self.name,
            "needs_optimization": False,
            "message": "Current parameters performing well",
            "confidence": 0.80
        }
    
    def _record_performance(self, performance: Dict, parameters: Dict):
        """Record performance metrics"""
        self.performance_history.append({
            "timestamp": self.last_update,
            "performance": performance,
            "parameters": parameters
        })
        
        # Keep last 1000 records
        if len(self.performance_history) > 1000:
            self.performance_history.pop(0)
    
    def _should_optimize(self) -> bool:
        """
        Determine if optimization is needed
        
        Criteria:
        - Performance declining
        - Enough data collected
        - Regular optimization cycle
        """
        if len(self.performance_history) < 50:
            return False
        
        # Check performance trend
        recent_performance = [
            p['performance'].get('win_rate', 0.5) 
            for p in self.performance_history[-20:]
        ]
        
        if len(recent_performance) >= 10:
            recent_avg = np.mean(recent_performance[-10:])
            previous_avg = np.mean(recent_performance[-20:-10])
            
            # Performance declining?
            if recent_avg < previous_avg * 0.9:
                logger.info("📉 Performance declining - optimization needed")
                return True
        
        # Regular optimization every 100 cycles
        if self.optimization_cycles % 100 == 0 and self.optimization_cycles > 0:
            return True
        
        return False
    
    def _generate_optimization_suggestions(
        self, 
        current_params: Dict, 
        current_performance: Dict
    ) -> List[Dict]:
        """
        Generate parameter optimization suggestions
        
        Uses simple heuristics for Phase 3
        Phase 6+ will use Bayesian optimization
        """
        suggestions = []
        
        # SMA period optimization
        if 'sma_fast_period' in current_params:
            fast = current_params['sma_fast_period']
            slow = current_params['sma_slow_period']
            
            # Suggest variations
            suggestions.append({
                "parameter": "sma_fast_period",
                "current": fast,
                "suggested": max(5, fast - 2),
                "reason": "Test shorter fast period for faster signals"
            })
            
            suggestions.append({
                "parameter": "sma_fast_period",
                "current": fast,
                "suggested": fast + 2,
                "reason": "Test longer fast period for smoother signals"
            })
        
        # Position size optimization
        if 'position_size' in current_params:
            size = current_params['position_size']
            win_rate = current_performance.get('win_rate', 0.5)
            
            if win_rate > 0.6:
                suggestions.append({
                    "parameter": "position_size",
                    "current": size,
                    "suggested": min(0.2, size * 1.1),
                    "reason": f"Good win rate ({win_rate:.1%}), consider increasing position"
                })
            elif win_rate < 0.4:
                suggestions.append({
                    "parameter": "position_size",
                    "current": size,
                    "suggested": max(0.01, size * 0.9),
                    "reason": f"Low win rate ({win_rate:.1%}), consider decreasing position"
                })
        
        self.optimization_cycles += 1
        return suggestions
    
    def test_parameters(self, params: Dict, result: Dict):
        """Record A/B test results"""
        param_key = str(sorted(params.items()))
        
        if param_key not in self.parameter_tests:
            self.parameter_tests[param_key] = {
                "params": params,
                "results": [],
                "avg_performance": 0.0
            }
        
        self.parameter_tests[param_key]["results"].append(result)
        
        # Update average
        results = self.parameter_tests[param_key]["results"]
        self.parameter_tests[param_key]["avg_performance"] = np.mean([
            r.get('win_rate', 0.5) for r in results
        ])
    
    def get_best_parameters(self) -> Dict:
        """Get best performing parameters"""
        if not self.parameter_tests:
            return {}
        
        best_key = max(
            self.parameter_tests.keys(),
            key=lambda k: self.parameter_tests[k]["avg_performance"]
        )
        
        return self.parameter_tests[best_key]["params"]
    
    def get_status(self) -> Dict[str, Any]:
        """Get Optima status"""
        return {
            "name": self.name,
            "type": self.agent_type,
            "active": self.is_active,
            "last_update": self.last_update.isoformat(),
            "optimization_cycles": self.optimization_cycles,
            "performance_records": len(self.performance_history),
            "parameter_tests": len(self.parameter_tests),
            "best_parameters": self.get_best_parameters()
        }