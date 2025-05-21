# user/apps.py

from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'

    def ready(self):
        # 여기서는 아무것도 하지 않고, 다른 작업은 signals.py에서 처리
        pass
