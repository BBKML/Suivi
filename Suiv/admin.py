# Modification des titres de l'interface d'administration Django
from django.contrib import admin
from django.http import HttpResponse
import csv
from django.core.exceptions import PermissionDenied
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import path, reverse
from django.utils.html import format_html
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils import timezone
from django import forms
from Suiv.models import (
    CustomUser, Grade, Statut, AnneeAcademique, Enseignant, 
    NiveauEtude, Semestre, Salle, Cours, SuiviEnseignement, Enseigner, GroupeEtudiant
)

User = get_user_model()
admin.site.site_header = "UNA"
admin.site.site_title = "Administration du site"
admin.site.index_title = "Bienvenue sur le tableau de bord"


# Mixin pour les boutons d'action (modifier et supprimer)
class ActionButtonsMixin:
    """Mixin pour ajouter des boutons d'action aux modèles admin"""
    
    def actions_buttons(self, obj):
        """Affiche les boutons modifier et supprimer"""
        buttons = []
        
        # Bouton Modifier - on suppose que l'utilisateur a les permissions de base
        change_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk])
        buttons.append(
            f'<a class="button btn btn-warning btn-sm" href="{change_url}" title="Modifier">'
            f'<i class="fas fa-edit"></i></a>'
        )
        
        # Bouton Supprimer - on suppose que l'utilisateur a les permissions de base
        delete_url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_delete', args=[obj.pk])
        buttons.append(
            f'<a class="button btn btn-danger btn-sm" href="{delete_url}" title="Supprimer" '
            f'onclick="return confirm(\'Êtes-vous sûr de vouloir supprimer cet élément ?\')">'
            f'<i class="fas fa-trash"></i></a>'
        )
        
        return format_html(' '.join(buttons)) if buttons else "Aucune action disponible"
    
    actions_buttons.short_description = "Actions"
    actions_buttons.allow_tags = True


# Mixin pour les fonctionnalités d'impression - évite la duplication de code
class PrintableMixin:
    """Mixin pour ajouter des fonctionnalités d'impression aux modèles admin"""
    
    print_template = None  # À définir dans les classes enfants
    
    def imprimer(self, obj):
        return format_html(
            '<a class="button btn btn-primary" href="{}">'
            '<i class="fas fa-print"></i> Imprimer</a>',
            reverse(f'admin:{self.get_print_url_name()}', args=[obj.pk])
        )
    
    imprimer.short_description = "Impression"
    
    def get_print_url_name(self):
        """Retourne le nom de l'URL pour l'impression"""
        return f'imprimer_{self.model._meta.model_name}'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                f'imprimer/{self.model._meta.model_name}/<int:object_id>/', 
                self.admin_site.admin_view(self.print_view), 
                name=self.get_print_url_name()
            ),
        ]
        return custom_urls + urls
    
    def print_view(self, request, object_id):
        obj = get_object_or_404(self.model, pk=object_id)
        
        # Vérification des permissions
        if not self.has_view_permission(request, obj):
            messages.error(request, "Vous n'avez pas les permissions nécessaires pour effectuer cette action.")
            return redirect('admin:index')
            
        context = {self.model._meta.model_name: obj}
        return render(request, self.print_template, context)


# Personnalisation de l'interface d'administration des utilisateurs
class CustomUserAdmin(ActionButtonsMixin, UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined', 'actions_buttons')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_per_page = 15
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    
    actions = ['activer_utilisateurs', 'desactiver_utilisateurs']
    
    def activer_utilisateurs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} utilisateur(s) activé(s) avec succès.")
    activer_utilisateurs.short_description = "Activer les utilisateurs sélectionnés"
    
    def desactiver_utilisateurs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} utilisateur(s) désactivé(s) avec succès.")
    desactiver_utilisateurs.short_description = "Désactiver les utilisateurs sélectionnés"


# Enregistrement des classes d'administration pour les modèles simples
@admin.register(Grade)
class GradeAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ("libelle_grade", "get_enseignants_count", "actions_buttons")
    search_fields = ("libelle_grade",)
    list_per_page = 10
    
    def get_enseignants_count(self, obj):
        """Affiche le nombre d'enseignants pour chaque grade"""
        return obj.enseignants.count()
    get_enseignants_count.short_description = "Nombre d'enseignants"


