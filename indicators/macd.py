import pandas as pd
import matplotlib.pyplot as plt
from settings.actual import actual


def plot_macd(prices, figure):
    """Рассчитывает и отображает индикатор MACD"""
    # Преобразуем список цен в pandas Series
    close_prices = pd.Series(prices)

    # Рассчитываем EMA с периодами 12 и 26
    ema12 = close_prices.ewm(span=12, adjust=False).mean()
    ema26 = close_prices.ewm(span=26, adjust=False).mean()

    # Линия MACD - разница между EMA12 и EMA26
    macd_line = ema12 - ema26
    # Сигнальная линия - EMA от MACD с периодом 9
    signal_line = macd_line.ewm(span=9, adjust=False).mean()
    # Гистограмма MACD - разница между MACD и сигнальной линией
    macd_hist = macd_line - signal_line

    # Верхний график - цены
    ax1 = figure.add_subplot(211)
    xs = range(len(prices))
    ys = prices
    graph_color = 'green' if ys[0] < ys[-1] else 'red'


    ax1.plot(xs, ys, color=graph_color)

    # Нижний график - MACD
    ax2 = figure.add_subplot(212)
    ax2.plot(macd_line, label='MACD', color='blue')
    ax2.plot(signal_line, label='Signal', color='orange')

    # Гистограмма MACD
    colors = ['green' if val >= 0 else 'red' for val in macd_hist]
    ax2.bar(macd_hist.index, macd_hist, color=colors, alpha=0.5)

    ax2.axhline(0, color='gray', linestyle='--')
    ax2.set_title('MACD')
    ax2.legend()

    return figure