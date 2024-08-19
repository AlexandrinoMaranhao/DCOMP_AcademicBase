# dcomp_acadbase/core/models.py
import hashlib
from django.db import models
#from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError
from usuario.models import User

# Create your models here.
# MODELO MONOGRAFIA
class Monografia(models.Model):
    STATUS_CHOICES = [
        ('DEFENDIDA, APROVADA', 'Defendida, Aprovada'),   
        ('DEFENDIDA, EM DILIGÊNCIA', 'Defendida, em Diligência')
    ]

    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monografia_autor', limit_choices_to={'tipo_usuario': 'ALUNO'})
    curso = models.CharField(max_length=255)
    orientador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monografia_orientador',limit_choices_to={'tipo_usuario': 'PROFESSOR'})
    banca_avaliadora = models.ManyToManyField(User, related_name='banca_avaliadores', limit_choices_to={'tipo_usuario': 'PROFESSOR'}, verbose_name='Banca Avaliadora')
    status =  models.CharField(max_length=255, choices=STATUS_CHOICES)
    resumo = models.TextField()
    palavras_chave = models.CharField(max_length=75, blank=True, verbose_name='Palavras-Chave')
    temas = models.CharField(max_length=75, blank=True)
    data_defesa = models.DateField(verbose_name='Data de Defesa da Monografia')
    data_publicacao = models.DateField(verbose_name='Data de Publicação da Monografia')
    qtd_paginas = models.PositiveIntegerField(verbose_name='Quantidade de Páginas')
    arquivo_pdf = models.FileField(upload_to='media/uploads/monografias/', verbose_name='Arquivo em formato PDF')
    #checksum = models.CharField(max_length=128, blank=True, null=True)
    is_rascunho = models.BooleanField(default=False, verbose_name='Rascunho') ##Lembrete: Quando for draft/rascunho, alguns campos podem ser blank

    #
    def banca_avaliadores_list(self):
        return ", ".join([avaliador.username for avaliador in self.banca_avaliadores.all()])
    banca_avaliadores_list.short_description = 'Banca Avaliadora'

    def generate_checksum(self, file_field):
        # Abre o arquivo em modo binário
        try:
            with default_storage.open(file_field.name, 'rb') as file:
                hash_md5 = hashlib.md5()

                for chunk in iter(lambda: file.read(4096), b""):
                    hash_md5.update(chunk)
                return hash_md5.hexdigest()
        except IOError:
            return None
    
    def clean(self):
        # Define o número mínimo de usuários exigidos
        min_avaliadores = 3
        if self.banca_avaliadores.count() < min_avaliadores:
            raise ValidationError(f'Você deve adicionar pelo menos {min_avaliadores} avaliadores na banca.')

    def save(self, *args, **kwargs):
        self.clean()  # Chama a validação ao salvar
        if self.arquivo_pdf and not self.is_rascunho:
            self.checksum = self.generate_checksum(self.arquivo_pdf)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo