from django.db import models

# Create your models here.
class Post(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='post_owner')
    title = models.CharField(max_length=200)
    body = models.CharField()

    def __str__(self):
        return self.title 


class Comment(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comment_owner')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=600)

    def __str__(self):
        return self.body



