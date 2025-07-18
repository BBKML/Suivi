from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.admin.views.decorators import staff_member_required
from .models import *

def home_view(request):
    if request.user.is_authenticated:
        return redirect('/admin/')  # Redirige vers /admin/ si l'utilisateur est connecté
    
    # Statistiques pour la page d'accueil
    context = get_dashboard_stats()
    return render(request, 'index.html', context)

def get_dashboard_stats():
    """Récupère toutes les statistiques pour le tableau de bord"""
    try:
        # Statistiques générales
        total_enseignants = Enseignant.objects.count()
        total_cours = Cours.objects.count()
        total_suivis = SuiviEnseignement.objects.count()
        total_groupes = GroupeEtudiant.objects.count()
        
        # Année académique active
        annee_active = AnneeAcademique.get_annee_active()
        annee_courante = annee_active.annee if annee_active else "Non définie"
        
        # Statistiques de l'année courante
        if annee_active:
            suivis_annee = SuiviEnseignement.objects.filter(annee_academique=annee_active)
            total_heures_annee = suivis_annee.aggregate(
                total=Sum('total_heures_cumulees')
            )['total'] or 0
            enseignants_actifs = suivis_annee.values('enseignant').distinct().count()
        else:
            total_heures_annee = 0
            enseignants_actifs = 0
        
        # Statistiques des 30 derniers jours
        date_30_jours = timezone.now().date() - timedelta(days=30)
        suivis_recents = SuiviEnseignement.objects.filter(date_cours__gte=date_30_jours)
        heures_recentes = suivis_recents.aggregate(
            total=Sum('total_heures_cumulees')
        )['total'] or 0
        
        # Top 5 des enseignants les plus actifs
        top_enseignants = Enseignant.objects.annotate(
            nb_suivis=Count('suivis')
        ).order_by('-nb_suivis')[:5]
        
        # Top 5 des cours les plus enseignés
        top_cours = Cours.objects.annotate(
            nb_suivis=Count('suivis')
        ).order_by('-nb_suivis')[:5]
        
        # Statistiques par niveau d'étude
        stats_niveaux = NiveauEtude.objects.annotate(
            nb_cours=Count('cours'),
            nb_suivis=Count('cours__suivis')
        ).order_by('-nb_cours')
        
        # Statistiques par semestre
        stats_semestres = Semestre.objects.annotate(
            nb_cours=Count('cours'),
            nb_suivis=Count('cours__suivis')
        ).order_by('-nb_cours')
        
        # Émargements délégués
        emargements_delegues = SuiviEnseignement.objects.filter(
            emargement_delegue=True
        ).count()
        
        # Statistiques des salles
        stats_salles = Salle.objects.annotate(
            nb_cours=Count('cours'),
            nb_suivis=Count('suivis')
        ).order_by('-nb_cours')
        
        # Évolution mensuelle (6 derniers mois)
        evolution_mensuelle = []
        for i in range(6):
            date_debut = timezone.now().date().replace(day=1) - timedelta(days=30*i)
            date_fin = date_debut.replace(day=28) + timedelta(days=4)
            date_fin = date_fin.replace(day=1) - timedelta(days=1)
            
            nb_suivis = SuiviEnseignement.objects.filter(
                date_cours__gte=date_debut,
                date_cours__lte=date_fin
            ).count()
            
            evolution_mensuelle.append({
                'mois': date_debut.strftime('%B %Y'),
                'nb_suivis': nb_suivis
            })
        
        evolution_mensuelle.reverse()
        
        return {
            'total_enseignants': total_enseignants,
            'total_cours': total_cours,
            'total_suivis': total_suivis,
            'total_groupes': total_groupes,
            'annee_courante': annee_courante,
            'total_heures_annee': round(total_heures_annee, 1),
            'enseignants_actifs': enseignants_actifs,
            'heures_recentes': round(heures_recentes, 1),
            'top_enseignants': top_enseignants,
            'top_cours': top_cours,
            'stats_niveaux': stats_niveaux,
            'stats_semestres': stats_semestres,
            'emargements_delegues': emargements_delegues,
            'stats_salles': stats_salles,
            'evolution_mensuelle': evolution_mensuelle,
        }
    except Exception as e:
        # En cas d'erreur, retourner des valeurs par défaut
        return {
            'total_enseignants': 0,
            'total_cours': 0,
            'total_suivis': 0,
            'total_groupes': 0,
            'annee_courante': "Non définie",
            'total_heures_annee': 0,
            'enseignants_actifs': 0,
            'heures_recentes': 0,
            'top_enseignants': [],
            'top_cours': [],
            'stats_niveaux': [],
            'stats_semestres': [],
            'emargements_delegues': 0,
            'stats_salles': [],
            'evolution_mensuelle': [],
        }

@staff_member_required
def print_view(request, object_id):
    # Remplacez cette logique par ce que vous voulez afficher pour l'impression
    # par exemple, récupérer un modèle ou une page spécifique
    context = {'object': None}  # Assurez-vous de définir le bon objet
    html = render_to_string('print_template.html', context)
    response = HttpResponse(html)
    response['Content-Type'] = 'application/pdf'  # Par exemple, pour imprimer en PDF
    response['Content-Disposition'] = 'inline; filename="page_a_imprimer.pdf"'
    return response

def print_enseignants_view(request):
    enseignants = Enseignant.objects.all().order_by('user__last_name')
    paginator = Paginator(enseignants, 10)  # 10 enseignants par page

    page = request.GET.get('page')
    try:
        enseignants_page = paginator.page(page)
    except PageNotAnInteger:
        enseignants_page = paginator.page(1)
    except EmptyPage:
        enseignants_page = paginator.page(paginator.num_pages)

    context = {'enseignants_page': enseignants_page}
    return render(request, 'admin/Suiv/enseignant/print_paginated.html', context)

