from datetime import datetime, timedelta

from settings.config import coin_name_max_lenght

def truncate_string(text):
    if len(text) > coin_name_max_lenght:
        return text[:coin_name_max_lenght - 3] + "..."
    else:
        return text

def get_date_from_period(days):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    return f"{days} дн. [{start_date} - {end_date}]"


# def check_entry_int_value(entry):
#     try:
#         value = int(entry.get())
#         if 0 < value < 365:
#             return value
#         else:
#             msg = CTkMessagebox(title="Ошибка ввода", message=f"Введенное значение должно быть больше 0 и меньше 365",
#                                 icon="info", option_1="Отмена")
#     except ValueError:
#         # Обработка ошибки, например, установка значения по умолчанию или сообщение пользователю
#         print("Пожалуйста, введите целое число")
#         return 0  # или другое значение по умолчанию