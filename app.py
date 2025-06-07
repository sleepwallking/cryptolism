import customtkinter
import matplotlib.pyplot as plt
from panels.top_panel import TopPanel
from panels.left_panel import LeftPanel
from panels.center_panel import CenterPanel
from panels.right_panel import RightPanel
from settings.current_state import current_state

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

        # Инициализация панелей
        self.top_panel = TopPanel(self)
        self.left_panel = LeftPanel(self)
        self.center_panel = CenterPanel(self)
        self.right_panel = RightPanel(self)

        # Настройка сетки
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Установка начального состояния
        self.set_coin('bitcoin')


    def set_coin(self, coin):
        current_state.coin = coin
        self.center_panel.get_coin(current_state.coin, current_state.period)

    def set_period(self, days):
        current_state.period = days
        self.center_panel.get_coin(current_state.coin, current_state.period)

    def set_graph(self, graph):
        current_state.graph = graph
        self.center_panel.get_coin(current_state.coin, current_state.period)