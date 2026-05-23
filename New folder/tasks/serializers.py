from rest_framework import serializers

from .models import Task, Comment


class CommentSerializer(serializers.ModelSerializer):

    user_email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:

        model = Comment

        fields = '__all__'

        read_only_fields = [
            'user',
            'task',
            'user_email'
        ]


class TaskSerializer(serializers.ModelSerializer):

    comments = CommentSerializer(
        many=True,
        read_only=True
    )

    class Meta:

        model = Task

        fields = '__all__'

        read_only_fields = [
            'created_by',
            'board',
            'comments'
        ]