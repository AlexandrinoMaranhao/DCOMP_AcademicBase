from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'nome', 'email', 'tipo_usuario')
    search_fields = ('username', 'nome', 'email', 'tipo_usuario')
    list_filter = ('tipo_usuario',)
