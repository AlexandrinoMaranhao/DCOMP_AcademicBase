## core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Monografia, Banca
from .serializers import MonografiaSerializer, BancaSerializer

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('index') ## Redirecionaria para Tela Cadastro, Edição ou Remoção
    else:
        form = AuthenticationForm()
        return Response({'msg': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        
    return render(request, 'index.html', {'form': form})

class MonografiaViewSet(viewsets.ModelViewSet):
    queryset = Monografia.objects.all()
    serializer_class = MonografiaSerializer


class BancaViewSet(viewsets.ModelViewSet):
    queryset = Banca.objects.all()
    serializer_class = BancaSerializer