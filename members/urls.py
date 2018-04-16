from django.conf.urls import url
from django.urls import path

from members import views


app_name = 'members'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('details/<int:assignment_id>', views.assignment_status, name='status'),
    path('complete/<int:assignment_id>/<int:student_id>', views.complete, name='complete'),
    path('completion/', views.completion_status, name='completion'),
]
