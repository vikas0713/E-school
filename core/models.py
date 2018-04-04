from django.db import models


# Create your models here.


class Core(models.Model):
    """
	Base model of the project
	"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
