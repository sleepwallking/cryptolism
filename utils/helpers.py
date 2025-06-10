from datetime import datetime, timedelta
from CTkMessagebox import CTkMessagebox
from settings.config import coin_name_max_lenght
from utils.messages import EMPTY_FIELD_ERROR_MSG, WRONG_VAR_ERROR_MSG


def truncate_string(text):
    if len(text) > coin_name_max_lenght:
        return text[:coin_name_max_lenght - 3] + "..."
    else:
        return text

def get_date_from_period(days):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    return f"{days} дн. [{start_date} - {end_date}]"


def validate_input(text):
    if not text:
        CTkMessagebox(title="Ошибка ввода", message=EMPTY_FIELD_ERROR_MSG, icon="warning", option_1="Отмена")
        return None

    try:
        number = int(text)
        if 1 <= number <= 365:
            return number # Подходящее под условия значение возвращается сразу
    except ValueError:
        pass

    CTkMessagebox(title="Ошибка ввода", message=WRONG_VAR_ERROR_MSG, icon="warning", option_1="Отмена")
    return None


