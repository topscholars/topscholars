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

class SUBMISSIONREVIEW():
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
                        'submissionversioncomment': submissionversion.comment,
                        }
            elif submissionid != False and submissionid != '':
                submission = Submission.objects.get(id=submissionid)
                submissionversion = Submissionversion.objects.get(submissionid=submission.id,version=submission.getLatestVersion)
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
                        'submissionversioncomment': submissionversion.comment,
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
            submissionversionid = request.POST.get('submissionversionid', False)
            stage = request.POST.get('stage', False)
            progress = request.POST.get('progress', False)
            comment = request.POST.get('comment', False)
            criteriaid = request.POST.getlist('criteriaid[]', False)
            criteriaval = request.POST.getlist('criteriaval[]', False)
            criteriaval[0]
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionvs = Submissionversion.objects.get(id=submissionversionid)
            
            submissionid = submissionvs.submissionid.id
            submission = Submission.objects.get(id=submissionid)
            submission.progress = progress
            submission.save()
            
            submissionvs.teacherstatus = 1
            submissionvs.stage = stage
            submissionvs.comment = comment
            submissionvs.modifiedby = userid
            submissionvs.modifieddt = datetime.now()
            submissionvs.save()


            i=0
            for criteria in criteriaid:
                entity = Entity.objects.get(id=5)
                rubricklink = Rubriclink()
                rubricklink.entityid = entity
                rubricklink.recid = submissionversionid
                rubricklink.rubiccriteriaid = criteria
                rubricklink.rubricscaleid = criteriaval[i]
                rubricklink.save()
                i += 1

            data_json = {
                        'status': criteriaval[0],
                        }
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
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionversionid = request.GET.get('submissionversionid', False)
            submissionvshgid = Submissionversionhighlight.objects.filter(submissionversionid=submissionversionid,disabled=0,deleted=0).values_list('id')
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            taglinklist = Taglink.objects.filter(recid__in=submissionvshgid,entityid=5,deleted=0,clientid=clientid).values_list('tagid')
            taglist = list(Tag.objects.filter(id__in=taglinklist,disabled=0,deleted=0,clientid=clientid).values('id','name','parentid'))
            data = simplejson.dumps(taglist)
            return HttpResponse(data, mimetype='application/json')

    def tagClickHighlightList(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            taglinkid = request.GET.get('taglinkid', False)
            submissionversionid = request.GET.get('submissionversionid', False)
            taglinklist = Taglink.objects.filter(tagid=taglinkid,entityid=5,deleted=0,clientid=clientid).values_list('recid')
            
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionvshglist= list(Submissionversionhighlight.objects.filter(submissionversionid=submissionversionid,id__in=taglinklist,disabled=0,deleted=0).values('id','comment'))
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