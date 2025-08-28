from django.shortcuts import render
from users.models import Notes
from Backend.serializer import NoteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
# Create your views here.


class NotesView(viewsets.ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]
    
