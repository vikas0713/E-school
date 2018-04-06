from django.db import models
from django.db.models import CASCADE

from assignments.models import Assignment
from core.models import Core
from members.models import Member
from standards.models import Standard


class Student(Core):
	"""
	Students in school
	"""
	student_name = models.CharField(max_length=100)
	standard = models.ForeignKey(Standard, on_delete=CASCADE)
	parent = models.ForeignKey(Member, on_delete=CASCADE)

	def __str__(self):
		return self.student_name
