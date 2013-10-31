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
            return HttpResponse('error', mimetype='application/json')
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
                        'submissionduedate': submissionversion.submissionid.duedate,
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
                return HttpResponse('not found', mimetype='application/json')

            
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def getSubmissionVersionHighlightList(self,request):
        try:
            userid = request.session['userid']
            versionid = request.GET.get('versionid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            data_json = ''
            submissionversionhighlightlist = list(Submissionversionhighlight.objects.filter(submissionversionid = versionid).values('id','hightlighttext'))
            data = simplejson.dumps(submissionversionhighlightlist)
            return HttpResponse(data, mimetype='application/json')

    def getSubmissionVersionHighlight(self,request):
        try:
            userid = request.session['userid']
            highlightid = request.GET.get('highlightid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            data_json = ''
            if highlightid != False and highlightid != '':
                submissionversionhighlight = Submissionversionhighlight.objects.get(id=highlightid)
                data_json = {
                        'highlightComment': submissionversionhighlight.comment,
                        }
            else:
                return HttpResponse('not found', mimetype='application/json')

            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        
    def getSubmissionVersionHighlightTags(self,request):
        try:
            userid = request.session['userid']
            highlightid = request.GET.get('highlightid', False)
        except KeyError:
            return HttpResponse('error', mimetype='application/json')
        else:
            data_json = []
            if highlightid != False and highlightid != '':
                cursor = connection.cursor()
                cursor.execute('select Taglink.id,Tag.name from Taglink left join Tag on Taglink.tagid = Tag.id left join TagEntity on Tag.id = TagEntity.tagid where Taglink.recid = %s and TagEntity.entityid = 5',[highlightid])
                
                for row in cursor.fetchall():
                    data_json.append({ "id": str(row[0]), "name": row[1] })
                    data = simplejson.dumps(data_json)
                    return HttpResponse(data, mimetype='application/json')
            else:
                return HttpResponse('not found', mimetype='application/json')
