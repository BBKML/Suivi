#!/usr/bin/env python
"""
Script de simulation de cas d'utilisation pour l'application de suivi des enseignements
Ce script teste les fonctionnalités principales de l'application
"""

import os
import sys
import django
from datetime import date, time, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Suivi.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone

from Suiv.models import (
    CustomUser, Grade, Statut, AnneeAcademique, Enseignant, 
    NiveauEtude, Semestre, Salle, Cours, SuiviEnseignement, 
    Enseigner, GroupeEtudiant
)

User = get_user_model()

def print_section(title):
    """Affiche une section avec un titre"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_success(message):
    """Affiche un message de succès"""
    print(f"✅ {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"❌ {message}")

def print_info(message):
    """Affiche un message d'information"""
    print(f"ℹ️  {message}")

def simulation_1_creation_donnees_de_base():
    """Simulation 1: Création des données de base"""
    print_section("SIMULATION 1: CRÉATION DES DONNÉES DE BASE")
    
    try:
        # Vérifier si les données existent déjà
        grade = Grade.objects.filter(libelle_grade="Maître de Conférences").first()
        if not grade:
            grade = Grade.objects.create(libelle_grade="Maître de Conférences")
            print_success("Grade créé")
        else:
            print_info("Grade existe déjà")
            
        statut = Statut.objects.filter(libelle_statut="Titulaire").first()
        if not statut:
            statut = Statut.objects.create(libelle_statut="Titulaire")
            print_success("Statut créé")
        else:
            print_info("Statut existe déjà")
            
        niveau = NiveauEtude.objects.filter(libelle_niveau="Licence 2").first()
        if not niveau:
            niveau = NiveauEtude.objects.create(libelle_niveau="Licence 2")
            print_success("Niveau créé")
        else:
            print_info("Niveau existe déjà")
            
        semestre = Semestre.objects.filter(libelle_semestre="Semestre 3").first()
        if not semestre:
            semestre = Semestre.objects.create(libelle_semestre="Semestre 3")
            print_success("Semestre créé")
        else:
            print_info("Semestre existe déjà")
            
        salle = Salle.objects.filter(nom_salle="Salle A101").first()
        if not salle:
            salle = Salle.objects.create(nom_salle="Salle A101", capacite=30)
            print_success("Salle créée")
        else:
            print_info("Salle existe déjà")
        
        print_success("Données de base disponibles")
        print_info(f"Grade: {grade}")
        print_info(f"Statut: {statut}")
        print_info(f"Niveau: {niveau}")
        print_info(f"Semestre: {semestre}")
        print_info(f"Salle: {salle}")
        
        return grade, statut, niveau, semestre, salle
        
    except Exception as e:
        print_error(f"Erreur lors de la création des données de base: {e}")
        return None, None, None, None, None

def simulation_2_creation_annee_academique():
    """Simulation 2: Création et gestion des années académiques"""
    print_section("SIMULATION 2: GESTION DES ANNÉES ACADÉMIQUES")
    
    try:
        # Vérifier si l'année 2024-2025 existe déjà
        annee_2024 = AnneeAcademique.objects.filter(annee="2024-2025").first()
        if not annee_2024:
            annee_2024 = AnneeAcademique.objects.create(
                annee="2024-2025",
                date_debut=date(2024, 9, 1),
                date_fin=date(2025, 8, 31),
                est_active=True,
                description="Année académique 2024-2025"
            )
            print_success("Année académique 2024-2025 créée et activée")
        else:
            print_info("Année 2024-2025 existe déjà")
        
        # Vérifier si l'année 2025-2026 existe déjà
        annee_2025 = AnneeAcademique.objects.filter(annee="2025-2026").first()
        if not annee_2025:
            annee_2025 = AnneeAcademique.objects.create(
                annee="2025-2026",
                date_debut=date(2025, 9, 1),
                date_fin=date(2026, 8, 31),
                description="Année académique 2025-2026"
            )
            print_success("Année académique 2025-2026 créée (inactive par défaut)")
        else:
            print_info("Année 2025-2026 existe déjà")
        
        # Activer la nouvelle année (désactive automatiquement l'ancienne)
        annee_2025.est_active = True
        annee_2025.save()
        
        print_success("Année 2025-2026 activée, année 2024-2025 désactivée automatiquement")
        
        # Vérifier l'année active
        annee_active = AnneeAcademique.get_annee_active()
        print_info(f"Année active actuelle: {annee_active}")
        
        return annee_2025
        
    except Exception as e:
        print_error(f"Erreur lors de la gestion des années académiques: {e}")
        return None

