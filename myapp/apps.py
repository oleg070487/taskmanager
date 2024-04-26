from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    # def ready(self):
    #     from .tasks import schedule_notifications
    #     import threading
    #
    #     # Запуск планировщика в отдельном потоке
    #     t = threading.Thread(target=schedule_notifications)
    #     t.start()
