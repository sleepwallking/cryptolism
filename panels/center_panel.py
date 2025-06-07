import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sys import getsizeof
from functools import partial
from decimal import Decimal
import pandas as pd
import mplfinance as mpf
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from settings.config import ohlc_timeframes, ohlc_themes, plot_functions
from settings.current_state import current_state
from utils.helpers import get_date_from_period, validate_input
from utils.messages import CANDLE_CHART_ERROR_MSG
from api.coingecko import CoingeckoAPI


class CenterPanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=1, column=1, padx=master.padding, pady=master.padding, sticky="nsew")
        self.current_canvas = None
        self.cache_for_prices = {}
        self.coingecko = CoingeckoAPI()
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # Информационная метка
        self.info_label = customtkinter.CTkLabel(self, font=self.master.font_bold)
        self.info_label.grid(row=0, column=0, padx=self.master.padding + 10, pady=self.master.padding, sticky="W")

        # Фрейм для кнопок
        self.buttons_frame = customtkinter.CTkFrame(self)
        self.buttons_frame.grid(row=2, column=0, padx=self.master.padding, pady=self.master.padding, sticky="nsew")

        # Настройка колонок
        for i in range(6):
            self.buttons_frame.grid_columnconfigure(i, weight=1)

        # Кнопки временных периодов
        for i, timeframe in enumerate(ohlc_timeframes):
            button = customtkinter.CTkButton(
                self.buttons_frame,
                text=f"{timeframe} дн.",
                command=partial(self.master.set_period, timeframe)
            )
            button.grid(row=0, column=i, padx=self.master.padding, pady=self.master.padding, sticky="nsew")

        # Поле ввода и кнопка поиска
        vcmd = (self.master.register(validate_input), '%P')
        self.time_search_entry = customtkinter.CTkEntry(
            self.buttons_frame,
            placeholder_text="Ввести диапазон: ",
            validate="key",
            validatecommand=vcmd
        )
        self.time_search_entry.grid(row=0, column=4, padx=self.master.padding, pady=self.master.padding, sticky="nsew")

        self.time_search_button = customtkinter.CTkButton(
            self.buttons_frame,
            text="Найти",
            command=lambda: self.master.set_period(int(self.time_search_entry.get()))
        )
        self.time_search_button.grid(row=0, column=5, padx=self.master.padding, pady=self.master.padding, sticky="nsew")



    def get_coin(self, coin, days=7):
        plt.close('all')

        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()

        cache_key = f'{coin}{days}'
        prices = self.cache_for_prices.get(cache_key)

        if prices:
            print(f'Данные взяты из кэша, текущий размер кэша: {getsizeof(self.cache_for_prices)}')
        else:
            prices = self.cache_for_prices[cache_key] = self.coingecko.get_data_from_api(coin, days)
            print('Данные получены с api и добавлены в кэш')

        xs = range(len(prices))
        ys = prices
        price = Decimal(str(prices[-1])).quantize(Decimal("1.00"))
        figure = plt.figure(figsize=(18, 10), tight_layout=True)
        graph_color = 'green' if ys[0] < ys[-1] else 'red'

        if current_state.graph == "свечной":
            if days not in ohlc_timeframes:
                days = current_state.period = 7
                CTkMessagebox(title="Ошибка ввода", message=CANDLE_CHART_ERROR_MSG, icon="info", option_1="Отмена")

            ohlc = self.coingecko.get_ohlc_data_from_api(coin, days)
            data = []

            for i in ohlc:
                data.append([datetime.fromtimestamp(int(i[0]) / 1000), i[1], i[2], i[3], i[4]])

            df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
            df.set_index('Date', inplace=True)

            figure, ax = mpf.plot(
                df,
                type='candle',
                style=ohlc_themes[current_state.theme],
                returnfig=True,
                figsize=(18, 10),
                volume=False,
                tight_layout=True,
            )
            figure.suptitle(f'{current_state.coin} | {price}$', fontsize=14, y=0.9, x=0.9)

        elif current_state.graph == 'линейный':
            ax = figure.add_subplot(111)
            ax.plot(xs, ys, color=graph_color)
        else:
            figure = plot_functions[current_state.graph](prices, figure)

        if not hasattr(self, 'current_canvas') or not self.current_canvas:
            self.current_canvas = FigureCanvasTkAgg(figure, master=self)
            self.current_canvas.get_tk_widget().grid(row=1, column=0)
        else:
            # Иначе обновляем существующий canvas
            self.current_canvas.figure = figure
            self.current_canvas.draw()

        plt.title(f'{current_state.coin} | {price}$')
        self.info_label.configure(
            text=f"период: {get_date_from_period(current_state.period)} | график: {current_state.graph}")

        self.current_canvas = FigureCanvasTkAgg(figure, master=self)
        self.current_canvas.get_tk_widget().grid(row=1, column=0)
