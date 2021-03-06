
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas as pd

"""
Indicators for Freqtrade
author@: Gerald Lonlas
modified@: Harry Chakryan
"""


def pivot_points_camarilla(dataframe: pd.DataFrame, timeperiod=30) -> pd.DataFrame:
    """
    Pivot Points Camarilla

    https://www.tradingview.com/support/solutions/43000521824-pivot-points-standard/

    Formula:
    Pivot = (Previous High + Previous Low + Previous Close)/3

    Resistance #1 = Previous Close + 1.1 * (Previous High - Previous Low)/12
    Support #1 = Previous Close - 1.1 * (Previous High - Previous Low)/12
    
    Resistance #2 = Previous Close + 1.1 * (Previous High - Previous Low)/6
    Support #2 = Previous Close - 1.1 * (Previous High - Previous Low)/6
    
    Resistance #3 = Previous Close + 1.1 * (Previous High - Previous Low)/4
    Support #3 = Previous Close - 1.1 * (Previous High - Previous Low)/4
    
    Resistance #4 = Previous Close + 1.1 * (Previous High - Previous Low)/2
    Support #4 = Previous Close - 1.1 * (Previous High - Previous Low)/2


    :param dataframe:
    :param timeperiod: Period to compare (in ticker)
    :return: dataframe
    """

    data = {}

    low = qtpylib.rolling_mean(
        series=pd.Series(
            index=dataframe.index,
            data=dataframe['low']
        ),
        window=timeperiod
    )

    high = qtpylib.rolling_mean(
        series=pd.Series(
            index=dataframe.index,
            data=dataframe['high']
        ),
        window=timeperiod
    )

    close = qtpylib.rolling_mean(
        series=pd.Series(
            index=dataframe.index,
            data=dataframe['close']
        ),
        window=timeperiod
    )

    # Pivot
    data['pivot'] = qtpylib.rolling_mean(
        series=qtpylib.typical_price(dataframe),
        window=timeperiod
    )

    # Support and Resistance #1
    data['r1'] = close + 1.1 * (high - low)/12
    data['s1'] = close - 1.1 * (high - low)/12
    
    # Support and Resistance #2
    data['r2'] = close + 1.1 * (high - low)/6
    data['s2'] = close - 1.1 * (high - low)/6
    
    # Support and Resistance #3
    data['r3'] = close + 1.1 * (high - low)/4
    data['s3'] = close - 1.1 * (high - low)/4
    
    # Support and Resistance #4
    data['r4'] = close + 1.1 * (high - low)/2
    data['s4'] = close - 1.1 * (high - low)/2

    return pd.DataFrame(
        index=dataframe.index,
        data=data
    )
