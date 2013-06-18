from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    published = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    body = models.TextField()

    def __unicode__(self):
        return self.body


#### Models needed for testing NestedObjects

@python_2_unicode_compatible
class Count(models.Model):
    num = models.PositiveSmallIntegerField()
    parent = models.ForeignKey('self', null=True)

    def __str__(self):
        return six.text_type(self.num)


class Event(models.Model):
    date = models.DateTimeField(auto_now_add=True)


class Location(models.Model):
    event = models.OneToOneField(Event, verbose_name='awesome event')


class Guest(models.Model):
    event = models.OneToOneField(Event)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "awesome guest"


class EventGuide(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
