from django.contrib import admin
from .models import User, Monografia, Banca

# Register your models here.
#admin.site.register(Monografia)
#admin.site.register(Banca)

@admin.register(Monografia)
class MonografiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'curso', 'status', 'data_publicacao', 'qtd_paginas', 'is_rascunho')
    search_fields = ('titulo', 'autor__username', 'curso', 'status')

@admin.register(Banca)
class BancaAdmin(admin.ModelAdmin):
    list_display = ('monografia', 'data_defesa')
    search_fields = ('monografia__titulo', 'data_defesa')
    