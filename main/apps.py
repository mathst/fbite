from django.apps import AppConfig


class MeuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals  # Importa o módulo signals ao inicializar o aplicativo
