from rest_framework import serializers
from users.models import Notes

class NoteSerializer(serializers.ModelSerializer):
    class meta:
        model = Notes
        fields = ["title", "content", "id"]