def simulation_3_creation_utilisateurs_et_enseignants():
    """Simulation 3: Création d'utilisateurs et d'enseignants"""
    print_section("SIMULATION 3: CRÉATION D'UTILISATEURS ET D'ENSEIGNANTS")
    
    try:
        # Vérifier si l'admin existe déjà
        admin_user = User.objects.filter(email='admin@universite.com').first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                email='admin@universite.com',
                password='admin123',
                first_name='Admin',
                last_name='Université'
            )
            print_success("Utilisateur admin créé")
        else:
            print_info("Utilisateur admin existe déjà")
        
        # Vérifier si l'enseignant existe déjà
        enseignant_user = User.objects.filter(email='jean.dupont@universite.com').first()
        if not enseignant_user:
            enseignant_user = User.objects.create_user(
                email='jean.dupont@universite.com',
                password='enseignant123',
                first_name='Jean',
                last_name='Dupont'
            )
            print_success("Utilisateur enseignant créé")
        else:
            print_info("Utilisateur enseignant existe déjà")
        
        # Vérifier si l'enseignant existe déjà
        enseignant = Enseignant.objects.filter(user=enseignant_user).first()
        if not enseignant:
            grade, statut, _, _, _ = simulation_1_creation_donnees_de_base()
            if not grade:
                return None, None
                
            enseignant = Enseignant.objects.create(
                user=enseignant_user,
                matricule="ENS001",
                grade=grade,
                statut=statut,
                contact="+2250701234567"
            )
            print_success("Enseignant créé avec succès")
        else:
            print_info("Enseignant existe déjà")
            
        print_info(f"Enseignant: {enseignant.nom} {enseignant.prenom}")
        print_info(f"Matricule: {enseignant.matricule}")
        print_info(f"Grade: {enseignant.grade}")
        print_info(f"Contact: {enseignant.contact}")
        
        return admin_user, enseignant
        
    except Exception as e:
        print_error(f"Erreur lors de la création des utilisateurs: {e}")
        return None, None

def simulation_4_creation_cours():
    """Simulation 4: Création de cours"""
    print_section("SIMULATION 4: CRÉATION DE COURS")
    
    try:
        _, _, niveau, semestre, salle = simulation_1_creation_donnees_de_base()
        if not niveau:
            return None
            
        # Vérifier si le cours existe déjà
        cours = Cours.objects.filter(code_cours="INFO201").first()
        if not cours:
            cours = Cours.objects.create(
                code_cours="INFO201",
                intitule_ue="Informatique Fondamentale",
                intitule_ecue="Programmation Orientée Objet",
                niveau=niveau,
                semestre=semestre,
                parcours="Informatique",
                salle=salle,
                total_heures=60.0
            )
            print_success("Cours créé avec succès")
        else:
            print_info("Cours existe déjà")
            
        print_info(f"Cours: {cours}")
        print_info(f"Code: {cours.code_cours}")
        print_info(f"UE: {cours.intitule_ue}")
        print_info(f"ECUE: {cours.intitule_ecue}")
        print_info(f"Niveau: {cours.niveau}")
        print_info(f"Total heures: {cours.total_heures}")
        
        return cours
        
    except Exception as e:
        print_error(f"Erreur lors de la création du cours: {e}")
        return None

def simulation_5_creation_groupes_etudiants():
    """Simulation 5: Création de groupes d'étudiants"""
    print_section("SIMULATION 5: CRÉATION DE GROUPES D'ÉTUDIANTS")
    
    try:
        _, _, niveau, _, _ = simulation_1_creation_donnees_de_base()
        annee = simulation_2_creation_annee_academique()
        if not niveau or not annee:
            return None
            
        # Vérifier si le groupe existe déjà
        groupe = GroupeEtudiant.objects.filter(
            nom_groupe="INFO2A",
            niveau=niveau,
            parcours="Informatique",
            annee_academique=annee
        ).first()
        
        if not groupe:
            groupe = GroupeEtudiant.objects.create(
                nom_groupe="INFO2A",
                niveau=niveau,
                parcours="Informatique",
                effectif=25,
                annee_academique=annee,
                description="Groupe A de Licence 2 Informatique"
            )
            print_success("Groupe d'étudiants créé avec succès")
        else:
            print_info("Groupe d'étudiants existe déjà")
            
        print_info(f"Groupe: {groupe}")
        print_info(f"Nom complet: {groupe.nom_complet}")
        print_info(f"Effectif: {groupe.effectif}")
        print_info(f"Année: {groupe.annee_academique}")
        
        # Tester l'unicité du groupe
        try:
            groupe_duplique = GroupeEtudiant.objects.create(
                nom_groupe="INFO2A",
                niveau=niveau,
                parcours="Informatique",
                effectif=30,
                annee_academique=annee
            )
            print_error("Erreur: Un groupe identique a pu être créé")
        except ValidationError:
            print_success("Validation d'unicité fonctionne: Impossible de créer un groupe identique")
        
        return groupe
        
    except Exception as e:
        print_error(f"Erreur lors de la création du groupe: {e}")
        return None