@staff_member_required
def mark_as_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.read = True
    notification.save()
    return redirect('/admin/notifications/')  # Redirige vers la page des notifications

@staff_member_required
def advanced_stats_view(request):
    """Vue pour les statistiques avancées"""
    context = get_advanced_stats()
    return render(request, 'admin/advanced_stats.html', context)

def get_advanced_stats():
    """Récupère des statistiques avancées pour l'admin"""
    try:
        # Statistiques par période
        aujourd_hui = timezone.now().date()
        semaine_debut = aujourd_hui - timedelta(days=aujourd_hui.weekday())
        mois_debut = aujourd_hui.replace(day=1)
        
        # Suivis par période
        suivis_aujourd_hui = SuiviEnseignement.objects.filter(date_cours=aujourd_hui).count()
        suivis_semaine = SuiviEnseignement.objects.filter(
            date_cours__gte=semaine_debut
        ).count()
        suivis_mois = SuiviEnseignement.objects.filter(
            date_cours__gte=mois_debut
        ).count()
        
        # Heures par période
        heures_aujourd_hui = SuiviEnseignement.objects.filter(
            date_cours=aujourd_hui
        ).aggregate(total=Sum('total_heures_cumulees'))['total'] or 0
        
        heures_semaine = SuiviEnseignement.objects.filter(
            date_cours__gte=semaine_debut
        ).aggregate(total=Sum('total_heures_cumulees'))['total'] or 0
        
        heures_mois = SuiviEnseignement.objects.filter(
            date_cours__gte=mois_debut
        ).aggregate(total=Sum('total_heures_cumulees'))['total'] or 0
        
        # Statistiques par type d'enseignement
        stats_types = {
            'cm': SuiviEnseignement.objects.aggregate(total=Sum('heures_cm'))['total'] or 0,
            'td': SuiviEnseignement.objects.aggregate(total=Sum('heures_td'))['total'] or 0,
            'tp': SuiviEnseignement.objects.aggregate(total=Sum('heures_tp'))['total'] or 0,
        }
        
        # Top 10 des enseignants par heures
        top_enseignants_heures = Enseignant.objects.annotate(
            total_heures=Sum('suivis__total_heures_cumulees')
        ).filter(total_heures__gt=0).order_by('-total_heures')[:10]
        
        # Statistiques par salle
        stats_salles_detaillees = Salle.objects.annotate(
            nb_suivis=Count('suivis'),
            total_heures=Sum('suivis__total_heures_cumulees'),
            taux_utilisation=Avg('suivis__total_heures_cumulees')
        ).order_by('-nb_suivis')
        
        # Évolution hebdomadaire (12 dernières semaines)
        evolution_hebdomadaire = []
        for i in range(12):
            semaine_debut = aujourd_hui - timedelta(weeks=i+1, days=aujourd_hui.weekday())
            semaine_fin = semaine_debut + timedelta(days=6)
            
            nb_suivis = SuiviEnseignement.objects.filter(
                date_cours__gte=semaine_debut,
                date_cours__lte=semaine_fin
            ).count()
            
            heures = SuiviEnseignement.objects.filter(
                date_cours__gte=semaine_debut,
                date_cours__lte=semaine_fin
            ).aggregate(total=Sum('total_heures_cumulees'))['total'] or 0
            
            evolution_hebdomadaire.append({
                'semaine': f"Sem. {semaine_debut.strftime('%d/%m')}",
                'nb_suivis': nb_suivis,
                'heures': round(heures, 1)
            })
        
        evolution_hebdomadaire.reverse()
        
        # Statistiques des émargements délégués
        stats_delegations = {
            'total': SuiviEnseignement.objects.filter(emargement_delegue=True).count(),
            'avec_motif': SuiviEnseignement.objects.filter(
                emargement_delegue=True,
                motif_delegation__isnull=False
            ).exclude(motif_delegation='').count(),
            'sans_motif': SuiviEnseignement.objects.filter(
                emargement_delegue=True
            ).filter(
                Q(motif_delegation__isnull=True) | Q(motif_delegation='')
            ).count(),
        }
        
        # Performance par grade
        performance_grades = Grade.objects.annotate(
            nb_enseignants=Count('enseignants'),
            total_heures=Sum('enseignants__suivis__total_heures_cumulees'),
            nb_suivis=Count('enseignants__suivis')
        ).order_by('-total_heures')
        
        return {
            'suivis_aujourd_hui': suivis_aujourd_hui,
            'suivis_semaine': suivis_semaine,
            'suivis_mois': suivis_mois,
            'heures_aujourd_hui': round(heures_aujourd_hui, 1),
            'heures_semaine': round(heures_semaine, 1),
            'heures_mois': round(heures_mois, 1),
            'stats_types': stats_types,
            'top_enseignants_heures': top_enseignants_heures,
            'stats_salles_detaillees': stats_salles_detaillees,
            'evolution_hebdomadaire': evolution_hebdomadaire,
            'stats_delegations': stats_delegations,
            'performance_grades': performance_grades,
        }
    except Exception as e:
        return {
            'suivis_aujourd_hui': 0,
            'suivis_semaine': 0,
            'suivis_mois': 0,
            'heures_aujourd_hui': 0,
            'heures_semaine': 0,
            'heures_mois': 0,
            'stats_types': {'cm': 0, 'td': 0, 'tp': 0},
            'top_enseignants_heures': [],
            'stats_salles_detaillees': [],
            'evolution_hebdomadaire': [],
            'stats_delegations': {'total': 0, 'avec_motif': 0, 'sans_motif': 0},
            'performance_grades': [],
        }
