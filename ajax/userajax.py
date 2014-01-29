from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson
from django.core import serializers
from django.db.models.query import RawQuerySet
from django.db import connection
from tsweb.models import *
from django.db.models import Q
from itertools import chain
from django.core.mail import send_mail

from datetime import datetime
import time
import random

class USERLIST():
    def get(self,request):
        cursor = connection.cursor()
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            #classlist = Classschedule.objects.filter(id=id)
            cursor.execute("SELECT id,firstname,middlename,lastname,salutation,title,department,dob,homephone,officephone,officeext,mobilephone,emailaddress,securityprofileid FROM userlist  WHERE id = %s", [id])
            
            results = cursor.fetchall()
            for r in results:
                if r[7] is None :
                    dob = ''
                else :
                    dob = r[7].strftime(DATE_FORMAT)
                    
                data_json = {
                        'id': r[0],
                        'firstname': r[1],
                        'middlename': r[2],
                        'lastname': r[3],
                        'salutation': r[4],
                        'title': r[5],
                        'department': r[6],
                        'dob': dob,
                        'homephone': r[8],
                        'officephone': r[9],
                        'officeext': r[10],
                        'mobilephone': r[11],
                        'emailaddress': r[12],
                        'securityprofile': r[13],
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
            id = request.POST.get('id', False)
            title= request.POST.get('title', False)
            department= request.POST.get('department', False)
            salutation= request.POST.get('salutation', False)
            dob = request.POST.get('dob', False)
            emailaddress = request.POST.get('emailaddress', False)
            firstname = request.POST.get('firstname', False)
            middlename = request.POST.get('middlename', False)
            lastname = request.POST.get('lastname', False)
            homephone = request.POST.get('homephone', False)
            officephone = request.POST.get('officephone', False)
            officeext = request.POST.get('officeext', False)
            mobilephone = request.POST.get('mobilephone', False)
            securityprofile = request.POST.get('securityprofile', False)
            password = request.POST.get('password', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            userlist = Userlist.objects.get(id=id)
            userlist.title = title
            userlist.department = department
            userlist.salutation = salutation
            #userlist.dob = dob
            userlist.emailaddress = emailaddress
            userlist.firstname = firstname
            userlist.middlename = middlename
            userlist.lastname = lastname
            userlist.homephone = homephone
            userlist.officephone = officephone
            userlist.officeext = officeext
            userlist.mobilephone = mobilephone
            userlist.dob = datetime.strptime(dob,DATE_FORMAT)
            if securityprofile != False:
                userlist.securityprofileid = securityprofile
            userlist.modifieddt = datetime.now()
            userlist.modifiedby = userid
            userlist.save()
            
            if password != False and password != '':
                login = Login.objects.get(id=userid)
                login.password = password
                login.modifieddt = datetime.now()
                login.modifiedby = userid
                login.save()

            data_json = { 'status': 'success', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
    
    def add(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            title= request.POST.get('title', False)
            department= request.POST.get('department', False)
            salutation= request.POST.get('salutation', False)
            dob = request.POST.get('dob', False)
            emailaddress = request.POST.get('emailaddress', False)
            firstname = request.POST.get('firstname', False)
            middlename = request.POST.get('middlename', False)
            lastname = request.POST.get('lastname', False)
            homephone = request.POST.get('homephone', False)
            officephone = request.POST.get('officephone', False)
            officeext = request.POST.get('officeext', False)
            mobilephone = request.POST.get('mobilephone', False)
            securityprofile = request.POST.get('securityprofile', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            try:
                usercheck = Userlist.objects.get(emailaddress=emailaddress)
            except Userlist.DoesNotExist:
                userlist = Userlist()
                userlist.title = title
                userlist.department = department
                userlist.salutation = salutation
                #userlist.dob = dob
                userlist.emailaddress = emailaddress
                userlist.firstname = firstname
                userlist.middlename = middlename
                userlist.lastname = lastname
                userlist.homephone = homephone
                userlist.officephone = officephone
                userlist.officeext = officeext
                userlist.mobilephone = mobilephone
                userlist.dob = datetime.strptime(dob,DATE_FORMAT)
                userlist.securityprofileid = securityprofile
                userlist.clientid = clientid
                userlist.createddt = datetime.now()
                userlist.createdby = userid
                userlist.modifieddt = datetime.now()
                userlist.modifiedby = userid
                userlist.save()
                
                #password = random 6 digit
                password = random.randrange(0, 999999, 6)
                
                recid = Userlist.objects.latest('id').id
                
                login = Login()
                login.loginname = emailaddress
                login.password = password
                #login.hint = hint
                login.usertypeid = 1
                login.recid = recid
                login.modifieddt = datetime.now()
                login.modifiedby = userid
                login.createddt = datetime.now()
                login.createdby = userid
                login.disabled = 0
                login.deleted = 0
                login.clientid = clientid
                login.save()

                emailto = [emailaddress]
    
                body = 'Dear ' + firstname + ' ' + middlename + ' ' + lastname + ',\n\n' + 'Thank you for joining Writability!  We are excited to welcome you to the community.\n\n' + 'You can now login to your account with the following details:\n' + '\n' + 'User: ' + emailaddress + '\n' + 'Password: ' + str(password) + '\n\n' + 'Please don\'t hesitate to contact us at help@writability.org if you have any questions or issues.\n\n' + 'Good luck writing!\n\n' +'The Writability Team'
    
                send_mail('New Account Creation - Success', body , 'noreply@writability.org',emailto, fail_silently=False)

                data_json = { 'status': 'success',
                             'email': emailaddress,
                             'password': password, }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                data_json = { 'status': 'error', }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
        
    def getSalutation(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:  
            select = 'Salutation'
            obj = Selectiongroup.objects.get(groupname=select)
            id = obj.id
            selectlist = list(Selectionlist.objects.filter(selectiongroupid=id,disabled=0,deleted=0).values('id','selectionname'))
            data = simplejson.dumps(selectlist)
        return HttpResponse(data, mimetype='application/json')
    
    def getSecurityProfile(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:  
            securityprofilelist = list(Securityprofile.objects.filter(disabled=0,deleted=0).values('id','name'))
            data = simplejson.dumps(securityprofilelist)
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
        
    def editData(self,request):
        try:
            DATE_FORMAT = "%d-%m-%Y" 
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            recid = login.recid
            cursor = connection.cursor()
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            #classlist = Classschedule.objects.filter(id=id)
            cursor.execute("SELECT ul.id,ul.firstname,ul.middlename,ul.lastname,ul.salutation,ul.title,ul.department,ul.dob,ul.homephone,ul.officephone,ul.officeext,ul.mobilephone,ul.emailaddress,l.loginname FROM userlist as ul join login as l on (l.usertypeid = 1 and l.recid = ul.id)  WHERE ul.id = %s", [recid])
            
            results = cursor.fetchall()
            for r in results:
                if r[7] is None :
                    dob = ''
                else :
                    dob = r[7].strftime(DATE_FORMAT)
                    
                data_json = {
                        'id': r[0],
                        'firstname': r[1],
                        'middlename': r[2],
                        'lastname': r[3],
                        'salutation': r[4],
                        'title': r[5],
                        'department': r[6],
                        'dob': dob,
                        'homephone': r[8],
                        'officephone': r[9],
                        'officeext': r[10],
                        'mobilephone': r[11],
                        'emailaddress': r[12],
                        'user': r[13],
                        }
            data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
        
class TUSERLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            description=request.GET.get('description',False)
            userlist = ''
            if description == False or description == '':
                userlist = Userlist.objects.filter(clientid=clientid)
            else:
                userlist = Userlist.objects.filter(clientid=clientid,firstname__contains=description)
            context = {'userlist': userlist}
            return render(request, 'tsweb/teacher/userlistajax.html', context)
            
