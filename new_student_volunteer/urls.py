from django.conf.urls import url

from . import views
app_name='new_student_volunteer'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]
