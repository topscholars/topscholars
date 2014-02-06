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
import random

class TAGLIST():
    def get(self,request):
        cursor = connection.cursor()
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            #classlist = Classschedule.objects.filter(id=id)
            cursor.execute("SELECT tag.id, tag.name, tag.description, tag.parentid, cl.categoryid FROM tag as tag left join categorylink as cl on tag.id = cl.recid and cl.entityid = '12' WHERE tag.id = %s", [id])
            results = cursor.fetchall()
            for r in results:
                    
                data_json = {
                        'id': r[0],
                        'name': r[1],
                        'descriptions': r[2],
                        'parentid': r[3],
                        'categoryid': r[4],
                        }
            data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    
    def getParentTag(self,request):
        try:
            userid = request.session['userid']
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            if id == False or id == '':
                taglist = list(Tag.objects.filter(Q(disabled=0,deleted=0,clientid=clientid)).values('id','name'))
            else:
                taglist = list(Tag.objects.filter(~Q(id=id),Q(disabled=0,deleted=0,clientid=clientid)).values('id','name'))
            data = simplejson.dumps(taglist)
        return HttpResponse(data, mimetype='application/json')
    
    def save(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            
            id = request.POST.get('id', False)
            name = request.POST.get('name', False)
            descriptions = request.POST.get('descriptions', False)
            categoryid = request.POST.get('categoryid', False)
            parentid = request.POST.get('parentid', False)
            
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                Tag.objects.get(~Q(id=id), Q(name=name))
            except Tag.DoesNotExist:
                taglist = Tag.objects.get(id=id)
                taglist.name = name
                if parentid == False:
                    taglist.parentid = 0
                else:
                    taglist.parentid = parentid
                taglist.tagcolor = '#ffff00'
                taglist.abilitylevel = 0
                taglist.description = descriptions
                taglist.modifieddt = datetime.now()
                taglist.modifiedby = userid
                taglist.clientid = clientid
                taglist.save()
                
                #category id save
                category = Category.objects.get(id=categoryid)
                categorylinklist = Categorylink.objects.get(entityid=12, recid=id)
                categorylinklist.categoryid = category
                categorylinklist.modifieddt = datetime.now()
                categorylinklist.modifiedby = userid
                categorylinklist.save()
                    
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
            
            id = request.POST.get('id', False)
            name = request.POST.get('name', False)
            descriptions = request.POST.get('descriptions', False)
            categoryid = request.POST.get('categoryid', False)
            parentid = request.POST.get('parentid', False)
            
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                Tag.objects.get(Q(name=name))
            except Tag.DoesNotExist:
                taglist = Tag()
                taglist.name = name
                if parentid == False:
                    taglist.parentid = 0
                else:
                    taglist.parentid = parentid
                #must be selecttion
                #taglist.abilitylevel = 0
                if clientid == 0:
                    taglist.system = 1
                else:
                    taglist.system = 0
                taglist.tagcolor = '#ffff00'
                taglist.abilitylevel = 0
                taglist.description = descriptions
                taglist.createddt = datetime.now()
                taglist.createdby = userid
                taglist.modifieddt = datetime.now()
                taglist.modifiedby = userid
                taglist.disabled = 0
                taglist.deleted = 0
                taglist.clientid = clientid
                taglist.save()
                
                recid = Tag.objects.latest('id').id
                
                entitylist = Entity.objects.get(id=12)
                category = Category.objects.get(id=categoryid)
                #category id save
                categorylinklist = Categorylink()
                categorylinklist.entityid = entitylist
                categorylinklist.recid = recid
                categorylinklist.categoryid = category
                categorylinklist.totalweight = 0
                categorylinklist.createddt = datetime.now()
                categorylinklist.createdby = userid
                categorylinklist.modifieddt = datetime.now()
                categorylinklist.modifiedby = userid
                categorylinklist.deleted = 0
                categorylinklist.clientid = clientid
                categorylinklist.save()
                
                data_json = { 'status': 'success', }
            else:
                data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
class TTAGLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            description=request.GET.get('description',False)
            taglist = ''
            if description == False or description == '':
                taglist = Tag.objects.filter(clientid=clientid, disabled=0, deleted=0)
            else:
                taglist = Tag.objects.filter(clientid=clientid,firstname__contains=description, disabled=0, deleted=0)
            context = {'taglist': taglist}
            return render(request, 'tsweb/teacher/taglistajax.html', context)
            
