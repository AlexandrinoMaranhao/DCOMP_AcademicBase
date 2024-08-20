# dcomp-acadbase/dcomp_acadbase/core/forms.py

from django import forms
from .models import Monografia
from usuario.models import User

class MonografiaForm(forms.ModelForm):
    class Meta:
        model =  Monografia
        fields = [
            'titulo', 'autor', 'curso', 'orientador', 'banca_avaliadora',
            'status', 'resumo', 'palavras_chave', 'temas', 
            'data_defesa', 'data_publicacao', 'qtd_paginas', 'arquivo_pdf', 'is_rascunho',
        ]
        widgets = {
            'banca_avaliadora': forms.CheckboxSelectMultiple
        }