@admin.register(Statut)
class StatutAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ("libelle_statut", "get_enseignants_count", "actions_buttons")
    search_fields = ("libelle_statut",)
    
    def get_enseignants_count(self, obj):
        """Affiche le nombre d'enseignants pour chaque statut"""
        return obj.enseignants.count()
    get_enseignants_count.short_description = "Nombre d'enseignants"


@admin.register(AnneeAcademique)
class AnneeAcademiqueAdmin(ActionButtonsMixin, admin.ModelAdmin):
   
    list_display = ("annee", "get_enseignants_count", "get_suivis_count", "actions_buttons")
    search_fields = ("annee",)
    list_per_page = 5
    
    def get_enseignants_count(self, obj):
        """Affiche le nombre d'enseignants pour chaque année académique"""
        return obj.enseignants.count()
    get_enseignants_count.short_description = "Nombre d'enseignants"
    
    def get_suivis_count(self, obj):
        """Affiche le nombre de suivis pour chaque année académique"""
        return obj.suivis.count()
    get_suivis_count.short_description = "Nombre de suivis"


@admin.register(NiveauEtude)
class NiveauEtudeAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ("libelle_niveau", "get_cours_count", "actions_buttons")
    search_fields = ("libelle_niveau",)
    list_per_page = 5
    
    def get_cours_count(self, obj):
        """Affiche le nombre de cours pour chaque niveau d'étude"""
        return obj.cours.count()
    get_cours_count.short_description = "Nombre de cours"


@admin.register(Semestre)
class SemestreAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ("libelle_semestre", "get_cours_count", "actions_buttons")
    search_fields = ("libelle_semestre",)
    
    def get_cours_count(self, obj):
        """Affiche le nombre de cours pour chaque semestre"""
        return obj.cours.count()
    get_cours_count.short_description = "Nombre de cours"


@admin.register(Salle)
class SalleAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ("nom_salle", "capacite", "get_cours_count", "actions_buttons")
    search_fields = ("nom_salle",)
    list_filter = ("capacite",)
    list_per_page = 10
    
    def get_cours_count(self, obj):
        """Affiche le nombre de cours affectés à chaque salle"""
        return obj.cours.count()
    get_cours_count.short_description = "Nombre de cours"


@admin.register(Cours)
class CoursAdmin(PrintableMixin, ActionButtonsMixin, admin.ModelAdmin):
    list_display = ("code_cours", "intitule_ue", "intitule_ecue", "niveau", "semestre", "parcours", "salle", "total_heures", "get_enseignants_count", "actions_buttons")
    search_fields = ("code_cours", "intitule_ue", "intitule_ecue", "parcours")
    list_filter = ("niveau", "semestre", "parcours", "salle")
    list_per_page = 15
    ordering = ("code_cours",)
    print_template = 'admin/cours/print_multiple_cours.html'
    actions = ['exporter_cours_csv', 'imprimer_selection_cours']
    
    def has_change_permission(self, request, obj=None):
        if obj and hasattr(request.user, 'enseignant') and obj.enseignants.filter(id=request.user.enseignant.id).exists():
            # Si l'enseignant essaie de modifier un cours qui lui a été attribué, on bloque la modification
            self.message_user(request, "Modification impossible : vous ne pouvez pas modifier ce cours qui vous a été attribué.", level=messages.ERROR)
            return False
        
        return super().has_change_permission(request, obj)

    def get_enseignants_count(self, obj):
        """Affiche le nombre d'enseignants assignés à chaque cours"""
        return obj.enseignants_cours.count()  # Utiliser le related_name défini dans le modèle Enseigner

  
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser and hasattr(request.user, 'enseignant'):
            queryset = queryset.filter(enseignants=request.user.enseignant)
        return queryset

    def exporter_cours_csv(self, request, queryset):
        """Exportation des cours sélectionnés en CSV."""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="liste_cours.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Code', 'UE', 'ECUE', 'Niveau', 'Semestre', 'Parcours', 'Salle', 'Heures'
        ])

        for cours in queryset:
            writer.writerow([
                cours.code_cours,
                cours.intitule_ue,
                cours.intitule_ecue,
                cours.niveau.libelle_niveau if cours.niveau else '',
                cours.semestre.libelle_semestre if cours.semestre else '',
                cours.parcours,
                cours.salle.nom_salle if cours.salle else '',
                cours.total_heures
            ])
        return response
    exporter_cours_csv.short_description = "Exporter les cours en CSV"

    def imprimer_selection_cours(self, request, queryset):
        """Imprimer les cours sélectionnés."""
        if not queryset:
            self.message_user(request, "Aucun cours sélectionné pour l'impression.")
            return

        context = {
            'cours_list': queryset,
            'today': timezone.now(),
            'title': 'Impression des cours'
        }
        return render(request, 'admin/cours/print_multiple_cours.html', context)
    imprimer_selection_cours.short_description = "Imprimer les cours sélectionnés"


