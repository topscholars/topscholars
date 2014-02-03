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

class VIEWAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
            login = Login.objects.get(id=userid)
            studentid = login.recid
            studentlist = Studentlist.objects.get(id=studentid)
        except Studentlist.DoesNotExist:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            submissionversionid = studentlist.lastsubmissionversionid
            try:
                submissionversion = Submissionversion.objects.get(id=submissionversionid)
            except Submissionversion.DoesNotExist:
                data_json = {
                    'essay' : '',
                    }
            else:
                data_json = {
                    'essay' : submissionversion.essay,
                    }
                
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')