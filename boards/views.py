from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Board, BoardMember
from .serializers import (
    BoardSerializer,
    BoardMemberSerializer
)
from .permissions import is_board_member
from accounts.models import User


class BoardListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        owned_boards = Board.objects.filter(
            owner=request.user
        )

        member_boards = Board.objects.filter(
            members__user=request.user
        )

        boards = owned_boards.union(member_boards)

        serializer = BoardSerializer(
            boards,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = BoardSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                owner=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
        
        
class BoardDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):

        try:
            return Board.objects.get(id=pk)

        except Board.DoesNotExist:
            return None

    def get(self, request, pk):

        board = self.get_object(pk)

        if not board:
            return Response(
                {"error": "Board not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not is_board_member(board, request.user):
            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BoardSerializer(board)

        return Response(serializer.data)

    def put(self, request, pk):

        board = self.get_object(pk)

        if not board:
            return Response(
                {"error": "Board not found"}
            )

        if board.owner != request.user:
            return Response(
                {"error": "Only owner can update board"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = BoardSerializer(
            board,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                owner=request.user
            )

            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self, request, pk):

        board = self.get_object(pk)

        if not board:
            return Response(
                {"error": "Board not found"}
            )

        if board.owner != request.user:
            return Response(
                {"error": "Only owner can delete board"},
                status=status.HTTP_403_FORBIDDEN
            )

        board.delete()

        return Response(
            {"message": "Board deleted"}
        )
        
class ShareBoardView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, board_id):

        try:
            board = Board.objects.get(id=board_id)

        except Board.DoesNotExist:
            return Response(
                {"error": "Board not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if board.owner != request.user:
            return Response(
                {"error": "Only owner can share board"},
                status=status.HTTP_403_FORBIDDEN
            )

        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        member, created = BoardMember.objects.get_or_create(
            board=board,
            user=user
        )

        if not created:
            return Response(
                {"message": "User already added"}
            )

        serializer = BoardMemberSerializer(member)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )