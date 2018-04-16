from django.db import models
from django.db.models import CASCADE

from core.models import Core
from members.models import Member
from standards.models import Standard


class Subject(Core):
	"""
	Subjects according to standards
	"""
	subject_name = models.CharField(max_length=50)
	standard = models.ForeignKey(Standard, on_delete=CASCADE)
	teacher = models.ForeignKey(Member, on_delete=CASCADE)

	class Meta:
		unique_together = ('standard', 'teacher',)

	def __str__(self):
		return self.subject_name
