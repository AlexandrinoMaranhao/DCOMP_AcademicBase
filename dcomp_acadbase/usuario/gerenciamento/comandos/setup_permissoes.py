# dcomp_acadbase/usuario/gerenciamente/comandos/setup_permissoes.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Monografia
from usuario.models import User

class Command(BaseCommand):
    help = 'Set up initial groups and permissions'

    def handle(self, *args, **kwargs):
         # Definir os ContentTypes para modelos específicos
        content_types = {
            'monografia': ContentType.objects.get_for_model(Monografia),
            'user': ContentType.objects.get_for_model(User),
        }

        # Certifique-se de que o ContentType esteja correto
        # content_type = ContentType.objects.get_for_model(Permission)

        # Criando Permissões customizadas, caso não existam
        custom_permissions = [
            ('add_monografia', 'CRIAR MONOGRAFIA', 'monografia'),
            ('change_monografia', 'EDITAR MONOGRAFIA', 'monografia'),
            ('view_monografia', 'VISUALIZAR MONOGRAFIA', 'monografia'),
            ('delete_monografia', 'EXCLUIR MONOGRAFIA', 'monografia'),

            ('add_user', 'ADICIONAR USUÁRIO', 'usuario'),
            ('change_user', 'EDITAR USUÁRIO', 'usuario'),
            ('view_user', 'VER USUÁRIO', 'usuario'),
            ('delete_user', 'EXCLUIR USUÁRIO', 'usuario'),
        ]

        for codename, name, model in custom_permissions:
            content_type = content_types.get(model)
            if content_type:
                Permission.objects.get_or_create(codename=codename, name=name, content_type=content_type)
            else:
                self.stdout.write(self.style.ERROR(f'ContentType para o modelo "{model}" não encontrado.'))

        # Definir grupos
        groups = {
            'Funcionarios': ['add_monografia', 'change_monografia', 'view_monografia', 'submit_monografia', 
                             'add_user', 'change_user', 'view_user'],
            'ChefeSetor': ['add_monografia', 'change_monografia', 'view_monografia', 'delete_monografia',
                             'add_user', 'change_user', 'view_user', 'delete_user'],
            'Alunos': ['view_monografia'],
            'Professores': ['view_monografia'],
            'Externo': []  # Sem permissões específicas
        }

        for group_name, permissions in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{group_name}" criado.'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{group_name}" já existe.'))

            for perm in permissions:
                try:
                    permission = Permission.objects.get(codename=perm)
                    group.permissions.add(permission)
                    self.stdout.write(self.style.SUCCESS(f'Permissão "{perm}" adicionada ao grupo "{group_name}".'))
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permissão "{perm}" não encontrada.'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions have been set up successfully.'))
