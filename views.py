# Create your views here.
#Import Django class
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from tsweb.models import *
from ajax.classajax import *
from ajax.assignmentajax import *
from ajax.studentajax import *
from ajax.rubricajax import *
from ajax.submissionajax import *
from ajax.submissionreviewajax import *
from ajax.submissionreviewstudentajax import *
from ajax.loginajax import *
from ajax.userajax import *
from ajax.tagajax import *
from ajax.unitajax import *
from ajax.viewajax import *

#Login View
def login(request):
    username=request.POST.get('txtUsername',False)
    password=request.POST.get('txtPassword',False)
    if username == False:
        return render(request, 'tsweb/login.html', {'username':'','errmsg':''})
    else:
        try:
            user= Login.objects.get(loginname=username,deleted=0)
        except (KeyError, Login.DoesNotExist):
            if username != False or username != '':
                return render(request, 'tsweb/login.html', {'username':username, 'errmsg':'no_user',})
            else:
                return render(request, 'tsweb/login.html', {'username':username, 'errmsg':'',})
        else:
            if user.password == password:
                request.session['userid'] = user.id
                if user.usertypeid == 1:
                    return HttpResponseRedirect(reverse('tsweb:tunitlist'))
                elif user.usertypeid == 2:
                    return HttpResponseRedirect(reverse('tsweb:sindex'))
                else:
                    del request.session['userid']
                    return HttpResponseRedirect(reverse('tsweb:login'))
            else:
                return render(request, 'tsweb/login.html', {'username':username, 'errmsg':'no_password',})

def logout(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('tsweb:login'))
        
#Student Views
def sindex(request):
    try:
        userid = request.session['userid']
    except KeyError:
        pass
    else:
        login = Login.objects.get(id=userid)
        clientid = login.clientid
        studentid = login.recid
        user_name = login.loginname
        studentlist = Studentlist.objects.filter(id=studentid)
        student = Studentlist.objects.get(id=studentid)
        submissionversionid = student.lastsubmissionversionid
        classscheduleid = Studentclass.objects.filter(studentid=studentid, clientid=clientid,disabled=0,deleted=0).values_list('classscheduleid')
        classschedulelist = Classschedule.objects.filter(id__in=classscheduleid,disabled=0,deleted=0)
        submissionlist = Submission.objects.filter(studentid=studentid, disabled=0, deleted=0)
        context= {'studentlist': studentlist,
                  'submissionlist' : submissionlist,
                  'submissioncount':submissionlist.count(),
                  'classschedulelist': classschedulelist,
                  'user_name' : user_name}
        try: 
            submissionversion = Submissionversion.objects.get(id=submissionversionid)
        except Submissionversion.DoesNotExist:
            data_json = { 'status': 'blank', }
        else:
            assignment = submissionversion.submissionid.assignmentid
            context['submissionversion'] = submissionversion
            context['assignment'] = assignment

        try:
            lessonactivitylnkid = Studentlessonactivity.objects.filter(studentid=studentid,clientid=clientid,deleted=0).values_list('lessonactivitylnkid')

        except Studentlessonactivity.DoesNotExist:   
            data_json = { 'status': 'blank', }
        else:
            activityid = Lessonactivitylnk.objects.filter(id__in=lessonactivitylnkid,deleted=0).values_list('activityid')
            lessonactivitylist = Lessonactivity.objects.filter(id__in=activityid,clientid=clientid,deleted=0)
            context['lessonactivitylist'] = lessonactivitylist

        return render(request, 'tsweb/student/index.html', context)

