from django.db import models
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Core
from members.models import Member
from standards.models import Standard
from students.models import Student


class NoticeBoard(Core):
    notification_name = models.CharField(max_length=5000)
    standard = models.ForeignKey(Standard, on_delete=CASCADE)
    posted_by = models.ForeignKey(Member, on_delete=CASCADE)

    def __str__(self):
        return str(self.notification_name)


class Notification(Core):
    notice = models.ForeignKey(NoticeBoard, on_delete=CASCADE)
    notice_courtesy = models.ForeignKey(Member, on_delete=CASCADE)
    is_read = models.BooleanField(default=False, help_text="if checked, notice is read")

    def __str__(self):
        return str(self.notice)


@receiver(post_save, sender=NoticeBoard, dispatch_uid=None)
def notification(sender, instance, **kwargs):
    for student in Student.objects.filter(standard=instance.standard):
        parent = student.parent_id

        Notification.objects.get_or_create(notice_id=instance.id, notice_courtesy_id=parent)





