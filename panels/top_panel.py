import traceback
import customtkinter
import os
import matplotlib.pyplot as plt
from CTkMessagebox import CTkMessagebox
from settings.current_state import current_state
from windows.help import HelpWindow


class TopPanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, height=30)
        self.master = master
        self.grid(row=0, column=0, padx=master.padding, pady=(master.padding, 0), sticky="ew", columnspan=3)

        self.help_window = None
        self.setup_ui()

    def setup_ui(self):
        # Переключатель темы
        switch_var = customtkinter.StringVar(value="dark")
        self.switch = customtkinter.CTkSwitch(
            self,
            text="Смена темы",
            command=self.switch_event,
            variable=switch_var,
            onvalue="dark",
            offvalue="light"
        )
        self.switch.grid(row=0, column=0, padx=self.master.padding, pady=self.master.padding, sticky="nsew")

        # Кнопка печати
        self.paper_out_button = customtkinter.CTkButton(self, command=self.graph_paper_out, text='Распечатать график')
        self.paper_out_button.grid(row=0, column=1, padx=self.master.padding, pady=self.master.padding, sticky="nsew")

        # Кнопка помощи
        self.open_window_button = customtkinter.CTkButton(
            self,
            text="Помощь",
            command=self.open_help_window
        )
        self.open_window_button.grid(row=0, column=2, padx=self.master.padding, pady=self.master.padding, sticky="nsew")

    def switch_event(self):
        theme = self.switch._variable.get()
        customtkinter.set_appearance_mode(theme)
        plt.style.use('dark_background' if theme == 'dark' else 'default')
        current_state.theme = theme
        self.master.set_coin(current_state.coin)



    def graph_paper_out(self):
        filename = f'{current_state.coin}_{current_state.period}_{current_state.graph}.png'
        plt.savefig(filename)
        os.startfile(filename, "print")
        filepath = os.path.join(os.getcwd(), filename)
        CTkMessagebox(title="Печать графика", message=f"Файл сохранён по пути: {filepath}", icon="info",
                      option_1="Отмена")

    def open_help_window(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = HelpWindow(self.master)
        else:
            self.help_window.focus()