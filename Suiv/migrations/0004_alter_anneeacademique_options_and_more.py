# Generated by Django 5.1.7 on 2025-06-24 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Suiv', '0003_alter_groupeetudiant_date_creation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='anneeacademique',
            options={'verbose_name': 'Année académique', 'verbose_name_plural': 'Années académiques'},
        ),
        migrations.AlterModelOptions(
            name='groupeetudiant',
            options={'verbose_name': "Groupe d'étudiants", 'verbose_name_plural': "Groupes d'étudiants"},
        ),
        migrations.RemoveConstraint(
            model_name='groupeetudiant',
            name='unique_groupe_niveau_parcours_annee',
        ),
        migrations.RemoveField(
            model_name='anneeacademique',
            name='date_debut',
        ),
        migrations.RemoveField(
            model_name='anneeacademique',
            name='date_fin',
        ),
        migrations.RemoveField(
            model_name='anneeacademique',
            name='description',
        ),
        migrations.RemoveField(
            model_name='anneeacademique',
            name='est_active',
        ),
        migrations.RemoveField(
            model_name='groupeetudiant',
            name='annee_academique',
        ),
        migrations.RemoveField(
            model_name='groupeetudiant',
            name='date_creation',
        ),
        migrations.RemoveField(
            model_name='groupeetudiant',
            name='description',
        ),
        migrations.RemoveField(
            model_name='groupeetudiant',
            name='est_actif',
        ),
        migrations.RemoveField(
            model_name='suivienseignement',
            name='date_emargement',
        ),
        migrations.RemoveField(
            model_name='suivienseignement',
            name='delegue_contact',
        ),
        migrations.RemoveField(
            model_name='suivienseignement',
            name='delegue_nom',
        ),
        migrations.RemoveField(
            model_name='suivienseignement',
            name='motif_delegation',
        ),
        migrations.AddField(
            model_name='anneeacademique',
            name='enseignants',
            field=models.ManyToManyField(blank=True, related_name='annees_academiques', to='Suiv.enseignant'),
        ),
        migrations.AddField(
            model_name='anneeacademique',
            name='suivis',
            field=models.ManyToManyField(blank=True, related_name='annees_academiques', to='Suiv.suivienseignement'),
        ),
        migrations.AlterField(
            model_name='anneeacademique',
            name='annee',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='suivienseignement',
            name='annee_academique',
            field=models.CharField(default='2025', max_length=4),
        ),
        migrations.AddConstraint(
            model_name='groupeetudiant',
            constraint=models.UniqueConstraint(fields=('nom_groupe', 'niveau', 'parcours'), name='unique_groupe_niveau_parcours'),
        ),
    ]
