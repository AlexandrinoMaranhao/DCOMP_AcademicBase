import hashlib
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.files.storage import default_storage
from usuarios.models import User

# Create your models here.
## MODELOS CENTRAIS (pendente mudança)
class Monografia(models.Model):
    STATUS_CHOICES = [
        ('DEFENDIDA E APROVADA', 'Defendida e Aprovada'),   
        ('DEFENDIDA, EM DILIGÊNCIA', 'Defendida, em diligência')
    ]
    titulo = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monografia_autor')
    curso = models.CharField(max_length=255)
    orientador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monografia_orientador',limit_choices_to={'tipo_usuario': 'PROFESSOR'})
    status =  models.CharField(max_length=255, choices=STATUS_CHOICES)
    palavras_Chave = models.CharField(max_length=75, blank=True)
    temas = models.CharField(max_length=75, blank=True)
    data_de_Publicacao = models.DateField("Data de Publicação:")
    quantidade_Paginas = models.PositiveIntegerField()
    arquivo_PDF = models.FileField(upload_to='monografias/')
    checksum = models.CharField(max_length=128, blank=True, null=True)
    is_draft = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.arquivo_PDF and not self.checksum and not self.is_draft:
            self.checksum = self.generate_checksum(self.arquivo_PDF)
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
        
    class Meta:
        permissions = [
            ('approve_upload', 'pode aprovar ou não o upload de um arquivo PDF')
        ]

##
class Banca(models.Model):
    monografia = models.OneToOneField(Monografia, on_delete=models.CASCADE)
    avaliadores = models.ManyToManyField(User, related_name='banca_avaliador', limit_choices_to={'tipo_usuario': 'PROFESSOR'})
    aluno = models.ManyToManyField(User, related_name='banca_graduando', limit_choices_to={'tipo_usuario': 'ALUNO'})
    data_de_Defesa = models.DateField("Data de Defesa:")