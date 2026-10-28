from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from social_media.serializers import *
from social_media.models import Post,Comment,Like,Follow
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# Create your views here.

class RegisterView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"User registered successfully"},status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class PostListCreateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def get(self,request):
        posts=Post.objects.all().order_by=("-created_at")
        serializer=PostSerializer(posts,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self,request,pk):
        post=self.get_object(pk)
        if post is None:
            return Response({"message":"Post not found"},status=status.HTTP_404_NOT_FOUND)
        serializer=PostSerializer(post)
        return Response(serializer.data)

    def put(self,request,pk):
        post=self.get_object(pk)
        if post is None:
            return Response({"message":"Post not found"},status=status.HTTP_404_NOT_FOUND)
        if post.owner !=request.user:
            return Response({"message":"You cannot edit another user's post!"},status=status.HTTP_403_FORBIDDEN)
        serializer=PostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save(owner=post.owner)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        post=self.get_object(pk)
        if post is None:
            return Response({"message":"Post not found"},status=status.HTTP_404_NOT_FOUND)
        if post.owner !=request.user:
            return Response({"message":"You cannot edit another user's post!"},status=status.HTTP_403_FORBIDDEN)
        serializer=PostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(owner=post.owner)
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        post=self.get_object(pk)
        if post is None:
            return Response({"message":"Post not found"},status=status.HTTP_404_NOT_FOUND)
        if post.owner !=request.user:
                   return Response({"message":"You cannot delete another user's post!"},status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentListCreateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get (self,request):
        comments=Comment.objects.all().order_by("-added_at")
        post_id=request.query_params.get("post_object")
        if post_id:
            comments=comments.filter(post_object_id=post_id)
        serializer=CommentsSerializer(comments,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
               
class LikeListCreateView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        likes=Like.objects.all().order_by("-created_at")
        serializer=LikeSerializer(likes,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=LikeSerializer(data=request.data)
        if serializer.is_valid():
            post=serializer.validated_data["post_obj"]
            existing_like=Like.objects.filter(owner_obj=request.user,post_obj=post).exists()
            if existing_like:
                return Response({"message":"You have already liked this post!"},status=status.HTTP_400_BAD_REQUEST)
            serializer.save(owner_obj=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LikeDeleteView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def delete(self,request,pk):
        try:
            like=Like.objects.get(pk=pk,owner_obj=request.user)
        except Like.DoesNotExist:
            return Response({"message":"Like not found"},status=status.HTTP_404_NOT_FOUND)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 

class FollowListCreateView(APIView):
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]

    def get(self,request):
        follows=Follow.objects.filter(follower=request.user)
        serializer=FollowSerializer(follows,many=True)
        return Response(serializer.data)

    def post(self,request):
        following_id =request.data.get("following")
        if not following_id:
            return Response({"message":"following user ID is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            following_user=User.objects.get(id=following_id)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
        if following_user==request.user:
            return Response({"message":"You cannot follow yourself"},status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(follower=request.user,following=following_user).exists():
            return Response({"message":"Already following this user"},status=status.HTTP_400_BAD_REQUEST)
        follow=Follow.objects.create(follower=request.user,following=following_user)
        serializer=FollowSerializer(follow)
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class UnfollowView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def delete(self,request,pk):
        try:
            follow=Follow.objects.get(follower=request.user,following_id=pk)
        except Follow.DoesNotExist:
            return Response({"message":"Follow relationship not found"},status=status.HTTP_404_NOT_FOUND)
        follow.delete()
        return Response({"message":"Unfollowed successfully"},status=status.HTTP_200_OK)