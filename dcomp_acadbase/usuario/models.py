# dcomp-acadbase/dcomp_acadbase/usuario/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

# MODELO DE USUÁRIOS DO SISTEMA
class User(AbstractUser):
    ROLE_CHOICES = [
        ('FUNCIONARIO','Funcionario'),
        ('CHEFE', 'Chefe'),
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('EXTERNO', 'Externo')
    ]
    tipo_usuario = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EXTERNO', verbose_name='Tipo de Usuário')
    email = models.EmailField(max_length=255, unique=True)