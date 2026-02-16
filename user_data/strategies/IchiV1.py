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
        # Heikin-Ashi Candles
        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['ha_open'] = heikinashi['open']
        dataframe['ha_close'] = heikinashi['close']
        dataframe['ha_high'] = heikinashi['high']
        dataframe['ha_low'] = heikinashi['low']

        # Ichimoku Cloud on Heikin-Ashi
        nine_period_high = dataframe['ha_high'].rolling(window=9).max()
        nine_period_low = dataframe['ha_low'].rolling(window=9).min()
        dataframe['tenkan_sen'] = (nine_period_high + nine_period_low) / 2

        twenty_six_period_high = dataframe['ha_high'].rolling(window=26).max()
        twenty_six_period_low = dataframe['ha_low'].rolling(window=26).min()
        dataframe['kijun_sen'] = (twenty_six_period_high + twenty_six_period_low) / 2

        dataframe['senkou_span_a'] = ((dataframe['tenkan_sen'] + dataframe['kijun_sen']) / 2).shift(26)

        fifty_two_period_high = dataframe['ha_high'].rolling(window=52).max()
        fifty_two_period_low = dataframe['ha_low'].rolling(window=52).min()
        dataframe['senkou_span_b'] = ((fifty_two_period_high + fifty_two_period_low) / 2).shift(26)

        dataframe['leading_span_a'] = dataframe['senkou_span_a'].shift(26)
        dataframe['leading_span_b'] = dataframe['senkou_span_b'].shift(26)

        # Cloud top and bottom
        dataframe['cloud_top'] = dataframe[['senkou_span_a', 'senkou_span_b']].max(axis=1)
        dataframe['cloud_bottom'] = dataframe[['senkou_span_a', 'senkou_span_b']].min(axis=1)

        # 200 EMA Filter
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)

        # RSI
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Trend: HA Close > EMA 200
                (dataframe['ha_close'] > dataframe['ema200']) &
                # Price is above Cloud
                (dataframe['ha_close'] > dataframe['cloud_top']) &
                # Bullish Cross
                (qtpylib.crossed_above(dataframe['tenkan_sen'], dataframe['kijun_sen'])) &
                (dataframe['rsi'] < 70)
            ),
            'enter_long'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Bearish Cross or Price drops below Cloud
                (qtpylib.crossed_below(dataframe['tenkan_sen'], dataframe['kijun_sen'])) |
                (dataframe['ha_close'] < dataframe['cloud_bottom']) |
                (dataframe['rsi'] > 80)
            ),
            'exit_long'] = 1

        return dataframe