@admin.register(Enseignant)
class EnseignantAdmin(PrintableMixin, ActionButtonsMixin, admin.ModelAdmin):
    list_display = ('matricule', 'nom', 'prenom', 'email', 'grade', 'statut', 'structure_origine', 'contact', 'genre', 'get_cours_count', 'actions_buttons')
    search_fields = ('matricule', 'user__email', 'user__last_name', 'user__first_name', 'contact')
    list_filter = ('grade', 'statut',  'genre')
    ordering = ('user__last_name', 'user__first_name')
    print_template = 'admin/enseignant/print.html'
    actions = ['exporter_enseignants_csv', 'imprimer_selection_enseignants']
    
    def get_cours_count(self, obj):
        """Affiche le nombre de cours enseignés"""
        return obj.cours_enseignes.count()
    get_cours_count.short_description = "Cours enseignés"

    def nom(self, obj):
        return obj.user.last_name if obj.user else ""

    def prenom(self, obj):
        return obj.user.first_name if obj.user else ""

    def email(self, obj):
        return obj.user.email if obj.user else ""

    nom.admin_order_field = 'user__last_name'
    prenom.admin_order_field = 'user__first_name'
    email.admin_order_field = 'user__email'
    
    def exporter_enseignants_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="liste_enseignants.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Matricule', 'Nom', 'Prénom', 'Email', 'Grade', 'Statut', 
            'Structure d\'origine', 'Contact',  'Genre',
            'Nombre de cours'
        ])
        
        for enseignant in queryset:
            writer.writerow([
                enseignant.matricule,
                enseignant.nom,
                enseignant.prenom,
                enseignant.email,
                enseignant.grade.libelle_grade if enseignant.grade else '',
                enseignant.statut.libelle_statut if enseignant.statut else '',
                enseignant.structure_origine or '',
                enseignant.contact,
                enseignant.get_genre_display(),
                enseignant.cours_enseignes.count()
            ])
        return response
    exporter_enseignants_csv.short_description = "Exporter les enseignants sélectionnés en CSV"

    def imprimer_selection_enseignants(self, request, queryset):
        """Imprimer les enseignants sélectionnés."""
        if not queryset:
            self.message_user(request, "Aucun enseignant sélectionné pour l'impression.")
            return

        context = {
            'enseignant_list': queryset,
            'today': timezone.now(),
            'title': 'Impression des enseignants'
        }
        return render(request, 'admin/enseignant/print.html', context)
    imprimer_selection_enseignants.short_description = "Imprimer les enseignants sélectionnés"



