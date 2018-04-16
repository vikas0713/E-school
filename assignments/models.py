from django.db import models
from django.db.models import CASCADE

from core.models import Core
from members.models import Member
from standards.models import Standard
from students.models import Student
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


class FinishedAssignment(Core):
	"""
	Assignment is done or not
	"""
	student = models.ForeignKey(Student, on_delete=CASCADE)
	assignment = models.ForeignKey(Assignment, on_delete=CASCADE)
	teacher = models.ForeignKey(Member, on_delete=CASCADE)

	def __str__(self):
		return str(self.assignment.assignment_name) + '--' + str(self.student.id)
