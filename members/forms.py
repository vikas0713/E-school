from assignments.models import Assignment
from django import forms


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['standard', 'subject', 'assignment_name', 'teacher']