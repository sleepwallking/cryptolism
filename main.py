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

from settings.config import ohlc_avaible_timeframes
from utils.controls import IconButton, graphs_and_icons
from api.coingecko import CoingeckoAPI
from settings.current_state import current_state
from utils.helpers import truncate_string

coingecko = CoingeckoAPI()


customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("dark")



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1800x900")
        self.title("Cryptolism")
        self.iconbitmap("img/cryptolism.ico")
        self.padding = 5
        self.icon_size = 40
        plt.style.use('dark_background')
        self.font_bold = ("Segoe UI", 18, "normal")

        # Панели
        self.top_frame = customtkinter.CTkFrame(self, height=30)
        self.top_frame.grid(row=0, column=0, padx=self.padding, pady=(self.padding, 0), sticky="ew", columnspan=3)

        self.left_frame = customtkinter.CTkFrame(self)
        self.left_frame.grid(row=1, column=0, padx=(self.padding, 0), pady=self.padding, sticky='nsew')

        self.center_frame = customtkinter.CTkFrame(self, height=1200)
        self.center_frame.grid(row=1, column=1, padx=self.padding, pady=self.padding, sticky="nsew")

        self.right_frame = customtkinter.CTkFrame(self)
        self.right_frame.grid(row=1, column=2, padx=(0, self.padding), pady=self.padding, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)

        # Кнопки верхней панели

        def switch_event():
            theme = switch_var.get()
            if theme == 'light':
                customtkinter.set_appearance_mode('light')
                plt.style.use('default')
                current_state.theme = 'light'
            else:
                customtkinter.set_appearance_mode('dark')
                plt.style.use('dark_background')
                current_state.theme = 'dark'

            self.open_coin_window(current_state.coin)


        switch_var = customtkinter.StringVar(value="dark")
        self.switch = customtkinter.CTkSwitch(self.top_frame, text="Смена темы", command=switch_event,
                                        variable=switch_var, onvalue="dark", offvalue="light")
        self.switch.grid(row=0, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        def combobox_callback(choice):
            print("combobox dropdown clicked:", choice)

        self.change_api = customtkinter.CTkComboBox(self.top_frame, values=["coingecko", "binance", "bybit", "okx"],
                                     command=combobox_callback)

        self.change_api.grid(row=0, column=1, padx=self.padding, pady=self.padding, sticky="nsew")


        # Кнопки левой стороны (инструменты для графика)
        for graph_type in graphs_and_icons:
            self.graph_button = IconButton(self.left_frame, graphs_and_icons[graph_type], partial(self.set_graph_type, graph_type),
                                            width=self.icon_size, height=self.icon_size)
            self.graph_button.pack(padx=self.padding, pady=self.padding)

        # Фрейм для центральных кнопок

        self.center_frame_graph = customtkinter.CTkFrame(self.center_frame)
        self.center_frame_graph.grid(row=0, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        self.coin_frame = customtkinter.CTkFrame(self.center_frame_graph, height=800)
        self.coin_frame.grid(row=0, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        self.coin_label = customtkinter.CTkLabel(self.coin_frame, font=self.font_bold)
        self.coin_label.grid(row=0, column=0, padx=self.padding+10, pady=self.padding, sticky="W")

        self.center_frame_buttons = customtkinter.CTkFrame(self.coin_frame)
        self.center_frame_buttons.grid(row=2, column=0, padx=self.padding, pady=self.padding, sticky="nsew", columnspan=4)








        for i, timeframe in enumerate(ohlc_avaible_timeframes):
            self.timeframe_button = customtkinter.CTkButton(self.center_frame_buttons, text=f"{timeframe} дн.",
                                                                command=partial(self.plot_the_period, timeframe))
            self.timeframe_button.grid(row=0, column=i, padx=self.padding, pady=self.padding)


        self.time_search_entry = customtkinter.CTkEntry(self.center_frame_buttons, placeholder_text="Ввести диапазон: ")
        self.time_search_entry.grid(row=0, column=4, padx=self.padding, pady=self.padding)

        self.time_search_button = customtkinter.CTkButton(self.center_frame_buttons, text="Найти", command=lambda: self.check_entry_int_value())
        self.time_search_button.grid(row=0, column=5, padx=self.padding, pady=self.padding)

        self.cache_for_prices = {} # {'bitcoin7': [price1, price2, price3, price..., pricex], 'ethereum7': [price1, price2, price3, price..., pricex], 'coinx': [etc...]}
        self.open_coin_window('bitcoin')

        # Кнопки правой стороны (список монет)

        self.coin_list_label = customtkinter.CTkLabel(self.right_frame, text='Список валют')
        self.coin_list_label.grid(row=0, column=0)

        self.coin_search_entry = customtkinter.CTkEntry(self.right_frame, placeholder_text="Найти монету:")
        self.coin_search_entry.grid(row=1, column=0, padx=self.padding, pady=self.padding, sticky="nsew")
        self.coin_search_entry.bind("<KeyRelease>", self.filter_buttons)

        self.coins_list_frame = customtkinter.CTkScrollableFrame(self.right_frame, height=700)
        self.coins_list_frame.grid(row=2, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        coins = coingecko.get_coin_list()

        self.coins_buttons = []

        for i, coin in enumerate(coins):
            self.coin_button = customtkinter.CTkButton(self.coins_list_frame, width=180, text=truncate_string(coin),
                                                       command=partial(self.open_coin_window, coin))
            self.coin_button.grid(row=i, column=0, padx=self.padding, pady=self.padding)
            self.coins_buttons.append(self.coin_button)







    def filter_buttons(self, event):
        search_text = self.coin_search_entry.get().lower()  # Получаем текст из поля
        self.coins_list_frame._parent_canvas.yview_moveto(0)

        # Если поле пустое — показываем ВСЕ кнопки
        if not search_text:
            for i, btn in enumerate(self.coins_buttons):
                btn.grid(row=i, column=0, padx=self.padding, pady=self.padding)  # Восстанавливаем позицию
            return

        # Иначе фильтруем
        visible_row = 0  # Начинаем с ряда 2 (как в вашем коде)
        for btn in self.coins_buttons:
            btn_text = btn.cget("text").lower()  # Получаем текст кнопки

            if search_text in btn_text:
                btn.grid(row=visible_row, column=0, padx=self.padding, pady=self.padding)  # Показываем
                visible_row += 1  # Увеличиваем ряд для следующей кнопки
            else:
                btn.grid_remove()  # Скрываем (но сохраняем настройки grid)

    def check_entry_int_value(self):
        value = int(self.time_search_entry.get())
        if current_state.graph_type == "candlestick" and value not in ohlc_avaible_timeframes:
            ...
        else:
            self.plot_the_period(value)


    def set_graph_type(self, graph_type: str):
        current_state.graph_type = graph_type
        self.get_coin(current_state.coin, current_state.period)

    def open_coin_window(self, coin):
        current_state.coin = coin
        self.get_coin(coin)



    def plot_the_period(self, days):
        coin = current_state.coin
        current_state.period = days
        self.get_coin(coin, days)

    def plot_macd(self, prices):
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

        # Создаем график
        figure = plt.figure(figsize=(16, 7))
        figure.tight_layout()

        # Верхний график - цены
        ax1 = figure.add_subplot(211)
        xs = range(len(prices))
        ys = prices
        graph_color = 'green' if ys[0] < ys[-1] else 'red'

        if current_state.graph_type == 'scatter':
            ax1.scatter(xs, ys, color=graph_color)
        elif current_state.graph_type == 'bar':
            ax1.bar(xs, ys, color=graph_color)
            ax1.set_ylim(min(ys) * 0.95, max(ys) * 1.05)
        else:
            ax1.plot(xs, ys, color=graph_color)

        ax1.set_title(f'Цена {current_state.coin}')

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

    def plot_sma(self, prices, window=20):
        """Рассчитывает и отображает Simple Moving Average"""
        close_prices = pd.Series(prices)
        sma = close_prices.rolling(window=window).mean()

        figure = plt.figure(figsize=(16, 7))
        ax = figure.add_subplot(111)

        xs = range(len(prices))
        ys = prices
        graph_color = 'green' if ys[0] < ys[-1] else 'red'

        ax.plot(xs, ys, label='Цена', color=graph_color)
        ax.plot(xs, sma, label=f'SMA {window}', color='orange')
        ax.set_title(f'Цена {current_state.coin} с SMA {window}')
        ax.legend()

        return figure

    def plot_ema(self, prices, window=20):
        """Рассчитывает и отображает Exponential Moving Average"""
        close_prices = pd.Series(prices)
        ema = close_prices.ewm(span=window, adjust=False).mean()

        figure = plt.figure(figsize=(16, 7))
        ax = figure.add_subplot(111)

        xs = range(len(prices))
        ys = prices
        graph_color = 'green' if ys[0] < ys[-1] else 'red'

        ax.plot(xs, ys, label='Цена', color=graph_color)
        ax.plot(xs, ema, label=f'EMA {window}', color='purple')
        ax.set_title(f'Цена {current_state.coin} с EMA {window}')
        ax.legend()

        return figure

    def plot_rsi(self, prices, window=14):
        """Рассчитывает и отображает Relative Strength Index"""
        close_prices = pd.Series(prices)
        delta = close_prices.diff()

        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        figure = plt.figure(figsize=(16, 7))
        figure.tight_layout()

        ax1 = figure.add_subplot(211)
        xs = range(len(prices))
        ys = prices
        graph_color = 'green' if ys[0] < ys[-1] else 'red'
        ax1.plot(xs, ys, color=graph_color)
        ax1.set_title(f'Цена {current_state.coin}')

        ax2 = figure.add_subplot(212)
        ax2.plot(rsi, label='RSI', color='blue')
        ax2.axhline(70, color='red', linestyle='--')
        ax2.axhline(30, color='green', linestyle='--')
        ax2.set_ylim(0, 100)
        ax2.set_title('RSI (14 дней)')
        ax2.legend()

        return figure

    def get_coin(self, coin, days=7):
        plt.close('all')
        cached_data = self.cache_for_prices.get(f'{coin}{days}')

        if cached_data:
            prices = cached_data
            print(f'Данные взяты из кэша, текущий размер кэша: {getsizeof(self.cache_for_prices)}')
        else:
            prices = coingecko.get_data_from_api(coin, days)
            self.cache_for_prices[f'{coin}{days}'] = prices
            print('Данные получены с api и добавлены в кэш')

        xs = range(len(prices))
        ys = prices


        price = Decimal(str(ys[-1]))
        price = price.quantize(Decimal("1.00"))

        self.coin_label.configure(text=f'{coin} | Текущая цена: {price}$')

        figure = plt.figure(figsize=(16, 7))
        figure.tight_layout()
        ax = figure.add_subplot(111)

        graph_color = 'green' if ys[0] < ys[-1] else 'red'


        if current_state.graph_type == 'candlestick':
            if days not in ohlc_avaible_timeframes:
                days = 7
                msg = CTkMessagebox(title="Ошибка ввода", message=f"Свечной график может отображать только недельный, месячный, полугодичный или годовой график.\nПо умолчанию выведен недельный график (7 дн.)",
                                icon="info", option_1="Отмена")
            ohlc = coingecko.get_ohlc_data_from_api(coin, days)
            data = []

            for i in ohlc:
                data.append([datetime.fromtimestamp(int(i[0]) / 1000), i[1], i[2], i[3], i[4]])

            df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
            df.set_index('Date', inplace=True)

            themes = {'dark':'nightclouds', 'light':'binance'}

            figure, ax = mpf.plot(
                df,
                type='candle',
                style=themes[current_state.theme],
                returnfig=True,
                figsize=(16, 7),
                volume=False,
            )

        elif current_state.graph_type == 'macd':
            figure = self.plot_macd(prices)
        elif current_state.graph_type == 'sma':
            figure = self.plot_sma(prices)
        elif current_state.graph_type == 'ema':
            figure = self.plot_ema(prices)
        elif current_state.graph_type == 'rsi':
            figure = self.plot_rsi(prices)
        else:
            ax.plot(xs, ys, color=graph_color)
        print(current_state.period)
        print(days)
        canvas = FigureCanvasTkAgg(figure, master=self.coin_frame)
        canvas.get_tk_widget().grid(row=1, column=0)

app = App()
app.mainloop()
