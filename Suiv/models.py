from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.utils import timezone

import os


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None  # Supprime le champ username d'AbstractUser
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()  # Associer le manager personnalisé

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else "Utilisateur"

# Table Grade
class Grade(models.Model):
    libelle_grade = models.CharField(max_length=100,unique=True, verbose_name="Libellé du grade")

    def __str__(self):
        return self.libelle_grade

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"

# Table Statut
class Statut(models.Model):
    libelle_statut = models.CharField(max_length=100,unique=True, verbose_name="Libellé du statut")

    def __str__(self):
        return self.libelle_statut

    class Meta:
        verbose_name = "Statut"
        verbose_name_plural = "Statuts"

# Table Année Académique

   
# Table Niveau d'étude
class NiveauEtude(models.Model):
    libelle_niveau = models.CharField(max_length=100,unique=True, verbose_name="Libellé du niveau")

    def __str__(self):
        return self.libelle_niveau

    class Meta:
        verbose_name = "Niveau d'étude"
        verbose_name_plural = "Niveaux d'étude"

# Table Semestre
class Semestre(models.Model):
    libelle_semestre = models.CharField(max_length=100,unique=True, verbose_name="Libellé du semestre")

    def __str__(self):
        return self.libelle_semestre

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"

# Table Salle
class Salle(models.Model):
    nom_salle = models.CharField(max_length=100,unique=True, verbose_name="Nom de la salle")
    capacite = models.IntegerField(default=30, verbose_name="Capacité de la salle")

    def __str__(self):
        return self.nom_salle

    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"


# Modèle Enseigner
class Enseigner(models.Model):
    enseignant = models.ForeignKey(
        'Enseignant', on_delete=models.CASCADE, verbose_name="Enseignant", related_name="cours_enseignes"
    )
    cours = models.ForeignKey(
        'Cours', on_delete=models.CASCADE, verbose_name="Cours", related_name="enseignants_cours"  # Change here
    )

    def __str__(self):
        return f"{self.enseignant.nom} {self.enseignant.prenom} enseigne {self.cours.code_cours}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['enseignant', 'cours'], name='unique_enseignant_cours')
        ]
        verbose_name = "Enseignement"
        verbose_name_plural = "Enseignements"

# Table Cours
class Cours(models.Model):
    code_cours = models.CharField(max_length=50, unique=True, verbose_name="Code du cours")
   
    intitule_ue = models.CharField(max_length=255, verbose_name="Intitulé de l'UE")
    intitule_ecue = models.CharField(max_length=255, verbose_name="Intitulé de l'ECUE")
    niveau = models.ForeignKey(NiveauEtude, on_delete=models.CASCADE, verbose_name="Niveau d'étude", related_name="cours")
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, verbose_name="Semestre", related_name="cours")
    parcours = models.CharField(max_length=255, verbose_name="Parcours")
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Salle", related_name="cours")
    total_heures = models.FloatField(verbose_name="Total des heures", default=0)  # Ajout du champ total_heures

    def __str__(self):
        return f"{self.code_cours} - {self.intitule_ue}"

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"

        

User = get_user_model() 

class Enseignant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='enseignant', null=True, blank=True)
    genre = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin'), ('A', 'Autre')], null=True, blank=True)
    matricule = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Matricule",
        help_text="Identifiant unique de l'enseignant",
    )
    cours = models.ManyToManyField(Cours, related_name="enseignants", blank=True)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE, verbose_name="Grade", related_name="enseignants")
    statut = models.ForeignKey('Statut', on_delete=models.CASCADE, verbose_name="Statut", related_name="enseignants")
    structure_origine = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Structure d'origine"
    )
    contact = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Contact",
        help_text="Format : '+999999999'. Jusqu'à 15 chiffres.",
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Le format du numéro de contact est invalide."
            )
        ],
    )
    
    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"

    @property
    def nom(self):
        return self.user.last_name if self.user else ""

    @property
    def prenom(self):
        return self.user.first_name if self.user else ""

    @property
    def email(self):
        return self.user.email if self.user else ""

    def __str__(self):
        return f"{self.nom} {self.prenom}"



class GroupeEtudiant(models.Model):
    nom_groupe = models.CharField(max_length=100, verbose_name="Nom du groupe")
    niveau = models.ForeignKey(NiveauEtude, on_delete=models.CASCADE, verbose_name="Niveau d'étude")
    parcours = models.CharField(max_length=255, verbose_name="Parcours")
    effectif = models.PositiveIntegerField(default=0, blank=True, verbose_name="Effectif")
    
    def __str__(self):
       return f"{self.nom_groupe} - {self.parcours} ({self.niveau.libelle_niveau})"
    class Meta:
        verbose_name = "Groupe d'étudiants"
        verbose_name_plural = "Groupes d'étudiants"
        constraints = [
            models.UniqueConstraint(fields=['nom_groupe', 'niveau', 'parcours'], name='unique_groupe_niveau_parcours')
        ]



class SuiviEnseignement(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, verbose_name="Cours", related_name="suivis")
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE,blank=True , verbose_name="Enseignant", related_name="suivis")
    date_cours = models.DateField(verbose_name="Date du cours")
    horaire_debut = models.TimeField(verbose_name="Heure de début")
    horaire_fin = models.TimeField(verbose_name="Heure de fin")
    salle_de_cours = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Salle de cours", related_name="suivis")
    heures_cm = models.FloatField(default=0,verbose_name="Nombre d'heures CM")
    heures_td = models.FloatField(default=0,verbose_name="Nombre d'heures TD")
    heures_tp = models.FloatField(default=0,verbose_name="Nombre d'heures TP")
    groupes = models.ManyToManyField(GroupeEtudiant, verbose_name="Groupes d'étudiants", blank=True, related_name="suivis")
    total_heures_cumulees = models.FloatField(verbose_name="Total des heures cumulées", editable=False)
    emargement_delegue = models.BooleanField(default=False, verbose_name="Émargement délégué")
    annee_academique = models.CharField(max_length=4, default=str(timezone.now().year))
    
    def status_emargement(self):
       return "Oui" if self.emargement_delegue else "Non"

    # Reste du code inchangé...

    def clean(self):
        """Validation des valeurs avant l'enregistrement."""
        if not self.enseignant:
            raise ValidationError("L'enseignant doit être renseigné.")
        if any(h < 0 for h in [self.heures_cm, self.heures_td, self.heures_tp]):
            raise ValidationError("Les heures ne peuvent pas être négatives.")
        if self.horaire_debut and self.horaire_fin and self.horaire_debut >= self.horaire_fin:
            raise ValidationError("L'heure de fin doit être postérieure à l'heure de début.")

    
    def save(self, *args, **kwargs):
        """ Sauvegarde avec validation des données """
        self.clean()  # Appelle clean() avant de sauvegarder
        
        # Calcul des heures cumulées
        self.total_heures_cumulees = max(self.heures_cm, 0) + max(self.heures_td, 0) + max(self.heures_tp, 0)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Suivi du {self.date_cours} - {self.cours.code_cours}"

    class Meta:
        verbose_name = "Suivi de l'enseignement"
        verbose_name_plural = "Suivis des enseignements"



class AnneeAcademique(models.Model):
    annee = models.CharField(max_length=10)
    enseignants = models.ManyToManyField(Enseignant, related_name="annees_academiques", blank=True)
    suivis = models.ManyToManyField(SuiviEnseignement, related_name="annees_academiques", blank=True)
    class Meta:
            verbose_name = "Année académique"
            verbose_name_plural = "Années académiques"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"