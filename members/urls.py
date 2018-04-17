
from django.urls import path

from members import views


app_name = 'members'
urlpatterns = [

    path('login/', views.login, name='login'),
    path('logout/$', views.user_logout,name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('details/<int:assignment_id>', views.assignment_status, name='status'),
    path('complete/<int:assignment_id>/<int:student_id>', views.complete, name='complete'),
    path('create_assignment', views.create_assignment, name='create'),

]
