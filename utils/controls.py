import customtkinter
from PIL import Image

class IconButton(customtkinter.CTkButton):
    def __init__(self, master, icon_path, command, **kwargs):
        icon = customtkinter.CTkImage(Image.open(icon_path), size=(20, 20))
        super().__init__(master, image=icon, text="", command=command, **kwargs)

graphs_and_icons = {
            'линейный':"img/chart_w.png",
            'свечной':"img/candlestick_w.png",
            'macd':"img/macd_w.png",
            'sma':"img/sma_w.png",
            'ema':"img/ema_w.png",
            'rsi':"img/rsi_w.png",
            'bb':"img/macd_w.png",
        }