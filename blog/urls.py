from django.urls import path
from .views import PostListCreate, PostDetail, CommentListCreate, CommentDetail
from .views import LoginView, RegisterView

urlpatterns = [
    # Post
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),

    # Comment
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]