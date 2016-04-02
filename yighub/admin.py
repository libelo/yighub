from django.contrib import admin

# Register your models here.
from .models import User, Letter, Memo
from .models import BulletinBoard, TaskforceBoard, PublicBoard
from .models import BulletinEntry, TaskforceEntry, PublicEntry
from .models import BulletinComment, TaskforceComment, PublicComment
from .models import BulletinThumbnail, TaskforceThumbnail, PublicThumbnail
from .models import BulletinFile, TaskforceFile, PublicFile
from .models import Album, Photo, PhotoComment

class UserAdmin(admin.ModelAdmin):
	list_per_page = 500
admin.site.register(User, UserAdmin)

admin.site.register(BulletinBoard)
admin.site.register(TaskforceBoard)
admin.site.register(PublicBoard)

admin.site.register(BulletinEntry)
admin.site.register(TaskforceEntry)
admin.site.register(PublicEntry)

admin.site.register(BulletinComment)
admin.site.register(TaskforceComment)
admin.site.register(PublicComment)

admin.site.register(BulletinThumbnail)
admin.site.register(TaskforceThumbnail)
admin.site.register(PublicThumbnail)

admin.site.register(BulletinFile)
admin.site.register(TaskforceFile)
admin.site.register(PublicFile)

admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(PhotoComment)

admin.site.register(Letter)
admin.site.register(Memo)
