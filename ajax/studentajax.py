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
                if r[16] is not None:
                    dob = r[16].strftime(DATE_FORMAT)
                else: 
                    dob = ''
                    
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
                        'dob': dob,
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