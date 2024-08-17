from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Set up initial groups and permissions'

    def handle(self, *args, **kwargs):
        # Certifique-se de que o ContentType esteja correto
        content_type = ContentType.objects.get_for_model(Permission)

        # Criando Permissões customizadas
        custom_permissions = [
            ('add_monografia', 'CRIAR MONOGRAFIA'),
            ('change_monografia', 'EDITAR MONOGRAFIA'),
            ('view_monografia', 'VISUALIZAR MONOGRAFIA'),
            ('delete_monografia', 'EXCLUIR MONOGRAFIA'),

            ('add_user', 'ADICIONAR USUÁRIO'),
            ('change_user', 'EDITAR USUÁRIO'),
            ('view_user', 'VER USUÁRIO'),
            ('delete_user', 'EXCLUIR USUÁRIO'),

            ('add_banca', 'ADICIONAR BANCA'),
            ('change_banca', 'EDITAR BANCA'),
            ('view_banca', 'VER BANCA'),
            ('delete_banca', 'EXCLUIR BANCA'),

            ('approve_upload', 'APROVAR UPLOAD'),
            ('submit_monografia', 'SUBMETER MONOGRAFIA') ##A ideia é que ao submeter no sistema, ela fica pendente para aprovação no caso de um ROLE = Funcionario
        ]

        for codename, name in custom_permissions:
            Permission.objects.get_or_create(codename=codename, name=name, content_type=content_type)

        # Definir grupos
        groups = {
            'Funcionario': ['view user', 'change_monografia', 'view_monografia', 'submit_monografia'],
            'ChefeSetor': ['add_user', 'change_user', 'view_user', 'change_monografia', 'view_monografia', 'delete_monografia', 'approve_upload', 'submit_monografia'],
            'Aluno': ['view_monografia', ],
            'Professor': ['view_monografia', ],
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
