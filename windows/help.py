import customtkinter as ctk


class HelpWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("New Window")
        self.geometry("600x400")

        # Делаем окно модальным (необязательно)
        self.grab_set()

        # Добавляем виджеты в новое окно
        self.label = ctk.CTkLabel(self, text="Вспомогательное окно", font=("Arial", 16))
        self.label.pack(pady=20)

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