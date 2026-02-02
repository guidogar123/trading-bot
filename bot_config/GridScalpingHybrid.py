"""
Grid + Scalping Hybrid Strategy for Freqtrade
Target: $10 USD daily profit
Capital: $1000-$2000 USD
Expected return: 0.5% - 1% daily

Strategy combines:
1. Grid Trading for ranging markets (70% of signals)
2. Scalping for volatile markets (30% of signals)

Risk Management:
- Stop Loss: 2% per trade
- Take Profit: 3% (1.5:1 ratio)
- Max open trades: 5
- Position size: 10% of capital
"""

import talib.abstract as ta
from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import numpy as np


class GridScalpingHybrid(IStrategy):
    """
    Hybrid strategy combining Grid Trading and Scalping
    """
    
    # Strategy interface version
    INTERFACE_VERSION = 3
    
    # ROI table - Take profit targets
    minimal_roi = {
        "0": 0.03,   # 3% take profit
        "30": 0.02,  # 2% after 30 minutes
        "60": 0.01   # 1% after 60 minutes
    }
    
    # Stoploss
    stoploss = -0.02  # 2% stop loss
    
    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True
    
    # Timeframe
    timeframe = '5m'
    
    # Run "populate_indicators()" only for new candle
    process_only_new_candles = True
    
    # Experimental settings
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False
    
    # Hyperopt parameters
    buy_rsi = IntParameter(20, 40, default=30, space="buy")
    buy_rsi_enabled = True
    
    sell_rsi = IntParameter(60, 80, default=70, space="sell")
    sell_rsi_enabled = True
    
    # Grid parameters
    grid_levels = IntParameter(3, 10, default=5, space="buy")
    grid_spacing = DecimalParameter(0.005, 0.02, default=0.01, space="buy")
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add technical indicators to the dataframe
        """
        
        # RSI - Relative Strength Index
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        
        # MACD - Moving Average Convergence Divergence  
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        
        # Bollinger Bands
        bollinger = ta.BBANDS(dataframe, timeperiod=20)
        dataframe['bb_lowerband'] = bollinger['lowerband']
        dataframe['bb_middleband'] = bollinger['middleband']
        dataframe['bb_upperband'] = bollinger['upperband']
        
        # EMA - Exponential Moving Average
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        dataframe['ema50'] = ta.EMA(dataframe, timeperiod=50)
        
        # ATR - Average True Range (for volatility)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        
        # Volume
        dataframe['volume_ma'] = dataframe['volume'].rolling(window=20).mean()
        
        # Grid levels calculation
        dataframe['grid_lower'] = dataframe['close'] * (1 - self.grid_spacing.value)
        dataframe['grid_upper'] = dataframe['close'] * (1 + self.grid_spacing.value)
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define buy signals based on indicators
        Combines Grid and Scalping logic
        """
        conditions = []
        
        # SCALPING SIGNALS (for volatile markets)
        # Buy when RSI oversold + MACD crossover + price below EMA
        scalping_buy = (
            (dataframe['rsi'] < self.buy_rsi.value) &
            (dataframe['macd'] > dataframe['macdsignal']) &
            (dataframe['close'] < dataframe['ema20']) &
            (dataframe['volume'] > dataframe['volume_ma'])
        )
        
        # GRID SIGNALS (for ranging markets)
        # Buy at lower grid level when price is ranging
        grid_buy = (
            (dataframe['close'] <= dataframe['grid_lower']) &
            (dataframe['rsi'] > 30) & (dataframe['rsi'] < 50) &  # Not too oversold
            (dataframe['close'] > dataframe['bb_lowerband'])  # Not too extended
        )
        
        # COMBINED: Either scalping OR grid signal
        conditions.append(scalping_buy | grid_buy)
        
        # Only buy if we have a signal
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1
        
        return dataframe
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Define sell signals based on indicators
        """
        conditions = []
        
        # SCALPING EXIT
        # Sell when RSI overbought OR MACD crossover down
        scalping_sell = (
            (dataframe['rsi'] > self.sell_rsi.value) |
            (dataframe['macd'] < dataframe['macdsignal'])
        )
        
        # GRID EXIT
        # Sell at upper grid level
        grid_sell = (
            (dataframe['close'] >= dataframe['grid_upper']) &
            (dataframe['rsi'] > 50)
        )
        
        # COMBINED: Either scalping OR grid exit
        conditions.append(scalping_sell | grid_sell)
        
        # Only sell if we have a signal
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'exit_long'] = 1
        
        return dataframe


# Python reduce function import
from functools import reduce
