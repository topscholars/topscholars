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

class TSUBMISSIONLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            studentname=request.GET.get('studentname',False)
            submissionlist=''
            if studentname != False and studentname != '':
                submissionlist = Submissionversion.objects.filter(Q(submissionid__teacherid=userid) & Q(studentstatus=1) & Q(teacherstatus=0) & Q(deleted=0) & Q(studentstatus=1) & (Q(submissionid__studentid__firstname__contains=studentname) | Q(submissionid__studentid__middlename__contains=studentname) | Q(submissionid__studentid__lastname__contains=studentname)))
            else:
                submissionlist = Submissionversion.objects.filter(submissionid__teacherid=userid,studentstatus=1,teacherstatus=0,deleted=0)
            context = {'submissionlist': submissionlist}
            return render(request, 'tsweb/teacher/submissionlistajax.html', context)