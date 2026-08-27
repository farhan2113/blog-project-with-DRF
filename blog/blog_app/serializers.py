from rest_framework import serializers 
from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
User = get_user_model()

class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments = serializers.HyperlinkedRelatedField(
        many= True, view_name = 'comment-detail', read_only= True
    )
    username = serializers.ReadOnlyField(source= 'owner.username')
    class Meta:
        model = Post
        fields = ['url', 'id', 'title', 'body', 'comments', 'username']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.ReadOnlyField(source= 'owner.username')
    
    class Meta:
        model = Comment
        fields = ['url', 'id', 'body', 'post', 'username']


class UserSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(write_only=True)
    email = serializers.CharField()
    class Meta:
        model= User
        fields = ['username', 'email', 'password', 'password_2']


    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

    def validate_password(self, value):
        try:
            password_validation.validate_password(password=value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)

        
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        password_2 = validated_data.pop('password_2')

        if password != password_2:
            raise serializers.ValidationError('the two password fields are not have the same value.')

        user = User.objects.create(username=username, email= email)
        user.set_password(password)
        user.save()

        return validated_data


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['username', 'email', 'password']
