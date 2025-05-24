import os
import json
import requests
from dotenv import load_dotenv
from CTkMessagebox import CTkMessagebox

load_dotenv()


class CoingeckoAPI:
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")
        }

    def get_data_from_api(self, coin, days, currency = 'usd'):
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency={currency}&days={days}"

            response = requests.get(url, headers=self.headers)
            json_response = json.loads(response.text)
            prices = [i[1] for i in json_response['prices']]

            return prices

        except Exception:
            msg = CTkMessagebox(title="Ошибка!", message="Данный отрезок времени недоступен",
                                icon="warning", option_1="Отмена")



    
    def get_ohlc_data_from_api(self, coin, days, currency = 'usd'):
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/ohlc?vs_currency={currency}&days={days}"

        response = requests.get(url, headers=self.headers)
        json_response = json.loads(response.text)
        

        ohlc = [i for i in json_response]

        return ohlc