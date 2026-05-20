from rest_framework import serializers

from .models import Task, Comment


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'

        read_only_fields = [
            'created_by',
            'board'
        ]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

        read_only_fields = [
            'user',
            'task'
        ]