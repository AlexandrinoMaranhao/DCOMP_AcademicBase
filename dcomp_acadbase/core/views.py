# dcomp-acadbase/dcomp_acadbase/core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from .models import Monografia
from .serializers import MonografiaSerializer
from .forms import MonografiaForm

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
             # Redirecionamento baseado no tipo de usuário
            if user.tipo_usuario == 'FUNCIONARIO' or user.tipo_usuario == 'CHEFE':
                return redirect('monografia_form')  # Redireciona para o formulário de monografia
            elif user.tipo_usuario == 'ALUNO' or user.tipo_usuario == 'PROFESSOR' or user.tipo_usuario == 'EXTERNO':
                return redirect('monografia_list')  # Redireciona para a lista de monografias (apenas visualização)
            return redirect('index') # Redirecionaria para Tela das Opções de Cadastro, Edição e Remoção
    else:
        form = AuthenticationForm()
        
    return render(request, 'index.html', {'form': form})

@login_required
def monografia_form(request, pk=None):
    instance = get_object_or_404(Monografia, pk=pk) if pk else None
    form = MonografiaForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST' and form.is_valid():
        monografia = form.save(commit=False)  # Salva o objeto Monografia sem gravar no banco de dados
        print(f"Saving Monografia: {monografia}")  # Debugging: Print instance before savin
        monografia.save()  # Agora salva o objeto, o que gera um ID
        print(f"Saved Monografia with ID: {monografia.id}")  # Debugging: Print ID after saving
        try:
            monografia.clean()
            form.save_m2m() 
            return redirect('index') # Soon to be replaced by panel 'painel'
        except ValidationError as e:
            form.add_error('banca_avaliadora', e)  # Adiciona o erro ao formulário
    return render(request, 'core/monografia_form.html', {'form': form})

# @login_required
def monografia_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        monografias = Monografia.objects.filter(titulo__icontains=search_query)
    else:
        monografias = Monografia.objects.all()
    return render(request, 'core/monografia_list.html', {'Lista de Monografias': monografias})

# @login_required
# def monografia_edit(request):

# @login_required
# def monografia_delete(request):

# API (non-functional as of now)
class MonografiaViewSet(viewsets.ModelViewSet):
    queryset = Monografia.objects.all()
    serializer_class = MonografiaSerializer