# Generated by Django 5.1 on 2024-08-17 15:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='banca',
            name='aluno',
            field=models.ManyToManyField(limit_choices_to={'tipo_usuario': 'ALUNO'}, related_name='banca_graduando', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='banca',
            name='avaliadores',
            field=models.ManyToManyField(limit_choices_to={'tipo_usuario': 'PROFESSOR'}, related_name='banca_avaliador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='monografia',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monografia_autor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='monografia',
            name='orientador',
            field=models.ForeignKey(limit_choices_to={'tipo_usuario': 'PROFESSOR'}, on_delete=django.db.models.deletion.CASCADE, related_name='monografia_orientador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='banca',
            name='monografia',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.monografia'),
        ),
    ]
