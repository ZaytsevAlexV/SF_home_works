#from django.http import HttpResponse
#Первый, инициализирующий, определяет метод get_response
#, а во втором можно внедрить непосредственно код обработки запроса до представления и,
# соответственно, обработки ответа на запрос после его формирования.
import logging



class ErrorGenerator:
    def __init__(self, get_response):
        self.get_response = get_response

    # код, выполняемый до формирования ответа (или другого middleware)
    def __call__(self, request):
        logger = logging.getLogger('django.request')
        logger_sec = logging.getLogger('django.security')
        # код, выполняемый до формирования ответа (или другого middleware)
        # ...
        logger_sec.warning("Предупреждение безопасности")

        response = self.get_response(request)
        # код, выполняемый после формирования запроса (или нижнего слоя)
        #...
        logger.debug("Уровень отладки-debug")
        logger.info("Уровень информирования-info")
        logger.warning("Уровень Предупреждения-warning")
        logger.error("Уровень ошибки-error")
        logger.critical("Уровень критичной ошибки-critical")

        return response
