# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from models_base import User, Board, Entry, Comment, File, Thumbnail, Tag


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('date_joined', 'last_login', 'ordinal', 'level', 'point')


class BulletinBoard(Board):
    pass

class TaskforceBoard(Board):
    participant = models.ManyToManyField(User, null = True, blank = True)
    archive = models.BooleanField(default = False) 

class PublicBoard(Board):
    pass

class TaskforceBoardForm(forms.ModelForm):
    class Meta:
        model = TaskforceBoard
        fields = ('name', )


class BulletinEntry(Entry):
    board = models.ForeignKey(BulletinBoard)

class TaskforceEntry(Entry):
    board = models.ForeignKey(TaskforceBoard)

class PublicEntry(Entry):
    board = models.ForeignKey(PublicBoard)
    
class BulletinEntryForm(forms.ModelForm):
    class Meta:
        model = BulletinEntry
        fields = ('board', 'title', 'content', 'notice', 'tag')

class TaskforceEntryForm(forms.ModelForm):
    class Meta:
        model = TaskforceEntry
        fields = ('board', 'title', 'content', 'notice', 'tag')

class PublicEntryForm(forms.ModelForm):
    class Meta:
        model = PublicEntry
        fields = ('board', 'title', 'content', 'notice')


class BulletinComment(Comment):
    entry = models.ForeignKey(BulletinEntry, related_name = 'comments')

class TaskforceComment(Comment):
    entry = models.ForeignKey(TaskforceEntry, related_name = 'comments')

class PublicComment(Comment):
    entry = models.ForeignKey(PublicEntry, related_name = 'comments')


class BulletinThumbnail(Thumbnail):
    entry = models.ForeignKey(BulletinEntry, related_name = 'thumbnails')

class TaskforceThumbnail(Thumbnail):
    entry = models.ForeignKey(TaskforceEntry, related_name = 'thumbnails')

class PublicThumbnail(Thumbnail):
    entry = models.ForeignKey(PublicEntry, related_name = 'thumbnails')


class BulletinFile(File):
    entry = models.ForeignKey(BulletinEntry, related_name = 'files')

class TaskforceFile(File):
    entry = models.ForeignKey(TaskforceEntry, related_name = 'files')

class PublicFile(File):
    entry = models.ForeignKey(PublicEntry, related_name = 'files')


class Letter(models.Model):
    sender = models.ForeignKey(User, related_name = 'letter_senders')
    receiver = models.ForeignKey(User, related_name = 'letter_receivers')
    title = models.CharField(max_length = 200)
    content = models.TextField()
    read = models.BooleanField(default = False)
    time_created = models.DateTimeField(auto_now_add = True)
    file = models.FileField(upload_to = 'letter_files/%Y/%m/%d', blank = True)
    file_name = models.CharField(max_length = 200)
    #file_hit ? no.
    # read 를 count_view처럼? No.

    def __unicode__(self):
        return self.title

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ('receiver', 'title', 'content', 'file')

class Memo(models.Model):
    memo = models.CharField(max_length = 200)
    creator = models.ForeignKey(User, related_name = 'memo_creators')
    time_created = models.DateTimeField()

    def __unicode__(self):
        return self.memo

class Album(Board): # 그냥 Album으로 하자.
    #썸네일은 필요없다. 그냥 첫번째 사진을 썸네일로 한다.
    event_time = models.DateField(blank = True, null = True)
    count_view = models.PositiveIntegerField(default = 0)


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('name', 'event_time')

class Photo(models.Model):
    album = models.ForeignKey(Album, related_name = 'photos')
    photo = models.ImageField(upload_to = 'yighub/albums/%Y/%m/%d', ) # 외부용 null = True 
    description = models.TextField(blank = True)
    photographer = models.ForeignKey(User, related_name = 'photographers')
    time_created = models.DateTimeField()
    time_last_modified = models.DateTimeField()
    recommendation = models.ManyToManyField(User, related_name = 'photo_recommendations', blank = True, null = True)
    count_recommendation = models.PositiveIntegerField(default = 0)
    count_comment = models.PositiveIntegerField(default = 0)
    #arrangement는 필요없다. 그냥 id 순서로 늘어놓으면 될 듯.
    tag = models.ManyToManyField(Tag, related_name = 'photos', blank = True, null = True)

    def __unicode__(self):
        if self.description:
            return self.description
        else:
            return self.photographer.name + u'의 사진'

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('photo', 'description')

class PhotoComment(Comment):
    photo = models.ForeignKey(Photo, related_name = 'comments')

"""
class Image(models.Model):
    #...



class Website_Setting(models.Model):
    recruitment_duration # boolean
    president # name, email, phone_number
    vice_president # ''
    not_taskforce # do not shown in taskforce list
    # do not shown in newest list
    apply_form - 이건 아니고
    설명회 날짜
    지원서 마감일
    등등
"""

"""
class Point(models.Model):
    user
    point
    reason
    time
"""

"""
class poll

class choice
"""

# class Log