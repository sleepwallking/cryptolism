from matplotlib import pyplot as plt
import pandas as pd
from settings.current_state import current_state


def plot_rsi(prices, figure, window=14):
    """Рассчитывает и отображает Relative Strength Index"""
    close_prices = pd.Series(prices)
    delta = close_prices.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    ax1 = figure.add_subplot(211)
    xs = range(len(prices))
    ys = prices
    graph_color = 'green' if ys[0] < ys[-1] else 'red'
    ax1.plot(xs, ys, color=graph_color)

    ax2 = figure.add_subplot(212)
    ax2.plot(rsi, label='RSI', color='blue')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_ylim(0, 100)
    ax2.set_title(f'RSI {current_state.period}')
    ax2.legend()

    return figure