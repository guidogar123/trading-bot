"""
Risk Management Module for Trading Bot
Implements position sizing, stop loss, and daily limits
"""

from typing import Dict, Optional
from datetime import datetime, timedelta
import json


class RiskManager:
    """
    Manages trading risk with configurable parameters
    """
    
    def __init__(self, config: Dict):
        """
        Initialize risk manager with configuration
        
        Args:
            config: Dictionary with risk parameters
        """
        self.initial_capital = config.get('initial_capital', 1000)
        self.current_capital = self.initial_capital
        self.max_position_size = config.get('max_position_size', 0.10)  # 10% per trade
        self.max_open_trades = config.get('max_open_trades', 5)
        self.stop_loss_pct = config.get('stop_loss_pct', 0.02)  # 2%
        self.take_profit_pct = config.get('take_profit_pct', 0.03)  # 3%
        self.max_daily_drawdown = config.get('max_daily_drawdown', 0.10)  # 10%
        self.daily_profit_target = config.get('daily_profit_target', 10)  # $10 USD
        
        # Daily tracking
        self.daily_pnl = 0.0
        self.daily_trades = 0
        self.last_reset = datetime.now().date()
        self.open_positions = []
        
    def calculate_position_size(self, price: float, available_capital: float) -> float:
        """
        Calculate position size based on capital and max position percentage
        
        Args:
            price: Current price of asset
            available_capital: Available capital for trading
            
        Returns:
            Position size in quote currency
        """
        max_position_value = available_capital * self.max_position_size
        position_size = max_position_value / price
        return position_size
    
    def calculate_stop_loss(self, entry_price: float, is_long: bool = True) -> float:
        """
        Calculate stop loss price
        
        Args:
            entry_price: Entry price of position
            is_long: True for long position, False for short
            
        Returns:
            Stop loss price
        """
        if is_long:
            return entry_price * (1 - self.stop_loss_pct)
        else:
            return entry_price * (1 + self.stop_loss_pct)
    
    def calculate_take_profit(self, entry_price: float, is_long: bool = True) -> float:
        """
        Calculate take profit price
        
        Args:
            entry_price: Entry price of position
            is_long: True for long position, False for short
            
        Returns:
            Take profit price
        """
        if is_long:
            return entry_price * (1 + self.take_profit_pct)
        else:
            return entry_price * (1 - self.take_profit_pct)
    
    def can_open_trade(self) -> Dict[str, any]:
        """
        Check if a new trade can be opened
        
        Returns:
            Dictionary with 'allowed' bool and 'reason' string
        """
        # Reset daily stats if new day
        self._reset_if_new_day()
        
        # Check max open trades
        if len(self.open_positions) >= self.max_open_trades:
            return {
                'allowed': False,
                'reason': f'Max open trades reached ({self.max_open_trades})'
            }
        
        # Check daily drawdown
        daily_drawdown_pct = abs(self.daily_pnl) / self.initial_capital
        if self.daily_pnl < 0 and daily_drawdown_pct >= self.max_daily_drawdown:
            return {
                'allowed': False,
                'reason': f'Daily drawdown limit reached ({daily_drawdown_pct:.1%})'
            }
        
        # Check if daily profit target reached (optional stop)
        if self.daily_pnl >= self.daily_profit_target:
            return {
                'allowed': False,
                'reason': f'Daily profit target reached (${self.daily_pnl:.2f})'
            }
        
        return {
            'allowed': True,
            'reason': 'Trade allowed'
        }
    
    def record_trade(self, entry_price: float, exit_price: float, 
                    position_size: float, is_long: bool = True) -> Dict:
        """
        Record a completed trade and update stats
        
        Args:
            entry_price: Entry price
            exit_price: Exit price
            position_size: Size of position
            is_long: True for long, False for short
            
        Returns:
            Dictionary with trade results
        """
        # Calculate P&L
        if is_long:
            pnl = (exit_price - entry_price) * position_size
        else:
            pnl = (entry_price - exit_price) * position_size
        
        pnl_pct = pnl / (entry_price * position_size)
        
        # Update stats
        self.daily_pnl += pnl
        self.daily_trades += 1
        self.current_capital += pnl
        
        # Remove from open positions if exists
        self.open_positions = [p for p in self.open_positions 
                              if not (p['entry_price'] == entry_price and 
                                     p['position_size'] == position_size)]
        
        return {
            'pnl': pnl,
            'pnl_pct': pnl_pct,
            'daily_pnl': self.daily_pnl,
            'daily_trades': self.daily_trades,
            'current_capital': self.current_capital
        }
    
    def add_open_position(self, pair: str, entry_price: float, 
                         position_size: float, is_long: bool = True):
        """
        Add a position to open positions tracker
        """
        position = {
            'pair': pair,
            'entry_price': entry_price,
            'position_size': position_size,
            'is_long': is_long,
            'stop_loss': self.calculate_stop_loss(entry_price, is_long),
            'take_profit': self.calculate_take_profit(entry_price, is_long),
            'opened_at': datetime.now().isoformat()
        }
        self.open_positions.append(position)
    
    def get_stats(self) -> Dict:
        """
        Get current risk management stats
        
        Returns:
            Dictionary with current stats
        """
        return {
            'initial_capital': self.initial_capital,
            'current_capital': self.current_capital,
            'daily_pnl': self.daily_pnl,
            'daily_pnl_pct': (self.daily_pnl / self.initial_capital) * 100,
            'daily_trades': self.daily_trades,
            'open_positions': len(self.open_positions),
            'max_open_trades': self.max_open_trades,
            'daily_target': self.daily_profit_target,
            'target_progress': (self.daily_pnl / self.daily_profit_target) * 100 if self.daily_profit_target > 0 else 0,
            'last_reset': self.last_reset.isoformat()
        }
    
    def _reset_if_new_day(self):
        """
        Reset daily stats if it's a new day
        """
        today = datetime.now().date()
        if today != self.last_reset:
            self.daily_pnl = 0.0
            self.daily_trades = 0
            self.last_reset = today
    
    def save_state(self, filepath: str):
        """
        Save risk manager state to file
        """
        state = {
            'current_capital': self.current_capital,
            'daily_pnl': self.daily_pnl,
            'daily_trades': self.daily_trades,
            'last_reset': self.last_reset.isoformat(),
            'open_positions': self.open_positions
        }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_state(self, filepath: str):
        """
        Load risk manager state from file
        """
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
                self.current_capital = state.get('current_capital', self.initial_capital)
                self.daily_pnl = state.get('daily_pnl', 0.0)
                self.daily_trades = state.get('daily_trades', 0)
                self.last_reset = datetime.fromisoformat(state.get('last_reset', datetime.now().date().isoformat())).date()
                self.open_positions = state.get('open_positions', [])
        except FileNotFoundError:
            pass  # Use defaults if file doesn't exist


