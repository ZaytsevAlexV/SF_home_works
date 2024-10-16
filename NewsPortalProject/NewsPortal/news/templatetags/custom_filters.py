from django import template

register = template.Library()
# Регистрируем наш фильтр  чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.

# справочник простых слов и их заменителей
DIC_BAD_WORDS = {
    'шефов':'ш****',
    'котор':'к******',
    'клиент' : 'к******',
    'Клиент' : 'К******',
}
@register.filter()
def censor(value):
    """
      value: подстрака в которой надо будет проверять плохие слова
     """
    for bad_words, norm_words in DIC_BAD_WORDS.items():
        value = value.replace(bad_words, norm_words)
        print
    return value


if __name__ == '__main__':
    print (censor("шефов которые приготовили бутер для клиентов  "))
