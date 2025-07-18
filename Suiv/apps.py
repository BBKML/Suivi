from django.apps import AppConfig
import sys


class SuivConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Suiv'

    def ready(self):
        # Import du fichier personnalisé
        import Suiv.signals

        # Création automatique du superadmin si aucun n'existe
        if any(cmd in sys.argv for cmd in ['runserver', 'migrate', 'createsuperuser', 'shell']):
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(is_superuser=True).exists():
                User.objects.create_superuser(
                    username="admin",
                    email="admin@example.com",
                    password="adminpassword"
                )


