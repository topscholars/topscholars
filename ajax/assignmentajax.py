from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson
from django.core import serializers
from django.db.models.query import RawQuerySet
from django.db import connection
from tsweb.models import *
from django.db.models import Q
from itertools import chain

from datetime import datetime
import time

class ASSSIGNMENTLIST():
    def get(self,request):
        cursor = connection.cursor()
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            cursor.execute("SELECT id,name,description,rubricid,maxwords FROM assignment  WHERE id = %s", [id])
                   
            results = cursor.fetchall() 
            for r in results:
                data_json = {
                        'id': r[0],
                        'name': r[1],
                        'description': r[2],
                        'rubricid': r[3],
                        'maxwords': r[4],
                        }
            data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    
    def getRubricIdAssignment(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:  
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            rubriclist = list(Rubric.objects.filter(entityid=3,disabled=0,deleted=0,clientid=clientid).values('id','name'))
            data = simplejson.dumps(rubriclist)
        return HttpResponse(data, mimetype='application/json')
    
    def save(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
            name = request.GET.get('name', False)
            description = request.GET.get('description', False)
            rubricid = request.GET.get('rubricid', False)
            maxwords = request.GET.get('maxwords', False)
            disabled = request.GET.get('disabled', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            rubriclist = Rubric.objects.get(id=rubricid)
            assignment = Assignment.objects.get(id=id)
            assignment.name = name
            assignment.description = description
            assignment.maxwords = maxwords
            assignment.rubricid = rubriclist
            assignment.modifieddt = datetime.now()
            assignment.modifiedby = userid
            assignment.disabled = disabled
            assignment.save()
        return HttpResponse('success', mimetype='application/json')
    
    def add(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
            name = request.GET.get('name', False)
            description = request.GET.get('description', False)
            rubricid = request.GET.get('rubricid', False)
            maxwords = request.GET.get('maxwords', False)
            disabled = request.GET.get('disabled', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            
            rubriclist = Rubric.objects.get(id=rubricid)
            assignment = Assignment()
            assignment.name = name
            assignment.description = description
            assignment.maxwords = maxwords
            assignment.rubricid = rubriclist
            assignment.modifieddt = datetime.now()
            assignment.modifiedby = userid
            assignment.createddt = datetime.now()
            assignment.createdby = userid
            assignment.modifieddt = datetime.now()
            assignment.modifiedby = userid
            assignment.disabled = disabled
            assignment.deleted = 0
            assignment.clientid = clientid
            assignment.save()
        return HttpResponse('success', mimetype='application/json')
    
    def tAssignmentClass(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            id = request.GET.get('id', False)
            classassignid = Classassignment.objects.get(id=id)
        except Classassignment.DoesNotExist:
            return render(request, 'tsweb/teacher/assignmentlist_assignmentclass.html')
        else:
            classid = classassignid.classid.id
            classlist = Classschedule.objects.filter(id=classid,disabled=0,deleted=0,clientid=clientid)
            #return HttpResponse(classassignid, mimetype='application/json')
            context = {'classlist': classlist}
            return render(request, 'tsweb/teacher/assignmentlist_assignmentclass.html', context)
        
    def tAssignmentStudent(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            id = request.GET.get('id', False)
            if id == False:
                return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html')
            else:
                classassignid = Classassignment.objects.get(id=id)
                classid = classassignid.classid.id
                classlist = Classschedule.objects.filter(classid=classid,disabled=0,deleted=0,clientid=clientid)
                
                #return HttpResponse(classlist.id, mimetype='application/json')
                context = {'classlist': classlist}
                return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html', context)
        
    def tStudentAssignlist(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classlist = Classschedule.objects.filter(Q(classid=classid), Q(disabled=0,deleted=0,clientid=clientid))
            studentlist = Studentlist.objects.filter(id__in=studentid)
            context = {'studentlist': studentlist}
            return render(request, 'tsweb/teacher/classlist_studentlistajax.html', context)
        
    def tClassAssignlist(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
            classassignid = Classassignment.objects.get(id=id)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classid = classassignid.classid.id
            classlist = Classschedule.objects.filter(~Q(id=classid), Q(disabled=0,deleted=0,clientid=clientid))
            #return HttpResponse(classlist, mimetype='application/json')
            context = {'classlist': classlist}
            return render(request, 'tsweb/teacher/assignmentlist_classschedulelist.html', context)
    
    def addClassToAssignment(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:   
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classlist = Classlist.objects.get(id=id)
            classassignment = Classassignment()
            classassignment.classid = classlist
            return HttpResponse('success', mimetype='application/json')
        
class TASSIGNMENTLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            assignmentname=request.GET.get('assignmentname',False)
            classid=request.GET.get('classid',False)
            assignmentlist = ''
            if (assignmentname != False and assignmentname != '') and (classid != False and classid != ''):
                assignmentlist = Assignment.objects.filter(clientid=clientid,Classassignmenttoassignment__classid=classid,name__contains=assignmentname,deleted=0)
            elif assignmentname != False and assignmentname != '':
                assignmentlist = Assignment.objects.filter(clientid=clientid,name__contains=assignmentname,deleted=0)
            elif classid != False and classid != '':
                assignmentlist = Assignment.objects.filter(clientid=clientid,Classassignmenttoassignment__classid=classid,deleted=0)
            else:
                assignmentlist = Assignment.objects.filter(clientid=clientid,deleted=0)
            context = {'assignmentlist': assignmentlist}
            return render(request, 'tsweb/teacher/assignmentlistajax.html', context)