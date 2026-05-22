from rest_framework import serializers
from .models import Board, BoardMember

class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ['owner']

class BoardMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = BoardMember
        fields = '__all__'