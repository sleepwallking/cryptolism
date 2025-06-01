import os
import customtkinter
import matplotlib.pyplot as plt
import mplcursors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sys import getsizeof
from functools import partial
from decimal import Decimal
import pandas as pd
import mplfinance as mpf
from datetime import datetime
from CTkMessagebox import CTkMessagebox
from CTkToolTip import CTkToolTip
from settings.config import ohlc_timeframes, ohlc_themes, plot_functions
from utils.controls import IconButton, graphs_and_icons
from api.coingecko import CoingeckoAPI
from settings.current_state import current_state
from utils.helpers import truncate_string, get_date_from_period, validate_input
from utils.messages import CANDLE_CHART_ERROR_MSG, PRINT_OUT_INFO_MSG
from windows.help import HelpWindow

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
        self.font_bold = ("Segoe UI", 18, "normal")
        self.minsize(width=900, height=460)

        plt.style.use('dark_background')

        # Панели
        self.top_frame = customtkinter.CTkFrame(self, height=30)
        self.top_frame.grid(row=0, column=0, padx=self.padding, pady=(self.padding, 0), sticky="ew", columnspan=3)

        self.left_frame = customtkinter.CTkScrollableFrame(self, width=50)
        self.left_frame.grid(row=1, column=0, padx=(self.padding, 0), pady=self.padding, sticky='nsew')

        self.center_frame = customtkinter.CTkFrame(self)
        self.center_frame.grid(row=1, column=1, padx=self.padding, pady=self.padding, sticky="nsew")

        self.right_frame = customtkinter.CTkFrame(self)
        self.right_frame.grid(row=1, column=2, padx=(0, self.padding), pady=self.padding, sticky="nsew")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)



        # Верхняя панель (Настройки приложения)

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

            self.set_coin(current_state.coin)

        switch_var = customtkinter.StringVar(value="dark")
        self.switch = customtkinter.CTkSwitch(self.top_frame, text="Смена темы", command=switch_event,
                                        variable=switch_var, onvalue="dark", offvalue="light")
        self.switch.grid(row=0, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        def graph_paper_out():
            filename = f'{current_state.coin}_{current_state.period}_{current_state.graph}.png'

            plt.savefig(filename)
            os.startfile(filename, "print")

            filepath = os.path.join(os.getcwd(), filename)
            # print("Файл сохранён по пути:", filepath)

            print_out_info_msg = CTkMessagebox(title="Печать графика", message=PRINT_OUT_INFO_MSG+filepath,
                                                   icon="info", option_1="Отмена")


        self.paper_out_button = customtkinter.CTkButton(self.top_frame, command=graph_paper_out, text='Распечатать график')
        self.paper_out_button.grid(row=0, column=1, padx=self.padding, pady=self.padding, sticky="nsew")

        self.open_window_button = customtkinter.CTkButton(
            self.top_frame,
            text="Помощь",
            command=self.open_help_window
        )
        self.open_window_button.grid(row=0, column=2, padx=self.padding, pady=self.padding, sticky="nsew")

        self.help_window = None




        # Левая панель (Инструменты для графика)
        self.left_frame.grid_rowconfigure(0, weight=1)

        for graph_type in graphs_and_icons:
            self.graph_button = IconButton(self.left_frame, graphs_and_icons[graph_type], partial(self.set_graph, graph_type),
                                           width=self.icon_size, height=self.icon_size)
            self.graph_button.pack(padx=self.padding, pady=self.padding)
            self.graph_button_tooltip = CTkToolTip(self.graph_button, message=f"Отрисовка графика: {graph_type}")



        # Центральная панель (График)

        self.center_frame.grid_rowconfigure(0, weight=0)
        self.center_frame.grid_rowconfigure(1, weight=1)
        self.center_frame.grid_rowconfigure(2, weight=0)
        self.center_frame.grid_columnconfigure(0, weight=1)

        self.center_info_label = customtkinter.CTkLabel(self.center_frame, font=self.font_bold)
        self.center_info_label.grid(row=0, column=0, padx=self.padding+10, pady=self.padding, sticky="W")

        self.center_frame_buttons = customtkinter.CTkFrame(self.center_frame)
        self.center_frame_buttons.grid(row=2, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        for i in range(6):  # 6 колонок (4 кнопки + entry + button)
            self.center_frame_buttons.grid_columnconfigure(i, weight=1)

        for i, timeframe in enumerate(ohlc_timeframes):
            self.timeframe_button = customtkinter.CTkButton(self.center_frame_buttons, text=f"{timeframe} дн.",
                                                            command=partial(self.set_period, timeframe))
            self.timeframe_button.grid(row=0, column=i, padx=self.padding, pady=self.padding, sticky="nsew")

        vcmd = (self.register(validate_input), '%P')

        self.time_search_entry = customtkinter.CTkEntry(self.center_frame_buttons, placeholder_text="Ввести диапазон: ", validate="key", validatecommand=vcmd)
        self.time_search_entry.grid(row=0, column=4, padx=self.padding, pady=self.padding, sticky="nsew")

        self.time_search_button = customtkinter.CTkButton(self.center_frame_buttons, text="Найти", command=lambda: self.set_period(
            int(self.time_search_entry.get())))
        self.time_search_button.grid(row=0, column=5, padx=self.padding, pady=self.padding, sticky="nsew")



        # Правая панель (Список монет)

        self.right_frame.grid_rowconfigure(2, weight=1)

        self.coin_list_label = customtkinter.CTkLabel(self.right_frame, text='Список криптовалют')
        self.coin_list_label.grid(row=0, column=0)

        self.coin_search_entry = customtkinter.CTkEntry(self.right_frame, placeholder_text="Найти монету:")
        self.coin_search_entry.grid(row=1, column=0, padx=self.padding, pady=self.padding, sticky="nsew")
        self.coin_search_entry.bind("<KeyRelease>", self.filter_buttons)

        self.coins_list_frame = customtkinter.CTkScrollableFrame(self.right_frame, width=150)
        self.coins_list_frame.grid(row=2, column=0, padx=self.padding, pady=self.padding, sticky="nsew")

        coins = coingecko.get_coin_list()

        self.coins_buttons = []

        for i, coin in enumerate(coins):
            self.coin_button = customtkinter.CTkButton(self.coins_list_frame, text=truncate_string(coin),
                                                       command=partial(self.set_coin, coin))
            self.coin_button.grid(row=i, column=0, padx=self.padding, pady=self.padding)
            self.coins_buttons.append(self.coin_button)

        # Создание кэша и открытие графика

        self.cache_for_prices = {}  # {'bitcoin7': [price1, price2, price3, price..., pricex], 'ethereum7': [price1, price2, price3, price..., pricex], 'coinx': [etc...]}
        self.set_coin('bitcoin')


    def filter_buttons(self, event):
        search_text = self.coin_search_entry.get().lower()
        self.coins_list_frame._parent_canvas.yview_moveto(0)


        if not search_text:
            for i, btn in enumerate(self.coins_buttons):
                btn.grid(row=i, column=0, padx=self.padding, pady=self.padding)
            return


        visible_row = 0
        for btn in self.coins_buttons:
            btn_text = btn.cget("text").lower()

            if search_text in btn_text:
                btn.grid(row=visible_row, column=0, padx=self.padding, pady=self.padding)
                visible_row += 1
            else:
                btn.grid_remove()

    def open_help_window(self):
        """Открывает новое окно, если оно еще не открыто"""
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = HelpWindow(self)  # Создаем экземпляр нового окна
        else:
            self.help_window.focus()  # Если окно уже открыто, фокусируем его


    def set_graph(self, graph):
        current_state.graph = graph
        self.get_coin(current_state.coin, current_state.period)

    def set_coin(self, coin):
        current_state.coin = coin
        self.get_coin(current_state.coin, current_state.period)

    def set_period(self, days):
        current_state.period = days
        self.get_coin(current_state.coin, current_state.period)


    def get_coin(self, coin, days=7):
        plt.close('all')
        cache_key = f'{coin}{days}'
        prices = self.cache_for_prices.get(cache_key)

        if prices:
            print(f'Данные взяты из кэша, текущий размер кэша: {getsizeof(self.cache_for_prices)}')
        else:
            prices = self.cache_for_prices[cache_key] = coingecko.get_data_from_api(coin, days)
            print('Данные получены с api и добавлены в кэш')

        xs = range(len(prices))
        ys = prices
        price = Decimal(str(prices[-1])).quantize(Decimal("1.00"))
        figure = plt.figure(figsize=(18, 10), tight_layout=True)
        graph_color = 'green' if ys[0] < ys[-1] else 'red'


        if current_state.graph == "свечной":
            if days not in ohlc_timeframes:
                days = current_state.period = 7
                candle_chart_error_msg = CTkMessagebox(title="Ошибка ввода", message=CANDLE_CHART_ERROR_MSG,
                              icon="error", option_1="Отмена")

            ohlc = coingecko.get_ohlc_data_from_api(coin, days)
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

        plt.title(f'{current_state.coin} | {price}$')

        self.center_info_label.configure(
            text=f"период: {get_date_from_period(current_state.period)} | график: {current_state.graph}")

        canvas = FigureCanvasTkAgg(figure, master=self.center_frame)
        canvas.get_tk_widget().grid(row=1, column=0)



app = App()
app.mainloop()
