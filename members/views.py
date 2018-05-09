import csv
import datetime
import json
import os.path

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas

from assignments.models import Assignment, FinishedAssignment, Report
from members.forms import AssignmentForm, NoticeForm
from members.utility.utils import Authenticate
from noticeboard.models import Notification
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


@csrf_exempt
def user_logout(request):
    if request.user:
        auth.logout(request)
        return HttpResponseRedirect(reverse('members:login'))


@csrf_exempt
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
    """
    Finished Assignments are created
    :param request:
    :param assignment_id:
    :param student_id:
    :return:
    """
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


@login_required(login_url='/members/login/')
def create_assignment(request):
    """
    Assignment entities are used in django model form to create assignment
    :param request:
    :return:
    """
    form_class = AssignmentForm

    if request.method == 'GET':
        form = form_class()
        return render(request, 'create_assignment.html', {'form': form, 'create': True})

    elif request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid:
            form.save()
            return render(request, 'create_assignment.html', {'form': form, 'create': True})


def update_assignment(request, assignment_id):
    """
    Assignment will be Updated
    :param request:
    :param assignment_id:
    :return:
    """
    obj = get_object_or_404(Assignment, id=assignment_id)
    form = AssignmentForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()

        return HttpResponseRedirect(reverse('members:dashboard'))

    context = {

        'assignment': obj,
        'form': form,
        'create': False,
    }
    return render(request, 'create_assignment.html', context)


def delete_assignment(request, assignment_id):
    """
    Assignment will be Deleted
    :param request:
    :param assignment_id:
    :return:
    """
    obj = get_object_or_404(Assignment, id=assignment_id)
    obj.delete()
    messages.success(request, 'successfully deleted')
    return HttpResponseRedirect(reverse('members:dashboard'))


@csrf_exempt
def sorting_subject(request):
    """
    The Assignment is Ordered by Subject
    :param request:
    :return:
    """
    all_results = []
    if request.user.is_parent_or_teacher:
        for subject in Subject.objects.filter(teacher_id=request.user.id).order_by('subject_name'):
            all_results.append({'subject': subject, 'assignments': Assignment.objects.filter(standard_id=subject.standard_id).order_by('assignment_name')})
        return render(request, 'sorting_subject.html', {'results': all_results})
    else:
        for student in Student.objects.filter(parent_id=request.user.id):
            obj = {
                "student": student,
                "assignments": []
            }
            for assignment in Assignment.objects.filter(standard_id=student.standard_id).order_by('subject__subject_name'):
                if FinishedAssignment.objects.filter(student_id=student.id, assignment_id=assignment.id).exists():
                    status = True
                else:
                    status = False
                obj["assignments"].append({"assignment": assignment, "status": status,
                                           "time": assignment.created_at,
                                           "subject": assignment.subject})

            all_results.append(obj)
        return render(request, 'sorting_subject.html', {'results': all_results})


@csrf_exempt
def sorting_assignment(request):
    """
    The assignment is Ordered by Assignment
    :param request:
    :return:
    """
    all_results = []
    if request.user.is_parent_or_teacher:
        for subject in Subject.objects.filter(teacher_id=request.user.id):
            all_results.append({'subject': subject, 'assignments': Assignment.objects.filter(standard_id=subject.standard_id).order_by('assignment_name')})
        return render(request, 'sorting_assignment.html', {'results': all_results})
    else:
        for student in Student.objects.filter(parent_id=request.user.id):
            obj = {
                "student": student,
                "assignments": []
            }
            for assignment in Assignment.objects.filter(standard_id=student.standard_id).order_by('assignment_name'):
                if FinishedAssignment.objects.filter(student_id=student.id, assignment_id=assignment.id).exists():
                    status = True
                else:
                    status = False
                obj["assignments"].append({"assignment": assignment, "status": status,
                                           "time": assignment.created_at,
                                           "subject": assignment.subject})

            all_results.append(obj)
        return render(request, 'sorting_assignment.html', {'results': all_results})


@csrf_exempt
def sorting_standard(request):
    """
    The assignment is Ordered by Standard
    :param request:
    :return:
    """
    results = []
    if request.user.is_parent_or_teacher:
        for assignment in Assignment.objects.filter(teacher_id=request.user.id).order_by('standard__standard_identifier'):
            if results:
                available_standards = [k["standard"] for k in results]
                if assignment.standard in available_standards:
                    for each_standard in results:
                        if assignment.standard == each_standard["standard"]:
                            each_standard["assignments"].append(assignment)
                            break
                else:
                    results.append({"standard": assignment.standard,
                                    "assignments": [assignment]})

            else:
                results.append({"standard": assignment.standard,
                                "assignments": [assignment]})
        return render(request, 'sorting_standard.html', {"results": results})
    else:
        for student in Student.objects.filter(parent_id=request.user.id).order_by('standard__subject__subject_name'):
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

            results.append(obj)

        return render(request, 'sorting_standard.html', {"results": results})


