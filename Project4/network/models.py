from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    posts = models.ForeignKey('Post', on_delete=models.CASCADE, default= None, null=True, blank=True)
    followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)
        
    def serialize(self):
        return {
            "id": self.id,
            "posts": self.posts,
            "text": self.text,
            "following": [user.username for user in self.following.all()],
            "follower": [user.username for user in self.follower.all()]
        }

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, default= None, null=True, blank=True)
    text = models.CharField(max_length = 500)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='user_likes')


    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "text": self.text,
            # "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
            "likes_count": self.likes.count()
        }