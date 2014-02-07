from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson,timezone
from django.core import serializers
from django.db.models.query import RawQuerySet
from django.db import connection
from tsweb.models import *
from django.db.models import Q
from itertools import chain

from datetime import datetime, timedelta
import time


class ASSSIGNMENTLIST():
    def get(self,request):
        cursor = connection.cursor()
        try:
            DATE_FORMAT = "%d-%m-%Y %H:%M" 
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            cursor.execute("SELECT id,name,description,rubricid,maxwords,minwords, disabled,audience,contextsituation,duedatetime,numrevisions,goaloftask FROM assignment  WHERE id = %s", [id])
                   
            results = cursor.fetchall() 
            for r in results:
                if r[9] is None:
                    duedate = ''
                else:
                    timeshow = r[9] + timedelta(hours=7)
                    duedate = timeshow.strftime(DATE_FORMAT)
                parameters = "%d - %d" % (r[5] , r[4])
                data_json = {
                        'id': r[0],
                        'name': r[1],
                        'description': r[2],
                        'rubricid': r[3],
                        'maxwords': r[4],
                        'minwords': r[5],
                        'disabled': r[6],
                        'audience': r[7],
                        'context': r[8],
                        'duedate': duedate,
                        'revisions': r[10],
                        'goal': r[11],
                        'parameters': parameters,
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
    
    def getClassSelect(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            id = request.GET.get('id', False)
            classlist = list(Classschedule.objects.filter(Q(disabled=0,deleted=0,clientid=clientid)).values('id','code'))
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            if id != '':
                classlistselect = list(Classassignment.objects.filter(assignmentid=id,disabled=0,deleted=0).values('classid'))
                classselectarray = []
                for classdict in classlistselect:
                    classselectarray.append(classdict['classid'])
                
                classstorelist = []
                for classstore in classlist:
                    if classstore['id'] in classselectarray:
                        classstorelist.append({'id': classstore['id'], 'code': classstore['code'], 'selected': 'selected'})
                    else:
                        classstorelist.append({'id': classstore['id'], 'code': classstore['code'], 'selected': ''})
                data = simplejson.dumps(classstorelist)
            else:
                data = simplejson.dumps(classlist)
            return HttpResponse(data, mimetype='application/json')

        
    def getStudentSelect(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            assignmentid = request.GET.get('assignmentid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            studentlist = list(Studentlist.objects.filter(clientid=clientid).values('id','firstname','lastname'))
            if assignmentid != '':
                studentsubmissionlist = list(Submission.objects.filter(assignmentid=assignmentid,disabled=0,deleted=0).values('studentid'))
                
                studentselectarray = []
                for studentdict in studentsubmissionlist:
                    studentselectarray.append(studentdict['studentid'])
                    
                studentstorelist = []
                for studentstore in studentlist:
                    if studentstore['id'] in studentselectarray:
                        studentstorelist.append({'id': studentstore['id'], 'firstname': studentstore['firstname'], 'lastname': studentstore['lastname'], 'selected': 'selected'})
                    else:
                        studentstorelist.append({'id': studentstore['id'], 'firstname': studentstore['firstname'], 'lastname': studentstore['lastname'], 'selected': ''})
                data = simplejson.dumps(studentstorelist)
            else:
                data = simplejson.dumps(studentlist)
            return HttpResponse(data, mimetype='application/json')
    
    def save(self,request):
        try:
            DATE_FORMAT = "%d-%m-%Y %H:%M"
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            userlist = Userlist.objects.get(id=login.recid)
    
            id = request.POST.get('id', False)
            name = request.POST.get('name', False)
            description = request.POST.get('description', False)
            classids = request.POST.get('classid', False)
            maxwords = request.POST.get('maxwords', False)
            minwords = request.POST.get('minwords', False)
            audience = request.POST.get('audience', False)
            context = request.POST.get('context', False)
            duedate = request.POST.get('duedate', False)
            duedate_submission = duedate[:10]
            goal = request.POST.get('goal-of-task', False)
            revisions = request.POST.get('revisions', False)
            rubricid = request.POST.get('rubricid', False)
            disabled = request.POST.get('disabled', False)
            
            studentids = request.POST.get('studentid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            try:
                Assignment.objects.get(~Q(id=id),Q(name=name))
            except Assignment.DoesNotExist:
                rubriclist = Rubric.objects.get(id=rubricid)
                assignment = Assignment.objects.get(id=id)
                assignment.name = name
                assignment.description = description
                assignment.goaloftask = goal
                assignment.maxwords = maxwords
                assignment.minwords = minwords
                assignment.rubricid = rubriclist
                assignment.audience = audience
                assignment.contextsituation = context
                if duedate != '':
                    assignment.duedate = datetime.strptime(duedate,DATE_FORMAT)
                if revisions == False or revisions == '':
                    assignment.revisions = 0
                else:
                    assignment.revisions = revisions
                assignment.modifieddt = datetime.now()
                assignment.modifiedby = userid
                assignment.disabled = disabled
                assignment.save()
                
                DATE_FORMAT_SUBMISSION = "%d-%m-%Y"
                                
                try:
                    submissionlist = Submission.objects.filter(assignmentid=id)
                except Submission.DoesNotExist:
                    data_json = { 'status': 'blank', }
                except Submission.MultipleObjectsReturned:
                    for submissionstore in submissionlist:
                        submissionstore.disabled = 1
                        submissionstore.save()
                else:
                    for submissionstore in submissionlist:
                        submissionstore.disabled = 1
                        submissionstore.save() 
                        
                if studentids != False:
                    studentcheck = studentids.find(',')
                    if studentcheck > -1:
                        studentids = studentids.split(',')
                        assignmentlist = Assignment.objects.get(id=id)
                        for student in studentids:
                            studentlist = Studentlist.objects.get(id=student)
                            try: 
                                submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                            except Submission.DoesNotExist:
                                submission = Submission()
                                submission.studentid = studentlist
                                submission.teacherid=userlist
                                submission.assignmentid=assignmentlist
                                submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                                submission.progress=0
                                submission.createddt=datetime.now()
                                submission.createdby=userid
                                submission.modifieddt=datetime.now()
                                submission.modifiedby=userid
                                submission.deleted=0
                                submission.disabled=0
                                submission.save()
                            else:
                                submission.disabled=0
                                submission.save()
                    else:
                        studentlist = Studentlist.objects.get(id=studentids)
                        assignmentlist = Assignment.objects.get(id=id)
                        try: 
                            submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                        except Submission.DoesNotExist:
                            submission = Submission()
                            submission.studentid = studentlist
                            submission.teacherid=userlist
                            submission.assignmentid=assignmentlist
                            submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                            submission.progress=0
                            submission.createddt=datetime.now()
                            submission.createdby=userid
                            submission.modifieddt=datetime.now()
                            submission.modifiedby=userid
                            submission.deleted=0
                            submission.disabled=0
                            submission.save()
                            
                            newid = Submission.objects.latest("id")
                            
                            newversion = Submissionversion()
                            newversion.submissionid = newid
                            newversion.version = 1
                            newversion.studentstatus = 0
                            newversion.teacherstatus = 0
                            newversion.stage = 0
                            newversion.createddt = datetime.now()
                            newversion.createdby = userid
                            newversion.modifieddt = datetime.now()
                            newversion.modifiedby = userid
                            newversion.disabled = 0
                            newversion.deleted = 0
                            newversion.save()
                            
                try:
                    classassignmentlist = Classassignment.objects.filter(assignmentid=id)
                except Classassignment.DoesNotExist:
                    data_json = { 'status': 'blank', }
                except Classassignment.MultipleObjectsReturned:
                    for classassignmentstore in classassignmentlist:
                        assignmentlist = Assignment.objects.get(id=id)
                        studentclass = Studentclass.objects.filter(classscheduleid=classassignmentstore.classid).values_list('studentid')
                        
                        for row in studentclass:
                            studentlist = Studentlist.objects.get(id=row[0])
                            try: 
                                submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                            except Submission.DoesNotExist:
                                data_json = { 'status': 'blank', }    
                            else:
                                submission.disabled=1
                                submission.save()
                                
                        classassignmentstore.disabled = 1
                        classassignmentstore.save()
                else:
                    for classassignmentstore in classassignmentlist:
                        assignmentlist = Assignment.objects.get(id=id)
                        studentclass = Studentclass.objects.filter(classscheduleid=classassignmentstore.classid).values_list('studentid')
                        
                        for row in studentclass:
                            studentlist = Studentlist.objects.get(id=row[0])
                            try: 
                                submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                            except Submission.DoesNotExist:
                                data_json = { 'status': 'blank', }    
                            else:
                                submission.disabled=1
                                submission.save()
                        classassignmentstore.disabled = 1
                        classassignmentstore.save()
                
                if classids != False:
                    
                    classcheck = classids.find(',')
                    if classcheck > -1:
                        classids = classids.split(',')
                        for classid in classids:
                            classlist = Classschedule.objects.get(id=classid)
                            assignmentlist = Assignment.objects.get(id=id)
                            try:
                                ca = Classassignment.objects.get(classid=classlist, assignmentid=assignmentlist)
                            except Classassignment.DoesNotExist:
                                ca = Classassignment()
                                ca.classid = classlist
                                ca.assignmentid = assignmentlist
                                ca.createddt = datetime.now()
                                ca.createdby = userid
                                ca.modifieddt = datetime.now()
                                ca.modifiedby = userid
                                ca.disabled = 0
                                ca.deleted = 0
                                ca.save()
                            else:
                                ca.disabled = 0
                                ca.save()
                            
                            studentclass = Studentclass.objects.filter(classscheduleid=classid).values_list('studentid')
                             
                            for row in studentclass:
                                studentlist = Studentlist.objects.get(id=row[0])
                                try: 
                                    submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                                except Submission.DoesNotExist:
                                    submission = Submission()
                                    submission.studentid = studentlist
                                    submission.teacherid=userlist
                                    submission.assignmentid=assignmentlist
                                    submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                                    submission.progress=0
                                    submission.createddt=datetime.now()
                                    submission.createdby=userid
                                    submission.modifieddt=datetime.now()
                                    submission.modifiedby=userid
                                    submission.deleted=0
                                    submission.disabled=0
                                    submission.save()
                                    
                                    newid = Submission.objects.latest("id")
                                    
                                    newversion = Submissionversion()
                                    newversion.submissionid = newid
                                    newversion.version = 1
                                    newversion.studentstatus = 0
                                    newversion.teacherstatus = 0
                                    newversion.stage = 0
                                    newversion.createddt = datetime.now()
                                    newversion.createdby = userid
                                    newversion.modifieddt = datetime.now()
                                    newversion.modifiedby = userid
                                    newversion.disabled = 0
                                    newversion.deleted = 0
                                    newversion.save()
                                else:
                                    submission.disabled=0
                                    submission.modifieddt=datetime.now()
                                    submission.modifiedby=userid
                                    submission.save()
                        
                    else:
                        classlist = Classschedule.objects.get(id=classids)
                        assignmentlist = Assignment.objects.get(id=id)
                        
                        try:
                            ca = Classassignment.objects.get(classid=classlist, assignmentid=assignmentlist)
                        except Classassignment.DoesNotExist:
                            ca = Classassignment()
                            ca.classid = classlist
                            ca.assignmentid = assignmentlist
                            ca.createddt = datetime.now()
                            ca.createdby = userid
                            ca.modifieddt = datetime.now()
                            ca.modifiedby = userid
                            ca.disabled = 0
                            ca.deleted = 0
                            ca.save()
                        else:
                            ca.disabled = 0
                            ca.save()
                        
                        studentclass = Studentclass.objects.filter(classscheduleid=classids).values_list('studentid')
                             
                        for row in studentclass:
                            studentlist = Studentlist.objects.get(id=row[0])
                            try: 
                                submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                            except Submission.DoesNotExist:
                                submission = Submission()
                                submission.studentid = studentlist
                                submission.teacherid=userlist
                                submission.assignmentid=assignmentlist
                                submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                                submission.progress=0
                                submission.createddt=datetime.now()
                                submission.createdby=userid
                                submission.modifieddt=datetime.now()
                                submission.modifiedby=userid
                                submission.deleted=0
                                submission.disabled=0
                                submission.save()
                                
                                newid = Submission.objects.latest("id")
                                
                                newversion = Submissionversion()
                                newversion.submissionid = newid
                                newversion.version = 1
                                newversion.studentstatus = 0
                                newversion.teacherstatus = 0
                                newversion.stage = 0
                                newversion.createddt = datetime.now()
                                newversion.createdby = userid
                                newversion.modifieddt = datetime.now()
                                newversion.modifiedby = userid
                                newversion.disabled = 0
                                newversion.deleted = 0
                                newversion.save()
                            else:
                                submission.disabled=0
                                submission.modifieddt=datetime.now()
                                submission.modifiedby=userid
                                submission.save()
                
                data_json = { 'status': 'success', }
            else:
                data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            
            return HttpResponse(data, mimetype='application/json')
        
    def add(self,request):
        try:
            DATE_FORMAT = "%d-%m-%Y %H:%M"
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            userlist = Userlist.objects.get(id=login.recid)
            
            #id = request.POST.get('id', False)
            name = request.POST.get('name', False)
            description = request.POST.get('description', False)
            classids = request.POST.get('classid', False)
            maxwords = request.POST.get('maxwords', False)
            minwords = request.POST.get('minwords', False)
            audience = request.POST.get('audience', False)
            context = request.POST.get('context', False)
            duedate = request.POST.get('duedate', False)
            duedate_submission = duedate[:10]
            goal = request.POST.get('goal-of-task', False)
            revisions = request.POST.get('revisions', False)
            rubricid = request.POST.get('rubricid', False)
            disabled = request.POST.get('disabled', False)
            
            studentids = request.POST.get('studentid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            try:
                Assignment.objects.get(Q(name=name))
            except Assignment.DoesNotExist:
                rubriclist = Rubric.objects.get(id=rubricid)
                assignment = Assignment()
                assignment.name = name
                assignment.description = description
                assignment.goaloftask = goal
                if maxwords == False or maxwords == '':
                    assignment.maxwords = 0
                else:
                    assignment.maxwords = maxwords
                if minwords == False or minwords == '':
                    assignment.minwords = 0
                else:
                    assignment.minwords = minwords
                assignment.rubricid = rubriclist
                assignment.audience = audience
                assignment.contextsituation = context
                assignment.duedate = datetime.strptime(duedate,DATE_FORMAT)
                if revisions == False or revisions == '':
                    assignment.revisions = 0
                else:
                    assignment.revisions = revisions  
                assignment.modifieddt = datetime.now()
                assignment.modifiedby = userid
                assignment.createddt = datetime.now()
                assignment.createdby = userid
                assignment.disabled = disabled
                assignment.deleted = 0
                assignment.clientid = clientid
                assignment.save()
                
                DATE_FORMAT_SUBMISSION = "%d-%m-%Y"
                
                id = Assignment.objects.latest('id').id
                
                if classids != False:
                    classcheck = classids.find(',')
                    if classcheck > -1:
                        classids = classids.split(',')
                        for classid in classids:
                            classlist = Classschedule.objects.get(id=classid)
                            assignmentlist = Assignment.objects.get(id=id)
                            Classassignment.objects.get_or_create(classid=classlist, assignmentid=assignmentlist,
                                                                  defaults={ 'createddt' : datetime.now(),
                                                                                           'createdby' : userid,
                                                                                           'modifieddt' : datetime.now(),
                                                                                           'modifiedby' : userid,
                                                                                           'disabled' : 0,
                                                                                           'deleted' : 0,})
                            studentclass = Studentclass.objects.filter(classscheduleid=classid).values_list('studentid')
                             
                            for row in studentclass:
                                studentlist = Studentlist.objects.get(id=row[0])
                                try: 
                                    submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                                except Submission.DoesNotExist:
                                    submission = Submission()
                                    submission.studentid = studentlist
                                    submission.teacherid=userlist
                                    submission.assignmentid=assignmentlist
                                    submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                                    submission.progress=0
                                    submission.createddt=datetime.now()
                                    submission.createdby=userid
                                    submission.modifieddt=datetime.now()
                                    submission.modifiedby=userid
                                    submission.deleted=0
                                    submission.disabled=0
                                    submission.save()
                                    
                                    newid = Submission.objects.latest("id")
                            
                                    newversion = Submissionversion()
                                    newversion.submissionid = newid
                                    newversion.version = 1
                                    newversion.studentstatus = 0
                                    newversion.teacherstatus = 0
                                    newversion.stage = 0
                                    newversion.createddt = datetime.now()
                                    newversion.createdby = userid
                                    newversion.modifieddt = datetime.now()
                                    newversion.modifiedby = userid
                                    newversion.disabled = 0
                                    newversion.deleted = 0
                                    newversion.save()
                        
                    else:
                        classlist = Classschedule.objects.get(id=classids)
                        assignmentlist = Assignment.objects.get(id=id)
                        Classassignment.objects.get_or_create(classid=classlist, assignmentid=assignmentlist,
                                                              defaults={ 'createddt' : datetime.now(),
                                                                                           'createdby' : userid,
                                                                                           'modifieddt' : datetime.now(),
                                                                                           'modifiedby' : userid,
                                                                                           'disabled' : 0,
                                                                                           'deleted' : 0,})
                        studentclass = Studentclass.objects.filter(classscheduleid=classids).values_list('studentid')
                             
                        for row in studentclass:
                            studentlist = Studentlist.objects.get(id=row[0])
                            try: 
                                submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                            except Submission.DoesNotExist:
                                submission = Submission()
                                submission.studentid = studentlist
                                submission.teacherid=userlist
                                submission.assignmentid=assignmentlist
                                submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                                submission.progress=0
                                submission.createddt=datetime.now()
                                submission.createdby=userid
                                submission.modifieddt=datetime.now()
                                submission.modifiedby=userid
                                submission.deleted=0
                                submission.disabled=0
                                submission.save()
                                
                                newid = Submission.objects.latest("id")
                            
                                newversion = Submissionversion()
                                newversion.submissionid = newid
                                newversion.version = 1
                                newversion.studentstatus = 0
                                newversion.teacherstatus = 0
                                newversion.stage = 0
                                newversion.createddt = datetime.now()
                                newversion.createdby = userid
                                newversion.modifieddt = datetime.now()
                                newversion.modifiedby = userid
                                newversion.disabled = 0
                                newversion.deleted = 0
                                newversion.save()
                
                if studentids != False:
                    studentcheck = studentids.find(',')
                    if studentcheck > -1:
                        studentids = studentids.split(',')
                        assignmentlist = Assignment.objects.get(id=id)
                        for student in studentids:
                            studentlist = Studentlist.objects.get(id=student)
                            try: 
                                submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                            except Submission.DoesNotExist:
                                submission = Submission()
                                submission.studentid = studentlist
                                submission.teacherid=userlist
                                submission.assignmentid=assignmentlist
                                submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                                submission.progress=0
                                submission.createddt=datetime.now()
                                submission.createdby=userid
                                submission.modifieddt=datetime.now()
                                submission.modifiedby=userid
                                submission.deleted=0
                                submission.disabled=0
                                submission.save()
                    else:
                        studentlist = Studentlist.objects.get(id=studentids)
                        assignmentlist = Assignment.objects.get(id=id)
                        try: 
                            submission = Submission.objects.get(Q(studentid=studentlist),Q(assignmentid=assignmentlist),~Q(progress=100))
                        except Submission.DoesNotExist:
                            submission = Submission()
                            submission.studentid = studentlist
                            submission.teacherid=userlist
                            submission.assignmentid=assignmentlist
                            submission.duedate=datetime.strptime(duedate_submission,DATE_FORMAT_SUBMISSION)
                            submission.progress=0
                            submission.createddt=datetime.now()
                            submission.createdby=userid
                            submission.modifieddt=datetime.now()
                            submission.modifiedby=userid
                            submission.deleted=0
                            submission.disabled=0
                            submission.save()
                            
                            newid = Submission.objects.latest("id")
                            
                            newversion = Submissionversion()
                            newversion.submissionid = newid
                            newversion.version = 1
                            newversion.studentstatus = 0
                            newversion.teacherstatus = 0
                            newversion.stage = 0
                            newversion.createddt = datetime.now()
                            newversion.createdby = userid
                            newversion.modifieddt = datetime.now()
                            newversion.modifiedby = userid
                            newversion.disabled = 0
                            newversion.deleted = 0
                            newversion.save()
                            
                data_json = { 'status': 'success', }
            else:
                data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
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
            assignmentname=request.GET.get('search',False)
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