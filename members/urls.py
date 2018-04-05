from django.conf.urls import url
from django.urls import path

from members import views


app_name = 'members'
urlpatterns = [

    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
