import sys
from django.apps import AppConfig


class ContractsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contracts'

    def ready(self):
        # Prevent running keep-alive during management commands like makemigrations or collectstatic
        if 'manage.py' not in sys.argv:
            try:
                from .keep_alive import start_keep_alive
                start_keep_alive()
            except ImportError:
                pass
