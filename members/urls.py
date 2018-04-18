
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
    path('update_assignment/<int:assignment_id>/', views.update_assignment, name='update'),
    path('delete_assignment/<int:assignment_id>/', views.delete_assignment, name='delete'),
]
