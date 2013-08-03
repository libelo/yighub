from yighub.models import User, Letter, Memo
from yighub.models import BulletinBoard, TaskforceBoard, PublicBoard
from yighub.models import BulletinEntry, TaskforceEntry, PublicEntry
from yighub.models import BulletinComment, TaskforceComment, PublicComment
from yighub.models import BulletinFile, TaskforceFile, PublicFile

from django.contrib import admin

admin.site.register(User)

admin.site.register(BulletinBoard)
admin.site.register(TaskforceBoard)
admin.site.register(PublicBoard)

admin.site.register(BulletinEntry)
admin.site.register(TaskforceEntry)
admin.site.register(PublicEntry)

admin.site.register(BulletinComment)
admin.site.register(TaskforceComment)
admin.site.register(PublicComment)

admin.site.register(BulletinFile)
admin.site.register(TaskforceFile)
admin.site.register(PublicFile)

admin.site.register(Letter)
admin.site.register(Memo)