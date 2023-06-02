from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Persona, Citas

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PersonaSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Persona
        fields = ('id', 'user', 'nombre', 'apellidos', 'numero_identificacion', 'celular')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(user_data)
        persona = Persona.objects.create(user=user, **validated_data)
        return persona
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data is not None:
            user_serializer = UserSerializer(instance.user, data=user_data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
        return super().update(instance, validated_data)

class CitasSerializer(serializers.ModelSerializer):
    # persona = serializers.ReadOnlyField(source='persona.username')
    
    class Meta:
        model = Citas
        fields = ('id', 'sede', 'fecha_hora', 'descripcion', 'activa', 'persona')
        read_only_fields = ('persona',)
