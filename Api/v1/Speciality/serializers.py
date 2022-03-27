from rest_framework import serializers
from core.Speciality.models import Speciality


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = [
            'id',
            'name',
            'is_active',
        ]
