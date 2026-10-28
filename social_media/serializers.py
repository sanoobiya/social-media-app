from rest_framework import serializers
from django.contrib.auth.models import User
from social_media.models import Post,Comment,Like,Follow

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields=["id","password","username","email","first_name","last_name"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=["id","title","image","description","created_at","owner"]
        read_only_fields=["id","created_at","owner"]

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=["id","comment","added_at","owner","post_obj"]
        read_only_fields=["id","added_at","owner"]

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Like
        fields=["id","post_obj","owner_obj","created_at"]
        read_only_fields=["id","owner_obj","created_at"]

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model=Follow
        fields=["id","follower","following","created_at"]
        read_only_fields=["id","follower","created_at"]
