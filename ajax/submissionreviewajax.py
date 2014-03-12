from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson
from django.core import serializers
from django.db.models.query import RawQuerySet
from django.db import connection
from tsweb.models import *
from django.db.models import Q
from itertools import chain

from datetime import datetime, timedelta
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

            entity = Entity.objects.get(id=15)
            categorylist = Category.objects.get(name='Impact')
            Impact = 0
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionreviewerid)
            except Categoryweight.DoesNotExist:
                Impact = 0
            else:
                Impact = categoryweight.actualweight

            categorylist = Category.objects.get(name='Content')
            Content = 0
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionreviewerid)
            except Categoryweight.DoesNotExist:
                Content = 0
            else:
                Content = categoryweight.actualweight

            categorylist = Category.objects.get(name='Quality')
            Quality = 0
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionreviewerid)
            except Categoryweight.DoesNotExist:
                Quality = 0
            else:
                Quality = categoryweight.actualweight

            categorylist = Category.objects.get(name='Process')
            Process = 0
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionreviewerid)
            except Categoryweight.DoesNotExist:
                Process = 0
            else:
                Process = categoryweight.actualweight
                
            data_json = ''
            data_json = {
                'essay' : submissionreviewer.essay,
                'status' : submissionreviewer.status,
                'Impact': Impact,
                'Content': Content,
                'Quality': Quality,
                'Process': Process
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
                categoryid = ''
                try:
                    categorylink = Categorylink.objects.get(entityid=14,recid=highlightid)
                except Categorylink.DoesNotExist:
                    categoryid = ''
                else:
                    categoryid = categorylink.categoryid.id
                    
                data_json = {
                        'highlightComment': submissionversionhighlight.comment,
                        'highlightCategory': categoryid
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

    def stpsave(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionrvid = request.POST.get('submissionreviewerid', False)
            impact = request.POST.get('impact', False)
            quality = request.POST.get('quality', False)
            content = request.POST.get('content', False)
            process = request.POST.get('process', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            entity = Entity.objects.get(id=15)
            categorylist = Category.objects.get(name='Impact')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if impact != False and impact != '':
                    categoryweight.actualweight = impact
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if impact != False and impact != '':
                    categoryweight.actualweight = impact
                else:
                    categoryweight.actualweight = 0
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            
            
            categorylist = Category.objects.get(name='Content')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if content != False and content != '':
                    categoryweight.actualweight = content
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if content != False and content != '':
                    categoryweight.actualweight = content
                else:
                    categoryweight.actualweight = 0
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            

            categorylist = Category.objects.get(name='Quality')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if quality != False and quality != '':
                    categoryweight.actualweight = quality
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if quality != False and quality != '':
                    categoryweight.actualweight = quality
                else:
                    categoryweight.actualweight = 0
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()

            categorylist = Category.objects.get(name='Process')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if process != False and process != '':
                    categoryweight.actualweight = process
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if process != False and process != '':
                    categoryweight.actualweight = process
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
                
            data_json = {
                        'status': '1',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def submit(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionreviewerid = request.POST.get('submissionreviewerid', False)
##            stage = request.POST.get('stage', False)
##            progress = request.POST.get('progress', False)
##            comment = request.POST.get('comment', False)
            impact = request.POST.get('impact', False)
            quality = request.POST.get('quality', False)
            content = request.POST.get('content', False)
            process = request.POST.get('process', False)
##            criteriaid = request.POST.getlist('criteriaid[]', False)
##            criteriaval = request.POST.getlist('criteriaval[]', False)
##            criteriaval[0]
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionrv = Submissionreviewer.objects.get(id=submissionreviewerid)
            maxrevision = submissionrv.submissionversionid.submissionid.assignmentid.revisions
            progress = 0
            if maxrevision != 0:
                dprogress = submissionrv.submissionversionid.version / maxrevision * 100
                progress = int(dprogress)
            submissionrv.status = 1
##            submissionrv.comment = comment
            submissionrv.modifiedby = userid
            submissionrv.modifieddt = datetime.now()
            submissionrv.save()
            
            submissionrvid = Submissionreviewer.objects.latest("id").id
            #category weight
            
            entity = Entity.objects.get(id=15)
            categorylist = Category.objects.get(name='Impact')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if impact != False and impact != '':
                    categoryweight.actualweight = impact
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if impact != False and impact != '':
                    categoryweight.actualweight = impact
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            
            
            categorylist = Category.objects.get(name='Content')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if content != False and content != '':
                    categoryweight.actualweight = content
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if content != False and content != '':
                    categoryweight.actualweight = content
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            

            categorylist = Category.objects.get(name='Quality')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if quality != False and quality != '':
                    categoryweight.actualweight = quality
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if quality != False and quality != '':
                    categoryweight.actualweight = quality
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            
            categorylist = Category.objects.get(name='Process')
            try:
                categoryweight = Categoryweight.objects.get(entityid=entity, categoryid=categorylist, recid=submissionrvid)
            except Categoryweight.DoesNotExist:
                categoryweight = Categoryweight()
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if process != False and process != '':
                    categoryweight.actualweight = process
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            else:
                categoryweight.entityid = entity
                categoryweight.recid = submissionrvid
                categoryweight.categoryid = categorylist
                if process != False and process != '':
                    categoryweight.actualweight = process
                else:
                    categoryweight.actualweight = 0
                categoryweight.createddt = datetime.now()
                categoryweight.createdby = userid
                categoryweight.modifieddt = datetime.now()
                categoryweight.modifiedby = userid
                categoryweight.deleted = 0
                categoryweight.clientid = clientid
                categoryweight.save()
            
            submissionvs = Submissionversion.objects.get(id=submissionrv.submissionversionid.id)
            submissionvs.teacherstatus = 1
            submissionvs.stage = 0
##            submissionvs.comment = comment
            submissionvs.modifiedby = userid
            submissionvs.modifieddt = datetime.now()
            submissionvs.save()
            
            submission = Submission.objects.get(id=submissionvs.submissionid.id)
            submission.progress = progress
            submission.save()

            submission = Submission.objects.get(id=submissionvs.submissionid.id)

##            if submission.progress < 100:
            newversion = Submissionversion()
            newversion.submissionid = submission
            newversion.version = submissionvs.version + 1
            newversion.essay = submissionrv.essay
            newversion.studentstatus = 0
            newversion.teacherstatus = 0
            newversion.stage = 0
            newversion.createddt = datetime.now()
            newversion.createdby = userid
            newversion.modifieddt = datetime.now()
            newversion.modifiedby = userid
            newversion.disabled = 0
            newversion.deleted = 0
            newversion.save()

            essay = submissionrv.essay
            newid = Submissionversion.objects.latest("id")

            textcommentlist = Textcomment.objects.filter(entityid=15,recid=submissionreviewerid,deleted=0,disabled=0)
            entity = Entity.objects.get(id=16)
            for row in textcommentlist:
                newtextcomment = Textcomment()
                newtextcomment.entityid = entity
                newtextcomment.recid = newid.id
                newtextcomment.comment = row.comment
                newtextcomment.weight = row.weight
                newtextcomment.createddt = row.createddt
                newtextcomment.createdbyentity = row.createdbyentity
                newtextcomment.createdby = row.createdby
                newtextcomment.modifieddt = row.modifieddt
                newtextcomment.modifiedby = row.modifiedby
                newtextcomment.disabled = 0
                newtextcomment.deleted = 0
                newtextcomment.save()

                newtcid = Textcomment.objects.latest("id")
                essay = essay.replace ('name="' + str(row.id) + '"', 'name="' + str(newtcid.id) + '"').replace('openHighlightDialog(' + str(row.id) + ')','openHighlightDialog(' + str(newtcid.id) + ')')

                tllist = Taglink.objects.filter(recid=row.id,entityid=14,deleted=0)
                for tl in tllist:
                    newtl = Taglink()
                    newtl.entityid = tl.entityid
                    newtl.recid = newtcid.id
                    newtl.createddt = tl.createddt
                    newtl.createdby = tl.createdby
                    newtl.modifieddt = tl.modifieddt
                    newtl.modifiedby = tl.modifiedby
                    newtl.deleted = tl.deleted
                    newtl.clientid = tl.clientid
                    newtl.tagid = tl.tagid
                    newtl.save()

                try:
                    cl = Categorylink.objects.get(recid=row.id,entityid=14,deleted=0)
                except Categorylink.DoesNotExist:
                    cl = ''
                else:
                    newcl = Categorylink()
                    newcl.entityid = cl.entityid
                    newcl.recid = newtcid.id
                    newcl.totalweight = cl.totalweight
                    newcl.categoryid = cl.categoryid
                    newcl.createddt = cl.createddt
                    newcl.createdby = cl.createdby
                    newcl.modifieddt = cl.modifieddt
                    newcl.modifiedby = cl.modifiedby
                    newcl.deleted = cl.deleted
                    newcl.clientid = cl.clientid
                    newcl.save()

            newversion = Submissionversion.objects.get(id=newid.id)
            newversion.essay = essay
            newversion.save()
    
##            i=0
##            for criteria in criteriaid:
##                entity = Entity.objects.get(id=15)
##                criteriaid = Rubriccriteria.objects.get(id=criteria)
##                scaleid = Rubricscale.objects.get(id=criteriaval[i])
##                rubricklink = Rubriclink()
##                rubricklink.entityid = entity
##                rubricklink.recid = submissionversionid
##                rubricklink.rubiccriteriaid = criteriaid
##                rubricklink.rubricscaleid = scaleid
##                rubricklink.save()
##                i += 1

##            data_json = {
##                        'status': criteriaval[0],
##                        }
            data_json = {
                        'status': '1',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

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
            submissionvshg.createdbyentity = 13
            submissionvshg.createdby = userid
            submissionvshg.modifieddt = datetime.now()
            submissionvshg.modifiedby = userid
            submissionvshg.disabled = 0
            submissionvshg.deleted = 0
            submissionvshg.save()
            recid = Textcomment.objects.latest('id').id

            entitylist = Entity.objects.get(id=14)
            if tagids != False and tagids != '':
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
            cursor.execute("select smh.id, smh.comment, t.tagcolor from taglink as tl  join textcomment as smh on smh.id = tl.recid and smh.disabled=0 and smh.deleted=0 join tag as t on tl.tagid = t.id where tl.entityid=14 and tl.deleted=0 and tl.clientid=%s and smh.recid = %s and smh.entityid = 15 and smh.id in (select recid from categorylink where categoryid = %s and entityid = 14)", [clientid,submissionreviewerid,categoryid])
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
                    tagentitysibling = TagEntity.objects.filter(Q(entityid=5),~Q(tagid__id__in=tagids),Q(tagid__parentid=row.tagid.parentid),Q(tagid__deleted = 0))
                    for rowsibling in tagentitysibling:
                        if { "id": str(rowsibling.tagid.id), "label": rowsibling.tagid.name, "value": rowsibling.tagid.name } not in data_json:
                            data_json.append({ "id": str(rowsibling.tagid.id), "label": rowsibling.tagid.name, "value": rowsibling.tagid.name })
                tagentitychild = TagEntity.objects.filter(Q(entityid=5), ~Q(tagid__id__in=tagids), Q(tagid__parentid=row.tagid.id),Q(tagid__deleted = 0))
                for rowchild in tagentitychild:
                    if { "id": str(rowchild.tagid.id), "label": rowchild.tagid.name, "value": rowchild.tagid.name } not in data_json:
                        data_json.append({ "id": str(rowchild.tagid.id), "label": rowchild.tagid.name, "value": rowchild.tagid.name })
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def getCommentlist(self,request):
        try:
            DATE_FORMAT = "%d/%m/%Y %H:%M" 
            submissionreviewerid = request.GET.get('submissionreviewerid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data_json = []
            submissionreviewer = Submissionreviewer.objects.get(id = submissionreviewerid)
            textcommentlist = Textcomment.objects.filter((Q(entityid=5) & Q(recid=submissionreviewer.submissionversionid.submissionid.id) & Q(deleted=0)) | (Q(entityid=15) & Q(recid=submissionreviewerid) & Q(deleted=0))).exclude(comment__isnull=True).exclude(comment='').order_by('createddt')
            for row in textcommentlist.reverse():
                data_json.append({ "id": str(row.id), "entityid": str(row.entityid.id), "comment": row.comment, "createddt": row.getFormatCreateDT(), 'createdbyentity': row.createdbyentity, 'createdby': row.createdby, 'creator': row.getCreatorFirstname() })
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def addComment(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            submissionreviewerid = request.POST.get('submissionreviewerid', False)
            comment = request.POST.get('comment', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionreviewer = Submissionreviewer.objects.get(id = submissionreviewerid)
            entitylist = Entity.objects.get(id=5)
            submissionvshg = Textcomment()
            submissionvshg.entityid = entitylist
            submissionvshg.recid = submissionreviewer.submissionversionid.submissionid.id
            submissionvshg.comment = comment
            submissionvshg.weight = 0
            submissionvshg.createddt = datetime.now()
            submissionvshg.createdbyentity = 13
            submissionvshg.createdby = userid
            submissionvshg.modifieddt = datetime.now()
            submissionvshg.modifiedby = userid
            submissionvshg.disabled = 0
            submissionvshg.deleted = 0
            submissionvshg.save()
            recid = Textcomment.objects.latest('id').id
            
            data_json = { 'recid': recid, }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def editComment(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            textcommentid = request.POST.get('textcommentid', False)
            comment = request.POST.get('comment', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            textcomment = Textcomment.objects.get(id=textcommentid)
            textcomment.comment = comment
            textcomment.modifieddt = datetime.now()
            textcomment.modifiedby = userid
            textcomment.save()

            data_json = {
                        'status': 'success',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def delComment(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            textcommentid = request.POST.get('textcommentid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            textcomment = Textcomment.objects.get(id=textcommentid)
            textcomment.deleted = 1
            textcomment.modifieddt = datetime.now()
            textcomment.modifiedby = userid
            textcomment.save()

            data_json = {
                        'status': 'success',
                        }
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
            
