# dcomp-acadbase/dcomp_acadbase/core/serializers.py

from rest_framework import serializers
from .models import Monografia

class MonografiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monografia
        fields = '__all__'