# Example usage
if __name__ == "__main__":
    # Initialize risk manager
    config = {
        'initial_capital': 1000,
        'max_position_size': 0.10,
        'max_open_trades': 5,
        'stop_loss_pct': 0.02,
        'take_profit_pct': 0.03,
        'max_daily_drawdown': 0.10,
        'daily_profit_target': 10
    }
    
    rm = RiskManager(config)
    
    # Check if trade allowed
    result = rm.can_open_trade()
    print(f"Can trade: {result}")
    
    # Calculate position size
    btc_price = 50000
    available_capital = 1000
    position_size = rm.calculate_position_size(btc_price, available_capital)
    print(f"Position size: {position_size:.6f} BTC (${position_size * btc_price:.2f})")
    
    # Calculate stop loss and take profit
    entry_price = 50000
    stop_loss = rm.calculate_stop_loss(entry_price)
    take_profit = rm.calculate_take_profit(entry_price)
    print(f"Entry: ${entry_price}")
    print(f"Stop Loss: ${stop_loss:.2f} (-{rm.stop_loss_pct*100}%)")
    print(f"Take Profit: ${take_profit:.2f} (+{rm.take_profit_pct*100}%)")
    
    # Get stats
    stats = rm.get_stats()
    print(f"\nCurrent Stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
