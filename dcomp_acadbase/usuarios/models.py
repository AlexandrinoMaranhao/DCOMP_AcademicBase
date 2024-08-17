from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

## MODELOS DE USUÁRIOS DO SISTEMA
class User(AbstractUser):
    ROLE_CHOICES = [
        ('FUNCIONARIO','Funcionario'),
        ('CHEFE', 'Chefe do Setor'),
        ('ALUNO', 'Aluno'),
        ('PROFESSOR', 'Professor'),
        ('EXTERNO', 'Externo')
    ]
    tipo_usuario = models.CharField(max_length=20, choices=ROLE_CHOICES, default='EXTERNO')
    nome = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Alterado para evitar conflito
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Alterado para evitar conflito
        blank=True
    )

class Aluno(User):
    matricula_SUAP = models.CharField(max_length=20, unique=True)

class Professor(User):
    matricula_SIAPE = models.CharField(max_length=20, unique=True)

class Funcionario (User):
    matricula_SIAPE = models.CharField(max_length=20, unique=True)