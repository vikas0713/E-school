from assignments.models import Assignment
from django import forms

from members.models import Member


class AssignmentForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Member.objects.filter(is_parent_or_teacher=True))

    class Meta:
        model = Assignment
        fields = ['standard', 'subject', 'assignment_name', 'teacher']