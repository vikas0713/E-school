from assignments.models import Assignment
from django import forms

from members.models import Member
from noticeboard.models import NoticeBoard


class AssignmentForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Member.objects.filter(is_parent_or_teacher=True))

    def __init__(self, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        self.fields['standard'].widget.attrs['class'] = 'form-control'
        self.fields['subject'].widget.attrs['class'] = 'form-control'
        self.fields['teacher'].widget.attrs['class'] = 'form-control'
        self.fields['assignment_name'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Assignment
        fields = ['standard', 'subject', 'assignment_name', 'teacher']


class NoticeForm(forms.ModelForm):
    posted_by = forms.ModelChoiceField(queryset=Member.objects.filter(is_parent_or_teacher=True))

    class Meta:
        model = NoticeBoard
        fields = ['notification_name', 'standard', 'posted_by']
