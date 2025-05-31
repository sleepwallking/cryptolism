from matplotlib import pyplot as plt

from settings.current_state import current_state
import pandas as pd

def plot_sma(prices, figure, window=20):
    """Рассчитывает и отображает Simple Moving Average"""
    close_prices = pd.Series(prices)
    sma = close_prices.rolling(window=window).mean()

    ax = figure.add_subplot(111)

    xs = range(len(prices))
    ys = prices
    graph_color = 'green' if ys[0] < ys[-1] else 'red'

    ax.plot(xs, ys, label='Цена', color=graph_color)
    ax.plot(xs, sma, label=f'SMA {window}', color='orange')
    ax.legend()

    return figure