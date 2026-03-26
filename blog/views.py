from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, RegisterSerializer

# Swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# -------------------- POST --------------------

class PostListCreate(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Отримати список всіх постів",
        responses={200: PostSerializer(many=True)}
    )
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Створити новий пост",
        request_body=PostSerializer,
        responses={201: PostSerializer}
    )
    def post(self, request):
        if not request.user.is_staff:
            return Response(
                {"error": "Only admin users can create posts"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class PostDetail(APIView):

    @swagger_auto_schema(
        operation_description="Отримати пост за ID",
        responses={200: PostSerializer}
    )
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Оновити пост",
        request_body=PostSerializer,
        responses={200: PostSerializer}
    )
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Видалити пост",
        responses={204: "Deleted"}
    )
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------- COMMENT --------------------

class CommentListCreate(APIView):

    @swagger_auto_schema(
        operation_description="Отримати список коментарів",
        responses={200: CommentSerializer(many=True)}
    )
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Створити новий коментар",
        request_body=CommentSerializer,
        responses={201: CommentSerializer}
    )
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):

    @swagger_auto_schema(
        operation_description="Отримати коментар за ID",
        responses={200: CommentSerializer}
    )
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Оновити коментар",
        request_body=CommentSerializer,
        responses={200: CommentSerializer}
    )
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Видалити коментар",
        responses={204: "Deleted"}
    )
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):

    @swagger_auto_schema(
        operation_description="Login user and get token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: "Token returned"}
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        return Response({"error": "Invalid credentials"}, status=400)

class RegisterView(APIView):

    @swagger_auto_schema(
        operation_description="Register new user",
        request_body=RegisterSerializer,
        responses={201: "User created"}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created"}, status=201)
        return Response(serializer.errors, status=400)