@csrf_exempt
def notifications(request):
    """
    To show notice on Parent pannel as notification
    :return: notice,class, and posted_for
    """
    data = []
    for notification in Notification.objects.filter(notice_courtesy_id=request.user.id):

        data.append({'notice': notification.notice,
                     'class': notification.notice.standard,
                     'posted_for': notification.notice_courtesy,
                     'created_at': notification.notice.created_at,
                     'obj_id': notification.id,
                     'is_read':notification.is_read})
    return render(request, 'notifications.html', {'data': data})


@csrf_exempt
def create_notice(request):
    """
    To create notice by Teacher and used only in Teacher's Pannel
    :param request: Get request to render form
    :return: NoticeBoard Form entities 'notification_name','standard','posted_by'
    """
    if request.method == 'GET':
        form = NoticeForm()

        return render(request, 'create_notice.html', {'form': form})

    elif request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid:
            form.save()
            return render(request, 'create_notice.html', {'form': form})


@csrf_exempt
def notification_check(request):
    """
    :param request:
    :return:
    """
    if not request.user.is_parent_or_teacher:
        data = json.loads(request.body.decode(encoding='UTF-8'))
        if request.method == 'POST':
            for each_data in data['data']:
                obj = Notification.objects.get(id=int(each_data))
                obj.is_read = True
                obj.save()

    return HttpResponse('ok')


@csrf_exempt
def pdf_response(request):
    """
    response if assignment in pdf format
    :param requsest:
    :return:
    """
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pdf_report.pdf"'
    p = canvas.Canvas(response)
    coordinate_range = [i for i in range(750, 100, -50)]
    if not request.user.is_parent_or_teacher:
        for student, coordinate in zip(Student.objects.filter(parent_id=request.user.id), coordinate_range):
            student_str = 'student' + str(student)
            for assignments in Assignment.objects.filter(standard_id=student.standard_id):
                if FinishedAssignment.objects.filter(student_id=student.id,
                                                     assignment_id=assignments.id):
                    status = "completed"
                else:
                    status = "Not completed"

                student_str += "Assignment" + str(assignments) + "Status" + str(status) +"Subject" + \
                               str(assignments.subject)+"\n"

                p.drawString(0, coordinate, student_str)

        p.showPage()
        p.save()
        path = os.path.exists('/home/ayush/Downloads/pdf_report.pdf')

        if path:
            return HttpResponse("Sorry You Cannot Download the Document more than one ")
        else:
            return response


@csrf_exempt
def csv_response(request):
    """
    response if assignment in comma seperated values(CSV) format
    :param request:
    :return:
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_report.csv"'
    coordinate_range = [i for i in range(750, 100, -50)]
    writer = csv.writer(response)
    writer.writerow(["Student Name", "Class", "Subject", "Assignment Name", "Status"])
    writer.writerow([" "])
    if not request.user.is_parent_or_teacher:
        # Check if the record for specific user/parent exists
        # check if the difference of record time and current time is greater than limit
        # Download report and update record time with current time
        # else user/parent does not have permission
        # else Download report and create record.
        if Report.objects.filter(reported_user_id=request.user.id).exists():
            stored_obj = Report.objects.get(reported_user_id=request.user.id)
            time_t1 = stored_obj.report_time
            time_t2 = timezone.now()
            time_gap = (time_t2 - time_t1).seconds
            minutes = time_gap/60
            limit = 1440
            if minutes > limit:
                stored_obj.report_time = time_t2
                stored_obj.save()
                for student, coordinate in zip(Student.objects.filter(parent_id=request.user.id),
                                               coordinate_range):
                    student_str = ('student' + str(student))
                    for assignments in Assignment.objects.filter(standard_id=student.standard_id):
                        if FinishedAssignment.objects.filter(student_id=student.id,
                                                             assignment_id=assignments.id):
                            status = "completed"
                        else:
                            status = "Not completed"

                    student_str += (
                            "Subject" + str(assignments.subject) + "Assignment"
                            + str(assignments) + "Status" + str(status) + "Subject" +
                            str(assignments.subject) + "\n")
                    writer.writerow(
                        [student.student_name, student.standard, assignments.subject,
                         assignments.assignment_name,
                         status])
                return response
            else:
                return HttpResponse("User Parent doesn't have permission For Next 24 hr's!!")
        else:
            Report.objects.create(report_time=datetime.datetime.now(), reported_user=request.user)
            for student, coordinate in zip(Student.objects.filter(parent_id=request.user.id),
                                           coordinate_range):
                student_str = ('student' + str(student))
                for assignments in Assignment.objects.filter(standard_id=student.standard_id):
                    if FinishedAssignment.objects.filter(student_id=student.id,
                                                         assignment_id=assignments.id):
                        status = "completed"
                    else:
                        status = "Not completed"

                student_str += (
                        "Subject" + str(assignments.subject) + "Assignment" + str(assignments)
                        + "Status" + str(status) + "Subject" +
                        str(assignments.subject) + "\n")
                writer.writerow(
                    [student.student_name, student.standard, assignments.subject,
                     assignments.assignment_name,
                     status])
            return response








