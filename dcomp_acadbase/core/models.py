import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.files.storage import default_storage
from usuario.models import User

# Create your models here.
## MODELOS CENTRAIS (pendente mudança)
## MONOGRAFIA
class Monografia(models.Model):
    STATUS_CHOICES = [
        ('DEFENDIDA, APROVADA', 'Defendida, Aprovada'),   
        ('DEFENDIDA, EM DILIGÊNCIA', 'Defendida, em Diligência')
    ]
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monografia_autor')
    curso = models.CharField(max_length=255)
    orientador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monografia_orientador',limit_choices_to={'tipo_usuario': 'PROFESSOR'})
    status =  models.CharField(max_length=255, choices=STATUS_CHOICES)
    resumo = models.TextField()
    palavras_chave = models.CharField(max_length=75, blank=True, verbose_name='Palvavras-Chave')
    temas = models.CharField(max_length=75, blank=True)
    data_publicacao = models.DateField(verbose_name='Data de Publicação da Monografia')
    qtd_paginas = models.PositiveIntegerField(verbose_name='Quantidade de Páginas')
    arquivo_pdf = models.FileField(upload_to='monografias/', verbose_name='Arquivo em formato PDF')
    checksum = models.CharField(max_length=128, blank=True, null=True)
    is_rascunho = models.BooleanField(default=False, verbose_name='Rascunho') ##Lembrete: Quando for draft/rascunho, alguns campos podem ser blank

    def save(self, *args, **kwargs):
        if self.arquivo_pdf and not self.checksum and not self.is_rascunho:
            self.checksum = self.generate_checksum(self.arquivo_pdf)
        super().save(*args, **kwargs)

    def generate_checksum(self, file_field):
        # Open the file in binary mode
        try:
            with default_storage.open(file_field.name, 'rb') as file:
                hash_md5 = hashlib.md5()

                for chunk in iter(lambda: file.read(4096), b""):
                    hash_md5.update(chunk)
                return hash_md5.hexdigest()
        except IOError:
            return None
        
## BANCA AVALIADORA
class Banca(models.Model):
    monografia = models.OneToOneField(Monografia, on_delete=models.CASCADE)
    avaliadores = models.ManyToManyField(User, related_name='banca_avaliador', limit_choices_to={'tipo_usuario': 'PROFESSOR'})
    aluno = models.ManyToManyField(User, related_name='banca_graduando', limit_choices_to={'tipo_usuario': 'ALUNO'})
    data_defesa = models.DateField(verbose_name='Data de Defesa da Monografia')