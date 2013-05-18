from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

class Comment(models.Model):
    post = models.ForeignKey(Post)
    body = models.TextField()
