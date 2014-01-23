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

class UNITLIST():
    def get(self,request):
        cursor = connection.cursor()
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            cursor.execute("SELECT id,name,description,essentialquestion,establishedgoal,knowledge,skill,understanding FROM unit  WHERE id = %s", [id])
            
            results = cursor.fetchall()
            for r in results:
                data_json = {
                        'id': r[0],
                        'name': r[1],
                        'description': r[2],
                        'essentialquestion': r[3],
                        'establishedgoal': r[4],
                        'knowledge': r[5],
                        'skill': r[6],
                        'understanding': r[7],
                        }
            data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')
    
    def save(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            id = request.POST.get('id', False)
            name = request.POST.get('name', False)
            description = request.POST.get('description', False)
            essentialquestion = request.POST.get('essentialquestion', False)
            establishedgoal = request.POST.get('establishedgoal', False)
            knowledge = request.POST.get('knowledge', False)
            skill = request.POST.get('skill', False)
            understanding = request.POST.get('understanding', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                Unit.objects.get(~Q(id=id),Q(name=name))
            except Unit.DoesNotExist:
                unit = Unit.objects.get(id=id)
                unit.name = name
                unit.description = description
                unit.essentialquestion = essentialquestion
                unit.establishedgoal = establishedgoal
                unit.knowledge = knowledge
                unit.skill = skill
                unit.understanding = understanding
                unit.modifieddt = datetime.now()
                unit.modifiedby = userid
                unit.clientid = clientid
                unit.save()
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
            description = request.POST.get('description', False)
            essentialquestion = request.POST.get('essentialquestion', False)
            establishedgoal = request.POST.get('establishedgoal', False)
            knowledge = request.POST.get('knowledge', False)
            skill = request.POST.get('skill', False)
            understanding = request.POST.get('understanding', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                Unit.objects.get(Q(name=name))
            except Unit.DoesNotExist:
                unit = Unit()
                unit.name = name
                unit.description = description
                unit.essentialquestion = essentialquestion
                unit.establishedgoal = establishedgoal
                unit.knowledge = knowledge
                unit.skill = skill
                unit.understanding = understanding
                unit.disabled = 0
                unit.deleted = 0
                unit.modifieddt = datetime.now()
                unit.modifiedby = userid
                unit.createddt = datetime.now()
                unit.createdby = userid
                unit.clientid = clientid
                unit.save()
                data_json = { 'status': 'success', }
            else:
                data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def loadAvailableTags(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            taglist = list(Tag.objects.filter().values('name'))
        except Tag.DoesNotExist:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data = simplejson.dumps(taglist)
            return HttpResponse(data, mimetype='application/json')
        
class TUNITLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
            description=request.GET.get('description',False)
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            
            unitlist = ''
            if description == False or description == '':
                unitlist = Unit.objects.filter(clientid=clientid)
            else:
                unitlist = Unit.objects.filter(clientid=clientid,firstname__contains=description)
            context = {'unitlist': unitlist}
            return render(request, 'tsweb/teacher/unitlistajax.html', context)