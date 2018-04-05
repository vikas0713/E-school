from django.conf.urls import url


from members import views

urlpatterns = [

    url(r'^login', views.login, name='login'),
]