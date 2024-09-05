import requests
import json
from config import dic_value

# класс с обработчиком ошибок

# п 9 Текст любой ошибки с указанием типа ошибки должен отправляться пользователю в сообщения.
class ConvertBotException(Exception):
    pass
# п10 Для отправки запросов к API описать класс со статическим методом get_price(),

class BotMassage:
    def __init__(self, massage):
        self.massage = massage
    # Метод который из сообщения бота, выдает толькно нужные значения
    def get_params(self):
        messege_list = self.massage.text.split(" ")
        #print(type(messege_list))
        messege_list = list(map( lambda x: x.lower(), self.massage.text.split(" ")))
        if len(messege_list) != 3:
            raise ConvertBotException("Количество параметров не равно 3ем")
        if messege_list[2].isdigit() is not True:
            raise ConvertBotException(f"Не верно указано значение числа - {messege_list[2]} ")
        try:
            if dic_value[messege_list[0]] and dic_value[messege_list[1]]:
                pass
        except KeyError as keyE:
            raise ConvertBotException(f"К сожалению, пока мы не обрабатывам такую валюту {keyE}")
        else:
            base, quote, amount = messege_list

        return  base, quote, amount

# Класс с стат методом
class PushAPIConvertValue:
    @staticmethod
    def get_price(base,quote,amount):
        r_dic = {}
        r = requests.get(
            f'https://v6.exchangerate-api.com/v6/10ce6d17fdc7502ea6ea408b/pair/{dic_value[quote]}/{dic_value[base]}/{amount}')
        r_dic = json.loads(r.content)
        return r_dic['conversion_result']
