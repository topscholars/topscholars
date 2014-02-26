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
                       url(r'teacher/gettags/(?P<entityid>\d+)/', views.gettags, name='gettags'),
                       url(r'teacher/tlessonlist/', views.tlessonlist, name='tlessonlist'),
                       url(r'teacher/ttaglist/', views.ttaglist, name='ttaglist'),
                       url(r'teacher/userlist/', views.tuserlist, name='tuserlist'),
                       url(r'teacher/unitlist/', views.tunitlist, name='tunitlist'),
                       
                       url(r'google_register/', views.google_register, name='google_register'),
                       url(r'google/', views.google, name='google'),
                       url(r'index/', views.sindex, name='sindex'),
                       url(r'student/submissionreview/(?P<id>\d+)/', views.stsubmissionreview, name='stsubmissionreview'),

)
