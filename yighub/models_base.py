# -*- coding: utf-8 -*-

from django.db import models

MEMBER_LEVEL_CHOICES = (
                        ('non', 'non-member'),
                        ('pre', 'preliminary member'),
                        ('asc', 'associate member'),
                        ('reg', 'regular member'),
                        ('exe', 'executive member'),
                        ('mgr', 'website manager'),
                        )

def upload_profile_path(instance, filename):
    name = instance.name
    return 'yighub/profiles/%s/%s' % (name, filename)

def upload_avatar_path(instance, filename):
    name = instance.name
    return 'yighub/avatars/%s/%s' % (name, filename)

class User(models.Model):
    user_id = models.CharField(max_length = 30)
    password = models.CharField(max_length = 200) 
    name = models.CharField(max_length = 30)
    date_joined = models.DateField()
    last_login = models.DateTimeField()

    birthday = models.DateField(blank = True, null = True)
    email = models.EmailField(blank = True)
    sns = models.CharField(max_length = 200, blank = True) # sns
    phone_number = models.CharField(max_length = 20, blank = True)
    
    ordinal = models.PositiveSmallIntegerField(blank = True, null = True) # null for non-member

    level = models.CharField(max_length = 3, choices = MEMBER_LEVEL_CHOICES)
    career1 = models.CharField(max_length = 200, blank = True)
    career2 = models.CharField(max_length = 200, blank = True)
    career3 = models.CharField(max_length = 200, blank = True)
    career4 = models.CharField(max_length = 200, blank = True)
    career5 = models.CharField(max_length = 200, blank = True)
    self_introduction = models.TextField(blank = True)
    point = models.PositiveIntegerField(default = 0)

    profile = models.ImageField(upload_to = upload_profile_path, blank = True, ) # 외부용 null = True 
    avatar = models.ImageField(upload_to = upload_avatar_path, blank = True, ) # 내부용 null = True

    def __unicode__(self):
        return self.name

class Board(models.Model):
    name = models.CharField(max_length = 50)
    count_entry = models.PositiveIntegerField(default = 0)
    # due_date = models.DateField(blank = True, null = True)
    newest_entry = models.PositiveIntegerField(null = True, blank = True)
    newest_time = models.DateTimeField(null = True, blank = True) 
    permission_reading = models.CharField(max_length = 3, choices = MEMBER_LEVEL_CHOICES, default = 'non')
    permission_writing = models.CharField(max_length = 3, choices = MEMBER_LEVEL_CHOICES, default = 'non')

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length = 200)

class Entry(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name = 'entry_creators')
    time_created = models.DateTimeField()
    time_last_modified = models.DateTimeField()
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

class Comment(models.Model):
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

def upload_thumbnail_path(instance, filename):
    board = 'board' + str(instance.entry.board.id)
    time = instance.entry.time_created
    return 'yighub/thumbnails/%s/%s/%s/%s/%s' % (board, time.year, time.month, time.day, instance.name)

class Thumbnail(models.Model):
    name = models.CharField(max_length = 200)
    thumbnail = models.ImageField(upload_to = upload_thumbnail_path)

    def __unicode__(self):
        return self.name

def upload_file_path(instance, filename):
    board = 'board' + str(instance.entry.board.id)
    time = instance.entry.time_created
    return 'yighub/files/%s/%s/%s/%s/%s' % (board, time.year, time.month, time.day, instance.name)

class File(models.Model):
    name = models.CharField(max_length = 200)
    file = models.FileField(upload_to = upload_file_path)
    hit = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        return self.name
