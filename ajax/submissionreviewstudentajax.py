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

class SUBMISSIONCREATE():
    def getSubmissionVersion(self,request):
        try:
            userid = request.session['userid']
            submissionid = request.GET.get('submissionid', False)
            versionid = request.GET.get('versionid', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            DATE_FORMAT = "%d-%m-%Y" 
            data_json = ''
            if versionid != False and versionid != '':
                submissionversion = Submissionversion.objects.get(id=versionid)
                currentversion = ''
                if submissionversion.version == submissionversion.submissionid.getLatestVersion():
                    currentversion = 'y'
                else:
                    currentversion = 'n'
                data_json = {
                        'submissionversionid': submissionversion.id,
                        'submissionversionversion': submissionversion.version,
                        'assignmentname': submissionversion.submissionid.assignmentid.name,
                        'assignmentdesc': submissionversion.submissionid.assignmentid.description,
                        'assignmentmaxword': submissionversion.submissionid.assignmentid.maxwords,
                        'assignmentrubric': submissionversion.submissionid.assignmentid.rubricid.name,
                        'submissionduedate': submissionversion.submissionid.duedate.strftime(DATE_FORMAT),
                        'submissionprogress': submissionversion.submissionid.progress,
                        'submissioncomment': submissionversion.submissionid.comment,
                        'submissionversionstage': submissionversion.stage,
                        'submissionversionessay': submissionversion.essay,
                        'submissionversionessaytextarea': submissionversion.essay,
                        'submissionversioncomment': submissionversion.comment,
                        'currentversion': currentversion,
                        'submissionstudentstatus': submissionversion.studentstatus,
                        'submissionteacherstatus': submissionversion.teacherstatus,
                        }
            elif submissionid != False and submissionid != '':
                submission = Submission.objects.get(id=submissionid)
                try:
                    submissionversion = Submissionversion.objects.get(submissionid=submission.id,version=submission.getLatestVersion)
                except Submissionversion.DoesNotExist:
                    data_json = { }
                    data = simplejson.dumps(data_json)
                    return HttpResponse(data, mimetype='application/json')
                else:
                    if submissionversion.version == submissionversion.submissionid.getLatestVersion():
                        currentversion = 'y'
                    else:
                        currentversion = 'n'
                    data_json = {
                            'submissionversionid': submissionversion.id,
                            'submissionversionversion': submissionversion.version,
                            'assignmentname': submissionversion.submissionid.assignmentid.name,
                            'assignmentdesc': submissionversion.submissionid.assignmentid.description,
                            'assignmentmaxword': submissionversion.submissionid.assignmentid.maxwords,
                            'assignmentrubric': submissionversion.submissionid.assignmentid.rubricid.name,
                            'submissionduedate': submissionversion.submissionid.duedate.strftime(DATE_FORMAT),
                            'submissionprogress': submissionversion.submissionid.progress,
                            'submissioncomment': submissionversion.submissionid.comment,
                            'submissionversionstage': submissionversion.stage,
                            'submissionversionessay': submissionversion.essay,
                            'submissionversionessaytextarea': submissionversion.essay,
                            'submissionversioncomment': submissionversion.comment,
                            'currentversion': currentversion,
                            'submissionstudentstatus': submissionversion.studentstatus,
                            'submissionteacherstatus': submissionversion.teacherstatus,
                            }
            else:
                data_json = {
                            'status': 'no key passed',
                            }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')

            
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def getSubmissionVersionHighlightList(self,request):
        try:
            userid = request.session['userid']
            versionid = request.GET.get('versionid', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data_json = ''
            submissionversionhighlightlist = list(Submissionversionhighlight.objects.filter(submissionversionid = versionid,deleted=0).values('id','hightlighttext'))
            data = simplejson.dumps(submissionversionhighlightlist)
            return HttpResponse(data, mimetype='application/json')

    def getSubmissionVersionHighlight(self,request):
        try:
            userid = request.session['userid']
            highlightid = request.GET.get('highlightid', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data_json = ''
            if highlightid != False and highlightid != '':
                submissionversionhighlight = Submissionversionhighlight.objects.get(id=highlightid,deleted=0)
                data_json = {
                        'highlightComment': submissionversionhighlight.comment,
                        }
            else:
                data_json = {
                            'status': 'no key passed',
                            }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')

            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def getSubmissionVersionHighlightTags(self,request):
        try:
            userid = request.session['userid']
            highlightid = request.GET.get('highlightid', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data_json = []
            if highlightid != False and highlightid != '':
                taglinklist = Taglink.objects.filter(recid=highlightid,entityid=5,deleted=0)
                for row in taglinklist:
                    data_json.append({ "id": str(row.tagid.id), "name": row.tagid.name })
                
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                data_json = {
                            'status': 'no key passed',
                            }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')

    def delete(self,request):
        try:
            userid = request.session['userid']
            highlightid = request.POST.get('highlightid', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionhl = Submissionversionhighlight.objects.get(id=highlightid)
            submissionhl.deleted = 1
            submissionhl.modifiedby = userid
            submissionhl.modifieddt = datetime.now()
            submissionhl.save()

            Taglink.objects.filter(recid=highlightid,entityid=5,deleted=0).update(deleted=1,modifiedby=userid,modifieddt = datetime.now())
            
            data_json = {
                        'status': 'success',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def submit(self,request):
        try:
            userid = request.session['userid']
            submissionid = request.POST.get('submissionid', False)
            essay = request.POST.get('essay', False)
            submissionversionid = request.POST.get('submissionversionid', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            if submissionversionid == "":
                submissionlist = Submission.objects.get(id=submissionid)
                submissionvs = Submissionversion()
                submissionvs.submissionid =submissionlist
                #version have change none complete
                submissionvs.version = 1
                submissionvs.essay = essay
                submissionvs.studentstatus = 1
                submissionvs.teacherstatus = 0
                submissionvs.stage = 0
                submissionvs.createddt = datetime.now()
                submissionvs.createdby = userid
                submissionvs.modifieddt = datetime.now()
                submissionvs.modifiedby = userid
                submissionvs.disabled = 0
                submissionvs.deleted = 0
                submissionvs.save()
                
                recid = Submissionversion.objects.latest('id').id

                data_json = { 'submissionversionid': recid,
                             'status': 'success'}
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                submissionlist = Submission.objects.get(id=submissionid)
                submissionvs = Submissionversion.objects.get(id=submissionversionid)
                submissionvs.submissionid =submissionlist
                #version have change none complete
                submissionvs.version = 1
                submissionvs.essay = essay
                submissionvs.studentstatus = 1
                submissionvs.teacherstatus = 0
                submissionvs.stage = 0
                submissionvs.modifieddt = datetime.now()
                submissionvs.modifiedby = userid
                submissionvs.disabled = 0
                submissionvs.deleted = 0
                submissionvs.save()

                data_json = {'status': 'success'}
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
        
    def save(self,request):
        try:
            userid = request.session['userid']
            submissionid = request.POST.get('submissionid', False)
            essay = request.POST.get('essay', False)
            submissionversionid = request.POST.get('submissionversionid', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            if submissionversionid == "":
                submissionlist = Submission.objects.get(id=submissionid)
                submissionvs = Submissionversion()
                submissionvs.submissionid =submissionlist
                #version have change none complete
                submissionvs.version = 1
                submissionvs.essay = essay
                submissionvs.studentstatus = 0
                submissionvs.teacherstatus = 0
                submissionvs.stage = 0
                submissionvs.createddt = datetime.now()
                submissionvs.createdby = userid
                submissionvs.modifieddt = datetime.now()
                submissionvs.modifiedby = userid
                submissionvs.disabled = 0
                submissionvs.deleted = 0
                submissionvs.save()
                
                recid = Submissionversion.objects.latest('id').id

                data_json = { 'submissionversionid': recid,
                             'status': 'success'}
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                submissionlist = Submission.objects.get(id=submissionid)
                submissionvs = Submissionversion.objects.get(id=submissionversionid)
                submissionvs.submissionid =submissionlist
                #version have change none complete
                submissionvs.version = 1
                submissionvs.essay = essay
                submissionvs.studentstatus = 0
                submissionvs.teacherstatus = 0
                submissionvs.stage = 0
                submissionvs.modifieddt = datetime.now()
                submissionvs.modifiedby = userid
                submissionvs.disabled = 0
                submissionvs.deleted = 0
                submissionvs.save()

                data_json = {'status': 'success'}
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')

    def addSubmissionversionHighlight(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionversionid = request.POST.get('submissionversionid', False)
            startposition = request.POST.get('start', False)
            hightlighttext = request.POST.get('highlighttext', False)
            comment = request.POST.get('highlightComment', False)
            tagids = request.POST.getlist('tagids[]', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:

#             data=simplejson.dumps(tagids)
#             return HttpResponse(data, mimetype='application/json')
            submissionvshg = Submissionversionhighlight()
            submissionvshg.submissionversionid = submissionversionid
            submissionvshg.startposition = startposition
            submissionvshg.hightlighttext = hightlighttext
            submissionvshg.comment = comment
            submissionvshg.weight = 0
            submissionvshg.createddt = datetime.now()
            submissionvshg.createdby = userid
            submissionvshg.modifieddt = datetime.now()
            submissionvshg.modifiedby = userid
            submissionvshg.disabled = 0
            submissionvshg.deleted = 0
            submissionvshg.save()
            recid = Submissionversionhighlight.objects.latest('id').id
            
            for tagid in tagids:
                taglist = Tag.objects.get(id=tagid)
                entitylist = Entity.objects.get(id=5)
                taglink = Taglink()
                taglink.tagid = taglist
                taglink.entityid = entitylist
                taglink.recid = recid
                taglink.createddt = datetime.now()
                taglink.createdby = userid
                taglink.modifieddt = datetime.now()
                taglink.modifiedby = userid
                taglink.deleted = 0
                taglink.clientid = clientid
                taglink.save()
                
            data_json = { 'recid': recid, }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def saveSubmissionversionHighlight(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            highlightid = request.POST.get('highlightid', False)
            submissionversionid = request.POST.get('submissionversionid', False)
            comment = request.POST.get('highlightComment', False)
            tagids = request.POST.getlist('tagids[]', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionvshg = Submissionversionhighlight.objects.get(id=highlightid)
            submissionvshg.submissionversionid = submissionversionid
            submissionvshg.comment = comment
            submissionvshg.modifieddt = datetime.now()
            submissionvshg.modifiedby = userid
            submissionvshg.save()
            
            Taglink.objects.filter(recid=highlightid,entityid=5,deleted=0).update(deleted=1,modifiedby=userid,modifieddt = datetime.now())
            
            for tagid in tagids:
                try:
                    taglist = Tag.objects.get(id=tagid)
                    entitylist = Entity.objects.get(id=5)
                    taglink = Taglink.objects.get(recid=highlightid,entityid=5,tagid=tagid)
                except Taglink.DoesNotExist:
                    taglink = Taglink()
                    taglink.tagid = taglist
                    taglink.entityid = entitylist
                    taglink.recid = highlightid
                    taglink.createddt = datetime.now()
                    taglink.createdby = userid
                    taglink.modifieddt = datetime.now()
                    taglink.modifiedby = userid
                    taglink.deleted = 0
                    taglink.clientid = clientid
                    taglink.save()
                else:
                    taglink.tagid = taglist
                    taglink.entityid = entitylist
                    taglink.recid = highlightid
                    taglink.modifieddt = datetime.now()
                    taglink.modifiedby = userid
                    taglink.deleted = 0
                    taglink.clientid = clientid
                    taglink.save()
                 
            data_json = { 'recid': highlightid, }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def tagHighlightList(self,request):
        try:
            cursor = connection.cursor()
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionversionid = request.GET.get('submissionversionid', False)
            
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            cursor.execute("select t.id,t.name,t.parentid,count(t.id) as number from submissionversionhighlight as smh join taglink as tl on tl.recid = smh.id and tl.entityid=5 and tl.deleted = 0 and tl.clientid= %s join tag as t on t.id = tl.tagid and t.disabled=0 and t.deleted = 0 and t.clientid= %s where smh.submissionversionid = %s and smh.disabled=0 and smh.deleted=0 group by t.id", [clientid,clientid,submissionversionid])
            taglist = cursor.fetchall() 
            data = simplejson.dumps(taglist)
            return HttpResponse(data, mimetype='application/json')

    def tagClickHighlightList(self,request):
        try:
            cursor = connection.cursor()
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            taglinkid = request.GET.get('taglinkid', False)
            submissionversionid = request.GET.get('submissionversionid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            #cursor.execute("select t.id,t.name,t.parentid,count(t.id) as number from submissionversionhighlight as smh join taglink as tl on tl.recid = smh.id and tl.entityid=5 and tl.deleted = 0 and tl.clientid= %s join tag as t on t.id = tl.tagid and t.disabled=0 and t.deleted = 0 and t.clientid= %s where smh.submissionversionid = %s and smh.disabled=0 and smh.deleted=0 group by t.id", [clientid,clientid,submissionversionid])
            cursor.execute("select smh.id, smh.comment, t.tagcolor from taglink as tl  join submissionversionhighlight as smh on smh.id = tl.recid and smh.disabled=0 and smh.deleted=0 join tag as t on tl.tagid = t.id where tl.tagid = %s and tl.entityid=5 and tl.deleted=0 and tl.clientid=%s and smh.submissionversionid = %s", [taglinkid,clientid,submissionversionid])
            submissionvshglist = cursor.fetchall()
#             taglinklist = Taglink.objects.filter(tagid=taglinkid,entityid=5,deleted=0,clientid=clientid).values_list('recid')
#         except KeyError:
#             data_json = { 'status': 'error', }
#             data = simplejson.dumps(data_json)
#             return HttpResponse(data, mimetype='application/json')
#         else:
#             submissionvshglist= list(Submissionversionhighlight.objects.filter(submissionversionid=submissionversionid,id__in=taglinklist,disabled=0,deleted=0).values('id','comment'))
            data = simplejson.dumps(submissionvshglist)
            return HttpResponse(data, mimetype='application/json')
    
    def getSelectStage(self,request):
        try:
            selectionlist = list(Selectionlist.objects.filter(selectiongroupid=4, disabled=0, deleted=0).values('selectionname', 'selectionvalue'))
        except Selectionlist.DoesNotExist:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data = simplejson.dumps(selectionlist)
            return HttpResponse(data, mimetype='application/json')
        
    def getSelectSuggest(self,request):
        try:
            tagids = request.POST.getlist('tagids[]', False)  
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data_json = []
            tagentity = TagEntity.objects.filter(entityid=5,tagid__id__in=tagids)
            for row in tagentity:
                if row.tagid.parentid != 0:
                    tagentitysibling = TagEntity.objects.filter(Q(entityid=5),~Q(tagid__id__in=tagids),Q(tagid__parentid=row.tagid.parentid))
                    for rowsibling in tagentitysibling:
                        if { "id": str(rowsibling.tagid.id), "label": rowsibling.tagid.name, "value": rowsibling.tagid.name } not in data_json:
                            data_json.append({ "id": str(rowsibling.tagid.id), "label": rowsibling.tagid.name, "value": rowsibling.tagid.name })
                tagentitychild = TagEntity.objects.filter(Q(entityid=5), ~Q(tagid__id__in=tagids), Q(tagid__parentid=row.tagid.id))
                for rowchild in tagentitychild:
                    if { "id": str(rowchild.tagid.id), "label": rowchild.tagid.name, "value": rowchild.tagid.name } not in data_json:
                        data_json.append({ "id": str(rowchild.tagid.id), "label": rowchild.tagid.name, "value": rowchild.tagid.name })
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def getSubmitRubric(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionid = request.GET.get('submissionid', False)
            submission = Submission.objects.get(id=submissionid)
            
            rubric = submission.assignmentid.rubricid
            rubricid = rubric.id
            rubriccriterialist = list(Rubriccriteria.objects.filter(rubricid=rubricid,disabled=0,deleted=0,clientid=clientid).values('id','rubricid', 'criteria'))
        except Submission.DoesNotExist:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data = simplejson.dumps(rubriccriterialist)
            return HttpResponse(data, mimetype='application/json')
        
    def getSelectRubricCriteria(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            rubricid = request.GET.get('rubricid', False)
            rubricscalelist = list(Rubricscale.objects.filter(rubricid=rubricid,disabled=0,deleted=0,clientid=clientid).values('id','scale'))
        except Rubricscale.DoesNotExist:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data = simplejson.dumps(rubricscalelist)
            return HttpResponse(data, mimetype='application/json')