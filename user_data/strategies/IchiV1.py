import numpy as np
import pandas as pd
from freqtrade.strategy import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

class IchiV1(IStrategy):
    """
    Ichimoku Strategy V1
    Based on Ichimoku Cloud indicators.
    """
    
    # Strategy parameters
    timeframe = '5m'
    
    # ROI table:
    minimal_roi = {
        "0": 0.05,
        "30": 0.03,
        "60": 0.02,
        "120": 0.01
    }

    # Stoploss:
    stoploss = -0.10

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Ichimoku Cloud
        # Tenkan-sen (Conversion Line): (9-period high + 9-period low / 2)
        nine_period_high = dataframe['high'].rolling(window=9).max()
        nine_period_low = dataframe['low'].rolling(window=9).min()
        dataframe['tenkan_sen'] = (nine_period_high + nine_period_low) / 2

        # Kijun-sen (Base Line): (26-period high + 26-period low / 2)
        twenty_six_period_high = dataframe['high'].rolling(window=26).max()
        twenty_six_period_low = dataframe['low'].rolling(window=26).min()
        dataframe['kijun_sen'] = (twenty_six_period_high + twenty_six_period_low) / 2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line) / 2
        dataframe['senkou_span_a'] = ((dataframe['tenkan_sen'] + dataframe['kijun_sen']) / 2).shift(26)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low / 2)
        fifty_two_period_high = dataframe['high'].rolling(window=52).max()
        fifty_two_period_low = dataframe['low'].rolling(window=52).min()
        dataframe['senkou_span_b'] = ((fifty_two_period_high + fifty_two_period_low) / 2).shift(26)

        # Leading Spans
        dataframe['leading_span_a'] = dataframe['senkou_span_a'].shift(26)
        dataframe['leading_span_b'] = dataframe['senkou_span_b'].shift(26)

        # Cloud top and bottom
        dataframe['cloud_green'] = (dataframe['senkou_span_a'] > dataframe['senkou_span_b'])
        dataframe['cloud_top'] = dataframe[['senkou_span_a', 'senkou_span_b']].max(axis=1)
        dataframe['cloud_bottom'] = dataframe[['senkou_span_a', 'senkou_span_b']].min(axis=1)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Price is above Cloud
                (dataframe['close'] > dataframe['cloud_top']) &
                # Tenkan crosses above Kijun (Bullish Cross)
                (qtpylib.crossed_above(dataframe['tenkan_sen'], dataframe['kijun_sen'])) &
                # RSI is not overbought
                (dataframe['rsi'] < 70)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Tenkan crosses below Kijun (Bearish Cross)
                (qtpylib.crossed_below(dataframe['tenkan_sen'], dataframe['kijun_sen'])) |
                # RSI is overbought
                (dataframe['rsi'] > 80)
            ),
            'exit_long'] = 1

        return dataframe
