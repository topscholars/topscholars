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
    def getSubmissionReviewer(self,request):
        try:
            userid = request.session['userid']
            submissionreviewerid = request.GET.get('submissionreviewerid', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionreviewer = Submissionreviewer.objects.get(id = submissionreviewerid)
            data_json = ''
            data_json = {
                'essay' : submissionreviewer.essay,
                'status' : submissionreviewer.status
                }
            data = simplejson.dumps(data_json)
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
                submissionversionhighlight = Textcomment.objects.get(id=highlightid,deleted=0)
                categorylink = Categorylink.objects.get(entityid=14,recid=highlightid)
                data_json = {
                        'highlightComment': submissionversionhighlight.comment,
                        'highlightCategory': categorylink.categoryid.id
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
                taglinklist = Taglink.objects.filter(recid=highlightid,entityid=14,deleted=0)
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
            submissionreviewerid = request.POST.get('submissionreviewerid', False)
            essay = request.POST.get('essay', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionhl = Textcomment.objects.get(id=highlightid)
            submissionhl.deleted = 1
            submissionhl.modifiedby = userid
            submissionhl.modifieddt = datetime.now()
            submissionhl.save()

            Taglink.objects.filter(recid=highlightid,entityid=14,deleted=0).update(deleted=1,modifiedby=userid,modifieddt = datetime.now())

            submissionreviewer = Submissionreviewer.objects.get(id=submissionreviewerid)
            submissionreviewer.essay = essay;
            submissionreviewer.modifieddt = datetime.now()
            submissionreviewer.modifiedby = userid
            submissionreviewer.save()
            
            data_json = {
                        'status': 'success',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

##    def submit(self,request):
##        try:
##            userid = request.session['userid']
##            submissionversionid = request.POST.get('submissionversionid', False)
##            stage = request.POST.get('stage', False)
##            progress = request.POST.get('progress', False)
##            comment = request.POST.get('comment', False)
##            criteriaid = request.POST.getlist('criteriaid[]', False)
##            criteriaval = request.POST.getlist('criteriaval[]', False)
##            criteriaval[0]
##        except KeyError:
##            data_json = {
##                        'status': 'user not logged in',
##                        }
##            data = simplejson.dumps(data_json)
##            return HttpResponse(data, mimetype='application/json')
##        else:
##            submissionvs = Submissionversion.objects.get(id=submissionversionid)
##            
##            submissionid = submissionvs.submissionid.id
##            submission = Submission.objects.get(id=submissionid)
##            submission.progress = progress
##            submission.save()
##            
##            submissionvs.teacherstatus = 1
##            submissionvs.stage = stage
##            submissionvs.comment = comment
##            submissionvs.modifiedby = userid
##            submissionvs.modifieddt = datetime.now()
##            submissionvs.save()
##
##
##            i=0
##            for criteria in criteriaid:
##                entity = Entity.objects.get(id=5)
##                criteriaid = Rubriccriteria.objects.get(id=criteria)
##                scaleid = Rubricscale.objects.get(id=criteriaval[i])
##                rubricklink = Rubriclink()
##                rubricklink.entityid = entity
##                rubricklink.recid = submissionversionid
##                rubricklink.rubiccriteriaid = criteriaid
##                rubricklink.rubricscaleid = scaleid
##                rubricklink.save()
##                i += 1
##
##            data_json = {
##                        'status': criteriaval[0],
##                        }
##            data = simplejson.dumps(data_json)
##            return HttpResponse(data, mimetype='application/json')

    def addSubmissionversionHighlight(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionreviewerid = request.POST.get('submissionreviewerid', False)
            comment = request.POST.get('highlightComment', False)
            tagids = request.POST.getlist('tagids[]', False)
            categoryid = request.POST.get('categoryid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            entitylist = Entity.objects.get(id=15)
            submissionvshg = Textcomment()
            submissionvshg.entityid = entitylist
            submissionvshg.recid = submissionreviewerid
            submissionvshg.comment = comment
            submissionvshg.weight = 0
            submissionvshg.createddt = datetime.now()
            submissionvshg.createdby = userid
            submissionvshg.modifieddt = datetime.now()
            submissionvshg.modifiedby = userid
            submissionvshg.disabled = 0
            submissionvshg.deleted = 0
            submissionvshg.save()
            recid = Textcomment.objects.latest('id').id

            entitylist = Entity.objects.get(id=14)
            for tagid in tagids:
                taglist = Tag.objects.get(id=tagid)
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

            if categoryid != False and categoryid != '':
                category = Category.objects.get(id=categoryid)
                categorylink = Categorylink()
                categorylink.entityid = entitylist
                categorylink.recid = recid
                categorylink.totalweight = 0
                categorylink.categoryid = category
                categorylink.createddt = datetime.now()
                categorylink.createdby = userid
                categorylink.modifieddt = datetime.now()
                categorylink.modifiedby = userid
                categorylink.deleted = 0
                categorylink.clientid = clientid
                categorylink.save()
            
            data_json = { 'recid': recid, }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def saveSubmissionversionHighlight(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            highlightid = request.POST.get('highlightid', False)
            comment = request.POST.get('highlightComment', False)
            tagids = request.POST.getlist('tagids[]', False)
            categoryid = request.POST.get('categoryid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionvshg = Textcomment.objects.get(id=highlightid)
            submissionvshg.comment = comment
            submissionvshg.modifieddt = datetime.now()
            submissionvshg.modifiedby = userid
            submissionvshg.save()
            
            Taglink.objects.filter(recid=highlightid,entityid=14,deleted=0).update(deleted=1,modifiedby=userid,modifieddt = datetime.now())

            entitylist = Entity.objects.get(id=14)
            for tagid in tagids:
                try:
                    taglist = Tag.objects.get(id=tagid)
                    taglink = Taglink.objects.get(recid=highlightid,entityid=14,tagid=tagid)
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
                    
            if categoryid == False or categoryid == '':
                categoryid = 0
            else:
                category = Category.objects.get(id=categoryid)
                
            try:
                categorylink = Categorylink.objects.get(recid=highlightid,entityid=14)
            except Categorylink.DoesNotExist:
                if categoryid != 0:
                    categorylink = Categorylink()
                    categorylink.entityid = entitylist
                    categorylink.recid = highlightid
                    categorylink.totalweight = 0
                    categorylink.categoryid = category
                    categorylink.createddt = datetime.now()
                    categorylink.createdby = userid
                    categorylink.modifieddt = datetime.now()
                    categorylink.modifiedby = userid
                    categorylink.deleted = 0
                    categorylink.clientid = clientid
                    categorylink.save()
            else:
                if categoryid != 0:
                    categorylink.categoryid = category
                    categorylink.modifieddt = datetime.now()
                    categorylink.modifiedby = userid
                    categorylink.deleted = 0
                    categorylink.save()
                else:
                    categorylink.deleted = 1
                    categorylink.save()
                 
            data_json = { 'recid': highlightid, }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def updateReviewerEssay(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionreviewerid = request.POST.get('submissionreviewerid', False)
            essay = request.POST.get('essay', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionreviewer = Submissionreviewer.objects.get(id=submissionreviewerid)
            submissionreviewer.essay = essay;
            submissionreviewer.modifieddt = datetime.now()
            submissionreviewer.modifiedby = userid
            submissionreviewer.save()

        data_json = { 'recid': submissionreviewerid, }
        data = simplejson.dumps(data_json)
        return HttpResponse(data, mimetype='application/json')

    def tagHighlightList(self,request):
        try:
            cursor = connection.cursor()
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionreviewerid = request.GET.get('submissionreviewerid', False)
            
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            cursor.execute("select t.id,t.name,t.parentid,count(t.id) as number from textcomment as smh join taglink as tl on tl.recid = smh.id and tl.entityid=14 and tl.deleted = 0 and tl.clientid= %s join tag as t on t.id = tl.tagid and t.disabled=0 and t.deleted = 0 and t.clientid= %s where smh.entityid = 15 and smh.recid = %s and smh.disabled=0 and smh.deleted=0 group by t.id", [clientid,clientid,submissionreviewerid])
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
            submissionreviewerid = request.GET.get('submissionreviewerid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            cursor.execute("select smh.id, smh.comment, t.tagcolor from taglink as tl  join textcomment as smh on smh.id = tl.recid and smh.disabled=0 and smh.deleted=0 join tag as t on tl.tagid = t.id where tl.tagid = %s and tl.entityid=14 and tl.deleted=0 and tl.clientid=%s and smh.recid = %s", [taglinkid,clientid,submissionreviewerid])
            submissionvshglist = cursor.fetchall()
            data = simplejson.dumps(submissionvshglist)
            return HttpResponse(data, mimetype='application/json')
    
    def tagCategoryHighlightList(self,request):
        try:
            cursor = connection.cursor()
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            categoryid = request.GET.get('categoryid', False)
            submissionreviewerid = request.GET.get('submissionreviewerid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            cursor.execute("select smh.id, smh.comment, t.tagcolor from taglink as tl  join textcomment as smh on smh.id = tl.recid and smh.disabled=0 and smh.deleted=0 join tag as t on tl.tagid = t.id where tl.entityid=14 and tl.deleted=0 and tl.clientid=%s and smh.recid = %s and smh.id in (select recid from categorylink where categoryid = %s and entityid = 14)", [clientid,submissionreviewerid,categoryid])
            submissionvshglist = cursor.fetchall()
            data = simplejson.dumps(submissionvshglist)
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

##    def getSubmitRubric(self,request):
##        try:
##            userid = request.session['userid']
##            login = Login.objects.get(id=userid)
##            clientid = login.clientid
##            submissionid = request.GET.get('submissionid', False)
##            submission = Submission.objects.get(id=submissionid)
##            
##            rubric = submission.assignmentid.rubricid
##            rubricid = rubric.id
##            rubriccriterialist = list(Rubriccriteria.objects.filter(rubricid=rubricid,disabled=0,deleted=0,clientid=clientid).values('id','rubricid', 'criteria'))
##        except Submission.DoesNotExist:
##            data_json = { 'status': 'error', }
##            data = simplejson.dumps(data_json)
##            return HttpResponse(data, mimetype='application/json')
##        else:
##            data = simplejson.dumps(rubriccriterialist)
##            return HttpResponse(data, mimetype='application/json')
##        
##    def getSelectRubricCriteria(self,request):
##        try:
##            userid = request.session['userid']
##            login = Login.objects.get(id=userid)
##            clientid = login.clientid
##            rubricid = request.GET.get('rubricid', False)
##            rubricscalelist = list(Rubricscale.objects.filter(rubricid=rubricid,disabled=0,deleted=0,clientid=clientid).values('id','scale'))
##        except Rubricscale.DoesNotExist:
##            data_json = { 'status': 'error', }
##            data = simplejson.dumps(data_json)
##            return HttpResponse(data, mimetype='application/json')
##        else:
##            data = simplejson.dumps(rubricscalelist)
##            return HttpResponse(data, mimetype='application/json')
            
