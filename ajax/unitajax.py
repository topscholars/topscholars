import json

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

                lesson = Unitlessonlnk.objects.filter(unitid=id,deleted=0).order_by('order')
                lessonname = []
                for item in lesson:
                    lessonname.append({ "id": str(item.id), "name": item.lessonid.name})
                lessonlist = simplejson.dumps(lessonname)

                activity = []
                lesson = Unitlessonlnk.objects.filter(unitid=id,deleted=0,lessonid__name__isnull=False,lessonid__goaloftask__isnull=False,lessonid__deliverable__isnull=False).exclude(lessonid__name__exact='').exclude(lessonid__goaloftask__exact='').exclude(lessonid__deliverable__exact='').order_by('order')
                for item in lesson:
                    numberofcriteria = Lessonrubriccriterialnk.objects.filter(unitid=id,lessonid=item.lessonid.id,deleted=0).count()
                    if(numberofcriteria > 0):
                        lessonactivitylnk = Lessonactivitylnk.objects.filter(lessonid=item.lessonid.id,deleted=0,activityid__deleted=0).order_by('activityid__order')
                        activityname = []
                        activityobj = ''
                        for lessonactivity in lessonactivitylnk:
                            acttype = "manual"
                            if lessonactivity.activityid.activitytype == 27:
                                acttype = "auto"
                            activityname.append({ "id": str(lessonactivity.activityid.id), "name": lessonactivity.activityid.name, "type": acttype})
                            activityobj = simplejson.dumps(activityname)
                        activity.append({ "id": str(item.id), "name": item.lessonid.name, "goaloftask": item.lessonid.goaloftask, "activity": activityobj})
                activitylist = simplejson.dumps(activity)
                                          
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
                        'lesson': lessonlist,
                        'activity': activitylist
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
            taglist = list(Tag.objects.filter(id__in = tagidlist).values('hashtag'))
        except Tag.DoesNotExist:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data = simplejson.dumps(taglist)
            return HttpResponse(data, mimetype='application/json')

    def getAssignmentList(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            unitid = request.GET.get('unitid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            if unitid == False or unitid == '':
                assignmentlist = list(Assignment.objects.filter(disabled = 0, deleted = 0, clientid = clientid).values("id","name"))                              
            else:
                assignment = UnitAssignment.objects.filter(unitid__id=unitid,deleted=0).values_list("assignmentid", flat=True)
                assignmentlist = list(Assignment.objects.filter(disabled = 0, deleted = 0, clientid = clientid).exclude(id__in=assignment).values("id","name"))                              
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
            impactlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 1).values("id","criteria","weight","hashtag"))
            qualitylist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 2).values("id","criteria","weight","hashtag"))
            contentlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 3).values("id","criteria","weight","hashtag"))
            processlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.rubricid.id, categoryid = 4).values("id","criteria","weight","hashtag"))
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
            impactlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 1).values("id","criteria","weight","hashtag"))
            qualitylist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 2).values("id","criteria","weight","hashtag"))
            contentlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 3).values("id","criteria","weight","hashtag"))
            processlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = assignment.assignmentid.rubricid.id, categoryid = 4).values("id","criteria","weight","hashtag"))
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

    def saveActivityOrder(self,request):
        try:
            userid = request.session['userid']
            strlesson = request.POST.get('lessonlist', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            lessonlist = json.JSONDecoder().decode(strlesson)
            for r in lessonlist: 
                if r['id'] != '':
                    try:
                        lessonorder = int(r['order'])
                    except ValueError:
                        lessonorder = 0
                    try:
                        lesson = Unitlessonlnk.objects.get(id=int(r['id']))
                    except ValueError:
                        continue
                    else:
                        lesson.order = lessonorder
                        lesson.modifieddt = datetime.now()
                        lesson.modifiedby = userid
                        lesson.save()

                        if r['activity'] != '':
##                            activitylist = json.JSONDecoder().decode(r['activity'])
                            activitylist = r['activity']
                            for a in activitylist:
                                if a['id'] != '':
                                    try:
                                        activityorder = int(a['order'])
                                    except ValueError:
                                        activityorder = 0
                                    try:
                                        activity = Lessonactivity.objects.get(id=int(a['id']))
                                    except ValueError:
                                        continue
                                    else:
                                        activity.order = activityorder
                                        activity.modifieddt = datetime.now()
                                        activity.modifiedby = userid
                                        activity.save()

            data_json = { 'status': 'success' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def savePerformance(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            unitassignmentid = request.POST.get('unitassignmentid', False)
            maxwords = request.POST.get('maxwords', False)
            minwords = request.POST.get('minwords', False)
            audience = request.POST.get('audience', False)
            context = request.POST.get('context', False)
            goal = request.POST.get('goal-of-task', False)
            revisions = request.POST.get('revisions', False)
            maxscalevalue = request.POST.get('maxscale', False)
            impact_weight = request.POST.get('impact_weight', False)
            quality_weight = request.POST.get('quality_weight', False)
            content_weight = request.POST.get('content_weight', False)
            process_weight = request.POST.get('process_weight', False)
            impact_criteria = request.POST.get('impact_criteria', False)
            quality_criteria = request.POST.get('quality_criteria', False)
            content_criteria = request.POST.get('content_criteria', False)
            process_criteria = request.POST.get('process_criteria', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                unitassignment = UnitAssignment.objects.get(id=unitassignmentid)
            except UnitAssignment.DoesNotExist:
                data_json = { 'status': 'error' }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                unit = Unit.objects.get(id=unitassignment.unitid.id)
                assignment = Assignment.objects.get(id=unitassignment.assignmentid.id)
                rubric = Rubric.objects.get(id=assignment.rubricid.id)
                
                impactcriterialist = json.JSONDecoder().decode(impact_criteria)
                qualitycriterialist = json.JSONDecoder().decode(quality_criteria)
                contentcriterialist = json.JSONDecoder().decode(content_criteria)
                processcriterialist = json.JSONDecoder().decode(process_criteria)
                Rubriccriteria.objects.filter(Q(rubricid = rubric.id) & (Q(categoryid = 1) | Q(categoryid = 2) | Q(categoryid = 3) | Q(categoryid = 4))).update(deleted=1,modifiedby=userid,modifieddt = datetime.now())
                c1 = Category.objects.get(id=1)
                c2 = Category.objects.get(id=2)
                c3 = Category.objects.get(id=3)
                c4 = Category.objects.get(id=4)
                    
                order = 1
                for r in impactcriterialist:
                    if r['id'] == '':
                        impactcriteria = Rubriccriteria()
                        impactcriteria.rubricid = rubric
                        impactcriteria.criteria = r['criteria']
                        impactcriteria.categoryid = c1
                        if r['weight'] == '':
                            impactcriteria.weight = 0
                        else:
                            impactcriteria.weight = int(r['weight'])
                        impactcriteria.hashtag = r['tag']
                        impactcriteria.order = order
                        impactcriteria.createddt = datetime.now()
                        impactcriteria.createdby = userid
                        impactcriteria.modifieddt = datetime.now()
                        impactcriteria.modifiedby = userid
                        impactcriteria.disabled = 0
                        impactcriteria.deleted = 0
                        impactcriteria.clientid = clientid
                        impactcriteria.save()
                        order = order + 1
                    else:
                        try:
                            impactcriteria = Rubriccriteria.objects.get(id=int(r['id']))
                        except ValueError:
                            impactcriteria = Rubriccriteria()
                            impactcriteria.rubricid = rubric
                            impactcriteria.criteria = r['criteria']
                            impactcriteria.categoryid = c1
                            if r['weight'] == '':
                                impactcriteria.weight = 0
                            else:
                                impactcriteria.weight = int(r['weight'])
                            impactcriteria.hashtag = r['tag']
                            impactcriteria.order = order
                            impactcriteria.createddt = datetime.now()
                            impactcriteria.createdby = userid
                            impactcriteria.modifieddt = datetime.now()
                            impactcriteria.modifiedby = userid
                            impactcriteria.disabled = 0
                            impactcriteria.deleted = 0
                            impactcriteria.clientid = clientid
                            impactcriteria.save()
                            order = order + 1
                        except Rubriccriteria.DoesNotExist:
                            impactcriteria = Rubriccriteria()
                            impactcriteria.rubricid = rubric
                            impactcriteria.criteria = r['criteria']
                            impactcriteria.categoryid = c1
                            if r['weight'] == '':
                                impactcriteria.weight = 0
                            else:
                                impactcriteria.weight = int(r['weight'])
                            impactcriteria.hashtag = r['tag']
                            impactcriteria.order = order
                            impactcriteria.createddt = datetime.now()
                            impactcriteria.createdby = userid
                            impactcriteria.modifieddt = datetime.now()
                            impactcriteria.modifiedby = userid
                            impactcriteria.disabled = 0
                            impactcriteria.deleted = 0
                            impactcriteria.clientid = clientid
                            impactcriteria.save()
                            order = order + 1
                        else:
                            impactcriteria.rubricid = rubric
                            impactcriteria.criteria = r['criteria']
                            if r['weight'] == '':
                                impactcriteria.weight = 0
                            else:
                                impactcriteria.weight = int(r['weight'])
                            impactcriteria.hashtag = r['tag']
                            impactcriteria.order = order
                            impactcriteria.modifieddt = datetime.now()
                            impactcriteria.modifiedby = userid
                            impactcriteria.deleted = 0
                            impactcriteria.save()
                            order = order + 1

                order = 1
                for r in qualitycriterialist:
                    if r['id'] == '':
                        qualitycriteria = Rubriccriteria()
                        qualitycriteria.rubricid = rubric
                        qualitycriteria.criteria = r['criteria']
                        qualitycriteria.categoryid = c2
                        if r['weight'] == '':
                            qualitycriteria.weight = 0
                        else:
                            qualitycriteria.weight = int(r['weight'])
                        qualitycriteria.hashtag = r['tag']
                        qualitycriteria.order = order
                        qualitycriteria.createddt = datetime.now()
                        qualitycriteria.createdby = userid
                        qualitycriteria.modifieddt = datetime.now()
                        qualitycriteria.modifiedby = userid
                        qualitycriteria.disabled = 0
                        qualitycriteria.deleted = 0
                        qualitycriteria.clientid = clientid
                        qualitycriteria.save()
                        order = order + 1
                    else:
                        try:
                            qualitycriteria = Rubriccriteria.objects.get(id=int(r['id']))
                        except ValueError:
                            qualitycriteria = Rubriccriteria()
                            qualitycriteria.rubricid = rubric
                            qualitycriteria.criteria = r['criteria']
                            qualitycriteria.categoryid = c2
                            if r['weight'] == '':
                                qualitycriteria.weight = 0
                            else:
                                qualitycriteria.weight = int(r['weight'])
                            qualitycriteria.hashtag = r['tag']
                            qualitycriteria.order = order
                            qualitycriteria.createddt = datetime.now()
                            qualitycriteria.createdby = userid
                            qualitycriteria.modifieddt = datetime.now()
                            qualitycriteria.modifiedby = userid
                            qualitycriteria.disabled = 0
                            qualitycriteria.deleted = 0
                            qualitycriteria.clientid = clientid
                            qualitycriteria.save()
                            order = order + 1
                        except Rubriccriteria.DoesNotExist:
                            qualitycriteria = Rubriccriteria()
                            qualitycriteria.rubricid = rubric
                            qualitycriteria.criteria = r['criteria']
                            qualitycriteria.categoryid = c2
                            if r['weight'] == '':
                                qualitycriteria.weight = 0
                            else:
                                qualitycriteria.weight = int(r['weight'])
                            qualitycriteria.hashtag = r['tag']
                            qualitycriteria.order = order
                            qualitycriteria.createddt = datetime.now()
                            qualitycriteria.createdby = userid
                            qualitycriteria.modifieddt = datetime.now()
                            qualitycriteria.modifiedby = userid
                            qualitycriteria.disabled = 0
                            qualitycriteria.deleted = 0
                            qualitycriteria.clientid = clientid
                            qualitycriteria.save()
                            order = order + 1
                        else:
                            qualitycriteria.rubricid = rubric
                            qualitycriteria.criteria = r['criteria']
                            if r['weight'] == '':
                                qualitycriteria.weight = 0
                            else:
                                qualitycriteria.weight = int(r['weight'])
                            qualitycriteria.hashtag = r['tag']
                            qualitycriteria.order = order
                            qualitycriteria.modifieddt = datetime.now()
                            qualitycriteria.modifiedby = userid
                            qualitycriteria.deleted = 0
                            qualitycriteria.save()
                            order = order + 1

                order = 1
                for r in contentcriterialist:
                    if r['id'] == '':
                        contentcriteria = Rubriccriteria()
                        contentcriteria.rubricid = rubric
                        contentcriteria.criteria = r['criteria']
                        contentcriteria.categoryid = c3
                        if r['weight'] == '':
                            contentcriteria.weight = 0
                        else:
                            contentcriteria.weight = int(r['weight'])
                        contentcriteria.hashtag = r['tag']
                        contentcriteria.order = order
                        contentcriteria.createddt = datetime.now()
                        contentcriteria.createdby = userid
                        contentcriteria.modifieddt = datetime.now()
                        contentcriteria.modifiedby = userid
                        contentcriteria.disabled = 0
                        contentcriteria.deleted = 0
                        contentcriteria.clientid = clientid
                        contentcriteria.save()
                        order = order + 1
                    else:
                        try:
                            contentcriteria = Rubriccriteria.objects.get(id=int(r['id']))
                        except ValueError:
                            contentcriteria = Rubriccriteria()
                            contentcriteria.rubricid = rubric
                            contentcriteria.criteria = r['criteria']
                            contentcriteria.categoryid = c3
                            if r['weight'] == '':
                                contentcriteria.weight = 0
                            else:
                                contentcriteria.weight = int(r['weight'])
                            contentcriteria.hashtag = r['tag']
                            contentcriteria.order = order
                            contentcriteria.createddt = datetime.now()
                            contentcriteria.createdby = userid
                            contentcriteria.modifieddt = datetime.now()
                            contentcriteria.modifiedby = userid
                            contentcriteria.disabled = 0
                            contentcriteria.deleted = 0
                            contentcriteria.clientid = clientid
                            contentcriteria.save()
                            order = order + 1
                        except Rubriccriteria.DoesNotExist:
                            contentcriteria = Rubriccriteria()
                            contentcriteria.rubricid = rubric
                            contentcriteria.criteria = r['criteria']
                            contentcriteria.categoryid = c3
                            if r['weight'] == '':
                                contentcriteria.weight = 0
                            else:
                                contentcriteria.weight = int(r['weight'])
                            contentcriteria.hashtag = r['tag']
                            contentcriteria.order = order
                            contentcriteria.createddt = datetime.now()
                            contentcriteria.createdby = userid
                            contentcriteria.modifieddt = datetime.now()
                            contentcriteria.modifiedby = userid
                            contentcriteria.disabled = 0
                            contentcriteria.deleted = 0
                            contentcriteria.clientid = clientid
                            contentcriteria.save()
                            order = order + 1
                        else:
                            contentcriteria.rubricid = rubric
                            contentcriteria.criteria = r['criteria']
                            if r['weight'] == '':
                                contentcriteria.weight = 0
                            else:
                                contentcriteria.weight = int(r['weight'])
                            contentcriteria.hashtag = r['tag']
                            contentcriteria.order = order
                            contentcriteria.modifieddt = datetime.now()
                            contentcriteria.modifiedby = userid
                            contentcriteria.deleted = 0
                            contentcriteria.save()
                            order = order + 1

                order = 1
                for r in processcriterialist:
                    if r['id'] == '':
                        processcriteria = Rubriccriteria()
                        processcriteria.rubricid = rubric
                        processcriteria.criteria = r['criteria']
                        processcriteria.categoryid = c4
                        if r['weight'] == '':
                            processcriteria.weight = 0
                        else:
                            processcriteria.weight = int(r['weight'])
                        processcriteria.hashtag = r['tag']
                        processcriteria.order = order
                        processcriteria.createddt = datetime.now()
                        processcriteria.createdby = userid
                        processcriteria.modifieddt = datetime.now()
                        processcriteria.modifiedby = userid
                        processcriteria.disabled = 0
                        processcriteria.deleted = 0
                        processcriteria.clientid = clientid
                        processcriteria.save()
                        order = order + 1
                    else:
                        try:
                            processcriteria = Rubriccriteria.objects.get(id=int(r['id']))
                        except ValueError:
                            processcriteria = Rubriccriteria()
                            processcriteria.rubricid = rubric
                            processcriteria.criteria = r['criteria']
                            processcriteria.categoryid = c4
                            if r['weight'] == '':
                                processcriteria.weight = 0
                            else:
                                processcriteria.weight = int(r['weight'])
                            processcriteria.hashtag = r['tag']
                            processcriteria.order = order
                            processcriteria.createddt = datetime.now()
                            processcriteria.createdby = userid
                            processcriteria.modifieddt = datetime.now()
                            processcriteria.modifiedby = userid
                            processcriteria.disabled = 0
                            processcriteria.deleted = 0
                            processcriteria.clientid = clientid
                            processcriteria.save()
                            order = order + 1
                        except Rubriccriteria.DoesNotExist:
                            processcriteria = Rubriccriteria()
                            processcriteria.rubricid = rubric
                            processcriteria.criteria = r['criteria']
                            processcriteria.categoryid = c4
                            if r['weight'] == '':
                                processcriteria.weight = 0
                            else:
                                processcriteria.weight = int(r['weight'])
                            processcriteria.hashtag = r['tag']
                            processcriteria.order = order
                            processcriteria.createddt = datetime.now()
                            processcriteria.createdby = userid
                            processcriteria.modifieddt = datetime.now()
                            processcriteria.modifiedby = userid
                            processcriteria.disabled = 0
                            processcriteria.deleted = 0
                            processcriteria.clientid = clientid
                            processcriteria.save()
                            order = order + 1
                        else:
                            processcriteria.rubricid = rubric
                            processcriteria.criteria = r['criteria']
                            if r['weight'] == '':
                                processcriteria.weight = 0
                            else:
                                processcriteria.weight = int(r['weight'])
                            processcriteria.hashtag = r['tag']
                            processcriteria.order = order
                            processcriteria.modifieddt = datetime.now()
                            processcriteria.modifiedby = userid
                            processcriteria.deleted = 0
                            processcriteria.save()
                            order = order + 1

                entityid = Entity.objects.get(id=6)
                try:
                    impact = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 1)
                except Categorylink.DoesNotExist:
                    impact = Categorylink()
                    impact.entityid = entityid
                    impact.recid = rubric.id
                    impact.categoryid = c1
                    impact.totalweight = impact_weight
                    impact.createddt = datetime.now()
                    impact.createdby = userid
                    impact.modifieddt = datetime.now()
                    impact.modifiedby = userid
                    impact.deleted = 0
                    impact.clientid = clientid
                    impact.save()
                else:
                    impact.totalweight = impact_weight
                    impact.modifieddt = datetime.now()
                    impact.modifiedby = userid
                    impact.save()

                try:
                    quality = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 2)
                except Categorylink.DoesNotExist:
                    quality = Categorylink()
                    quality.entityid = entityid
                    quality.recid = rubric.id
                    quality.categoryid = c2
                    quality.totalweight = quality_weight
                    quality.createddt = datetime.now()
                    quality.createdby = userid
                    quality.modifieddt = datetime.now()
                    quality.modifiedby = userid
                    quality.deleted = 0
                    quality.clientid = clientid
                    quality.save()
                else:
                    quality.totalweight = quality_weight
                    quality.modifieddt = datetime.now()
                    quality.modifiedby = userid
                    quality.save()

                try:
                    content = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 3)
                except Categorylink.DoesNotExist:
                    content = Categorylink()
                    content.entityid = entityid
                    content.recid = rubric.id
                    content.categoryid = c3
                    content.totalweight = content_weight
                    content.createddt = datetime.now()
                    content.createdby = userid
                    content.modifieddt = datetime.now()
                    content.modifiedby = userid
                    content.deleted = 0
                    content.clientid = clientid
                    content.save()
                else:
                    content.totalweight = content_weight
                    content.modifieddt = datetime.now()
                    content.modifiedby = userid
                    content.save()

                try:
                    process = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 4)
                except Categorylink.DoesNotExist:
                    process = Categorylink()
                    process.entityid = entityid
                    process.recid = rubric.id
                    process.categoryid = c4
                    process.totalweight = process_weight
                    process.createddt = datetime.now()
                    process.createdby = userid
                    process.modifieddt = datetime.now()
                    process.modifiedby = userid
                    process.deleted = 0
                    process.clientid = clientid
                    process.save()
                else:
                    process.totalweight = process_weight
                    process.modifieddt = datetime.now()
                    process.modifiedby = userid
                    process.save()

                rubric.maxscalevalue = maxscalevalue
                rubric.modifieddt = datetime.now()
                rubric.modifiedby = userid
                rubric.save()

                assignment.goaloftask = goal
                if maxwords == False or maxwords == '':
                    assignment.maxwords = 0
                else:
                    assignment.maxwords = maxwords
                if minwords == False or minwords == '':
                    assignment.minwords = 0
                else:
                    assignment.minwords = minwords
                assignment.audience = audience
                assignment.contextsituation = context
                if revisions == False or revisions == '':
                    assignment.revisions = 0
                else:
                    assignment.revisions = revisions  
                assignment.modifieddt = datetime.now()
                assignment.modifiedby = userid
                assignment.save()
                
                data_json = { 'status': 'success' }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            

    def addPerformance(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            unitid = request.POST.get('unitid', False)
            name = request.POST.get('name', False)
            assignmentid = request.POST.get('assignment', False)
            maxwords = request.POST.get('maxwords', False)
            minwords = request.POST.get('minwords', False)
            audience = request.POST.get('audience', False)
            context = request.POST.get('context', False)
            goal = request.POST.get('goal-of-task', False)
            revisions = request.POST.get('revisions', False)
            maxscalevalue = request.POST.get('maxscale', False)
            impact_weight = request.POST.get('impact_weight', False)
            quality_weight = request.POST.get('quality_weight', False)
            content_weight = request.POST.get('content_weight', False)
            process_weight = request.POST.get('process_weight', False)
            impact_criteria = request.POST.get('impact_criteria', False)
            quality_criteria = request.POST.get('quality_criteria', False)
            content_criteria = request.POST.get('content_criteria', False)
            process_criteria = request.POST.get('process_criteria', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            if assignmentid == False or assignmentid == '':
                try:
                    Assignment.objects.get(name=name,clientid=clientid,deleted=0)
                except Assignment.DoesNotExist:
                    rubrictypeint = Selectionlist.objects.get(id=1)
                    rubric = Rubric()
                    rubric.name = name
                    rubric.entityid = 3
                    rubric.typeid = rubrictypeint
                    rubric.maxscalevalue = maxscalevalue
                    rubric.createddt = datetime.now()
                    rubric.createdby = userid
                    rubric.modifieddt = datetime.now()
                    rubric.modifiedby = userid
                    rubric.disabled = 0
                    rubric.deleted = 0
                    rubric.clientid = clientid
                    rubric.system = 0
                    rubric.save()

                    rubriclist = Rubric.objects.latest("id")
                    
                    assignment = Assignment()
                    assignment.name = name
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
                    assignment.duedate = datetime.now()
                    if revisions == False or revisions == '':
                        assignment.revisions = 0
                    else:
                        assignment.revisions = revisions  
                    assignment.modifieddt = datetime.now()
                    assignment.modifiedby = userid
                    assignment.createddt = datetime.now()
                    assignment.createdby = userid
                    assignment.disabled = 0
                    assignment.deleted = 0
                    assignment.clientid = clientid
                    assignment.save()

                    assignmentlist = Assignment.objects.latest("id")

                    unit = Unit.objects.get(id=unitid)
                    unitassignment = UnitAssignment()
                    unitassignment.unitid = unit
                    unitassignment.assignmentid = assignmentlist
                    unitassignment.createddt = datetime.now()
                    unitassignment.createdby = userid
                    unitassignment.modifieddt = datetime.now()
                    unitassignment.modifiedby = userid
                    unitassignment.deleted = 0
                    unitassignment.clientid = clientid
                    unitassignment.save()

                    entityid = Entity.objects.get(id=6)
                    c1 = Category.objects.get(id=1)
                    impact = Categorylink()
                    impact.entityid = entityid
                    impact.recid = rubriclist.id
                    impact.categoryid = c1
                    impact.totalweight = impact_weight
                    impact.createddt = datetime.now()
                    impact.createdby = userid
                    impact.modifieddt = datetime.now()
                    impact.modifiedby = userid
                    impact.deleted = 0
                    impact.clientid = clientid
                    impact.save()

                    c2 = Category.objects.get(id=2)
                    quality = Categorylink()
                    quality.entityid = entityid
                    quality.recid = rubriclist.id
                    quality.categoryid = c2
                    quality.totalweight = quality_weight
                    quality.createddt = datetime.now()
                    quality.createdby = userid
                    quality.modifieddt = datetime.now()
                    quality.modifiedby = userid
                    quality.deleted = 0
                    quality.clientid = clientid
                    quality.save()

                    c3 = Category.objects.get(id=3)
                    content = Categorylink()
                    content.entityid = entityid
                    content.recid = rubriclist.id
                    content.categoryid = c3
                    content.totalweight = content_weight
                    content.createddt = datetime.now()
                    content.createdby = userid
                    content.modifieddt = datetime.now()
                    content.modifiedby = userid
                    content.deleted = 0
                    content.clientid = clientid
                    content.save()

                    c4 = Category.objects.get(id=4)
                    process = Categorylink()
                    process.entityid = entityid
                    process.recid = rubriclist.id
                    process.categoryid = c4
                    process.totalweight = process_weight
                    process.createddt = datetime.now()
                    process.createdby = userid
                    process.modifieddt = datetime.now()
                    process.modifiedby = userid
                    process.deleted = 0
                    process.clientid = clientid
                    process.save()

                    impactcriterialist = json.JSONDecoder().decode(impact_criteria)
                    qualitycriterialist = json.JSONDecoder().decode(quality_criteria)
                    contentcriterialist = json.JSONDecoder().decode(content_criteria)
                    processcriterialist = json.JSONDecoder().decode(process_criteria)

                    order = 1
                    for r in impactcriterialist:
                        impactcriteria = Rubriccriteria()
                        impactcriteria.rubricid = rubriclist
                        impactcriteria.criteria = r['criteria']
                        impactcriteria.categoryid = c1
                        if r['weight'] == '':
                            impactcriteria.weight = 0
                        else:
                            impactcriteria.weight = int(r['weight'])
                        impactcriteria.hashtag = r['tag']
                        impactcriteria.order = order
                        impactcriteria.createddt = datetime.now()
                        impactcriteria.createdby = userid
                        impactcriteria.modifieddt = datetime.now()
                        impactcriteria.modifiedby = userid
                        impactcriteria.disabled = 0
                        impactcriteria.deleted = 0
                        impactcriteria.clientid = clientid
                        impactcriteria.save()
                        order = order + 1

                    order = 1
                    for r in qualitycriterialist:
                        qualitycriteria = Rubriccriteria()
                        qualitycriteria.rubricid = rubriclist
                        qualitycriteria.criteria = r['criteria']
                        qualitycriteria.categoryid = c2
                        if r['weight'] == '':
                            qualitycriteria.weight = 0
                        else:
                            qualitycriteria.weight = int(r['weight'])
                        qualitycriteria.hashtag = r['tag']
                        qualitycriteria.order = order
                        qualitycriteria.createddt = datetime.now()
                        qualitycriteria.createdby = userid
                        qualitycriteria.modifieddt = datetime.now()
                        qualitycriteria.modifiedby = userid
                        qualitycriteria.disabled = 0
                        qualitycriteria.deleted = 0
                        qualitycriteria.clientid = clientid
                        qualitycriteria.save()
                        order = order + 1

                    order = 1
                    for r in contentcriterialist:
                        contentcriteria = Rubriccriteria()
                        contentcriteria.rubricid = rubriclist
                        contentcriteria.criteria = r['criteria']
                        contentcriteria.categoryid = c3
                        if r['weight'] == '':
                            contentcriteria.weight = 0
                        else:
                            contentcriteria.weight = int(r['weight'])
                        contentcriteria.hashtag = r['tag']
                        contentcriteria.order = order
                        contentcriteria.createddt = datetime.now()
                        contentcriteria.createdby = userid
                        contentcriteria.modifieddt = datetime.now()
                        contentcriteria.modifiedby = userid
                        contentcriteria.disabled = 0
                        contentcriteria.deleted = 0
                        contentcriteria.clientid = clientid
                        contentcriteria.save()
                        order = order + 1

                    order = 1
                    for r in processcriterialist:
                        processcriteria = Rubriccriteria()
                        processcriteria.rubricid = rubriclist
                        processcriteria.criteria = r['criteria']
                        processcriteria.categoryid = c4
                        if r['weight'] == '':
                            processcriteria.weight = 0
                        else:
                            processcriteria.weight = int(r['weight'])
                        processcriteria.hashtag = r['tag']
                        processcriteria.order = order
                        processcriteria.createddt = datetime.now()
                        processcriteria.createdby = userid
                        processcriteria.modifieddt = datetime.now()
                        processcriteria.modifiedby = userid
                        processcriteria.disabled = 0
                        processcriteria.deleted = 0
                        processcriteria.clientid = clientid
                        processcriteria.save()
                        order = order + 1

                    lesson = Lesson()
                    lesson.name = name
                    lesson.lessontype = 25
                    lesson.abilitylevel = 0
                    lesson.goaloftask = goal
                    lesson.createddt = datetime.now()
                    lesson.createdby = userid
                    lesson.modifieddt = datetime.now()
                    lesson.modifiedby = userid
                    lesson.disabled = 0
                    lesson.deleted = 0
                    lesson.clientid = clientid
                    lesson.save()

                    lessonlist = Lesson.objects.latest("id")

                    unitnum = Unitlessonlnk.objects.filter(unitid=unit.id,deleted=0).count()
                    unitlesson = Unitlessonlnk()
                    unitlesson.unitid = unit
                    unitlesson.assignmentid = assignmentlist
                    unitlesson.lessonid = lessonlist
                    unitlesson.createddt = datetime.now()
                    unitlesson.createdby = userid
                    unitlesson.modifieddt = datetime.now()
                    unitlesson.modifiedby = userid
                    unitlesson.deleted = 0
                    unitlesson.order = unitnum + 1
                    unitlesson.save()

                    impactlist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 1)
                    order = 1
                    for r in impactlist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                        
                    qualitylist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 2)
                    order = 1
                    for r in qualitylist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                        
                    contentlist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 3)
                    order = 1
                    for r in contentlist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                        
                    processlist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 4)
                    order = 1
                    for r in processlist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    
                    activity = Lessonactivity()
                    activity.name = name
                    activity.activitytype = 26
                    activity.assignmentid = assignmentlist.id
                    activity.createddt = datetime.now()
                    activity.createdby = userid
                    activity.modifieddt = datetime.now()
                    activity.modifiedby  = userid
                    activity.deleted = 0
                    activity.order = 100
                    activity.clientid = clientid
                    activity.abilitylevel = 0
                    activity.criteriaid = 0
                    activity.save()

                    activitylist = Lessonactivity.objects.latest("id")

                    lessonactivity = Lessonactivitylnk()
                    lessonactivity.lessonid = lessonlist
                    lessonactivity.activityid = activitylist
                    lessonactivity.createddt = datetime.now()
                    lessonactivity.createdby = userid
                    lessonactivity.modifieddt = datetime.now()
                    lessonactivity.modifiedby = userid
                    lessonactivity.deleted = 0
                    lessonactivity.lessonrubriccriterialnkid = 0
                    lessonactivity.save()
                    
                    data_json = { 'status': 'success' }
                else:
                    data_json = { 'status': 'duplicate' }
            else:
                try:
                    unitassignment = UnitAssignment.objects.get(unitid__id=unitid,assignmentid__id=assignmentid,deleted=0)
                except UnitAssignment.DoesNotExist:
                    unit = Unit.objects.get(id=unitid)
                    assignment = Assignment.objects.get(id=assignmentid)
                    rubriclist = Rubric.objects.get(id=assignment.rubricid.id)
                    unitassignment = UnitAssignment()
                    unitassignment.unitid = unit
                    unitassignment.assignmentid = assignment
                    unitassignment.createddt = datetime.now()
                    unitassignment.createdby = userid
                    unitassignment.modifieddt = datetime.now()
                    unitassignment.modifiedby = userid
                    unitassignment.deleted = 0
                    unitassignment.clientid = clientid
                    unitassignment.save()

                    impactcriterialist = json.JSONDecoder().decode(impact_criteria)
                    qualitycriterialist = json.JSONDecoder().decode(quality_criteria)
                    contentcriterialist = json.JSONDecoder().decode(content_criteria)
                    processcriterialist = json.JSONDecoder().decode(process_criteria)
                    Rubriccriteria.objects.filter(Q(rubricid = rubriclist.id) & (Q(categoryid = 1) | Q(categoryid = 2) | Q(categoryid = 3) | Q(categoryid = 4))).update(deleted=1,modifiedby=userid,modifieddt = datetime.now())
                    c1 = Category.objects.get(id=1)
                    c2 = Category.objects.get(id=2)
                    c3 = Category.objects.get(id=3)
                    c4 = Category.objects.get(id=4)
                    
                    order = 1
                    for r in impactcriterialist:
                        if r['id'] == '':
                            impactcriteria = Rubriccriteria()
                            impactcriteria.rubricid = rubriclist
                            impactcriteria.criteria = r['criteria']
                            impactcriteria.categoryid = c1
                            if r['weight'] == '':
                                impactcriteria.weight = 0
                            else:
                                impactcriteria.weight = int(r['weight'])
                            impactcriteria.hashtag = r['tag']
                            impactcriteria.order = order
                            impactcriteria.createddt = datetime.now()
                            impactcriteria.createdby = userid
                            impactcriteria.modifieddt = datetime.now()
                            impactcriteria.modifiedby = userid
                            impactcriteria.disabled = 0
                            impactcriteria.deleted = 0
                            impactcriteria.clientid = clientid
                            impactcriteria.save()
                            order = order + 1
                        else:
                            try:
                                impactcriteria = Rubriccriteria.objects.get(id=int(r['id']))
                            except ValueError:
                                impactcriteria = Rubriccriteria()
                                impactcriteria.rubricid = rubriclist
                                impactcriteria.criteria = r['criteria']
                                impactcriteria.categoryid = c1
                                if r['weight'] == '':
                                    impactcriteria.weight = 0
                                else:
                                    impactcriteria.weight = int(r['weight'])
                                impactcriteria.hashtag = r['tag']
                                impactcriteria.order = order
                                impactcriteria.createddt = datetime.now()
                                impactcriteria.createdby = userid
                                impactcriteria.modifieddt = datetime.now()
                                impactcriteria.modifiedby = userid
                                impactcriteria.disabled = 0
                                impactcriteria.deleted = 0
                                impactcriteria.clientid = clientid
                                impactcriteria.save()
                                order = order + 1
                            except Rubriccriteria.DoesNotExist:
                                impactcriteria = Rubriccriteria()
                                impactcriteria.rubricid = rubriclist
                                impactcriteria.criteria = r['criteria']
                                impactcriteria.categoryid = c1
                                if r['weight'] == '':
                                    impactcriteria.weight = 0
                                else:
                                    impactcriteria.weight = int(r['weight'])
                                impactcriteria.hashtag = r['tag']
                                impactcriteria.order = order
                                impactcriteria.createddt = datetime.now()
                                impactcriteria.createdby = userid
                                impactcriteria.modifieddt = datetime.now()
                                impactcriteria.modifiedby = userid
                                impactcriteria.disabled = 0
                                impactcriteria.deleted = 0
                                impactcriteria.clientid = clientid
                                impactcriteria.save()
                                order = order + 1
                            else:
                                impactcriteria.rubricid = rubriclist
                                if r['weight'] == '':
                                    impactcriteria.weight = 0
                                else:
                                    impactcriteria.weight = int(r['weight'])
                                impactcriteria.hashtag = r['tag']
                                impactcriteria.order = order
                                impactcriteria.modifieddt = datetime.now()
                                impactcriteria.modifiedby = userid
                                impactcriteria.deleted = 0
                                impactcriteria.save()
                                order = order + 1

                    order = 1
                    for r in qualitycriterialist:
                        if r['id'] == '':
                            qualitycriteria = Rubriccriteria()
                            qualitycriteria.rubricid = rubriclist
                            qualitycriteria.criteria = r['criteria']
                            qualitycriteria.categoryid = c2
                            if r['weight'] == '':
                                qualitycriteria.weight = 0
                            else:
                                qualitycriteria.weight = int(r['weight'])
                            qualitycriteria.hashtag = r['tag']
                            qualitycriteria.order = order
                            qualitycriteria.createddt = datetime.now()
                            qualitycriteria.createdby = userid
                            qualitycriteria.modifieddt = datetime.now()
                            qualitycriteria.modifiedby = userid
                            qualitycriteria.disabled = 0
                            qualitycriteria.deleted = 0
                            qualitycriteria.clientid = clientid
                            qualitycriteria.save()
                            order = order + 1
                        else:
                            try:
                                qualitycriteria = Rubriccriteria.objects.get(id=int(r['id']))
                            except ValueError:
                                qualitycriteria = Rubriccriteria()
                                qualitycriteria.rubricid = rubriclist
                                qualitycriteria.criteria = r['criteria']
                                qualitycriteria.categoryid = c2
                                if r['weight'] == '':
                                    qualitycriteria.weight = 0
                                else:
                                    qualitycriteria.weight = int(r['weight'])
                                qualitycriteria.hashtag = r['tag']
                                qualitycriteria.order = order
                                qualitycriteria.createddt = datetime.now()
                                qualitycriteria.createdby = userid
                                qualitycriteria.modifieddt = datetime.now()
                                qualitycriteria.modifiedby = userid
                                qualitycriteria.disabled = 0
                                qualitycriteria.deleted = 0
                                qualitycriteria.clientid = clientid
                                qualitycriteria.save()
                                order = order + 1
                            except Rubriccriteria.DoesNotExist:
                                qualitycriteria = Rubriccriteria()
                                qualitycriteria.rubricid = rubriclist
                                qualitycriteria.criteria = r['criteria']
                                qualitycriteria.categoryid = c2
                                if r['weight'] == '':
                                    qualitycriteria.weight = 0
                                else:
                                    qualitycriteria.weight = int(r['weight'])
                                qualitycriteria.hashtag = r['tag']
                                qualitycriteria.order = order
                                qualitycriteria.createddt = datetime.now()
                                qualitycriteria.createdby = userid
                                qualitycriteria.modifieddt = datetime.now()
                                qualitycriteria.modifiedby = userid
                                qualitycriteria.disabled = 0
                                qualitycriteria.deleted = 0
                                qualitycriteria.clientid = clientid
                                qualitycriteria.save()
                                order = order + 1
                            else:
                                qualitycriteria.rubricid = rubriclist
                                if r['weight'] == '':
                                    qualitycriteria.weight = 0
                                else:
                                    qualitycriteria.weight = int(r['weight'])
                                qualitycriteria.hashtag = r['tag']
                                qualitycriteria.order = order
                                qualitycriteria.modifieddt = datetime.now()
                                qualitycriteria.modifiedby = userid
                                qualitycriteria.deleted = 0
                                qualitycriteria.save()
                                order = order + 1

                    order = 1
                    for r in contentcriterialist:
                        if r['id'] == '':
                            contentcriteria = Rubriccriteria()
                            contentcriteria.rubricid = rubriclist
                            contentcriteria.criteria = r['criteria']
                            contentcriteria.categoryid = c3
                            if r['weight'] == '':
                                contentcriteria.weight = 0
                            else:
                                contentcriteria.weight = int(r['weight'])
                            contentcriteria.hashtag = r['tag']
                            contentcriteria.order = order
                            contentcriteria.createddt = datetime.now()
                            contentcriteria.createdby = userid
                            contentcriteria.modifieddt = datetime.now()
                            contentcriteria.modifiedby = userid
                            contentcriteria.disabled = 0
                            contentcriteria.deleted = 0
                            contentcriteria.clientid = clientid
                            contentcriteria.save()
                            order = order + 1
                        else:
                            try:
                                contentcriteria = Rubriccriteria.objects.get(id=int(r['id']))
                            except ValueError:
                                contentcriteria = Rubriccriteria()
                                contentcriteria.rubricid = rubriclist
                                contentcriteria.criteria = r['criteria']
                                contentcriteria.categoryid = c3
                                if r['weight'] == '':
                                    contentcriteria.weight = 0
                                else:
                                    contentcriteria.weight = int(r['weight'])
                                contentcriteria.hashtag = r['tag']
                                contentcriteria.order = order
                                contentcriteria.createddt = datetime.now()
                                contentcriteria.createdby = userid
                                contentcriteria.modifieddt = datetime.now()
                                contentcriteria.modifiedby = userid
                                contentcriteria.disabled = 0
                                contentcriteria.deleted = 0
                                contentcriteria.clientid = clientid
                                contentcriteria.save()
                                order = order + 1
                            except Rubriccriteria.DoesNotExist:
                                contentcriteria = Rubriccriteria()
                                contentcriteria.rubricid = rubriclist
                                contentcriteria.criteria = r['criteria']
                                contentcriteria.categoryid = c3
                                if r['weight'] == '':
                                    contentcriteria.weight = 0
                                else:
                                    contentcriteria.weight = int(r['weight'])
                                contentcriteria.hashtag = r['tag']
                                contentcriteria.order = order
                                contentcriteria.createddt = datetime.now()
                                contentcriteria.createdby = userid
                                contentcriteria.modifieddt = datetime.now()
                                contentcriteria.modifiedby = userid
                                contentcriteria.disabled = 0
                                contentcriteria.deleted = 0
                                contentcriteria.clientid = clientid
                                contentcriteria.save()
                                order = order + 1
                            else:
                                contentcriteria.rubricid = rubriclist
                                if r['weight'] == '':
                                    contentcriteria.weight = 0
                                else:
                                    contentcriteria.weight = int(r['weight'])
                                contentcriteria.hashtag = r['tag']
                                contentcriteria.order = order
                                contentcriteria.modifieddt = datetime.now()
                                contentcriteria.modifiedby = userid
                                contentcriteria.deleted = 0
                                contentcriteria.save()
                                order = order + 1

                    order = 1
                    for r in processcriterialist:
                        if r['id'] == '':
                            processcriteria = Rubriccriteria()
                            processcriteria.rubricid = rubriclist
                            processcriteria.criteria = r['criteria']
                            processcriteria.categoryid = c4
                            if r['weight'] == '':
                                processcriteria.weight = 0
                            else:
                                processcriteria.weight = int(r['weight'])
                            processcriteria.hashtag = r['tag']
                            processcriteria.order = order
                            processcriteria.createddt = datetime.now()
                            processcriteria.createdby = userid
                            processcriteria.modifieddt = datetime.now()
                            processcriteria.modifiedby = userid
                            processcriteria.disabled = 0
                            processcriteria.deleted = 0
                            processcriteria.clientid = clientid
                            processcriteria.save()
                            order = order + 1
                        else:
                            try:
                                processcriteria = Rubriccriteria.objects.get(id=int(r['id']))
                            except ValueError:
                                processcriteria = Rubriccriteria()
                                processcriteria.rubricid = rubriclist
                                processcriteria.criteria = r['criteria']
                                processcriteria.categoryid = c4
                                if r['weight'] == '':
                                    processcriteria.weight = 0
                                else:
                                    processcriteria.weight = int(r['weight'])
                                processcriteria.hashtag = r['tag']
                                processcriteria.order = order
                                processcriteria.createddt = datetime.now()
                                processcriteria.createdby = userid
                                processcriteria.modifieddt = datetime.now()
                                processcriteria.modifiedby = userid
                                processcriteria.disabled = 0
                                processcriteria.deleted = 0
                                processcriteria.clientid = clientid
                                processcriteria.save()
                                order = order + 1
                            except Rubriccriteria.DoesNotExist:
                                processcriteria = Rubriccriteria()
                                processcriteria.rubricid = rubriclist
                                processcriteria.criteria = r['criteria']
                                processcriteria.categoryid = c4
                                if r['weight'] == '':
                                    processcriteria.weight = 0
                                else:
                                    processcriteria.weight = int(r['weight'])
                                processcriteria.hashtag = r['tag']
                                processcriteria.order = order
                                processcriteria.createddt = datetime.now()
                                processcriteria.createdby = userid
                                processcriteria.modifieddt = datetime.now()
                                processcriteria.modifiedby = userid
                                processcriteria.disabled = 0
                                processcriteria.deleted = 0
                                processcriteria.clientid = clientid
                                processcriteria.save()
                                order = order + 1
                            else:
                                processcriteria.rubricid = rubriclist
                                if r['weight'] == '':
                                    processcriteria.weight = 0
                                else:
                                    processcriteria.weight = int(r['weight'])
                                processcriteria.hashtag = r['tag']
                                processcriteria.order = order
                                processcriteria.modifieddt = datetime.now()
                                processcriteria.modifiedby = userid
                                processcriteria.deleted = 0
                                processcriteria.save()
                                order = order + 1

                    entityid = Entity.objects.get(id=6)
                    try:
                        impact = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 1)
                    except Categorylink.DoesNotExist:
                        impact = Categorylink()
                        impact.entityid = entityid
                        impact.recid = rubriclist.id
                        impact.categoryid = c1
                        impact.totalweight = impact_weight
                        impact.createddt = datetime.now()
                        impact.createdby = userid
                        impact.modifieddt = datetime.now()
                        impact.modifiedby = userid
                        impact.deleted = 0
                        impact.clientid = clientid
                        impact.save()
                    else:
                        impact.totalweight = impact_weight
                        impact.modifieddt = datetime.now()
                        impact.modifiedby = userid
                        impact.save()

                    try:
                        quality = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 2)
                    except Categorylink.DoesNotExist:
                        quality = Categorylink()
                        quality.entityid = entityid
                        quality.recid = rubriclist.id
                        quality.categoryid = c2
                        quality.totalweight = quality_weight
                        quality.createddt = datetime.now()
                        quality.createdby = userid
                        quality.modifieddt = datetime.now()
                        quality.modifiedby = userid
                        quality.deleted = 0
                        quality.clientid = clientid
                        quality.save()
                    else:
                        quality.totalweight = quality_weight
                        quality.modifieddt = datetime.now()
                        quality.modifiedby = userid
                        quality.save()

                    try:
                        content = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 3)
                    except Categorylink.DoesNotExist:
                        content = Categorylink()
                        content.entityid = entityid
                        content.recid = rubriclist.id
                        content.categoryid = c3
                        content.totalweight = content_weight
                        content.createddt = datetime.now()
                        content.createdby = userid
                        content.modifieddt = datetime.now()
                        content.modifiedby = userid
                        content.deleted = 0
                        content.clientid = clientid
                        content.save()
                    else:
                        content.totalweight = content_weight
                        content.modifieddt = datetime.now()
                        content.modifiedby = userid
                        content.save()

                    try:
                        process = Categorylink.objects.get(entityid = 6,recid = assignment.rubricid.id, categoryid = 4)
                    except Categorylink.DoesNotExist:
                        process = Categorylink()
                        process.entityid = entityid
                        process.recid = rubriclist.id
                        process.categoryid = c4
                        process.totalweight = process_weight
                        process.createddt = datetime.now()
                        process.createdby = userid
                        process.modifieddt = datetime.now()
                        process.modifiedby = userid
                        process.deleted = 0
                        process.clientid = clientid
                        process.save()
                    else:
                        process.totalweight = process_weight
                        process.modifieddt = datetime.now()
                        process.modifiedby = userid
                        process.save()

                    rubric = Rubric.objects.get(id=assignment.rubricid.id)
                    rubric.maxscalevalue = maxscalevalue
                    rubric.modifieddt = datetime.now()
                    rubric.modifiedby = userid
                    rubric.save()

                    lesson = Lesson()
                    lesson.name = name
                    lesson.lessontype = 25
                    lesson.abilitylevel = 0
                    lesson.goaloftask = goal
                    lesson.createddt = datetime.now()
                    lesson.createdby = userid
                    lesson.modifieddt = datetime.now()
                    lesson.modifiedby = userid
                    lesson.disabled = 0
                    lesson.deleted = 0
                    lesson.clientid = clientid
                    lesson.save()

                    lessonlist = Lesson.objects.latest("id")

                    unitnum = Unitlessonlnk.objects.filter(unitid=unit.id,deleted=0).count()
                    unitlesson = Unitlessonlnk()
                    unitlesson.unitid = unit
                    unitlesson.assignmentid = assignment
                    unitlesson.lessonid = lessonlist
                    unitlesson.createddt = datetime.now()
                    unitlesson.createdby = userid
                    unitlesson.modifieddt = datetime.now()
                    unitlesson.modifiedby = userid
                    unitlesson.deleted = 0
                    unitlesson.order = unitnum + 1
                    unitlesson.save()

                    impactlist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 1)
                    order = 1
                    for r in impactlist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                        
                    qualitylist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 2)
                    order = 1
                    for r in qualitylist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                        
                    contentlist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 3)
                    order = 1
                    for r in contentlist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                        
                    processlist = Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = rubriclist.id, categoryid = 4)
                    order = 1
                    for r in processlist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unit
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = r
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    
                    activity = Lessonactivity()
                    activity.name = name
                    activity.activitytype = 26
                    activity.assignmentid = assignment.id
                    activity.createddt = datetime.now()
                    activity.createdby = userid
                    activity.modifieddt = datetime.now()
                    activity.modifiedby  = userid
                    activity.deleted = 0
                    activity.order = 100
                    activity.clientid = clientid
                    activity.abilitylevel = 0
                    activity.criteriaid = 0
                    activity.save()

                    activitylist = Lessonactivity.objects.latest("id")

                    lessonactivity = Lessonactivitylnk()
                    lessonactivity.lessonid = lessonlist
                    lessonactivity.activityid = activitylist
                    lessonactivity.createddt = datetime.now()
                    lessonactivity.createdby = userid
                    lessonactivity.modifieddt = datetime.now()
                    lessonactivity.modifiedby = userid
                    lessonactivity.deleted = 0
                    lessonactivity.lessonrubriccriterialnkid = 0
                    lessonactivity.save()

                    assignment.goaloftask = goal
                    if maxwords == False or maxwords == '':
                        assignment.maxwords = 0
                    else:
                        assignment.maxwords = maxwords
                    if minwords == False or minwords == '':
                        assignment.minwords = 0
                    else:
                        assignment.minwords = minwords
                    assignment.audience = audience
                    assignment.contextsituation = context
                    if revisions == False or revisions == '':
                        assignment.revisions = 0
                    else:
                        assignment.revisions = revisions  
                    assignment.modifieddt = datetime.now()
                    assignment.modifiedby = userid
                    assignment.save()
                    
                    data_json = { 'status': 'success' }
                else:
                    data_json = { 'status': 'duplicate' }

            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def getRubricCategory(self,request):
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            unitassignment = UnitAssignment.objects.get(id=id)
            impactlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = unitassignment.assignmentid.rubricid.id, categoryid = 1).values("id","criteria"))
            qualitylist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = unitassignment.assignmentid.rubricid.id, categoryid = 2).values("id","criteria"))
            contentlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = unitassignment.assignmentid.rubricid.id, categoryid = 3).values("id","criteria"))
            processlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = unitassignment.assignmentid.rubricid.id, categoryid = 4).values("id","criteria"))

            data_json = {
                    'evd_evidence_performance_name': id,
                    'impactlist': impactlist,
                    'qualitylist': qualitylist,
                    'contentlist': contentlist,
                    'processlist': processlist
                    }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def getEvidence(self,request):
        try:
            id = request.GET.get('id', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            lesson = Unitlessonlnk.objects.get(id=id)
            impactlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = lesson.assignmentid.rubricid.id, categoryid = 1).values("id","criteria"))
            qualitylist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = lesson.assignmentid.rubricid.id, categoryid = 2).values("id","criteria"))
            contentlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = lesson.assignmentid.rubricid.id, categoryid = 3).values("id","criteria"))
            processlist = list(Rubriccriteria.objects.filter(disabled = 0, deleted = 0, rubricid = lesson.assignmentid.rubricid.id, categoryid = 4).values("id","criteria"))

            unitassignment = UnitAssignment.objects.get(unitid=lesson.unitid.id,assignmentid=lesson.assignmentid.id,deleted=0)

            impactselectlist = list(Lessonrubriccriterialnk.objects.filter(deleted = 0, unitid = lesson.unitid.id, lessonid = lesson.lessonid.id).values("criteriaid"))
            qualityselectlist = list(Lessonrubriccriterialnk.objects.filter(deleted = 0, unitid = lesson.unitid.id, lessonid = lesson.lessonid.id).values("criteriaid"))
            contentselectlist = list(Lessonrubriccriterialnk.objects.filter(deleted = 0, unitid = lesson.unitid.id, lessonid = lesson.lessonid.id).values("criteriaid"))
            processselectlist = list(Lessonrubriccriterialnk.objects.filter(deleted = 0, unitid = lesson.unitid.id, lessonid = lesson.lessonid.id).values("criteriaid"))
            
            data_json = {
                    'evd_evidence_id': lesson.id,
                    'evd_evidence_performance_name': unitassignment.id,
                    'evd_evidence_name': lesson.lessonid.name,
                    'evd_evidence_goal': lesson.lessonid.goaloftask,
                    'evd_evidence_deliverables': lesson.lessonid.deliverable,
                    'impactlist': impactlist,
                    'qualitylist': qualitylist,
                    'contentlist': contentlist,
                    'processlist': processlist,
                    'impactselectlist': impactselectlist,
                    'qualityselectlist': qualityselectlist,
                    'contentselectlist': contentselectlist,
                    'processselectlist': processselectlist
                    }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def addEvidence(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            unitid = request.POST.get('unitid', False)
            unitassignmentid = request.POST.get('unitassignmentid', False)
            name = request.POST.get('name', False)
            goal = request.POST.get('goal', False)
            deliverable = request.POST.get('deliverable', False)
            impact_criteria = request.POST.get('impact_criteria', False)
            quality_criteria = request.POST.get('quality_criteria', False)
            content_criteria = request.POST.get('content_criteria', False)
            process_criteria = request.POST.get('process_criteria', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            unitassignment = UnitAssignment.objects.get(id=unitassignmentid)
            try:
                unitlesson = Unitlessonlnk.objects.get(lessonid__name=name,unitid=unitid,assignmentid=unitassignment.assignmentid.id,deleted=0)
            except Unitlessonlnk.DoesNotExist:
                lesson = Lesson()
                lesson.name = name
                lesson.lessontype = 25
                lesson.abilitylevel = 0
                lesson.goaloftask = goal
                lesson.deliverable = deliverable
                lesson.createddt = datetime.now()
                lesson.createdby = userid
                lesson.modifieddt = datetime.now()
                lesson.modifiedby = userid
                lesson.disabled = 0
                lesson.deleted = 0
                lesson.clientid = clientid
                lesson.save()
                lessonlist = Lesson.objects.latest("id")

                unitnum = Unitlessonlnk.objects.filter(unitid=unitid,deleted=0).count()
                unitlesson = Unitlessonlnk()
                unitlesson.unitid = unitassignment.unitid
                unitlesson.assignmentid = unitassignment.assignmentid
                unitlesson.lessonid = lessonlist
                unitlesson.createddt = datetime.now()
                unitlesson.createdby = userid
                unitlesson.modifieddt = datetime.now()
                unitlesson.modifiedby = userid
                unitlesson.deleted = 0
                unitlesson.order = unitnum + 1
                unitlesson.save()

                impactcriterialist = json.JSONDecoder().decode(impact_criteria)
                qualitycriterialist = json.JSONDecoder().decode(quality_criteria)
                contentcriterialist = json.JSONDecoder().decode(content_criteria)
                processcriterialist = json.JSONDecoder().decode(process_criteria)

                order = 1
                for r in impactcriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    lessonrubriccriterialnk = Lessonrubriccriterialnk()
                    lessonrubriccriterialnk.unitid = unitassignment.unitid
                    lessonrubriccriterialnk.lessonid = lessonlist
                    lessonrubriccriterialnk.criteriaid = criteria
                    lessonrubriccriterialnk.createddt = datetime.now()
                    lessonrubriccriterialnk.createdby = userid
                    lessonrubriccriterialnk.modifieddt = datetime.now()
                    lessonrubriccriterialnk.modifiedby = userid
                    lessonrubriccriterialnk.deleted = 0
                    lessonrubriccriterialnk.order = order
                    lessonrubriccriterialnk.clientid = clientid
                    lessonrubriccriterialnk.save()
                    order = order + 1
                    
                order = 1
                for r in qualitycriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    lessonrubriccriterialnk = Lessonrubriccriterialnk()
                    lessonrubriccriterialnk.unitid = unitassignment.unitid
                    lessonrubriccriterialnk.lessonid = lessonlist
                    lessonrubriccriterialnk.criteriaid = criteria
                    lessonrubriccriterialnk.createddt = datetime.now()
                    lessonrubriccriterialnk.createdby = userid
                    lessonrubriccriterialnk.modifieddt = datetime.now()
                    lessonrubriccriterialnk.modifiedby = userid
                    lessonrubriccriterialnk.deleted = 0
                    lessonrubriccriterialnk.order = order
                    lessonrubriccriterialnk.clientid = clientid
                    lessonrubriccriterialnk.save()
                    order = order + 1
                    
                order = 1
                for r in contentcriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    lessonrubriccriterialnk = Lessonrubriccriterialnk()
                    lessonrubriccriterialnk.unitid = unitassignment.unitid
                    lessonrubriccriterialnk.lessonid = lessonlist
                    lessonrubriccriterialnk.criteriaid = criteria
                    lessonrubriccriterialnk.createddt = datetime.now()
                    lessonrubriccriterialnk.createdby = userid
                    lessonrubriccriterialnk.modifieddt = datetime.now()
                    lessonrubriccriterialnk.modifiedby = userid
                    lessonrubriccriterialnk.deleted = 0
                    lessonrubriccriterialnk.order = order
                    lessonrubriccriterialnk.clientid = clientid
                    lessonrubriccriterialnk.save()
                    order = order + 1
                    
                order = 1
                for r in processcriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    lessonrubriccriterialnk = Lessonrubriccriterialnk()
                    lessonrubriccriterialnk.unitid = unitassignment.unitid
                    lessonrubriccriterialnk.lessonid = lessonlist
                    lessonrubriccriterialnk.criteriaid = criteria
                    lessonrubriccriterialnk.createddt = datetime.now()
                    lessonrubriccriterialnk.createdby = userid
                    lessonrubriccriterialnk.modifieddt = datetime.now()
                    lessonrubriccriterialnk.modifiedby = userid
                    lessonrubriccriterialnk.deleted = 0
                    lessonrubriccriterialnk.order = order
                    lessonrubriccriterialnk.clientid = clientid
                    lessonrubriccriterialnk.save()
                    order = order + 1
                
                data_json = { 'status': 'success' }
            else:
                data_json = { 'status': 'duplicate' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def saveEvidence(self,request):
        DATE_FORMAT = "%d-%m-%Y" 
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            unitlessonlnkid = request.POST.get('unitlessonlnkid', False)
            unitassignmentid = request.POST.get('unitassignmentid', False)
            name = request.POST.get('name', False)
            goal = request.POST.get('goal', False)
            deliverable = request.POST.get('deliverable', False)
            impact_criteria = request.POST.get('impact_criteria', False)
            quality_criteria = request.POST.get('quality_criteria', False)
            content_criteria = request.POST.get('content_criteria', False)
            process_criteria = request.POST.get('process_criteria', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                unitlesson = Unitlessonlnk.objects.get(id=unitlessonlnkid)
            except UnitAssignment.DoesNotExist:
                data_json = { 'status': 'error' }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                lessonlist = Lesson.objects.get(id=unitlesson.lessonid.id)

                impactcriterialist = json.JSONDecoder().decode(impact_criteria)
                qualitycriterialist = json.JSONDecoder().decode(quality_criteria)
                contentcriterialist = json.JSONDecoder().decode(content_criteria)
                processcriterialist = json.JSONDecoder().decode(process_criteria)

                Lessonrubriccriterialnk.objects.filter(unitid=unitlesson.unitid.id,lessonid=unitlesson.lessonid.id).update(deleted=1,modifiedby=userid,modifieddt = datetime.now())
                unitassignment = UnitAssignment.objects.get(id=unitassignmentid)
                order = 1
                for r in impactcriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    try:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk.objects.get(unitid=unitlesson.unitid.id,lessonid=unitlesson.lessonid.id,criteriaid=criteria.id)
                    except Lessonrubriccriterialnk.DoesNotExist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unitassignment.unitid
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = criteria
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    else:
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    
                order = 1
                for r in qualitycriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    try:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk.objects.get(unitid=unitlesson.unitid.id,lessonid=unitlesson.lessonid.id,criteriaid=criteria.id)
                    except Lessonrubriccriterialnk.DoesNotExist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unitassignment.unitid
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = criteria
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    else:
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    
                order = 1
                for r in contentcriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    try:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk.objects.get(unitid=unitlesson.unitid.id,lessonid=unitlesson.lessonid.id,criteriaid=criteria.id)
                    except Lessonrubriccriterialnk.DoesNotExist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unitassignment.unitid
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = criteria
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    else:
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    
                order = 1
                for r in processcriterialist:
                    criteria = Rubriccriteria.objects.get(id=int(r['id']))
                    try:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk.objects.get(unitid=unitlesson.unitid.id,lessonid=unitlesson.lessonid.id,criteriaid=criteria.id)
                    except Lessonrubriccriterialnk.DoesNotExist:
                        lessonrubriccriterialnk = Lessonrubriccriterialnk()
                        lessonrubriccriterialnk.unitid = unitassignment.unitid
                        lessonrubriccriterialnk.lessonid = lessonlist
                        lessonrubriccriterialnk.criteriaid = criteria
                        lessonrubriccriterialnk.createddt = datetime.now()
                        lessonrubriccriterialnk.createdby = userid
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.clientid = clientid
                        lessonrubriccriterialnk.save()
                        order = order + 1
                    else:
                        lessonrubriccriterialnk.modifieddt = datetime.now()
                        lessonrubriccriterialnk.modifiedby = userid
                        lessonrubriccriterialnk.deleted = 0
                        lessonrubriccriterialnk.order = order
                        lessonrubriccriterialnk.save()
                        order = order + 1

                lessonlist.name = name
                lessonlist.goaloftask = goal
                lessonlist.deliverable = deliverable
                lessonlist.modifieddt = datetime.now()
                lessonlist.modifiedby = userid
                lessonlist.save()

                activity = []
                lesson = Unitlessonlnk.objects.filter(unitid=unitlesson.unitid.id,deleted=0,lessonid__name__isnull=False,lessonid__goaloftask__isnull=False,lessonid__deliverable__isnull=False).exclude(lessonid__name__exact='').exclude(lessonid__goaloftask__exact='').exclude(lessonid__deliverable__exact='').order_by('order')
                for item in lesson:
                    numberofcriteria = Lessonrubriccriterialnk.objects.filter(unitid=unitlesson.unitid.id,lessonid=item.lessonid.id,deleted=0).count()
                    if(numberofcriteria > 0):
                        lessonactivitylnk = Lessonactivitylnk.objects.filter(lessonid=item.lessonid.id,deleted=0,activityid__deleted=0).order_by('activityid__order')
                        activityname = []
                        activityobj = ''
                        for lessonactivity in lessonactivitylnk:
                            acttype = "manual"
                            if lessonactivity.activityid.activitytype == 27:
                                acttype = "auto"
                            activityname.append({ "id": str(lessonactivity.activityid.id), "name": lessonactivity.activityid.name, "type": acttype})
                            activityobj = simplejson.dumps(activityname)
                        activity.append({ "id": str(item.id), "name": item.lessonid.name, "goaloftask": item.lessonid.goaloftask, "activity": activityobj})
                activitylist = simplejson.dumps(activity)
                
                data_json = { 'status': 'success', 
                              'activity': activitylist }
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
