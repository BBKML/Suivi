# Boutons d'Action dans l'Interface d'Administration

## Description

Ce module ajoute des boutons "Modifier" et "Supprimer" à toutes les listes d'objets dans l'interface d'administration Django. Ces boutons permettent d'accéder rapidement aux actions de modification et de suppression des éléments.

## Fonctionnalités

### Boutons d'Action
- **Bouton Modifier** : Accès direct à la page de modification d'un objet
- **Bouton Supprimer** : Accès direct à la page de suppression avec confirmation
- **Icônes FontAwesome** : Utilisation d'icônes pour une meilleure UX
- **Responsive Design** : Adaptation automatique sur mobile

### Modèles Supportés
Tous les modèles de l'application ont été mis à jour pour inclure les boutons d'action :

- `CustomUser` - Utilisateurs
- `Grade` - Grades des enseignants
- `Statut` - Statuts des enseignants
- `AnneeAcademique` - Années académiques
- `NiveauEtude` - Niveaux d'étude
- `Semestre` - Semestres
- `Salle` - Salles de cours
- `Cours` - Cours
- `Enseignant` - Enseignants
- `SuiviEnseignement` - Suivis d'enseignement
- `GroupeEtudiant` - Groupes d'étudiants
- `Enseigner` - Relations enseignant-cours
- `Notification` - Notifications

## Installation

### 1. Fichiers CSS et JavaScript
Les fichiers suivants ont été créés :
- `static/css/admin_buttons.css` - Styles pour les boutons
- `static/js/admin_actions.js` - Interactions JavaScript

### 2. Template Personnalisé
Le template `templates/admin/base_site.html` a été créé pour inclure les fichiers CSS et JavaScript.

### 3. Mixin ActionButtonsMixin
Le mixin `ActionButtonsMixin` a été ajouté au fichier `admin.py` pour fournir la fonctionnalité des boutons d'action.

## Utilisation

### Pour les Administrateurs
Les boutons d'action apparaissent automatiquement dans toutes les listes d'objets de l'interface d'administration.

### Pour les Enseignants
Les enseignants voient également les boutons d'action, mais avec des restrictions basées sur leurs permissions :
- Ils ne peuvent modifier que leurs propres suivis d'enseignement
- Ils ne peuvent pas modifier les cours qui leur ont été attribués
- Ils ne peuvent pas supprimer les suivis validés par le délégué

## Personnalisation

### Styles CSS
Vous pouvez personnaliser l'apparence des boutons en modifiant le fichier `static/css/admin_buttons.css`.

### Comportement JavaScript
Vous pouvez modifier les interactions en éditant le fichier `static/js/admin_actions.js`.

### Permissions
Les permissions sont gérées automatiquement par Django. Les boutons n'apparaissent que si l'utilisateur a les permissions nécessaires.

## Sécurité

- Les boutons respectent les permissions Django
- Confirmation obligatoire pour la suppression
- Validation côté serveur maintenue
- Protection CSRF activée

## Compatibilité

- Django 4.0+
- Interface d'administration Django standard
- Compatible avec Django Jazzmin
- Responsive design pour mobile

## Maintenance

### Ajouter des boutons à un nouveau modèle
1. Ajouter `ActionButtonsMixin` à la classe d'administration
2. Ajouter `'actions_buttons'` au `list_display`
3. Les boutons apparaîtront automatiquement

### Exemple
```python
@admin.register(MonNouveauModele)
class MonNouveauModeleAdmin(ActionButtonsMixin, admin.ModelAdmin):
    list_display = ('champ1', 'champ2', 'actions_buttons')
```

## Support

Pour toute question ou problème, consultez la documentation Django ou contactez l'équipe de développement. 