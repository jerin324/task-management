from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Task, Comment
from .serializers import (
    TaskSerializer,
    CommentSerializer
)

from boards.models import Board
from boards.permissions import is_board_member

class TaskListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):

        try:
            board = Board.objects.get(id=board_id)

        except Board.DoesNotExist:
            return Response(
                {"error": "Board not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_board_member(board, request.user):

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        tasks = Task.objects.filter(board=board)

        serializer = TaskSerializer(
            tasks,
            many=True
        )

        return Response(serializer.data)

    def post(self, request, board_id):

        try:
            board = Board.objects.get(id=board_id)

        except Board.DoesNotExist:
            return Response(
                {"error": "Board not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_board_member(board, request.user):

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                board=board,
                created_by=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Task.objects.get(id=pk)

        except Task.DoesNotExist:
            return None

    def get(self, request, pk):

        task = self.get_object(pk)

        if not task:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_board_member(task.board, request.user):

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskSerializer(task)

        return Response(serializer.data)

    def put(self, request, pk):

        task = self.get_object(pk)

        if not task:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_board_member(task.board, request.user):

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):

        task = self.get_object(pk)

        if not task:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_board_member(task.board, request.user):

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        task.delete()

        return Response(
            {"message": "Task deleted"}
        )
        
        
class CommentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):

        try:
            task = Task.objects.get(id=task_id)

        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_board_member(task.board, request.user):

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                task=task,
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )