from indicators.macd import plot_macd
from indicators.sma import plot_sma
from indicators.ema import plot_ema
from indicators.rsi import plot_rsi
from indicators.bb import plot_bollinger_bands as plot_bb


ohlc_timeframes = [7, 30, 180, 365]
ohlc_themes = {'dark':'nightclouds', 'light':'binance'}
coin_name_max_lenght = 20


plot_functions = {
    'macd': plot_macd,
    'sma': plot_sma,
    'ema': plot_ema,
    'rsi': plot_rsi,
    'bb': plot_bb
}