from django.db import models
from django.db.models import CASCADE

from core.models import Core
from members.models import Member
from standards.models import Standard
from subjects.models import Subject


class Assignment(Core):
	"""
	Assignment given to a specific class
	"""
	assignment_name = models.CharField(max_length=50)
	subject = models.ForeignKey(Subject, on_delete=CASCADE)
	standard = models.ForeignKey(Standard, on_delete=CASCADE)
	teacher = models.ForeignKey(Member, on_delete=CASCADE)

	def __str__(self):
		return self.assignment_name
