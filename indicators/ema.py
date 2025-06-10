from matplotlib import pyplot as plt

from settings.actual import actual
import pandas as pd

def plot_ema(prices, figure, window=20):
    """Рассчитывает и отображает Exponential Moving Average"""
    close_prices = pd.Series(prices)
    ema = close_prices.ewm(span=window, adjust=False).mean()


    ax = figure.add_subplot(111)

    xs = range(len(prices))
    ys = prices
    graph_color = 'green' if ys[0] < ys[-1] else 'red'

    ax.plot(xs, ys, label='Цена', color=graph_color)
    ax.plot(xs, ema, label=f'EMA {window}', color='purple')
    ax.legend()

    return figure