import json

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from assignments.models import Assignment, FinishedAssignment
from members.utility.utils import Authenticate
from students.models import Student
from subjects.models import Subject


@csrf_exempt
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
    ,parent view will return the assignment details of student according to the subject
    and assignment status
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
            obj = {
                "student": student,
                "assignments": []
            }
            for assignment in Assignment.objects.filter(standard_id=student.standard_id):
                if FinishedAssignment.objects.filter(student_id=student.id, assignment_id=assignment.id).exists():
                    status = True
                else:
                    status = False
                obj["assignments"].append({"assignment": assignment, "status": status,
                                           "time": assignment.created_at,
                                           "subject": assignment.subject})

            all_results.append(obj)

    return render(request, 'dashboard.html', {'results': all_results})


@csrf_exempt
@login_required(login_url='/members/login/')
def assignment_status(request, assignment_id):
    """
    weather the assigment is done
    :param request:
    :return:
    """
    if request.user.is_parent_or_teacher:
        response = []
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist as e:
            assignment = None
        if assignment:
            all_students = Student.objects.filter(standard_id=assignment.standard_id)
            student_finished = [
                assignment.student for assignment in
                FinishedAssignment.objects.filter(assignment_id=assignment_id)
            ]
            for each_student in all_students:
                if each_student in student_finished:
                    obj = {
                        "status": True,
                        "student": each_student
                    }
                else:
                    obj = {
                        "status": False,
                        "student": each_student
                    }
                response.append(obj)

            return render(request, 'assignment_status.html', {'content': response, 'assignment': assignment})

        return HttpResponse("Assignment Not Found")


@csrf_exempt
@login_required(login_url='/members/login/')
def complete(request, assignment_id, student_id):
    if request.user.is_parent_or_teacher:
        try:

            # if True:
            assignment = Assignment.objects.get(id=assignment_id)
            student = Student.objects.get(id=student_id)
            data = str(assignment)
            name = str(student)
            FinishedAssignment.objects.create(
                assignment_id=assignment.id, student_id=student.id,
                teacher_id=request.user.id
            )

        except:
            # else:
            data = None
            name = None

        return HttpResponse(content_type='application/json', content=json.dumps({'assignment': data, 'student': name}))




