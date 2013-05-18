from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    body = models.TextField()

    def __unicode__(self):
        return self.body