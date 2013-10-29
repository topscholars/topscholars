# Create your views here.
#Import Django class
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from tsweb.models import *
#from tsweb.ajaxs import *
from ajax.classajax import *
from ajax.assignmentajax import *
from ajax.studentajax import *
from ajax.rubricajax import *
from ajax.submissionajax import *

#Login View
def login(request):
    username=request.POST.get('txtUsername',False)
    password=request.POST.get('txtPassword',False)
    if username == False:
        return render(request, 'tsweb/login.html', {'username':'','errmsg':''})
    else:
        try:
            user= Login.objects.get(loginname=username)
        except (KeyError, Login.DoesNotExist):
            return render(request, 'tsweb/login.html', {'username':username, 'errmsg':'Invalid username.',})
        else:
            if user.password == password:
                request.session['userid'] = user.id
                return HttpResponseRedirect(reverse('tsweb:tclasslist'))
            else:
                return render(request, 'tsweb/login.html', {'username':username, 'errmsg':'Invalid password.',})

def logout(request):
    try:
        del request.session['userid']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('tsweb:login'))

#Student Views
def sindex(request):
    return render(request, 'tsweb/student/index.html', '')

#Teacher Views
def tclasslist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        return render(request, 'tsweb/teacher/classlist.html', '')

def tassignmentlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        clientid = login.clientid
        classlist = Classlist.objects.filter(clientid=clientid)
        context= {'classlist' : classlist}
        return render(request, 'tsweb/teacher/assignmentlist.html', context)

def tstudentlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        login = Login.objects.get(id=userid)
        clientid = login.clientid
        classlist = Classlist.objects.filter(clientid=clientid)
        context= {'classlist' : classlist}
        return render(request, 'tsweb/teacher/studentlist.html', context)



def trubriclist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        return render(request, 'tsweb/teacher/rubriclist.html', '')

def tsubmissionlist(request):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        return render(request, 'tsweb/teacher/submissionlist.html', '')

def tsubmissionreview(request, id):
    try:
        userid = request.session['userid']
    except KeyError:
        return HttpResponseRedirect(reverse('tsweb:login'))
    else:
        return render(request, 'tsweb/teacher/submissionreview.html', '')
    
def tprocessajax(request):
    txtclass = request.GET.get('class',False)
    txtmethod = request.GET.get('method',False)

    className = eval(txtclass)()
    if txtmethod == False:
        methodToCall = getattr(className, 'get')
        #method = className.getJson(request)
    else:
        methodToCall = getattr(className, txtmethod)
    method = methodToCall(request)
    return method 

