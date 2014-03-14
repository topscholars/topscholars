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

class CLASSLIST():
    def get(self,request):
        cursor = connection.cursor()
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            #classlist = Classschedule.objects.filter(id=id)
            cursor.execute("SELECT id,code,subcode,abilitylevel,teacherid,startdate,enddate,starttime,endtime,disabled,dayofweek,description FROM classschedule  WHERE id = %s", [id])
            
            results = cursor.fetchall()
            for r in results:
                data_json = {
                        'id': r[0],
                        'code': r[1],
                        'subcode': r[2],
                        'abilitylevel': r[3],
                        'teacherid': r[4],
                        'startdate': r[5].strftime(DATE_FORMAT),
                        'enddate': r[6].strftime(DATE_FORMAT),
                        'starttime': r[7],
                        'endtime': r[8],
                        'disabled': r[9],
                        'dayofweek': r[10],
                        'description': r[11],
                        }
            data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    
    def selectAbility(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            selectiongrouplist = Selectiongroup.objects.get(groupname='LevelOfAbility')
            selectionlist = list(Selectionlist.objects.filter(selectiongroupid=selectiongrouplist.id, disabled=0,deleted=0).values('selectionname', 'id'))
            data = simplejson.dumps(selectionlist)

        return HttpResponse(data, mimetype='application/json')
    
    def getTeacher(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            if login.usertypeid==1:
                recid = Login.objects.filter(usertypeid=1).values_list('recid')
                user = list(Userlist.objects.filter(id__in=recid,clientid=clientid).values('id','firstname','middlename','lastname'))
                data = simplejson.dumps(user)
        return HttpResponse(data, mimetype='application/json')
    
    def getStudentSelect(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classscheduleid = request.GET.get('classscheduleid', False)
            studentlist = list(Studentlist.objects.filter(Q(clientid=clientid)).values('id','firstname', 'middlename', 'lastname'))
            if classscheduleid == '':
                data = simplejson.dumps(studentlist)
                return HttpResponse(data, mimetype='application/json')
            else:
                studentlistselect = list(Studentclass.objects.filter(classscheduleid=classscheduleid,disabled=0,deleted=0).values('studentid'))
        except Studentclass.DoesNotExist:
            data = simplejson.dumps(studentlist)
            return HttpResponse(data, mimetype='application/json')
        else:
            studentselectarray = []
            for studentdict in studentlistselect:
                studentselectarray.append(studentdict['studentid'])
            
            studentstorelist = []
            for studentstore in studentlist:
                if studentstore['id'] in studentselectarray:
                    studentstorelist.append({'id': studentstore['id'], 'firstname': studentstore['firstname'], 'middlename': studentstore['middlename'], 'lastname': studentstore['lastname'], 'selected': 'selected'})
                else:
                    studentstorelist.append({'id': studentstore['id'], 'firstname': studentstore['firstname'], 'middlename': studentstore['middlename'], 'lastname': studentstore['lastname'], 'selected': ''})
            data = simplejson.dumps(studentstorelist)
            return HttpResponse(data, mimetype='application/json')
        
    def getUnitSelect(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classscheduleid = request.GET.get('classscheduleid', False)
            unitlist = list(Unit.objects.filter(Q(clientid=clientid),Q(disabled=0),Q(deleted=0)).values('id','name'))
            if classscheduleid == '':
                data = simplejson.dumps(unitlist)
                return HttpResponse(data, mimetype='application/json')
            else:
                unitlistselect = list(Unitclass.objects.filter(classscheduleid=classscheduleid,disabled=0,deleted=0).values('unitid'))
        except Unitclass.DoesNotExist:
            data = simplejson.dumps(unitlist)
            return HttpResponse(data, mimetype='application/json')
        else:
            unitselectarray = []
            for unitdict in unitlistselect:
                unitselectarray.append(unitdict['unitid'])
            
            unitstorelist = []
            for unitstore in unitlist:
                if unitstore['id'] in unitselectarray:
                    unitstorelist.append({'id': unitstore['id'], 'name': unitstore['name'], 'selected': 'selected'})
                else:
                    unitstorelist.append({'id': unitstore['id'], 'name': unitstore['name'], 'selected': ''})
            data = simplejson.dumps(unitstorelist)
            return HttpResponse(data, mimetype='application/json')

    def saveUnit(self, request, id, unit, studentid):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            userlist = Userlist.objects.get(id=login.recid)
            unitclasslist = Unitclass.objects.filter(classscheduleid=id)
        except Unitclass.DoesNotExist:
            data_json = { 'status': 'blank', }
        except Unitclass.MultipleObjectsReturned:
            for unitclassstore in unitclasslist:
                unitclassstore.disabled = 1
                unitclassstore.save()
        else:
            for unitclassstore in unitclasslist:
                unitclassstore.disabled = 1
                unitclassstore.save()      
                
        classschedule = Classschedule.objects.get(id=id)
         
        if unit != False:
 
            unitcheck = unit.find(',')
            if unitcheck > -1:
                unitids= unit.split(',')
                for unitid in unitids:
                    unitlist = Unit.objects.get(id=unitid)
 
                    try:
                        u = Unitclass.objects.get(unitid = unitlist,classscheduleid = classschedule)
                    except Unitclass.DoesNotExist:
                        u = Unitclass()
                        u.unitid = unitlist
                        u.classscheduleid = classschedule
                        u.createddt = datetime.now()
                        u.createdby = userid
                        u.modifieddt = datetime.now()
                        u.modifiedby = userid
                        u.disabled = 0
                        u.deleted = 0
                        u.clientid = clientid
                        u.save()
                    else:
                        u.disabled = 0
                        u.save()
                        
                    assignmentlist = UnitAssignment.objects.filter(unitid=unitid).values_list('assignmentid')
                    
                    for assignmentid in assignmentlist:
                        assigmentobj = Assignment.objects.get(id=assignmentid[0])
                        if studentid != False:
                            studentcheck = studentid.find(',')
                            if studentcheck > -1:
                                studentid = studentid.split(',')
                                for studentids in studentid:
                                    try:
                                        studentlist = Studentlist.objects.get(id=studentids)
                                        submissionlist = Submission.objects.get(studentid=studentids, assignmentid=assignmentid[0], disabled=0,deleted=0)
                                    except Submission.DoesNotExist:
                                        submission = Submission()
                                        submission.studentid = studentlist
                                        submission.teacherid=userlist
                                        submission.assignmentid=assigmentobj
                                        submission.duedate= assigmentobj.duedate
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
                                try:
                                    studentlist = Studentlist.objects.get(id=studentid)
                                    submissionlist = Submission.objects.get(studentid=studentid, assignmentid=assignmentid[0], disabled=0,deleted=0)
                                except Submission.DoesNotExist:
                                    submission = Submission()
                                    submission.studentid = studentlist
                                    submission.teacherid=userlist
                                    submission.assignmentid=assigmentobj
                                    submission.duedate= assigmentobj.duedate
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
                unitlist = Unit.objects.get(id=unit)
                try:
                    u = Unitclass.objects.get(unitid = unitlist,classscheduleid = classschedule)
                except Unitclass.DoesNotExist:
                    u = Unitclass()
                    u.unitid = unitlist
                    u.classscheduleid = classschedule
                    u.createddt = datetime.now()
                    u.createdby = userid
                    u.modifieddt = datetime.now()
                    u.modifiedby = userid
                    u.disabled = 0
                    u.deleted = 0
                    u.clientid = clientid
                    u.save()
                else:
                    u.disabled = 0
                    u.save()
                    
                assignmentlist = UnitAssignment.objects.filter(unitid=unit).values_list('assignmentid')
                    
                for assignmentid in assignmentlist:
                    assigmentobj = Assignment.objects.get(id=assignmentid[0])
                    if studentid != False:
                        studentcheck = studentid.find(',')
                        if studentcheck > -1:
                            studentid = studentid.split(',')
                            for studentids in studentid:
                                try:
                                    studentlist = Studentlist.objects.get(id=studentids)
                                    submissionlist = Submission.objects.get(studentid=studentids, assignmentid=assignmentid[0], disabled=0,deleted=0)
                                except Submission.DoesNotExist:
                                    submission = Submission()
                                    submission.studentid = studentlist
                                    submission.teacherid=userlist
                                    submission.assignmentid=assigmentobj
                                    submission.duedate= assigmentobj.duedate
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
                            try:
                                studentlist = Studentlist.objects.get(id=studentid)
                                submissionlist = Submission.objects.get(studentid=studentid, assignmentid=assignmentid[0], disabled=0,deleted=0)
                            except Submission.DoesNotExist:
                                submission = Submission()
                                submission.studentid = studentlist
                                submission.teacherid=userlist
                                submission.assignmentid=assigmentobj
                                submission.duedate= assigmentobj.duedate
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
        return
        
    
    def save(self,request):
        DATE_FORMAT = "%d-%m-%Y"
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            id = request.POST.get('id', False)
            unit = request.POST.get('unit', False)
            abilitylevel = request.POST.get('abilitylevel', False)
            description = request.POST.get('description', False)
            studentid = request.POST.get('studentid', False)
            code = request.POST.get('code', False)
            subcode = request.POST.get('subcode', False)
            dayofweek = request.POST.get('dayofweek', False)
            disabled = request.POST.get('disabled', False)
            enddate = request.POST.get('enddate', False)
            startdate = request.POST.get('startdate', False)
            endtime = request.POST.get('endtime', False)
            starttime = request.POST.get('starttime', False)
            teacherid = request.POST.get('teacherid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                Classschedule.objects.get(~Q(id=id),Q(code=code))
            except Classschedule.DoesNotExist:
                selectiongrouplist = Selectiongroup.objects.get(groupname='LevelOfAbility')
                selectionlist = Selectionlist.objects.get(selectiongroupid=selectiongrouplist.id,id=abilitylevel, disabled=0,deleted=0)
                classschedule = Classschedule.objects.get(id=id)
                classschedule.abilitylevel = selectionlist
                classschedule.code = code
                classschedule.subcode = subcode
                classschedule.description = description
                classschedule.disabled = disabled
                classschedule.endtime = endtime
                classschedule.starttime = starttime
                classschedule.teacherid = teacherid
                classschedule.dayofweek = dayofweek
                classschedule.enddate = datetime.strptime(enddate,DATE_FORMAT)
                classschedule.startdate = datetime.strptime(startdate,DATE_FORMAT)
                classschedule.modifieddt = datetime.now()
                classschedule.modifiedby = userid
                classschedule.save()

                CLASSLIST.saveUnit(self, request, id, unit, studentid)
                
                try:
                    studentclasslist = Studentclass.objects.filter(classscheduleid=id)
                except Studentclass.DoesNotExist:
                    data_json = { 'status': 'blank', }
                except Studentclass.MultipleObjectsReturned:
                    for studentclassstore in studentclasslist:
                        studentclassstore.disabled = 1
                        studentclassstore.save()
                else:
                    for studentclassstore in studentclasslist:
                        studentclassstore.disabled = 1
                        studentclassstore.save()

                if studentid != False:
                    studentcheck = studentid.find(',')
                    if studentcheck > -1:
                        studentid = studentid.split(',')
                        for studentids in studentid:
                            studentlist = Studentlist.objects.get(id=studentids)
                            try:
                                s = Studentclass.objects.get(studentid = studentlist,classscheduleid = classschedule)
                            except Studentclass.DoesNotExist:
                                s = Studentclass()
                                s.studentid = studentlist
                                s.classscheduleid = classschedule
                                s.grade = 0
                                s.status = 0
                                s.createddt = datetime.now()
                                s.createdby = userid
                                s.modifieddt = datetime.now()
                                s.modifiedby = userid
                                s.disabled = 0
                                s.deleted = 0
                                s.clientid = clientid
                                s.save()
                            else:
                                s.disabled = 0
                                s.save()
                    else:
                        studentlist = Studentlist.objects.get(id=studentid)
                        try:
                            s = Studentclass.objects.get(studentid = studentlist,classscheduleid = classschedule)
                        except Studentclass.DoesNotExist:
                            s = Studentclass()
                            s.studentid = studentlist
                            s.classscheduleid = classschedule
                            s.grade = 0
                            s.status = 0
                            s.createddt = datetime.now()
                            s.createdby = userid
                            s.modifieddt = datetime.now()
                            s.modifiedby = userid
                            s.disabled = 0
                            s.deleted = 0
                            s.clientid = clientid
                            s.save()
                        else:
                            s.disabled = 0
                            s.save()
                data_json = { 'status': 'success', }
            else:
                data_json = { 'status': 'error', }
                
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def add(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            unit = request.POST.get('unit', False)
            abilitylevel = request.POST.get('abilitylevel', False)
            description = request.POST.get('description', False)
            studentid = request.POST.get('studentid', False)
            code = request.POST.get('code', False)
            subcode = request.POST.get('subcode', False)
            dayofweek = request.POST.get('dayofweek', False)
            disabled = request.POST.get('disabled', False)
            enddate = request.POST.get('enddate', False)
            startdate = request.POST.get('startdate', False)
            endtime = request.POST.get('endtime', False)
            starttime = request.POST.get('starttime', False)
            teacherid = request.POST.get('teacherid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                Classschedule.objects.get(Q(code=code))
            except Classschedule.DoesNotExist:
                selectiongrouplist = Selectiongroup.objects.get(groupname='LevelOfAbility')
                selectionlist = Selectionlist.objects.get(selectiongroupid=selectiongrouplist.id,id=abilitylevel, disabled=0,deleted=0)
                classschedule = Classschedule()
                classschedule.abilitylevel = selectionlist
                classschedule.code = code
                classschedule.subcode = subcode
                classschedule.description = description
                classschedule.endtime = endtime
                classschedule.starttime = starttime
                classschedule.teacherid = teacherid
                classschedule.dayofweek = dayofweek
                classschedule.enddate = datetime.strptime(enddate,DATE_FORMAT)
                classschedule.startdate = datetime.strptime(startdate,DATE_FORMAT)
                classschedule.deleted = 0
                classschedule.disabled = disabled
                classschedule.createddt = datetime.now()
                classschedule.createdby = userid
                classschedule.modifieddt = datetime.now()
                classschedule.modifiedby = userid
                classschedule.clientid = clientid
                classschedule.save()
                
                id = Classschedule.objects.latest('id').id
                classschedulelist = Classschedule.objects.get(id=id)
                
                if unit != False:
                    unitcheck = unit.find(',')
                    if unitcheck > -1:
                        unitids= unit.split(',')
                        for unitid in unitids:
                            unitlist = Unit.objects.get(id=unitid)
        
                            Unitclass.objects.get_or_create(unitid = unitlist, 
                                                               classscheduleid = classschedulelist,
                                                               defaults={
                                                               'createddt' : datetime.now(),
                                                               'createdby' : userid,
                                                               'modifieddt' : datetime.now(),
                                                               'modifiedby' : userid,                                                          
                                                               'deleted' : 0,
                                                               'clientid' : clientid} 
                                                               )
                    else:
                        unitlist = Unit.objects.get(id=unit)
                        Unitclass.objects.get_or_create(unitid = unitlist, 
                                                           classscheduleid = classschedulelist,
                                                           defaults={
                                                           'createddt' : datetime.now(),
                                                           'createdby' : userid,
                                                           'modifieddt' : datetime.now(),
                                                           'modifiedby' : userid,
                                                           'deleted' : 0,
                                                           'clientid' : clientid} 
                                                           )
                
                if studentid != False:
                    studentcheck = studentid.find(',')
                    if studentcheck > -1:
                        studentid = studentid.split(',')
                        for studentids in studentid:
                            studentlist = Studentlist.objects.get(id=studentids)
        
                            Studentclass.objects.get_or_create(studentid = studentlist, 
                                                               classscheduleid = classschedulelist,
                                                               defaults={'grade': 0,
                                                               'status' : 0,
                                                               'createddt' : datetime.now(),
                                                               'createdby' : userid,
                                                               'modifieddt' : datetime.now(),
                                                               'modifiedby' : userid,
                                                               'disabled' : 0,
                                                               'deleted' : 0,
                                                               'clientid' : clientid} 
                                                               )
                    else:
                        studentlist = Studentlist.objects.get(id=studentid)
                        Studentclass.objects.get_or_create(studentid = studentlist, 
                                                           classscheduleid = classschedulelist,
                                                           defaults={'grade': 0,
                                                           'status' : 0,
                                                           'createddt' : datetime.now(),
                                                           'createdby' : userid,
                                                           'modifieddt' : datetime.now(),
                                                           'modifiedby' : userid,
                                                           'disabled' : 0,
                                                           'deleted' : 0,
                                                           'clientid' : clientid} 
                                                           )
                data_json = { 'status': 'success', }
            else:
                data_json = { 'status': 'error', }
                
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def getTStudentList(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classid = request.GET.get('classid', False)
            studentid = Studentclass.objects.filter(classscheduleid=classid,disabled=0,deleted=0,clientid=clientid).values_list('studentid')
            studentlist = Studentlist.objects.filter(id__in=studentid)
            context = {'studentlist': studentlist}
            return render(request, 'tsweb/teacher/classlist_studentlistajax.html', context)
    
    def getTStudentAddList(self,request):
        try:
            cursor = connection.cursor()
            userid = request.session['userid']
            classid = request.GET.get('classid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            classschedule = Classschedule.objects.get(clientid=clientid, id=classid)
            studentlist = Studentclass.objects.filter(clientid=clientid).values_list('studentid')
            studentObj1 = Studentlist.objects.filter(~Q(id__in = studentlist)).values_list('id')
            #cursor.execute("select sl.id,cs.startdate,cs.enddate,cs.starttime,cs.endtime,cs.dayofweek from studentlist as sl join studentclass as sc on (sl.id = sc.studentid) join classschedule as cs on (sc.classscheduleid = cs.id) where sc.clientid=%s and (sc.classscheduleid = %s and sc.status = 1 or !(sc.classscheduleid = %s))",[clientid, classid, classid])
            cursor.execute("select sl.id,cs.startdate,cs.enddate,cs.starttime,cs.endtime,cs.dayofweek from studentlist as sl join studentclass as sc on (sl.id = sc.studentid) join classschedule as cs on (sc.classscheduleid = cs.id) where sc.clientid=%s  and ((sc.classscheduleid = %s and sc.status = 1)  or sc.studentid not in (select sc2.studentid from studentclass sc2 where sc2.classscheduleid = %s ))",[clientid, classid, classid])
            classStartDate = int(time.mktime(classschedule.startdate.timetuple()))
            classEndDate = int(time.mktime(classschedule.enddate.timetuple()))
            classStartTime = int(classschedule.starttime.replace(':',''))
            classEndTime = int(classschedule.endtime.replace(':',''))
            classDayofweek = classschedule.dayofweek.split(',')

            resultid = []
            for obj in studentObj1:
                resultid.append(obj[0])
                
            for row in cursor.fetchall():
                studentId = row[0]
                startdate = int(time.mktime(row[1].timetuple()))
                enddate = int(time.mktime(row[2].timetuple()))
                starttime = int(row[3].replace(':',''))
                endtime = int(row[4].replace(':',''))
                dayofweek = row[5].split(',')
                if (classStartDate > startdate and classStartDate > enddate) or (classEndDate < startdate and classEndDate < enddate):
                    resultid.append(studentId)
                else:
                    haveday = 0
                    for day in dayofweek:
                        if day in classDayofweek:
                            haveday = 1
                            break
                    if haveday == 1:
                        if (classStartTime > starttime and classStartTime > endtime) or (classEndTime < starttime and classEndTime < endtime):
                            resultid.append(studentId)
                    else:
                        resultid.append(studentId)
                        
            studentListResult = Studentlist.objects.filter(id__in = resultid)
            context = {'studentlist': studentListResult}
            return render(request, 'tsweb/teacher/classlist_studentaddajax.html', context)
        
    def addStudentInClass(self,request):
        try:
            userid = request.session['userid']
            classid = request.POST.get('classid', False)
            studentid = request.POST.get('studentid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            
            studentlist = Studentlist.objects.get(id=studentid)
            classschedulelist = Classschedule.objects.get(id=classid)
            
            studentclass = Studentclass()
            studentclass.studentid = studentlist
            studentclass.classscheduleid = classschedulelist
            studentclass.grade = 0
            studentclass.status = 0
            studentclass.createddt = datetime.now()
            studentclass.createdby = userid
            studentclass.modifieddt = datetime.now()
            studentclass.modifiedby = userid
            studentclass.disabled = 0
            studentclass.deleted = 0
            studentclass.clientid = clientid
            studentclass.save()
            data_json = { 'status': 'success', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
            
    def changePassword(self,request):
        try:
            userid = request.session['userid']
            password = request.POST.get('password', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            login.password = password
            login.modifieddt = datetime.now()
            login.modifiedby = userid
            login.save()
            data_json = { 'status': 'success', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
class TCLASSLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            description=request.GET.get('description',False)
            classlist = ''
            if description == False or description == '':
                classlist = Classschedule.objects.filter(clientid=clientid,deleted=0)
            else:
                classlist = Classschedule.objects.filter(clientid=clientid,code__contains=description,deleted=0)
                #classlist = Classschedule.objects.filter(clientid=clientid,classid__description__contains=description,deleted=0)
            context = {'classlist': classlist}
            return render(request, 'tsweb/teacher/classlistajax.html', context)
            