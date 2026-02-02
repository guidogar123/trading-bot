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
        # Default: 9, 26, 52
        ichi = ta.ICHIMOKU(dataframe)
        dataframe['tenkan_sen'] = ichi['tenkan_sen']
        dataframe['kijun_sen'] = ichi['kijun_sen']
        dataframe['senkou_span_a'] = ichi['senkou_span_a']
        dataframe['senkou_span_b'] = ichi['senkou_span_b']
        dataframe['leading_span_a'] = ichi['leading_span_a']
        dataframe['leading_span_b'] = ichi['leading_span_b']
        dataframe['chicou_span'] = ichi['chicou_span']

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
