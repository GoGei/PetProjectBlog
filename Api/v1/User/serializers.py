from rest_framework import serializers
from Api.v1.Speciality.serializers import SpecialitySerializer
from core.User.models import User, Patient, Doctor
from core.Speciality.models import Speciality


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'is_active',
        ]

    def validate(self, data):
        try:
            User.objects.get(email=data['email'])
            raise serializers.ValidationError({'user': 'User with this email is already exists'})
        except User.DoesNotExist:
            return data


class PatientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'user',
            'address',
        ]


class DoctorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'user',
            'speciality',
            'price',
            'salary_percent',
        ]


class UserBaseSerializerFields(serializers.ModelSerializer):
    BASE_FIELDS = [
        'id',
        'email',
        'first_name',
        'last_name',
        'is_active',
    ]
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    is_active = serializers.BooleanField(source='user.is_active')


class SuperuserBaseSerializerFields(UserBaseSerializerFields):
    BASE_FIELDS = [
                      'is_staff',
                      'is_superuser',
                  ] + UserBaseSerializerFields.BASE_FIELDS

    is_staff = serializers.BooleanField(source='user.is_staff')
    is_superuser = serializers.BooleanField(source='user.is_superuser')


class PatientSerializer(UserBaseSerializerFields):
    class Meta:
        model = Patient
        fields = [
                     'address',
                 ] + UserBaseSerializerFields.BASE_FIELDS


class DoctorSerializer(SuperuserBaseSerializerFields):
    speciality = serializers.CharField(source='speciality.label')

    class Meta:
        model = Doctor
        fields = [
                     'price',
                     'speciality',
                     'indexed_tax',
                     'salary_percent',
                 ] + SuperuserBaseSerializerFields.BASE_FIELDS
