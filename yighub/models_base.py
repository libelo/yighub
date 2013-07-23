# -*- coding: utf-8 -*-

from django.db import models

class Board(models.Model):
    name = models.CharField(max_length = 50)
    count_entry = models.PositiveIntegerField(default = 0)
    # due_date = models.DateField(blank = True, null = True)
    newest_entry = models.PositiveIntegerField(null = True, blank = True)
    newest_time = models.DateTimeField(null = True, blank = True) 
    permission_writing = models.CharField(max_length = 3, choices = MEMBER_LEVEL_CHOICES)
    permission_reading = models.CharField(max_length = 3, choices = MEMBER_LEVEL_CHOICES)

    def __unicode__(self):
        return self.name

class Entry(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    creator = models.ForeignKey(User, related_name = 'entry_creators')
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

class File(models.Model):
    entry = models.ForeignKey(Entry, related_name = 'files') 
    name = models.CharField(max_length = 200)
    file = models.FileField(upload_to = 'files/%Y/%m/%d', )
    hit = models.PositiveIntegerField(default = 0)

    def __unicode__(self):
        return self.name