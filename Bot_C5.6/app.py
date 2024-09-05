
import telebot # импортируем библиотеку для работы с телеграммом
from config import TOKEN #испортируем секреты из защищенного файла
#импортируем словарь с валютами и значениями для APi
from config import dic_value
from extensions import ConvertBotException,PushAPIConvertValue, BotMassage

# создаем объект бота,с который мы ранее создали
bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start или 'help'
@bot.message_handler(commands=['start','help'])
def start_help(message):
    bot.send_message(message.chat.id, f" {message.chat.username}, данный бот поможет Вам с конвертацией валют. \n"
                                      f"Для этого требуется ввести последовательно (в одну строку, через пробел) значения:\n"
                                      f"1) <имя валюты, цену которой хотите узнать> \n"
                                      f"2) <имя валюты, в которой надо узнать цену первой валюты>\n"
                                      f"3) <количество первой валюты>"
                                      f"\n"
                                      f"\n"
                                      f"Для получения информации списка валют укажите команду: /values ")


# Обрабатываются все сообщения, содержащие команды '/values'
@bot.message_handler(commands=['values'])
def values(message):
    str_val = "Бот поддерживает следующие валюты:"
    for key in dic_value.keys():
        str_val = '\n'.join((str_val, key, ))

    bot.send_message(message.chat.id, str_val)

@bot.message_handler(content_types=["text"])
def convert(message):
    try:
    # всю логику убрали
        my_bot = BotMassage(message)
        base, quote, amount = my_bot.get_params()

    except ConvertBotException as ex:
        bot.reply_to(message, f" Ошибка пользователя: \n{ex} \n Повторите ввод. Помошь: /help")
    except Exception as ex:
        bot.reply_to(message, f" Ошибка сервера: \n{ex} \n Обратитесь к администратору")
    else:
        bot.reply_to(message,f" Цена {amount} {quote} в {base} = {PushAPIConvertValue.get_price(base,quote,amount)}")

#запускаем бота
bot.polling(none_stop=True)