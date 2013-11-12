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
            id = request.POST.get('id', False)
            name = request.POST.get('name', False)
            description = request.POST.get('description', False)
            rubricid = request.POST.get('rubricid', False)
            maxwords = request.POST.get('maxwords', False)
            disabled = request.POST.get('disabled', False)
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
            data_json = { 'status': 'success', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
    
    def add(self,request):
        try:
            userid = request.session['userid']
            id = request.POST.get('id', False)
            name = request.POST.get('name', False)
            description = request.POST.get('description', False)
            rubricid = request.POST.get('rubricid', False)
            maxwords = request.POST.get('maxwords', False)
            disabled = request.POST.get('disabled', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
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
            data_json = { 'status': 'success', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
    
    def tAssignmentClass(self,request):
#         data_json ={}
        classdict ={}
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            id = request.GET.get('id', False)
            cursor = connection.cursor()
            #cursor.execute('select sb.assignmentid, sb.studentid ,ifnull (sc.classscheduleid, 0), cs.code from submission as sb left join studentclass as sc on sc.studentid = sb.studentid left join classschedule as cs on cs.id = sc.classscheduleid where sb.assignmentid = %s',[id])
            #cursor.execute('select sb.assignmentid, sb.studentid ,ifnull (sc.classscheduleid, 0), cs.code from submission as sb left join studentclass as sc on sc.studentid = sb.studentid and sc.classscheduleid in (select classid from classassignment where assignmentid = %s) left join classschedule as cs on cs.id = sc.classscheduleid where sb.assignmentid = %s',[id,id])
            cursor.execute('select ifnull (sc.classscheduleid, 0) as codeid, cs.code, count(*) from submission as sb left join studentclass as sc on sc.studentid = sb.studentid and sc.classscheduleid in (select classid from classassignment where assignmentid = %s) left join classschedule as cs on cs.id = sc.classscheduleid where sb.assignmentid = %s group by codeid',[id,id])
            
            results = cursor.fetchall() 
            #submission = Submission.objects.filter(assignmentid=id,disabled=0,deleted=0).values_list('studentid')
        except results.DoesNotExist:
            return render(request, 'tsweb/teacher/assignmentlist_assignmentclass.html')
        else:
            for r in results:
                classdict[r[0]] = {}
                classdict[r[0]]['id'] = r[0]
                classdict[r[0]]['code'] = r[1]
                classdict[r[0]]['number'] = r[2]
#             i = 0
#             for r in results:
#                 data_json[i] = {}
#                 data_json[i]['studentid'] = r[1]
#                 data_json[i]['classid'] = r[2]
#                 data_json[i]['code'] = r[3]
#                 if data_json[i].has_key('number'):
#                     data_json[i]['number'] += 1
#                 else:
#                     data_json[i]['number'] = 1
#                 i +=1
#             classdict = {}
#             for index in range(len(data_json)):
#                 classid = data_json[index]['classid']
#                 classdict[classid] = {}
#                 classdict[classid]['id'] = data_json[index]['classid']
#                 classdict[classid]['code'] = data_json[index]['code']
#                 try:
#                     classdict[classid]['number'] +=1
#                 except KeyError:
#                     classdict[classid]['number'] = data_json[index]['number']
                    
            classlist = classdict.values()
            context = {'classlist': classlist}
            return render(request, 'tsweb/teacher/assignmentlist_assignmentclass.html', context)
        
    def tAssignmentStudent(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
            assignmentid = request.GET.get('assignmentid', False)
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            if id == False:
                return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html')
            else: 
                classassignment = Classassignment.objects.get(classid=id, assignmentid=assignmentid)
                classid = classassignment.classid
                studentid = Studentclass.objects.filter(classscheduleid=classid, clientid=clientid,disabled=0,deleted=0).values_list('studentid')
                submissionlist = Submission.objects.filter(studentid__in=studentid,assignmentid=assignmentid,disabled=0,deleted=0)
        except Classassignment.DoesNotExist:
            try:
                classassignment = Classassignment.objects.get(assignmentid=assignmentid)
                classid = classassignment.classid
                studentid = Studentclass.objects.filter(classscheduleid=classid, clientid=clientid,disabled=0,deleted=0).values_list('studentid')
                submissionlist = Submission.objects.filter(~Q(studentid__in=studentid),Q(assignmentid=assignmentid),Q(disabled=0),Q(deleted=0))
            except Classassignment.DoesNotExist:
                submissionlist = Submission.objects.filter(Q(assignmentid=assignmentid),Q(disabled=0),Q(deleted=0))
                context = {'submissionlist': submissionlist}
                return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html', context)
            except Classassignment.MultipleObjectsReturned:
                try:
                    classassignment = Classassignment.objects.filter(assignmentid=assignmentid).values_list('classid')
                    studentid = Studentclass.objects.filter(classscheduleid__in=classassignment, clientid=clientid,disabled=0,deleted=0).values_list('studentid')
                    submissionlist = Submission.objects.filter(~Q(studentid__in=studentid),Q(assignmentid=assignmentid),Q(disabled=0),Q(deleted=0))
                except Submission.DoesNotExist:
                    return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html')
                else:
                    context = {'submissionlist': submissionlist}
                    return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html', context)
            except Submission.DoesNotExist:
                return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html')
            else:
                context = {'submissionlist': submissionlist}
                return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html', context)
        else:
            context = {'submissionlist': submissionlist}
            return render(request, 'tsweb/teacher/assignmentlist_assignmentstudent.html', context)
        
    def tStudentAssignlist(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            studentid = Submission.objects.filter(assignmentid=id).values_list('studentid')
            
            studentlist = Studentlist.objects.filter(~Q(id__in=studentid))
            context = {'studentlist': studentlist}
            return render(request, 'tsweb/teacher/assignmentlist_studentlist.html', context)
        
    def tClassAssignlist(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            id = request.GET.get('id', False)
            classassignid = Classassignment.objects.filter(assignmentid=id).values_list('classid')
        except Classassignment.DoesNotExist:
            classlist = Classschedule.objects.filter(Q(disabled=0,deleted=0,clientid=clientid))
            context = {'classlist': classlist}
            return render(request, 'tsweb/teacher/assignmentlist_classschedulelist.html',context)
        else:
            #classid = classassignid.classid.id
            classlist = Classschedule.objects.filter(~Q(id__in=classassignid), Q(disabled=0,deleted=0,clientid=clientid))
            #return HttpResponse(classlist, mimetype='application/json')
            context = {'classlist': classlist}
            return render(request, 'tsweb/teacher/assignmentlist_classschedulelist.html', context)
    
    def addClassToAssignment(self,request):
        try:
            userid = request.session['userid']
            id = request.POST.get('id', False)
            duedate = request.POST.get('date', False)
            assignmentid = request.POST.get('assignmentid', False)
            DATE_FORMAT = "%d-%m-%Y" 
            userlist = Userlist.objects.get(id=userid)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:   
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classlist = Classschedule.objects.get(id=id)
            assignmentlist = Assignment.objects.get(id=assignmentid)
            Classassignment.objects.get_or_create(classid=classlist, assignmentid=assignmentlist)
            studentclass = Studentclass.objects.filter(classscheduleid=id).values_list('studentid')
            for row in studentclass:
                studentlist = Studentlist.objects.get(id=row[0])
                try: 
                    submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                except Submission.DoesNotExist:
                    submission = Submission()
                    submission.studentid = studentlist
                    submission.teacherid=userlist
                    submission.assignmentid=assignmentlist
                    submission.duedate=datetime.strptime(duedate,DATE_FORMAT)
                    submission.progress=0
                    submission.createddt=datetime.now()
                    submission.createdby=userid
                    submission.modifieddt=datetime.now()
                    submission.modifiedby=userid
                    submission.deleted=0
                    submission.disabled=0
                    submission.save()
            data_json = { 'status': 'success', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def addStudentToAssignment(self,request):
        try:
            userid = request.session['userid']
            id = request.POST.get('id', False)
            duedate = request.POST.get('date', False)
            assignmentid = request.POST.get('assignmentid', False)
            DATE_FORMAT = "%d-%m-%Y" 
            studentlist = Studentlist.objects.get(id=id)
            assignmentlist = Assignment.objects.get(id=assignmentid)
            userlist = Userlist.objects.get(id=userid)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:   
            try:
                submissionlist = Submission.objects.get(studentid=id,assignmentid=assignmentid)
            except Submission.DoesNotExist:
                submission = Submission()
                submission.studentid=studentlist
                submission.teacherid=userlist
                submission.assignmentid=assignmentlist
                submission.duedate=datetime.strptime(duedate,DATE_FORMAT)
                submission.progress=0
                submission.createddt=datetime.now()
                submission.createdby=userid
                submission.modifieddt=datetime.now()
                submission.modifiedby=userid
                submission.deleted=0
                submission.disabled=0
                submission.save()
            data_json = { 'status': 'success', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')



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