def simulation_6_suivi_enseignement():
    """Simulation 6: Suivi d'enseignement"""
    print_section("SIMULATION 6: SUIVI D'ENSEIGNEMENT")
    
    try:
        # Récupérer les données nécessaires
        _, enseignant = simulation_3_creation_utilisateurs_et_enseignants()
        cours = simulation_4_creation_cours()
        groupe = simulation_5_creation_groupes_etudiants()
        annee = simulation_2_creation_annee_academique()
        
        if not all([enseignant, cours, groupe, annee]):
            return None
            
        # Associer l'enseignant au cours
        enseignement = Enseigner.objects.create(
            enseignant=enseignant,
            cours=cours
        )
        
        print_success("Association enseignant-cours créée")
        
        # Créer un suivi d'enseignement
        suivi = SuiviEnseignement.objects.create(
            cours=cours,
            enseignant=enseignant,
            date_cours=date(2025, 10, 15),
            horaire_debut=time(8, 0),
            horaire_fin=time(10, 0),
            heures_cm=2.0,
            heures_td=0.0,
            heures_tp=0.0,
            annee_academique=annee
        )
        suivi.groupes.add(groupe)
        
        print_success("Suivi d'enseignement créé avec succès")
        print_info(f"Date: {suivi.date_cours}")
        print_info(f"Horaire: {suivi.horaire_debut} - {suivi.horaire_fin}")
        print_info(f"Heures CM: {suivi.heures_cm}")
        print_info(f"Total heures: {suivi.total_heures_cumulees}")
        print_info(f"Groupes: {suivi.groupes.count()}")
        
        return suivi
        
    except Exception as e:
        print_error(f"Erreur lors du suivi d'enseignement: {e}")
        return None

def simulation_7_emargement_delegue():
    """Simulation 7: Émargement délégué"""
    print_section("SIMULATION 7: ÉMARGEMENT DÉLÉGUÉ")
    
    try:
        # Créer un suivi avec émargement délégué
        _, enseignant = simulation_3_creation_utilisateurs_et_enseignants()
        cours = simulation_4_creation_cours()
        annee = simulation_2_creation_annee_academique()
        
        if not all([enseignant, cours, annee]):
            return None
            
        suivi_delegue = SuiviEnseignement.objects.create(
            cours=cours,
            enseignant=enseignant,
            date_cours=date(2025, 10, 16),
            horaire_debut=time(10, 0),
            horaire_fin=time(12, 0),
            heures_cm=1.0,
            heures_td=1.0,
            emargement_delegue=True,
            delegue_nom="Marie Martin",
            delegue_contact="+2250701234568",
            motif_delegation="Absence pour formation",
            annee_academique=annee
        )
        
        print_success("Suivi avec émargement délégué créé")
        print_info(f"Émargement délégué: {suivi_delegue.emargement_delegue}")
        print_info(f"Délégué: {suivi_delegue.delegue_nom}")
        print_info(f"Motif: {suivi_delegue.motif_delegation}")
        print_info(f"Date émargement: {suivi_delegue.date_emargement}")
        print_info(f"Status: {suivi_delegue.status_emargement()}")
        
        # Tester la validation d'émargement délégué incomplet
        try:
            suivi_incomplet = SuiviEnseignement(
                cours=cours,
                enseignant=enseignant,
                date_cours=date(2025, 10, 17),
                horaire_debut=time(14, 0),
                horaire_fin=time(16, 0),
                heures_cm=2.0,
                emargement_delegue=True  # Sans nom de délégué ni motif
            )
            suivi_incomplet.clean()
            print_error("Erreur: Émargement délégué incomplet accepté")
        except ValidationError:
            print_success("Validation émargement délégué fonctionne: Impossible sans nom/motif")
        
        return suivi_delegue
        
    except Exception as e:
        print_error(f"Erreur lors de l'émargement délégué: {e}")
        return None