class SuiviEnseignementBaseMixin:
    """Mixin de base pour les classes de SuiviEnseignement"""
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser and hasattr(request.user, 'enseignant'):
            queryset = queryset.filter(enseignant=request.user.enseignant)
        return queryset
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filtre les cours disponibles pour l'enseignant connecté"""
        if db_field.name == "cours" and hasattr(request.user, 'enseignant') and not request.user.is_superuser:
            enseignant = request.user.enseignant
            cours_ids = Enseigner.objects.filter(enseignant=enseignant).values_list('cours_id', flat=True)
            
            if not cours_ids:
                kwargs["queryset"] = Cours.objects.none()
                if request.method == "GET":  # Éviter les messages multiples lors de la soumission
                    messages.warning(request, "Vous n'êtes associé à aucun cours. Veuillez contacter l'administrateur.")
            else:
                kwargs["queryset"] = Cours.objects.filter(id__in=cours_ids)
        
        if db_field.name == "enseignant" and hasattr(request.user, 'enseignant') and not request.user.is_superuser:
            kwargs["queryset"] = Enseignant.objects.filter(id=request.user.enseignant.id)
            kwargs["initial"] = request.user.enseignant
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def has_change_permission(self, request, obj=None):
        if obj and obj.emargement_delegue and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.emargement_delegue and not request.user.is_superuser:
            messages.warning(request, "Modification impossible : le délégué a déjà signé.")
        return super().get_form(request, obj, **kwargs)
        
    def has_delete_permission(self, request, obj=None):
        if obj and obj.emargement_delegue:
            if not request.user.is_superuser:
                messages.warning(request, "Suppression impossible : le délégué a déjà signé.")
                return False
        return super().has_delete_permission(request, obj)

    def save_form(self, request, form, change):
        obj = form.save(commit=False)
        
        # Assigner automatiquement l'enseignant connecté
        if not request.user.is_superuser and hasattr(request.user, 'enseignant'):
            obj.enseignant = request.user.enseignant
        
        # Vérifier si l'enseignant est associé au cours avant de sauvegarder
        if not request.user.is_superuser and obj.cours:
            if not Enseigner.objects.filter(enseignant=obj.enseignant, cours=obj.cours).exists():
                form.add_error('cours', "Vous n'êtes pas autorisé à créer un suivi pour ce cours.")
                return form.save(commit=False)
        
        # Validation des horaires
        if obj.horaire_debut and obj.horaire_fin and obj.horaire_debut >= obj.horaire_fin:
            form.add_error('horaire_fin', "L'heure de fin doit être postérieure à l'heure de début.")
            return form.save(commit=False)
            
        return super().save_form(request, form, change)


# Mixin pour les boutons d'export et d'impression
class ExportPrintButtonsMixin:
    """Mixin pour ajouter des boutons d'export et d'impression aux modèles admin"""
    
    def export_print_buttons(self, obj):
        """Affiche les boutons exporter et imprimer"""
        buttons = []
        export_url = reverse(f'admin:{self.model._meta.model_name}_export_csv', args=[obj.pk])
        buttons.append(
            f'<a class="button btn btn-success btn-sm" href="{export_url}" title="Exporter en CSV">'
            f'<i class="fas fa-file-csv"></i></a>'
        )
        print_url = reverse(f'admin:{self.model._meta.model_name}_print', args=[obj.pk])
        buttons.append(
            f'<a class="button btn btn-info btn-sm" href="{print_url}" title="Imprimer">'
            f'<i class="fas fa-print"></i></a>'
        )
        return format_html(' '.join(buttons)) if buttons else "Aucune action disponible"
    
    export_print_buttons.short_description = "Export/Impression"
    export_print_buttons.allow_tags = True
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                f'export-csv/{self.model._meta.model_name}/<int:object_id>/', 
                self.admin_site.admin_view(self.export_csv_view), 
                name=f'{self.model._meta.model_name}_export_csv'
            ),
            path(
                f'print/{self.model._meta.model_name}/<int:object_id>/', 
                self.admin_site.admin_view(self.print_view), 
                name=f'{self.model._meta.model_name}_print'
            ),
        ]
        return custom_urls + urls
    
    def export_csv_view(self, request, object_id):
        """Vue pour l'export CSV d'un objet individuel"""
        obj = get_object_or_404(self.model, pk=object_id)
        
        # Vérification des permissions
        if not self.has_view_permission(request, obj):
            messages.error(request, "Vous n'avez pas les permissions nécessaires pour effectuer cette action.")
            return redirect('admin:index')
        
        # Créer un queryset avec un seul objet
        queryset = self.model.objects.filter(pk=object_id)
        
        # Appeler la méthode d'export existante
        if hasattr(self, 'exporter_suivi_csv'):
            return self.exporter_suivi_csv(request, queryset)
        else:
            # Export par défaut
            response = HttpResponse(content_type='text/csv', charset='utf-8')
            response['Content-Disposition'] = f'attachment; filename="{obj._meta.model_name}_{object_id}.csv"'
            
            writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # Écrire les en-têtes et données
            writer.writerow(['ID', 'Nom'])
            writer.writerow([obj.pk, str(obj)])
            
            return response
    
    def print_view(self, request, object_id):
        """Vue pour l'impression d'un objet individuel"""
        obj = get_object_or_404(self.model, pk=object_id)
        
        # Vérification des permissions
        if not self.has_view_permission(request, obj):
            messages.error(request, "Vous n'avez pas les permissions nécessaires pour effectuer cette action.")
            return redirect('admin:index')
        
        # Créer un queryset avec un seul objet
        queryset = self.model.objects.filter(pk=object_id)
        
        # Appeler la méthode d'impression existante
        if hasattr(self, 'imprimer_selection_suivis'):
            return self.imprimer_selection_suivis(request, queryset)
        else:
            # Impression par défaut
            context = {
                'object_list': queryset,
                'today': timezone.now(),
                'title': f'Impression de {obj._meta.verbose_name}'
            }
            return render(request, 'admin/print_default.html', context)


