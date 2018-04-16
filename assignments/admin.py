from django.contrib import admin

from assignments.models import Assignment, FinishedAssignment

admin.site.register(Assignment)
admin.site.register(FinishedAssignment)
