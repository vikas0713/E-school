from django.conf.urls import url


from members import views

urlpatterns = [

    url(r'^index', views.index, name='index'),
]
