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
            user = serializer.save()
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token
            data = {
                'username':request.data['username'],
                'email':request.data['email'],
                'access':str(access_token)
            }
            response = Response(data, status=status.HTTP_201_CREATED)
            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
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
        serializer = LogInSerializer(data= request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)
        
        user = serializer.validated_data['user']
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        response = Response({'detail':'loged in sccessfully', 'access':str(access_token)}, status=status.HTTP_200_OK)
        response.set_cookie(
            key='refresh_token',
            value= str(refresh_token),
            httponly=True,
            secure=False,
            samesite='Lax'
        )
            
        return response
        





class RefreshAcessTokenApiView(views.APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        try :
            token = RefreshToken(refresh_token)
            access_token = token.access_token
            response = Response({'access':str(access_token)})

            return response
        except (InvalidToken, TokenError):
            return Response({'detail':'invalid token'})
        
class LogOutApiView(views.APIView):
    def post(self, request):
        response = Response({'detail':'loged out successfully'})
        response.delete_cookie(key='refresh_token', samesite='Lax') 
        return response

            
