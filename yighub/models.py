# -*- coding: utf-8 -*-

from django.db import models
from django import forms

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

class Board(models.Model):
    name = models.CharField(max_length = 50)
    count_entry = models.PositiveIntegerField(default = 0)
    # due_date = models.DateField(blank = True, null = True)
    newest_entry = models.PositiveIntegerField(null = True, blank = True)
    newest_time = models.DateTimeField(null = True, blank = True) 
    participant = models.ManyToManyField(User, null = True, blank = True)
    archive = models.BooleanField(default = False) 
    authority = models.CharField(max_length = 3, choices = MEMBER_LEVEL_CHOICES) # permission으로 바꾸기

    def __unicode__(self):
        return self.name

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'participant')

class Tag(models.Model):
    name = models.CharField(max_length = 200)

class Entry(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name = 'entry_creators')
    board = models.ForeignKey(Board)
    time_created = models.DateTimeField(auto_now_add = True)
    time_last_modified = models.DateTimeField(auto_now = True)
    count_comment = models.PositiveIntegerField(default = 0)
    recommendation = models.ManyToManyField(User, related_name = 'entry_recommendations', blank = True, null = True)
    count_view = models.PositiveIntegerField(default = 0)
    count_recommendation = models.PositiveIntegerField(default = 0)
    notice = models.BooleanField(default = False)
    
    # hierarchy funcionality
    arrangement = models.PositiveIntegerField() # better to number or arrange_number ? number_arrange ?
    depth = models.PositiveSmallIntegerField(default = 0)
    parent = models.PositiveIntegerField(null = True, blank = True) # must be pk
    
    tag = models.ManyToManyField(Tag, related_name = 'entrys', blank = True, null = True)

    def __unicode__(self):
        return self.title

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('board', 'title', 'content', 'notice')

class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name='comment_creators')
    time_created = models.DateTimeField(auto_now_add = True)
    recommendation = models.ManyToManyField(User, related_name = 'comment_recommendations', blank = True, null = True)
    count_recommendation = models.PositiveIntegerField(default = 0)

    # hierarchy functionality
    arrangement = models.PositiveIntegerField()
    depth = models.PositiveSmallIntegerField(default = 0)
    parent = models.PositiveIntegerField(null = True, blank = True)
    
    def __unicode__(self):
        return self.content

class File(models.Model):
    entry = models.ForeignKey(Entry, related_name = 'files') 
    name = models.CharField(max_length = 200)
    file = models.FileField(upload_to = 'files/%Y/%m/%d', )
    hit = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        return self.name

class Intro(models.Model): # do not allow comment, and so on... diffrent from entry.
    
    INTRO_BOARD_CHOICES = (
                    ('int', 'introduction'),
                    ('vis', 'vision'),
                    ('act', 'activity'),
                    ('his', 'history'),
                    ('cli', 'clipping'),
                    ('rec', 'recruiting'),
                    ('apy', 'apply'),
                    ('sch', 'schedule'),
                    ('uni', 'universe'),
                    ('sima', 'simA fund'),
                    ('simb', 'simB fund'),
                    ('simv', 'simV fund'),
                    ('con', 'contact us'),
                    )
    board = models.CharField(max_length = 4, choices = INTRO_BOARD_CHOICES)
    title = models.CharField(max_length = 200, blank = True)
    content = models.TextField()
    time_last_modified = models.DateTimeField(auto_now = True)
    count_view = models.PositiveIntegerField(default = 0)
    file = models.FileField(upload_to = 'intro_files', )
    file_name = models.CharField(max_length = 200)
    hit = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        print self.title

class IntroForm(forms.ModelForm):
    class Meta:
        model = Intro
        fields = ('board', 'title', 'content', 'file')

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