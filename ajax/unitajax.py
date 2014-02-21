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
                assignment = UnitAssignment.objects.filter(unitid=id,deleted=0)
                assignmentname = []
                for item in assignment:
                    assignmentname.append({ "id": str(item.id), "name": item.assignmentid.name})
                assignmentlist = simplejson.dumps(assignmentname)
                                          
                data_json = {
                        'unitid': r[0],
                        'name': r[1],
                        'description': r[2],
                        'essentialquestion': r[3],
                        'establishedgoal': r[4],
                        'knowledge': r[5],
                        'skill': r[6],
                        'understanding': r[7],
                        'assignment': assignmentlist,
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
                data_json = { 'status': 'success', 'id': id }
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
                unitid = Unit.objects.latest("id").id
                data_json = { 'status': 'success', 'id': unitid }
            else:
                data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def loadAvailableTags(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            tagidlist = TagEntity.objects.filter(entityid=17,tagid__deleted = 0).values('tagid')
            taglist = list(Tag.objects.filter(id__in = tagidlist).values('name'))
        except Tag.DoesNotExist:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data = simplejson.dumps(taglist)
            return HttpResponse(data, mimetype='application/json')

    def getAssignmentList(self,request):
        userid = request.session['userid']
        login = Login.objects.get(id=userid)
        clientid = login.clientid
        assignmentlist = list(Assignment.objects.filter(disabled = 0, deleted = 0, clientid = clientid).values("id","name"))                              
        data_json = {
                'assignmentlist': assignmentlist,
                }
        data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')

    def getAssignment(self,request):
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            assignment = Assignment.objects.get(id=id)
            impactpercent = 0
            qualitypercent = 0
            contentpercent = 0
            processpercent = 0
            try:
                impact = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 1)
            except Categorylink.DoesNotExist:
                impactpercent = 0
            else:
                impactpercent = impact.totalweight
            try:
                quality = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 2)
            except Categorylink.DoesNotExist:
                qualitypercent = 0
            else:
                qualitypercent = quality.totalweight
            try:
                content = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 3)
            except Categorylink.DoesNotExist:
                contentpercent = 0
            else:
                contentpercent = content.totalweight
            try:
                process = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 4)
            except Categorylink.DoesNotExist:
                processpercent = 0
            else:
                processpercent = process.totalweight
            impactlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 1).values("id","criteria","weight"))
            qualitylist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 2).values("id","criteria","weight"))
            contentlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 3).values("id","criteria","weight"))
            processlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 4).values("id","criteria","weight"))
            data_json = {
                    'pfm_rubric_name': assignment.name,
                    'pfm_rubric_assignment': id,
                    'pfm_rubric_goal': assignment.goaloftask,
                    'pfm_rubric_audience': assignment.audience,
                    'pfm_rubric_context': assignment.contextsituation,
                    'pfm_rubric_parameters_min': assignment.minwords,
                    'pfm_rubric_parameters_max': assignment.maxwords,
                    'pfm_rubric_revisions': assignment.revisions,
                    'pfm_rubric_scale': assignment.rubricid.maxscalevalue,
                    'pfmi_impact_percent': impactpercent,
                    'pfmi_quality_percent': qualitypercent,
                    'pfmi_content_percent': contentpercent,
                    'pfmi_process_percent': processpercent,
                    'pfmi_impact_weight_input': impactpercent,
                    'pfmi_quality_weight_input': qualitypercent,
                    'pfmi_content_weight_input': contentpercent,
                    'pfmi_process_weight_input': processpercent,
                    'impactlist': impactlist,
                    'qualitylist': qualitylist,
                    'contentlist': contentlist,
                    'processlist': processlist
                    }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def getPerformance(self,request):
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            assignment = UnitAssignment.objects.get(id=id)
            impactpercent = 0
            qualitypercent = 0
            contentpercent = 0
            processpercent = 0
            try:
                impact = Categorylink.objects.get(entityid = 6,recid = assignment.assignmentid.rubricid.id, categoryid = 1)
            except Categorylink.DoesNotExist:
                impactpercent = 0
            else:
                impactpercent = impact.totalweight
            try:
                quality = Categorylink.objects.get(entityid = 6,recid = assignment.assignmentid.rubricid.id, categoryid = 2)
            except Categorylink.DoesNotExist:
                qualitypercent = 0
            else:
                qualitypercent = quality.totalweight
            try:
                content = Categorylink.objects.get(entityid = 6,recid = assignment.assignmentid.rubricid.id, categoryid = 3)
            except Categorylink.DoesNotExist:
                contentpercent = 0
            else:
                contentpercent = content.totalweight
            try:
                process = Categorylink.objects.get(entityid = 6,recid = assignment.assignmentid.rubricid.id, categoryid = 4)
            except Categorylink.DoesNotExist:
                processpercent = 0
            else:
                processpercent = process.totalweight
            impactlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 1).values("id","criteria","weight"))
            qualitylist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 2).values("id","criteria","weight"))
            contentlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 3).values("id","criteria","weight"))
            processlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 4).values("id","criteria","weight"))
            data_json = {
                    'pfm_rubric_id': id,
                    'pfm_rubric_name': assignment.assignmentid.name,
                    'pfm_rubric_assignment': assignment.assignmentid.id,
                    'pfm_rubric_goal': assignment.assignmentid.goaloftask,
                    'pfm_rubric_audience': assignment.assignmentid.audience,
                    'pfm_rubric_context': assignment.assignmentid.contextsituation,
                    'pfm_rubric_parameters_min': assignment.assignmentid.minwords,
                    'pfm_rubric_parameters_max': assignment.assignmentid.maxwords,
                    'pfm_rubric_revisions': assignment.assignmentid.revisions,
                    'pfm_rubric_scale': assignment.assignmentid.rubricid.maxscalevalue,
                    'pfmi_impact_percent': impactpercent,
                    'pfmi_quality_percent': qualitypercent,
                    'pfmi_content_percent': contentpercent,
                    'pfmi_process_percent': processpercent,
                    'pfmi_impact_weight_input': impactpercent,
                    'pfmi_quality_weight_input': qualitypercent,
                    'pfmi_content_weight_input': contentpercent,
                    'pfmi_process_weight_input': processpercent,
                    'impactlist': impactlist,
                    'qualitylist': qualitylist,
                    'contentlist': contentlist,
                    'processlist': processlist
                    }
            data = simplejson.dumps(data_json)
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
                unitlist = Unit.objects.filter(clientid=clientid,name__contains=description)
            context = {'unitlist': unitlist}
            return render(request, 'tsweb/teacher/unitlistajax.html', context)
