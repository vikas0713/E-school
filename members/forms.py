from assignments.models import Assignment
from django import forms

from members.models import Member
from noticeboard.models import NoticeBoard


class AssignmentForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Member.objects.filter(is_parent_or_teacher=True))

    class Meta:
        model = Assignment
        fields = ['standard', 'subject', 'assignment_name', 'teacher']


class NoticeForm(forms.ModelForm):
    posted_by = forms.ModelChoiceField(queryset=Member.objects.filter(is_parent_or_teacher=True))

    class Meta:
        model = NoticeBoard
        fields = ['notification_name', 'standard', 'posted_by']
