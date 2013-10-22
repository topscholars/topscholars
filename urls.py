from django.conf.urls import patterns, url

from tsweb import views

urlpatterns = patterns('',
                       url(r'^$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'teacher/classlist/', views.tclasslist, name='tclasslist'),
                       url(r'teacher/processajax/', views.tprocessajax, name='tprocessajax'),
                       url(r'teacher/assignmentlist/', views.tassignmentlist, name='tassignmentlist'),
                       url(r'teacher/studentlist/', views.tstudentlist, name='tstudentlist'),
                       url(r'teacher/rubriclist/', views.trubriclist, name='trubriclist'),
                       url(r'teacher/submissionlist/', views.tsubmissionlist, name='tsubmissionlist'),
                       url(r'teacher/submissionreview/(?P<id>\d+)/', views.tsubmissionreview, name='tsubmissionreview'),

                       url(r'index/', views.sindex, name='sindex'),

)
