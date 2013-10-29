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
            cursor.execute("SELECT id,code,subcode,classid,teacherid,startdate,enddate,starttime,endtime,disabled,dayofweek FROM classschedule  WHERE id = %s", [id])
                   
            results = cursor.fetchall() 
            for r in results:
                data_json = {
                        'id': r[0],
                        'code': r[1],
                        'subcode': r[2],
                        'classid': r[3],
                        'teacherid': r[4],
                        'startdate': r[5].strftime(DATE_FORMAT),
                        'enddate': r[6].strftime(DATE_FORMAT),
                        'starttime': r[7],
                        'endtime': r[8],
                        'disabled': r[9],
                        'dayofweek': r[10],
                        }
            data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    
    def getClass(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            if login.usertypeid==1:
                recid = Login.objects.filter(usertypeid=1).values_list('recid')
                classlist = list(Classlist.objects.filter(rubricid__in=recid,disabled=0,deleted=0,clientid=clientid).values('id','classname'))
                data = simplejson.dumps(classlist)
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
    
    def save(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
            classid= request.GET.get('classid', False)
            code = request.GET.get('code', False)
            subcode = request.GET.get('subcode', False)
            dayofweek = request.GET.get('dayofweek', False)
            disabled = request.GET.get('disabled', False)
            enddate = request.GET.get('enddate', False)
            startdate = request.GET.get('startdate', False)
            endtime = request.GET.get('endtime', False)
            starttime = request.GET.get('starttime', False)
            teacherid = request.GET.get('teacherid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            classlist = Classlist.objects.get(id=classid)
            classschedule = Classschedule.objects.get(id=id)
            classschedule.classid = classlist
            classschedule.code = code
            classschedule.subcode = subcode
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
        return HttpResponse('success', mimetype='application/json')
    
    def add(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
            classid= request.GET.get('classid', False)
            code = request.GET.get('code', False)
            subcode = request.GET.get('subcode', False)
            dayofweek = request.GET.get('dayofweek', False)
            disabled = request.GET.get('disabled', False)
            enddate = request.GET.get('enddate', False)
            startdate = request.GET.get('startdate', False)
            endtime = request.GET.get('endtime', False)
            starttime = request.GET.get('starttime', False)
            teacherid = request.GET.get('teacherid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            
            classlist = Classlist.objects.get(id=classid)
            
            classschedule = Classschedule()
            classschedule.classid = classlist
            classschedule.code = code
            classschedule.subcode = subcode
            classschedule.disabled = disabled
            classschedule.endtime = endtime
            classschedule.starttime = starttime
            classschedule.teacherid = teacherid
            classschedule.dayofweek = dayofweek
            classschedule.enddate = datetime.strptime(enddate,DATE_FORMAT)
            classschedule.startdate = datetime.strptime(startdate,DATE_FORMAT)
            classschedule.createddt = datetime.now()
            classschedule.createdby = userid
            classschedule.modifieddt = datetime.now()
            classschedule.modifiedby = userid
            classschedule.deleted = 0
            classschedule.clientid = clientid
            classschedule.save()
        return HttpResponse('success', mimetype='application/json')
    
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
            classid = request.GET.get('classid', False)
            studentid = request.GET.get('studentid', False)
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
            return HttpResponse('success')
        
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
                classlist = Classschedule.objects.filter(clientid=clientid,classid__description__contains=description,deleted=0)
            context = {'classlist': classlist}
            return render(request, 'tsweb/teacher/classlistajax.html', context)
            