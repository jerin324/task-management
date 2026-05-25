from rest_framework import serializers

from .models import Task, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='user.email', read_only=True)
    created_by = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'created_by', 'created_at']

        read_only_fields = [
            'user',
            'task',
            'author',
            'created_by',
            'created_at'
        ]


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.email', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'board', 'title', 'description', 'status', 'created_by', 'created_at', 'comments']

        read_only_fields = [
            'created_by',
            'board',
            'comments',
            'created_at'
        ]