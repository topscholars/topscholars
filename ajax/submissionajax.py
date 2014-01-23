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
from datetime import date
from datetime import time

class TSUBMISSIONLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            studentname=request.GET.get('studentname',False)
            submissionreviewerlist=''
            if studentname != False and studentname != '':
                submissionreviewerlist = Submissionreviewer.objects.filter(Q(entityid = 13) & Q(recid = userid) & Q(status = 0) & Q(deleted=0) & Q(disabled = 0) & (Q(submissionversionid__submissionid__studentid__firstname__contains=studentname) | Q(submissionversionid__submissionid__studentid__middlename__contains=studentname) | Q(submissionversionid__submissionid__studentid__lastname__contains=studentname)))
            else:
                submissionreviewerlist = Submissionreviewer.objects.filter(Q(entityid = 13) & Q(recid = userid) & Q(status = 0) & Q(deleted=0) & Q(disabled = 0))
            currentdate = date.today()
            context = {'submissionreviewerlist': submissionreviewerlist, 'currentdate':currentdate}
            return render(request, 'tsweb/teacher/submissionlistajax.html', context)
