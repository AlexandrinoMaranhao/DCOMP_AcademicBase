# dcomp-acadbase/dcomp_acadbase/core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets
from .models import Monografia
from .serializers import MonografiaSerializer
from .forms import MonografiaForm

def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirecionamento baseado no tipo de usuário
            if user.tipo_usuario == 'FUNCIONARIO' or user.tipo_usuario == 'CHEFE':
                return redirect('monografia_create')  # Redireciona para o formulário de monografia
            elif user.tipo_usuario == 'ALUNO' or user.tipo_usuario == 'PROFESSOR' or user.tipo_usuario == 'EXTERNO':
                return redirect('monografia_list')  # Redireciona para a lista de monografias (apenas visualização)
            return redirect('monografia_list') # Redirecionaria para Painel Geral das Opções de Cadastro, Edição e Remoção
    else:
        form = AuthenticationForm()
        
    return render(request, 'index.html', {'form': form})

# CREATE
@login_required
def monografia_create(request, pk=None):
    instance = Monografia.objects.get(pk=pk) if pk else None
    form = MonografiaForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            #monografia.user = request.user
            form.save()
            print(f'Saved Monografia with ID: {Monografia.id}') #Debugging: Print ID after saving
            messages.success(request, 'Monografia salva com sucesso!')  
            return redirect('monografia_list')
        else: 
            messages.error(request, 'Erro ao salvar monografia. Verifique os dados fornecidos.')
            form = MonografiaForm()
    return render(request, 'core/monografia_form.html', {'form': form})

# READ
#@login_required
def monografia_list(request, pk=None):
    search_query = request.GET.get('search', '')
    if search_query:
        monografias = Monografia.objects.filter(titulo__icontains=search_query)
    else:
        monografias = Monografia.objects.all()
    return render(request, 'core/monografia_list.html', {'monografias': monografias})

# UPDATE
@login_required
def monografia_edit(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)
    if request.method ==  'POST':
      form = MonografiaForm(request.POST, request.FILES, instance=monografia)
      if form.is_valid():
           form.save()
           messages.success(request, 'Monografia atualizada com sucesso!')
           return redirect('monografia_list')
      else:
       messages.error(request, 'Erro ao atualizar monografia. Verifique os dados fornecidos.')
       form = MonografiaForm(instance=monografia)

    return render(request, 'core/monografia_form.html', {'form': form,})

# DELETE
@login_required
def monografia_delete(request, pk):
  monografia = get_object_or_404(Monografia, pk=pk)
  if request.method ==  'POST':
      form = MonografiaForm(request.POST, request.FILES, instance=monografia)
      monografia.delete()
      messages.success(request, 'Monografia removida com sucesso!')
      return redirect('monografia_list')
  else:
    messages.error(request, 'Erro ao remover monografia.')
  return render(request, 'core/monografia_confirm_delete.html', {'form': form})

# DETAILS
def monografia_detail(request, pk):
    monografia = get_object_or_404(Monografia, pk=pk)
    return render(request, 'core/monografia_detail.html', {'monografia': monografia})

# API (kinda of non-functional as of now)
class MonografiaViewSet(viewsets.ModelViewSet):
    queryset = Monografia.objects.all()
    serializer_class = MonografiaSerializer