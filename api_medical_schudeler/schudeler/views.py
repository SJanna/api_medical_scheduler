from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Persona, Citas
from .serializers import PersonaSerializer, UserSerializer, CitasSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.utils import timezone
import datetime


class Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(username=user)
        return queryset


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Persona.objects.filter(user=user)
        else:
            queryset = Persona.objects.none()  # Retorna una consulta vacía
        return queryset


import datetime

class CitasViewSet(viewsets.ModelViewSet):
    queryset = Citas.objects.all()
    serializer_class = CitasSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        persona = Persona.objects.get(user=self.request.user)
        activas = Citas.objects.filter(activa=True, persona=persona)
        citas = Citas.objects.filter(activa=True)

        # Obtiene la fecha y hora de inicio de la nueva cita
        fecha_hora = serializer.validated_data['fecha_hora']
        print('Fecha actual:', fecha_hora)
        # Verifica si la fecha y hora de la nueva cita es posterior a la hora actual
        if fecha_hora < timezone.now():
            raise ValidationError("The appointment time must be in the future.")

        # Calcula la fecha y hora hasta una hora después de la nueva cita
        fecha_hora_despues = fecha_hora + timezone.timedelta(seconds=3599)
        fecha_hora_antes = fecha_hora - timezone.timedelta(seconds=3599)
        
        # Verifica si existe una cita activa con la misma fecha o hasta una hora después
        existe_cita = citas.filter(fecha_hora__range=(fecha_hora_antes, fecha_hora_despues)).exists()
        print(citas)
        if existe_cita:
            raise ValidationError("There is already a cita scheduled for that time or within one hour.")
        elif activas.count() >= 300:
            raise ValidationError("Maximum limit of active citas reached.")
        else:
            serializer.save(persona=persona)
