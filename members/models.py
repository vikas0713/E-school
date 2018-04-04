from django.contrib.auth.models import AbstractUser
from django.db import models


class Member(AbstractUser):
	"""
	Member models, participating in school activities
	"""
	is_parent_or_teacher = models.BooleanField(default=False, help_text="if not checked , then default will be parent")

	def __str__(self):
		return self.username
