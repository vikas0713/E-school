from django.db import models
from django.db.models import CASCADE

from core.models import Core
from standards.models import Standard


class Assignment(Core):
	"""
	Assignment given to a specific class
	"""
	assignment_name = models.CharField(max_length=50)
	standard = models.ForeignKey(Standard, on_delete=CASCADE)

	def __str__(self):
		return self.assignment_name
