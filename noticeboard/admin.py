from django.contrib import admin

from noticeboard.models import NoticeBoard, Notification

admin.site.register(NoticeBoard)
admin.site.register(Notification)
