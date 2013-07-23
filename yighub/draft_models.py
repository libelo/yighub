# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from base_model import Board, Entry, Comment, File

MEMBER_LEVEL_CHOICES = (
                        ('non', 'non-member'),
                        ('pre', 'preliminary member'),
                        ('asc', 'associate member'),
                        ('reg', 'regular member'),
                        ('exe', 'executive member'),
                        ('mgr', 'website manager'),
                        )

class User(models.Model):
    user_id = models.CharField(max_length = 30)
    password = models.CharField(max_length = 200) 
    name = models.CharField(max_length = 30)
    date_joined = models.DateField(auto_now_add = True)
    last_login = models.DateTimeField()

    birthday = models.DateField(blank = True, null = True)
    email = models.EmailField(blank = True)
    messenger = models.CharField(max_length = 50, blank = True) # sns
    phone_number = models.PositiveIntegerField(blank = True, null = True) # force users to input only numbers, for consistency
    
    ordinal = models.PositiveSmallIntegerField(blank = True, null = True) # null for non-member

    level = models.CharField(max_length = 3, choices = MEMBER_LEVEL_CHOICES)
    carrer1 = models.CharField(max_length = 200, blank = True)
    carrer2 = models.CharField(max_length = 200, blank = True)
    carrer3 = models.CharField(max_length = 200, blank = True)
    carrer4 = models.CharField(max_length = 200, blank = True)
    carrer5 = models.CharField(max_length = 200, blank = True)
    self_introduction = models.TextField(blank = True)
    point = models.PositiveIntegerField(default = 0)

    profile = models.ImageField(upload_to = 'images/profiles', blank = True, ) # 내부용 null = True
    picture = models.ImageField(upload_to = 'images/pictures', blank = True, ) # 외부용 null = True

    def __unicode__(self):
        return self.name

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
        fields = ('name', 'participant')


class Tag(models.Model):
    name = models.CharField(max_length = 200)


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
    entry = models.ForeignKey(BulletinEntry)

class TaskforceComment(Comment):
    entry = models.ForeignKey(TaskforceEntry)

class PublicComment(Comment):
    entry = models.ForeignKey(PublicEntry)


class BulletinFile(File):
    entry = models.ForeignKey(BulletinEntry)

class TaskforceFile(File):
    entry = models.ForeignKey(TaskforceEntry)

class PublicFile(File):
    entry = models.ForeignKey(PublicEntry)


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
        print self.title

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ('receiver', 'title', 'content', 'file')

class Memo(models.Model):
    memo = models.CharField(max_length = 200)
    creator = models.ForeignKey(User, related_name = 'memo_creators')
    time_created = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        print self.memo

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