"""
Generate synthetic market data for testing strategies
Creates realistic OHLCV data with trends and volatility
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta
import json


def generate_realistic_ohlcv(
    symbol: str,
    start_date: str,
    end_date: str,
    timeframe: str = "5m",
    initial_price: float = 30000.0,
    trend: float = 0.0001,  # Slight upward trend
    volatility: float = 0.02  # 2% volatility
):
    """
    Generate realistic OHLCV candle data
    
    Args:
        symbol: Trading pair (e.g., 'BTC/USDT')
        start_date: Start date in format 'YYYYMMDD'
        end_date: End date in format 'YYYYMMDD'
        timeframe: Candle timeframe (5m, 15m, 1h, etc.)
        initial_price: Starting price
        trend: Daily trend (0.0001 = 0.01% per candle)
        volatility: Price volatility (0.02 = 2%)
    """
    # Parse dates
    start = datetime.strptime(start_date, '%Y%m%d')
    end = datetime.strptime(end_date, '%Y%m%d')
    
    # Calculate number of candles
    timeframe_minutes = {
        '1m': 1, '5m': 5, '15m': 15, '30m': 30,
        '1h': 60, '4h': 240, '1d': 1440
    }
    
    minutes = timeframe_minutes.get(timeframe, 5)
    total_minutes = int((end - start).total_seconds() / 60)
    num_candles = total_minutes // minutes
    
    print(f"Generating {num_candles} candles for {symbol}...")
    
    # Generate timestamps
    timestamps = [start + timedelta(minutes=minutes * i) for i in range(num_candles)]
    
    # Generate prices with realistic movement
    np.random.seed(42)
    
    # Price movement
    returns = np.random.normal(trend, volatility, num_candles)
    prices = initial_price * np.exp(np.cumsum(returns))
    
    # Generate OHLCV data
    data = []
    for i, ts in enumerate(timestamps):
        close = prices[i]
        
        # Open is close of previous candle (or initial for first)
        open_price = prices[i-1] if i > 0 else initial_price
        
        # High and low based on volatility
        candle_range = close * volatility * np.random.uniform(0.5, 1.5)
        high = close + np.random.uniform(0, candle_range)
        low = close - np.random.uniform(0, candle_range)
        
        # Ensure OHLC relationship is valid
        high = max(open_price, close, high)
        low = min(open_price, close, low)
        
        # Volume (realistic with some spikes)
        base_volume = 100 * (1 + np.random.uniform(-0.5, 0.5))
        volume = base_volume * (1 + 5 * np.random.exponential(0.1))
        
        data.append({
            'date': int(ts.timestamp() * 1000),  # Milliseconds
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': round(volume, 2)
        })
    
    return data


def save_data(data, symbol, exchange='binance', data_dir='user_data/data'):
    """Save generated data in Freqtrade format"""
    
    # Create directory structure
    safe_symbol = symbol.replace('/', '_').replace(':', '_')
    exchange_dir = Path(data_dir) / exchange
    exchange_dir.mkdir(parents=True, exist_ok=True)
    
    # Save as JSON (Freqtrade format)
    filename = exchange_dir / f"{safe_symbol}-5m.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Saved {len(data)} candles to {filename}")
    
    return filename


def main():
    """Generate test data for all pairs"""
    
    pairs = {
        'BTC/USDT': {'price': 35000, 'volatility': 0.025, 'trend': 0.0002},
        'ETH/USDT': {'price': 2000, 'volatility': 0.03, 'trend': 0.0003},
        'SOL/USDT': {'price': 50, 'volatility': 0.04, 'trend': 0.0001},
        'BNB/USDT': {'price': 300, 'volatility': 0.025, 'trend': 0.00015},
    }
    
    # Generate 1 month of data (Nov 2023)
    start_date = '20231101'
    end_date = '20231130'
    
    print("=" * 60)
    print("  Generating Synthetic Market Data")
    print("  For testing trading strategies")
    print("=" * 60)
    print()
    
    for symbol, params in pairs.items():
        data = generate_realistic_ohlcv(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            timeframe='5m',
            initial_price=params['price'],
            volatility=params['volatility'],
            trend=params['trend']
        )
        
        save_data(data, symbol, exchange='binance')
        print()
    
    print("=" * 60)
    print("✅ Data generation complete!")
    print()
    print("You can now run backtesting with:")
    print()
    print("  freqtrade backtesting \\")
    print("    --strategy GridScalpingHybrid \\")
    print("    --timerange 20231101-20231130 \\")
    print("    --config user_data\\config.json")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
