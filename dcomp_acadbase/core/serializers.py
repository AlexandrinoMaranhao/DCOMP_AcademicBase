from rest_framework import serializers
from .models import Monografia, Banca

class MonografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monografia
        fields = '__all__'

class BancaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banca
        fields = '__all__'