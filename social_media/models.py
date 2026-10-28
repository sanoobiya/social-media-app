from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
# Create your models here.


class Post(models.Model):
    title=models.CharField(max_length=200)
    image=models.ImageField(upload_to="posts",null=True)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")

    class Meta:
        ordering=["-created_at"]
    def __str__(self):
        return self.title


class Comment(models.Model):
    comment=models.CharField(max_length=300)
    added_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
    post_obj=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")

    class Meta:
        ordering=["-added_at"]
    def __str__(self):
        return f"Comment by {self.owner} on {self.post_obj_id}"

class Like(models.Model):
    post_obj=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
    owner_obj=models.ForeignKey(User,on_delete=models.CASCADE,related_name="likes")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[UniqueConstraint(fields=["owner_obj","post_obj"],name="unique_user_post_like")]
    def __str__(self):
        return f"{self.owner_obj} likes {self.post_obj_id}"


class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
    following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints=[models.UniqueConstraint(fields=["follower","following"],name="unique_follow")]
    def __str__(self):
        return f"{self.follower} follows {self.following}"