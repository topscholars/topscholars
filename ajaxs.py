from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson
from django.core import serializers
from django.db.models.query import RawQuerySet
from django.db import connection
from tsweb.models import *
from django.db.models import Q

from datetime import datetime

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
                user = list(Userlist.objects.filter(id__in=recid,disabled=0,deleted=0,clientid=clientid).values('id','firstname','middlename','lastname'))
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

class STUDENTLIST():
    def get(self,request):
        cursor = connection.cursor()
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            #classlist = Classschedule.objects.filter(id=id)
            cursor.execute("SELECT id,firstname,lastname,middlename,address1,address2,address3,city,zipcode,state,country,mobilephone,homephone,otherphone,emailaddress1,emailaddress2,dob,gender,salutation,currentaccademicyear FROM studentlist  WHERE id = %s", [id])
                   
            results = cursor.fetchall() 
            for r in results:
                data_json = {
                        'id': r[0],
                        'firstname': r[1],
                        'lastname': r[2],
                        'middlename': r[3],
                        'address1': r[4],
                        'address2': r[5],
                        'address3': r[6],
                        'city': r[7],
                        'zipcode': r[8],
                        'state': r[9],
                        'country': r[10],
                        'mobilephone': r[11],
                        'homephone': r[12],
                        'otherphone': r[13],
                        'emailaddress1': r[14],
                        'emailaddress2': r[15],
                        'dob': r[16].strftime(DATE_FORMAT),
                        'gender': r[17],
                        'salutation': r[18],
                        'currentaccademicyear': r[19],
                        }
            data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    
    def getGender(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:  
            select = 'Gender'
            obj = Selectiongroup.objects.get(groupname=select)
            id = obj.id
            selectlist = list(Selectionlist.objects.filter(selectiongroupid=id,disabled=0,deleted=0).values('id','selectionname'))
            data = simplejson.dumps(selectlist)
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
    
    def save(self,request):
        DATE_FORMAT = "%d-%m-%Y"
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
            firstname = request.GET.get('firstname', False)
            lastname = request.GET.get('lastname', False)
            middlename = request.GET.get('middlename', False)
            address1 = request.GET.get('address1', False)
            address2 = request.GET.get('address2', False)
            address3 = request.GET.get('address3', False)
            city = request.GET.get('city', False)
            zipcode = request.GET.get('zipcode', False)
            state = request.GET.get('state', False)
            country = request.GET.get('country', False)
            mobilephone = request.GET.get('mobilephone', False)
            homephone = request.GET.get('homephone', False)
            otherphone = request.GET.get('otherphone', False)
            emailaddress1 = request.GET.get('emailaddress1', False)
            emailaddress2 = request.GET.get('emailaddress2', False)
            dob = request.GET.get('dob', False)
            gender = request.GET.get('gender', False)
            salutation = request.GET.get('salutation', False)
            currentaccademicyear = request.GET.get('currentaccademicyear', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            studentlist = Studentlist.objects.get(id=id)
            studentlist.firstname = firstname
            studentlist.lastname = lastname
            studentlist.middlename = middlename
            studentlist.address1 = address1
            studentlist.address2 = address2
            studentlist.address3 = address3
            studentlist.city = city
            studentlist.zipcode = zipcode
            studentlist.state = state
            studentlist.country = country
            studentlist.mobilephone = mobilephone
            studentlist.homephone = homephone
            studentlist.otherphone = otherphone
            studentlist.emailaddress1 = emailaddress1
            studentlist.emailaddress2 = emailaddress2
            studentlist.dob = datetime.strptime(dob,DATE_FORMAT)
            studentlist.gender = gender
            studentlist.salutation = salutation
            studentlist.currentaccademicyear = currentaccademicyear
            studentlist.save()
        return HttpResponse('success', mimetype='application/json')
    

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
        
class TSTUDENTLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            studentname=request.GET.get('studentname',False)
            classid=request.GET.get('classid',False)
            studentlist = ''
            activeid = Login.objects.filter(deleted=0,usertypeid=2).values_list('recid',flat=True)
            if (studentname != False and studentname != '') and (classid != False and classid != ''):
                studentlist = Studentlist.objects.filter(Q(clientid=clientid) & Q(id__in=activeid) & Q(Studentclasstostudents__classscheduleid__id=classid) & (Q(firstname__contains=studentname) | Q(middlename__contains=studentname) | Q(lastname__contains=studentname)))
            elif studentname != False and studentname != '':
                studentlist = Studentlist.objects.filter(Q(clientid=clientid) & Q(id__in=activeid) & (Q(firstname__contains=studentname) | Q(middlename__contains=studentname) | Q(lastname__contains=studentname)))
            elif classid != False and classid != '':
                studentlist = Studentlist.objects.filter(clientid=clientid,id__in=activeid,Studentclasstostudents__classscheduleid__id=classid)
            else:
                studentlist = Studentlist.objects.filter(clientid=clientid,id__in=activeid)
            context = {'studentlist': studentlist}
            return render(request, 'tsweb/teacher/studentlistajax.html', context)
        
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

class TRUBRICLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            rubricname=request.GET.get('rubricname',False)
            rubriclist=''
            if rubricname != False and rubricname != '':
                rubriclist = Rubric.objects.filter(clientid=clientid,name__contains=rubricname,deleted=0)
            else:
                rubriclist = Rubric.objects.filter(clientid=clientid,deleted=0)
            context = {'rubriclist': rubriclist}
            return render(request, 'tsweb/teacher/rubriclistajax.html', context)

class TSUBMISSIONLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            studentname=request.GET.get('studentname',False)
            submissionlist=''
            if studentname != False and studentname != '':
                submissionlist = Submissionversion.objects.filter(Q(submissionid__teacherid=userid) & Q(studentstatus=1) & Q(teacherstatus=0) & Q(deleted=0) & Q(studentstatus=1) & (Q(submissionid__studentid__firstname__contains=studentname) | Q(submissionid__studentid__middlename__contains=studentname) | Q(submissionid__studentid__lastname__contains=studentname)))
            else:
                submissionlist = Submissionversion.objects.filter(submissionid__teacherid=userid,studentstatus=1,teacherstatus=0,deleted=0)
            context = {'submissionlist': submissionlist}
            return render(request, 'tsweb/teacher/submissionlistajax.html', context)
