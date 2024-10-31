from .celery import app as celery_app
# насколько понял, в этом файле, то что будет запускать приложение сельдерея

__all__ = ('celery_app',)