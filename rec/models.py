from django.db import models
from django.contrib.auth.models import User
from easy_thumbnails.fields import ThumbnailerImageField

class Profile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=25, blank=True)
    image = ThumbnailerImageField(upload_to='profile_images/%Y/%m/%d', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def __unicode__(self):
        return self.name

class Mix(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, related_name='mixes')
    parent = models.ForeignKey('Mix', related_name='remixes', null=True, blank=True)
    file = models.FileField(upload_to='mixes/%Y/%m/%d', blank=True)
    tempo = models.IntegerField()
    title = models.CharField(max_length=25)
    play_count = models.IntegerField()
    favorites = models.ManyToManyField(User, related_name='favorite_mixes', blank=True)

    def __unicode__(self):
        return self.title

class Track(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    mix = models.ForeignKey('Mix', related_name='tracks')
    author = models.ForeignKey(User, related_name='tracks')
    sound = models.ForeignKey('TrackSound', related_name='tracks')
    offset = models.IntegerField() # ms
    volume = models.IntegerField()

    def __unicode__(self):
        return self.sound.title

class TrackSound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='track_sounds')
    file = models.FileField(upload_to='tracks/%Y/%m/%d')
    tempo = models.IntegerField()
    title = models.CharField(max_length=25)
    favorites = models.ManyToManyField(User, related_name='favorite_tracks', blank=True)

    def __unicode__(self):
        return self.title

class MixComment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    mix = models.ForeignKey('Mix', related_name='comments')
    author = models.ForeignKey(User, related_name='mix_comments')
    content = models.CharField(max_length=25)

    def __unicode__(self):
        return self.content
