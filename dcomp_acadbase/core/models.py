# dcomp-acadbase/dcomp_acadbase/core/models.py
import hashlib, codecs
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
    is_rascunho = models.BooleanField(default=False, verbose_name='Rascunho') ##Lembrete: Quando for draft/rascunho, alguns campos podem ser blank

    #
    def banca_avaliadora_list(self):
        return ", ".join([str(avaliador) for avaliador in self.banca_avaliadora.all()])
    banca_avaliadora_list.short_description = 'Banca Avaliadora'

    def generate_checksum(self, file_field):
        # Abre o arquivo em modo binário
        h= hashlib.md5()
        try:
            print(f"Generating checksum for file: {file_field.name}")
            with default_storage.open(file_field.name, 'rb') as file:

                for chunk in iter(lambda: file.read(4096), b""):
                    h.update(chunk)
                print(f"Checksum generated: ")
                return h.hexdigest()
        except IOError:
            print(f"Error generating checksum: ")
            return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.arquivo_pdf and not self.is_rascunho:
            print(f"Arquivo PDF Type: {type(self.arquivo_pdf)}")
            checksum = self.generate_checksum(self.arquivo_pdf)
            if checksum is None:
                checksum = "checksum_failed"

            print('\n'+ checksum) #Debugging Checksum Generation
            try:
                with open('core/checksum/checksum_logs.txt', 'a') as file:
                    file.write(checksum + ';\n')
            except IOError:
                return None
        
        

    def __str__(self):
        return self.titulo