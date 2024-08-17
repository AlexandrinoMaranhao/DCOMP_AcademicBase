from django.shortcuts import render
from rest_framework import viewsets
from .models import Monografia, Banca
from .serializers import MonografiaSerializer, BancaSerializer

# Create your views here.
def index(request):
    return render(request, 'index.html')

class MonografiaViewSet(viewsets.ModelViewSet):
    queryset = Monografia.objects.all()
    serializer_class = MonografiaSerializer


class BancaViewSet(viewsets.ModelViewSet):
    queryset = Banca.objects.all()
    serializer_class = BancaSerializer