from django.apps import AppConfig


class SuivConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Suiv'

    def ready(self):
        import Suiv.signals

      # Import du fichier personnalisé


