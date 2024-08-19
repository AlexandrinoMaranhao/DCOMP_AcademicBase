# dcomp-acadbase/dcomp_acadbase/core/admin.py

from django.contrib import admin
from .models import Monografia

# Register your models here.
@admin.register(Monografia)
class MonografiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'banca_avaliadora_list', 'curso', 'status', 'data_publicacao', 'qtd_paginas', 'is_rascunho')
    search_fields = ('titulo', 'autor__username', 'curso', 'status')   

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Se necessário, adicione lógica adicional aqui para relações ManyToMany