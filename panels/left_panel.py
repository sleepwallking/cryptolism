import customtkinter
from functools import partial
from utils.controls import IconButton, graphs_and_icons
from CTkToolTip import CTkToolTip


class LeftPanel(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.grid(row=1, column=0, padx=(master.padding, 0), pady=master.padding, sticky='nsew')
        self.setup_ui()

    def setup_ui(self):
        self.grid_rowconfigure(0, weight=1)

        for graph_type in graphs_and_icons:
            graph_button = IconButton(
                self,
                graphs_and_icons[graph_type],
                partial(self.master.set_graph, graph_type),
                width=self.master.icon_size,
                height=self.master.icon_size
            )
            graph_button.pack(padx=self.master.padding, pady=self.master.padding)
            CTkToolTip(graph_button, message=f"Отрисовка графика: {graph_type}")