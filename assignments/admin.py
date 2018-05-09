from django.contrib import admin

from assignments.models import Assignment, FinishedAssignment, Report

admin.site.register(Assignment)
admin.site.register(FinishedAssignment)
admin.site.register(Report)