@admin.register(SuiviEnseignement)
class SuiviEnseignementDynamicAdmin(SuiviEnseignementBaseMixin, ActionButtonsMixin, ExportPrintButtonsMixin, admin.ModelAdmin):
    """Administration du suivi de l'enseignement"""
    
    date_hierarchy = 'date_cours'
    list_per_page = 15
    ordering = ('-date_cours',)
    actions = ['exporter_suivi_csv', 'imprimer_selection_suivis']
    readonly_fields = ['annee_academique']
    list_display_enseignant = (
        'cours', 'date_cours', 'horaire_debut', 'horaire_fin', 
        'heures_cm', 'heures_td', 'heures_tp', 'total_heures_cumulees','status_emargement', 'actions_buttons', 'export_print_buttons'
    )
    list_display_admin = (
        'get_enseignant', 'get_parcours', 'get_niveau_etude', 'get_semestre', 'get_intitule_cours',
        'date_cours', 'horaire_debut', 'horaire_fin', 'total_heures_cumulees', 'status_emargement', 'actions_buttons', 'export_print_buttons'
    )
    list_filter_admin = (
        'date_cours', 'emargement_delegue', 'annee_academique',
        'cours__parcours', 'cours__niveau', 'cours__semestre', 'enseignant'
    )
    list_filter_enseignant = ('date_cours', 'cours__parcours', 'cours__niveau', 'emargement_delegue')

    search_fields_admin = (
        'cours__code_cours', 'cours__parcours', 'cours__intitule_ue', 'cours__intitule_ecue',
        'enseignant__user__first_name', 'enseignant__user__last_name', 'enseignant__matricule'
    )
    search_fields_enseignant = ('cours__code_cours', 'cours__intitule_ue', 'cours__intitule_ecue')

    def get_list_display(self, request):
        return self.list_display_admin if request.user.is_superuser else self.list_display_enseignant

    def get_list_filter(self, request):
        return self.list_filter_admin if request.user.is_superuser else self.list_filter_enseignant

    def get_search_fields(self, request):
        return self.search_fields_admin if request.user.is_superuser else self.search_fields_enseignant

    def get_readonly_fields(self, request, obj=None):
        fields = ['total_heures_cumulees', 'annee_academique']
        if not request.user.is_superuser:
            fields.append('emargement_delegue')
        return fields

    def get_enseignant(self, obj):
        return f"{obj.enseignant.user.last_name} {obj.enseignant.user.first_name}" if obj.enseignant and obj.enseignant.user else f"Enseignant {obj.enseignant.matricule}"
    get_enseignant.short_description = "Enseignant"

    def status_emargement(self, obj):
        return format_html('<span style="color: green;">OUI</span>' if obj.emargement_delegue else '<span style="color: red;">NON</span>')
    status_emargement.short_description = "Émargement"

    def get_parcours(self, obj):
        return obj.cours.parcours
    get_parcours.short_description = "Parcours"

    def get_niveau_etude(self, obj):
        return obj.cours.niveau
    get_niveau_etude.short_description = "Niveau d'étude"

    def get_semestre(self, obj):
        return obj.cours.semestre
    get_semestre.short_description = "Semestre"

    def get_intitule_cours(self, obj):
        return f"{obj.cours.code_cours} - {obj.cours.intitule_ue}"
    get_intitule_cours.short_description = "Cours"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "enseignant":
            # Si l'utilisateur connecté est un enseignant, on remplit automatiquement le champ et le cache
            if hasattr(request.user, 'enseignant') and not request.user.is_superuser:
                kwargs["queryset"] = Enseignant.objects.filter(id=request.user.enseignant.id)
                kwargs["initial"] = request.user.enseignant
                kwargs["widget"] = forms.HiddenInput()  # Cache le champ
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        """Empêche la suppression si l'émargement du délégué est validé"""
        if obj and obj.emargement_delegue and not request.user.is_superuser:
            messages.warning(request, "Suppression impossible : le délégué a déjà signé.")
            return False  # Interdit la suppression

        return super().has_delete_permission(request, obj)

    def save_model(self, request, obj, form, change):
        """Sauvegarde du modèle avec des vérifications supplémentaires"""
        if not obj.enseignant and hasattr(request.user, 'enseignant'):
            obj.enseignant = request.user.enseignant  # Assigner l'enseignant connecté
        
        # Vérifier que l'enseignant est associé au cours
        if not request.user.is_superuser and obj.enseignant and obj.cours:
            if not Enseigner.objects.filter(enseignant=obj.enseignant, cours=obj.cours).exists():
                raise ValidationError("Vous n'êtes pas autorisé à créer un suivi pour ce cours.")
        
        # Assignation de l'année académique si elle est vide
        if not obj.annee_academique or obj.annee_academique == '':
            obj.annee_academique = str(timezone.now().year)

        super().save_model(request, obj, form, change)

    def imprimer_selection_suivis(self, request, queryset):
        """Imprimer les suivis sélectionnés."""
        if not queryset:
            self.message_user(request, "Aucun suivi sélectionné pour l'impression.")
            return

        context = {
            'suivi_list': queryset,
            'today': timezone.now(),
            'title': 'Impression des suivis d\'enseignement'
        }
        return render(request, 'admin/suivi/print.html', context)

    imprimer_selection_suivis.short_description = "Imprimer les suivis sélectionnés"

    def exporter_suivi_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv', charset='utf-8')
        response['Content-Disposition'] = 'attachment; filename="suivi_enseignants.csv"'
        
        writer = csv.writer(response, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'Cours', 'Date', 'Horaire debut', 'Horaire fin', 'Heures CM', 'Heures TD', 'Heures TP', 
            'Total heures cumulees', 'Statut emargement'
        ])

        for suivi in queryset:
            writer.writerow([
                suivi.cours.intitule_ue,
                suivi.date_cours,
                suivi.horaire_debut,
                suivi.horaire_fin,
                suivi.heures_cm,
                suivi.heures_td,
                suivi.heures_tp,
                suivi.total_heures_cumulees,
                suivi.status_emargement()
            ])
        
        return response

    exporter_suivi_csv.short_description = "Exporter les suivis sélectionnés en CSV"

@admin.register(GroupeEtudiant)
class GroupeEtudiantAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ('nom_groupe', 'niveau', 'parcours', 'effectif', 'actions_buttons')
    list_filter = ('niveau', 'parcours')
    search_fields = ['nom_groupe', 'niveau__libelle_niveau', 'parcours']
    list_per_page = 15


# Enregistrement de l'utilisateur personnalisé
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Enseigner)
class EnseignerAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ('enseignant', 'cours', 'actions_buttons')
    search_fields = ('enseignant__user__last_name', 'enseignant__user__first_name', 'cours__code_cours', 'cours__intitule_ue')
    list_filter = ('cours__niveau', 'cours__semestre', 'enseignant__grade', 'enseignant__statut')
    autocomplete_fields = ('enseignant', 'cours')


from .models import Notification

class NotificationAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'read', 'actions_buttons')
    list_filter = ('read',)
    search_fields = ('message',)


