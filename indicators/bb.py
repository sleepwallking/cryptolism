from matplotlib import pyplot as plt
from settings.actual import actual
import pandas as pd
import numpy as np


def plot_bollinger_bands(prices, figure, window=20, num_std=2):
    """Рассчитывает и отображает полосы Боллинджера"""
    close_prices = pd.Series(prices)

    # Расчет средней линии (SMA)
    sma = close_prices.rolling(window=window).mean()

    # Расчет стандартного отклонения
    std = close_prices.rolling(window=window).std()

    # Верхняя и нижняя полосы
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)

    ax = figure.add_subplot(111)

    xs = range(len(prices))
    ys = prices
    graph_color = 'green' if ys[0] < ys[-1] else 'red'

    # Отображение цены и полос Боллинджера
    ax.plot(xs, ys, label='Цена', color=graph_color)
    ax.plot(xs, sma, label=f'SMA {window}', color='orange')
    ax.plot(xs, upper_band, label=f'Верхняя полоса ({num_std}σ)', color='blue', linestyle='--')
    ax.plot(xs, lower_band, label=f'Нижняя полоса ({num_std}σ)', color='blue', linestyle='--')

    # Заливка между полосами
    ax.fill_between(xs, upper_band, lower_band, color='blue', alpha=0.1)

    ax.legend()

    return figure