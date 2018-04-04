from django.db import models

# Create your models here.
from core.models import Core


class Standard(Core):
	"""
	Standards in a school
	"""
	standard_name = models.CharField(max_length=10)
	standard_identifier = models.IntegerField(unique=True)

	def __str__(self):
		return self.standard_name
