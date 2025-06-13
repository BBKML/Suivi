from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import Enseignant, Notification, SuiviEnseignement

User = get_user_model()

@receiver(post_save, sender=User)
def create_enseignant_for_user(sender, instance, created, **kwargs):
    if created:
        Enseignant.objects.create(user=instance)


@receiver(post_save, sender=SuiviEnseignement)
def notifier_admin_suivi_ajoute(sender, instance, created, **kwargs):
    """ Envoie une notification à l'admin lorsqu'un suivi est enregistré. """
    if created:  # Vérifie si c'est une nouvelle création
        admin_users = User.objects.filter(is_superuser=True)

        # Envoie un e-mail à l'admin
        send_mail(
            "🆕 Nouveau suivi enregistré",
            f"L'enseignant {instance.enseignant.nom} {instance.enseignant.prenom} a enregistré un suivi le {instance.date_cours}.",
            settings.DEFAULT_FROM_EMAIL,
            [admin.email for admin in admin_users if admin.email],
            fail_silently=True,
        )

        # Enregistrer une notification pour chaque admin
        for admin in admin_users:
            Notification.objects.create(
                user=admin,
                message=f"🔔 Nouvel enregistrement de suivi par {instance.enseignant.nom} {instance.enseignant.prenom}."
            )
