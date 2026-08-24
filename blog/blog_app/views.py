from django.shortcuts import render
from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LogInSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, views
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner= self.request.user)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner= self.request.user)




class SignUpApiView(views.APIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            self.serializer.save()
            data = {
                'username':user.username,
                'email':user.email
            }
            response = Response(data, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,
                samesite='Lax'
            )

            return response
        else:
            return Response(serializer.errors)




class LogInApiView(views.APIView):
    serializer_class = LogInSerializer
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        try:
            user = User.objects.get(username= username, email= email, password= password)
            response = Response({'detail':'loged in sccessfully'}, status=status.HTTP_200_OK)
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            response.set_cookie(
                key='refresh_token',
                value= str(refresh_token),
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            response.set_cookie(
                key='access_token',
                value= str(access_token),
                httponly=True,
                secure=False,
                samesite='Lax'
            )
            return response
        except Exception as e:
            response = Response({'detail':'please enter the correct usernme and email and password'})
            return response





class RefreshAcessTokenApiView(views.APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        try :
            token = RefreshToken(refresh_token)
            access_token = token.access_token
            response = Response({'detail':'access token refreshed'})
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                samesite='Lax',
                httponly=True,
                secure=False
            )
            return response
        except (InvalidToken, TokenError):
            return Response({'detail':'invalid token'})
        
            
