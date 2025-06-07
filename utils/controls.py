import customtkinter
from PIL import Image

class IconButton(customtkinter.CTkButton):
    def __init__(self, master, icon_path, command, **kwargs):
        icon = customtkinter.CTkImage(Image.open(icon_path), size=(20, 20))
        super().__init__(master, image=icon, text="", command=command, **kwargs)

graphs_and_icons = {
            'линейный':"img/chart.png",
            'свечной':"img/candlestick.png",
            'macd':"img/macd.png",
            'sma':"img/sma.png",
            'ema':"img/ema.png",
            'rsi':"img/rsi.png",
            'bb':"img/macd.png",
        }