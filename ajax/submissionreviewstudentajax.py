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
                taglinklist = Taglink.objects.filter(recid=highlightid,entityid=15,deleted=0)
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
            cursor.execute("select t.id,t.name,t.parentid,count(t.id) as number from textcomment as smh join taglink as tl on tl.recid = smh.id and tl.entityid=14 and tl.deleted = 0 and tl.clientid= %s join tag as t on t.id = tl.tagid and t.disabled=0 and t.deleted = 0 and t.clientid= %s where smh.recid = %s and smh.disabled=0 and smh.deleted=0 group by t.id", [clientid,clientid,submissionversionid])
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
            cursor.execute("select smh.id, smh.comment, t.tagcolor from taglink as tl  join textcomment as smh on smh.id = tl.recid and smh.disabled=0 and smh.deleted=0 join tag as t on tl.tagid = t.id where tl.entityid=14 and tl.deleted=0 and tl.clientid=%s and smh.recid = %s and smh.entityid = 5 and smh.id in (select recid from categorylink where categoryid = %s and entityid = 14)", [clientid,submissionversionid,categoryid])
            submissionvshglist = cursor.fetchall()
            data = simplejson.dumps(submissionvshglist)
            return HttpResponse(data, mimetype='application/json')
