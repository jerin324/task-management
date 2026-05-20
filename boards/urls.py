from django.urls import path

from .views import (
    BoardListCreateView,
    BoardDetailView,
    ShareBoardView
)

urlpatterns = [

    path('', BoardListCreateView.as_view()),
    path('<int:pk>/',BoardDetailView.as_view()),
    path('<int:board_id>/share/',ShareBoardView.as_view()),
]