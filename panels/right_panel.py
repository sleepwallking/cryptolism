import customtkinter
from functools import partial
from utils.helpers import truncate_string
from api.coingecko import CoingeckoAPI

class RightPanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=1, column=2, padx=(0, master.padding), pady=master.padding, sticky="nsew")
        self.coingecko = CoingeckoAPI()
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(2, weight=1)

        # Заголовок
        self.coin_list_label = customtkinter.CTkLabel(self, text='Список криптовалют')
        self.coin_list_label.grid(row=0, column=0)

        # Поле поиска
        self.coin_search_entry = customtkinter.CTkEntry(self, placeholder_text="Найти монету:")
        self.coin_search_entry.grid(row=1, column=0, padx=self.master.padding, pady=self.master.padding, sticky="nsew")
        self.coin_search_entry.bind("<KeyRelease>", self.filter_buttons)

        # Список монет
        self.coins_list_frame = customtkinter.CTkScrollableFrame(self, width=150)
        self.coins_list_frame.grid(row=2, column=0, padx=self.master.padding, pady=self.master.padding, sticky="nsew")

        # Кнопки монет
        self.coins_buttons = []
        coins = self.coingecko.get_coin_list()

        for i, coin in enumerate(coins):
            coin_button = customtkinter.CTkButton(
                self.coins_list_frame,
                text=truncate_string(coin),
                command=partial(self.master.set_coin, coin)
            )
            coin_button.grid(row=i, column=0, padx=self.master.padding, pady=self.master.padding)
            self.coins_buttons.append(coin_button)

    def filter_buttons(self, event):
        search_text = self.coin_search_entry.get().lower()
        self.coins_list_frame._parent_canvas.yview_moveto(0)

        visible_row = 0
        for btn in self.coins_buttons:
            matches_search = not search_text or search_text in btn.cget("text").lower()

            if matches_search:
                btn.grid(row=visible_row, column=0, padx=self.master.padding, pady=self.master.padding)
                visible_row += 1
            else:
                btn.grid_remove()