#Teacher Views
def tclasslist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        
        securityprofile = userlist.securityprofileid
        urlActive = 'classlist'
        context= {'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive, }
        return render(request, 'tsweb/teacher/classlist.html', context)

def tassignmentlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        clientid = login.clientid
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        
        securityprofile = userlist.securityprofileid
        classlist = Classschedule.objects.filter(clientid=clientid, disabled=0, deleted=0)
        #selectlist = Selectionlist.objects.filter(selectiongroupid=6, disabled=0, deleted=0)
        urlActive = 'assignmentlist'
        context= {'classlist' : classlist,
                  'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/assignmentlist.html', context)

def tstudentlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        clientid = login.clientid
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        securityprofile = userlist.securityprofileid
        Classschedulelist = Classschedule.objects.filter(disabled=0, deleted=0, clientid=clientid)
        urlActive = 'studentlist'
        context= {'Classschedulelist' : Classschedulelist,
                  'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/studentlist.html', context)

def trubriclist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        securityprofile = userlist.securityprofileid
        urlActive = 'rubriclist'
        context= {'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/rubriclist.html', context)

def tsubmissionlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        securityprofile = userlist.securityprofileid
        urlActive = 'submissionlist'
        context= {'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/submissionlist.html', context)
    
def tlessonlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        securityprofile = userlist.securityprofileid
        urlActive = 'lessonlist'
        
        context= {'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/lessonlist.html', context)
    
def ttaglist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        securityprofile = userlist.securityprofileid
        urlActive = 'taglist'
        
        #category select
        entity = Entity.objects.get(name='Tag')
        entityid = entity.id
        categoryentity = Categoryentity.objects.filter(entityid=entityid).values_list('categoryid')
        categorylist = Category.objects.filter(id__in=categoryentity)
        
        context= {'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'categorylist': categorylist,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/taglist.html', context)
    
def tuserlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        securityprofile = userlist.securityprofileid
        urlActive = 'userlist'
        context= {'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/userlist.html', context)
    
def tunitlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        user_name = login.loginname
        recid = login.recid
        userlist = Userlist.objects.get(id=recid)
        securityprofile = userlist.securityprofileid
        urlActive = 'unitlist'
        context= {'user_name' : user_name,
                  'securityprofile' : securityprofile,
                  'urlActive': urlActive,}
        return render(request, 'tsweb/teacher/unitlist.html', context)


def tsubmissionreview(request, id):
    try:
        userid = request.session['userid']
        login = Login.objects.get(id=userid)
        clientid = login.clientid
        usertypeid = login.usertypeid
        user_name = login.loginname
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        categoryentity = Categoryentity.objects.filter(Q(entityid = 14,categoryid__deleted = 0,categoryid__disabled = 0, disabled = 0, deleted = 0) & (Q(clientid = clientid) | Q(clientid = 0)))
        submissionreviewer = Submissionreviewer.objects.get(id = id)
        submissionreviewerlist = Submissionreviewer.objects.filter(submissionversionid__submissionid = submissionreviewer.submissionversionid.submissionid)
        selectionlist = Selectionlist.objects.filter(selectiongroupid=4, disabled=0, deleted=0)
        submission = submissionreviewer.submissionversionid.submissionid
        student_name = submissionreviewer.submissionversionid.submissionid.studentid.getFullName()
        assignment = submissionreviewer.submissionversionid.submissionid.assignmentid
        
        context= {'id' : id,
                  'user_name' : user_name,
                  'submissionreviewerlist' : submissionreviewerlist,
                  'categoryentity' : categoryentity,
                  'selectionlist': selectionlist,
                  'student_name': student_name,
                  'assignment': assignment,
                  'due_date': submission.duedate
                  }
        
        return render(request, 'tsweb/teacher/submissionreview.html', context)
        
def stsubmissionreview(request, id):
    try:
        userid = request.session['userid']
        login = Login.objects.get(id=userid)
        studentid = login.recid
        user_name = login.loginname
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        submission = Submission.objects.get(id=id, disabled=0, deleted=0)
        submissionversion = Submissionversion.objects.get(submissionid=submission.id,version=submission.getLatestVersion, disabled=0, deleted=0)
        submissionversionlist = Submissionversion.objects.filter(submissionid=id, disabled=0, deleted=0)
        
        studentlist = Studentlist.objects.filter(id=studentid)
        submissionlist = Submission.objects.filter(studentid=studentid, disabled=0, deleted=0)
        context = {
            'submissionversion' : submissionversion,
            'user_name' : user_name,
            'assignment' : submission.assignmentid,
            'submissionversionlist' : submissionversionlist,
            'studentlist' : studentlist, 
            'submissionlist' : submissionlist,
            'submissioncount':submissionlist.count(),
            }
        return render(request, 'tsweb/student/revision_editor.html', context)
    

def gettags(request, entityid):
    try:
        userid = request.session['userid']
        term = request.GET.get('term', False)
    except KeyError:
        data_json = {
                    'status': 'user not logged in',
                    }
        data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    else:
        
        tagentity = ''
        
        if len(term) == 1:
            data_json = []
            tagentity = TagEntity.objects.filter(entityid=entityid,tagid__name__istartswith=term, tagid__parentid=0)
            for row in tagentity:
                data_json.append({ "id": str(row.tagid.id), "label": row.tagid.name, "value": row.tagid.name })
        else:
            data_json = []
            tagentity = TagEntity.objects.filter(entityid=entityid,tagid__name__istartswith=term)
            for row in tagentity:
                if { "id": str(row.tagid.id), "label": row.tagid.name, "value": row.tagid.name } not in data_json:
                    data_json.append({ "id": str(row.tagid.id), "label": row.tagid.name, "value": row.tagid.name })
                if row.tagid.parentid != 0:
                    tagentitysibling = TagEntity.objects.filter(entityid=entityid,tagid__parentid=row.tagid.parentid)
                    for rowsibling in tagentitysibling:
                        if { "id": str(rowsibling.tagid.id), "label": rowsibling.tagid.name, "value": rowsibling.tagid.name } not in data_json:
                            data_json.append({ "id": str(rowsibling.tagid.id), "label": rowsibling.tagid.name, "value": rowsibling.tagid.name })
                tagentitychild = TagEntity.objects.filter(entityid=entityid,tagid__parentid=row.tagid.id)
                for rowchild in tagentitychild:
                    if { "id": str(rowchild.tagid.id), "label": rowchild.tagid.name, "value": rowchild.tagid.name } not in data_json:
                        data_json.append({ "id": str(rowchild.tagid.id), "label": rowchild.tagid.name, "value": rowchild.tagid.name })
                
        data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    
def tprocessajax(request):
    if request.method == 'GET':
        txtclass = request.GET.get('class',False)
        txtmethod = request.GET.get('method',False)
    elif request.method == 'POST':
        txtclass = request.POST.get('class',False)
        txtmethod = request.POST.get('method',False)
        
    className = eval(txtclass)()
        
    if txtmethod == False:
        methodToCall = getattr(className, 'get')
        #method = className.getJson(request)
    else:
        methodToCall = getattr(className, txtmethod)
    method = methodToCall(request)
    return method 


