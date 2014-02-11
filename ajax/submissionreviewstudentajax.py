from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson
from django.core import serializers
from django.db.models.query import RawQuerySet
from django.db import connection
from tsweb.models import *
from django.db.models import Q,Max
from itertools import chain

from datetime import datetime
import time

class SUBMISSIONCREATE():
    def getSubmissionVersion(self,request):
        try:
            userid = request.session['userid']
            submissionversionid = request.GET.get('submissionversionid', False)
        except KeyError:
            data_json = {
                        'status': 'user not logged in',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionversion = Submissionversion.objects.get(id=submissionversionid)
            data_json = ''
            data_json = {
                'essay' : submissionversion.essay,
                'status' : submissionversion.studentstatus
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
                categoryname = ''
                try:
                    categorylink = Categorylink.objects.get(entityid=14,recid=highlightid)
                except Categorylink.DoesNotExist:
                    categoryname = ''
                else:
                    categoryname = categorylink.categoryid.name
                    
                data_json = {
                        'highlightComment': submissionversionhighlight.comment,
                        'highlightCategory': categoryname
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
            submissionversionid = request.POST.get('submissionversionid', False)
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

            submissionvs = Submissionversion.objects.get(id=submissionversionid)
            submissionvs.essay = essay;
            submissionvs.modifieddt = datetime.now()
            submissionvs.modifiedby = userid
            submissionvs.save()
            
            data_json = {
                        'status': 'success',
                        }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')

    def submit(self,request):
        try:
            userid = request.session['userid']
            essay = request.POST.get('essay', False)
            submissionversionid = request.POST.get('submissionversionid', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionvs = Submissionversion.objects.get(id=submissionversionid)
            submissionvs.essay = essay
            submissionvs.studentstatus = 1
            submissionvs.modifieddt = datetime.now()
            submissionvs.modifiedby = userid
            submissionvs.save()

            submissionvs = Submissionversion.objects.get(id=submissionversionid)
            entitylist = Entity.objects.get(id=13)
            submissionreviewer = Submissionreviewer()
            submissionreviewer.submissionversionid = submissionvs
            submissionreviewer.entityid = entitylist
            submissionreviewer.recid = submissionvs.submissionid.teacherid.id
            submissionreviewer.essay = essay
            submissionreviewer.status = 0
            submissionreviewer.createddt = datetime.now()
            submissionreviewer.createdby = userid
            submissionreviewer.modifieddt = datetime.now()
            submissionreviewer.modifiedby = userid
            submissionreviewer.disabled = 0
            submissionreviewer.deleted = 0
            submissionreviewer.save()

            data_json = {'status': 'success'}
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def save(self,request):
        try:
            userid = request.session['userid']
            essay = request.POST.get('essay', False)
            submissionversionid = request.POST.get('submissionversionid', False)
        except KeyError:
            data_json = { 'status': 'error' }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionvs = Submissionversion.objects.get(id=submissionversionid)
            submissionvs.essay = essay
            submissionvs.modifieddt = datetime.now()
            submissionvs.modifiedby = userid
            submissionvs.save()
            
            login = Login.objects.get(id=userid)
            recid = login.recid
            
            studentlist = Studentlist.objects.get(id=recid)
            studentlist.lastsubmissionversionid = submissionversionid
            studentlist.modifieddt = datetime.now()
            studentlist.modifiedby = userid
            studentlist.save()

            data_json = {'status': 'success',
                         'submissionversionid': submissionversionid}
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
            cursor.execute("select t.id,t.name,t.parentid,count(t.id) as number from textcomment as smh join taglink as tl on tl.recid = smh.id and tl.entityid=14 and tl.deleted = 0 and tl.clientid= %s join tag as t on t.id = tl.tagid and t.disabled=0 and t.deleted = 0 and t.clientid= %s where smh.recid = %s and smh.disabled=0 and smh.deleted=0 and smh.entityid = 16 group by t.id", [clientid,clientid,submissionversionid])
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
            cursor.execute("select smh.id, smh.comment, t.tagcolor from taglink as tl  join textcomment as smh on smh.id = tl.recid and smh.disabled=0 and smh.deleted=0 join tag as t on tl.tagid = t.id where tl.tagid = %s and tl.entityid=14 and tl.deleted=0 and tl.clientid=%s and smh.recid = %s", [taglinkid,clientid,submissionversionid])
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
            submissionversionid = request.GET.get('submissionversionid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            cursor.execute("select smh.id, smh.comment, t.tagcolor from taglink as tl  join textcomment as smh on smh.id = tl.recid and smh.disabled=0 and smh.deleted=0 join tag as t on tl.tagid = t.id where tl.entityid=14 and tl.deleted=0 and tl.clientid=%s and smh.recid = %s and smh.entityid = 16 and smh.id in (select recid from categorylink where categoryid = %s and entityid = 14)", [clientid,submissionversionid,categoryid])
            submissionvshglist = cursor.fetchall()
            data = simplejson.dumps(submissionvshglist)
            return HttpResponse(data, mimetype='application/json')

    def getCommentlist(self,request):
        try:
            DATE_FORMAT = "%d/%m/%Y %H:%M" 
            submissionversionid = request.GET.get('submissionversionid', False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            data_json = []
            submissionversion = Submissionversion.objects.get(id = submissionversionid)
            textcommentlist = Textcomment.objects.filter((Q(entityid=5) & Q(recid=submissionversion.submissionid.id) & Q(deleted=0)) | (Q(entityid=16) & Q(recid=submissionversionid) & Q(deleted=0))).exclude(comment__isnull=True).exclude(comment='').order_by('createddt')
            for row in textcommentlist.reverse():
                data_json.append({ "id": str(row.id), "entityid": str(row.entityid.id), "comment": row.comment, "createddt": row.getFormatCreateDT(), 'createdbyentity': row.createdbyentity, 'createdby': row.createdby, 'creator': row.getCreatorFirstname() })
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
