from django.urls import path

from .views import (TaskListCreateView,TaskDetailView,CommentCreateView)

urlpatterns = [
    path('board/<int:board_id>/',TaskListCreateView.as_view()),
    path('board/<int:board_id>/tasks/',TaskListCreateView.as_view()),
    path('<int:pk>/',TaskDetailView.as_view()),
    path('comment/<int:task_id>/',CommentCreateView.as_view()),
    path('<int:task_id>/comments/',CommentCreateView.as_view()),
]