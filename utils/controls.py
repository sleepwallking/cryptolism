import customtkinter
from PIL import Image

class IconButton(customtkinter.CTkButton):
    def __init__(self, master, icon_path, command, **kwargs):
        icon = customtkinter.CTkImage(Image.open(icon_path), size=(20, 20))
        super().__init__(master, image=icon, text="", command=command, **kwargs)



graphs_and_icons = {
            'линейный':"resources/img/chart.png",
            'свечной':"resources/img/candlestick.png",
            'macd':"resources/img/macd.png",
            'sma':"resources/img/sma.png",
            'ema':"resources/img/ema.png",
            'rsi':"resources/img/rsi.png",
            'bb':"resources/img/bb.png",
        }