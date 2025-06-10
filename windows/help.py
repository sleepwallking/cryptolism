import customtkinter as ctk
import os

# Путь к файлу относительно текущего скрипта
HELP_WINDOW_TEXT_PATH = os.path.join(os.path.dirname(__file__), "../resources/text/help_window.txt")




class HelpWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Окно помощь")
        self.geometry("600x400")

        # Делаем окно модальным (необязательно)
        self.grab_set()

        # self.main_frame = ctk.CTkScrollableFrame(self)
        # self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        with open(HELP_WINDOW_TEXT_PATH, "r", encoding="utf-8") as f:
            help_window_text = f.read()




        self.help_textbox = ctk.CTkTextbox(self, wrap="word")
        self.help_textbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.help_textbox.insert("1.0", help_window_text)  # Вставляем текст
        self.help_textbox.configure(state="disabled")  # Если нужно запретить редактирование


        # Кнопка для закрытия окна
        self.close_button = ctk.CTkButton(
            self,
            text="Закрыть",
            command=self.destroy
        )
        self.close_button.pack(pady=10)

        # Обработчик закрытия окна
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Обработчик закрытия окна"""
        self.destroy()