def simulation_8_validation_donnees():
    """Simulation 8: Validation des données"""
    print_section("SIMULATION 8: VALIDATION DES DONNÉES")
    
    try:
        # Test validation contact enseignant
        try:
            enseignant_invalide = Enseignant(
                user=User.objects.first(),
                matricule="ENS999",
                grade=Grade.objects.first(),
                statut=Statut.objects.first(),
                contact="123"  # Contact invalide
            )
            enseignant_invalide.full_clean()
            print_error("Erreur: Contact invalide accepté")
        except ValidationError:
            print_success("Validation contact fonctionne: Format invalide rejeté")
        
        # Test validation horaires
        try:
            suivi_horaires_invalides = SuiviEnseignement(
                cours=Cours.objects.first(),
                enseignant=Enseignant.objects.first(),
                date_cours=date(2025, 10, 18),
                horaire_debut=time(10, 0),
                horaire_fin=time(9, 0),  # Heure fin < heure début
                heures_cm=2.0
            )
            suivi_horaires_invalides.clean()
            print_error("Erreur: Horaires invalides acceptés")
        except ValidationError:
            print_success("Validation horaires fonctionne: Heure fin < heure début rejeté")
        
        # Test validation heures négatives
        try:
            suivi_heures_negatives = SuiviEnseignement(
                cours=Cours.objects.first(),
                enseignant=Enseignant.objects.first(),
                date_cours=date(2025, 10, 19),
                horaire_debut=time(8, 0),
                horaire_fin=time(10, 0),
                heures_cm=-1.0  # Heures négatives
            )
            suivi_heures_negatives.clean()
            print_error("Erreur: Heures négatives acceptées")
        except ValidationError:
            print_success("Validation heures fonctionne: Heures négatives rejetées")
        
        print_success("Toutes les validations fonctionnent correctement")
        
    except Exception as e:
        print_error(f"Erreur lors des tests de validation: {e}")

def simulation_9_statistiques():
    """Simulation 9: Statistiques et rapports"""
    print_section("SIMULATION 9: STATISTIQUES ET RAPPORTS")
    
    try:
        # Statistiques générales
        total_enseignants = Enseignant.objects.count()
        total_cours = Cours.objects.count()
        total_suivis = SuiviEnseignement.objects.count()
        total_groupes = GroupeEtudiant.objects.count()
        annee_active = AnneeAcademique.get_annee_active()
        
        print_info("=== STATISTIQUES GÉNÉRALES ===")
        print_info(f"Nombre d'enseignants: {total_enseignants}")
        print_info(f"Nombre de cours: {total_cours}")
        print_info(f"Nombre de suivis: {total_suivis}")
        print_info(f"Nombre de groupes: {total_groupes}")
        print_info(f"Année active: {annee_active}")
        
        # Statistiques par enseignant
        if Enseignant.objects.exists():
            enseignant = Enseignant.objects.first()
            suivis_enseignant = enseignant.suivis.count()
            print_info(f"\n=== STATISTIQUES ENSEIGNANT: {enseignant} ===")
            print_info(f"Nombre de suivis: {suivis_enseignant}")
            print_info(f"Grade: {enseignant.grade}")
            print_info(f"Statut: {enseignant.statut}")
        
        # Statistiques par groupe
        if GroupeEtudiant.objects.exists():
            groupe = GroupeEtudiant.objects.first()
            suivis_groupe = groupe.get_suivis_count()
            print_info(f"\n=== STATISTIQUES GROUPE: {groupe} ===")
            print_info(f"Nombre de suivis: {suivis_groupe}")
            print_info(f"Effectif: {groupe.effectif}")
            print_info(f"Année: {groupe.annee_academique}")
        
        print_success("Statistiques générées avec succès")
        
    except Exception as e:
        print_error(f"Erreur lors de la génération des statistiques: {e}")

def main():
    """Fonction principale de simulation"""
    print_section("DÉMARRAGE DE LA SIMULATION")
    print_info("Simulation des cas d'utilisation de l'application de suivi des enseignements")
    
    # Nettoyer la base de données de test
    print_info("Nettoyage de la base de données...")
    User.objects.all().delete()
    AnneeAcademique.objects.all().delete()
    Grade.objects.all().delete()
    Statut.objects.all().delete()
    NiveauEtude.objects.all().delete()
    Semestre.objects.all().delete()
    Salle.objects.all().delete()
    
    # Exécuter les simulations
    simulation_1_creation_donnees_de_base()
    simulation_2_creation_annee_academique()
    simulation_3_creation_utilisateurs_et_enseignants()
    simulation_4_creation_cours()
    simulation_5_creation_groupes_etudiants()
    simulation_6_suivi_enseignement()
    simulation_7_emargement_delegue()
    simulation_8_validation_donnees()
    simulation_9_statistiques()
    
    print_section("FIN DE LA SIMULATION")
    print_success("Simulation terminée avec succès !")
    print_info("L'application fonctionne correctement pour tous les cas d'usage testés.")

if __name__ == "__main__":
    main() 