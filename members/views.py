from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from assignments.models import Assignment
from members.models import Member
from members.utility.utils import Authenticate
from students.models import Student
from subjects.models import Subject


def login(request):
    """
    Authenticate registered user by username and password
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('members:dashboard'))
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            auth_obj = Authenticate(username, password)
            user = auth_obj.authenticate_user()
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('members:dashboard'))

    return render(request, 'login.html')


@login_required(login_url='/members/login/')
def dashboard(request):
    """
    dashboard view for parent and teacher
    :param request:
    :return: teacher(subject ,assignment,) parent(student, assignment,)
    """
    all_results = []
    if request.user.is_parent_or_teacher:
        # in case if it's teacher

        for subject in Subject.objects.filter(teacher_id=request.user.id):
            assignment_list = Assignment.objects.filter(standard_id=subject.standard_id)
            all_results.append({'subject': subject, 'assignment': assignment_list})
    else:
        # in case if it's parent

        for student in Student.objects.filter(parent_id=request.user.id):
            assignment_list = Assignment.objects.filter(standard_id=student.standard_id)

            all_results.append({'student': student, 'assignment': assignment_list})
    return render(request, 'dashboard.html', {'results': all_results})
