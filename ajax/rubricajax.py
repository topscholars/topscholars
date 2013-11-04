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

class TRUBRICLISTAJAX():
    def get(self,request):
        try:
            userid = request.session['userid']
        except KeyError:
            return HttpResponseRedirect(reverse('tsweb:login'))
        else:
            login = Login.objects.get(id=userid)
            clientid = login.clientid
            rubricname=request.GET.get('rubricname',False)
            rubriclist=''
            if rubricname != False and rubricname != '':
                rubriclist = Rubric.objects.filter(clientid=clientid,name__contains=rubricname,deleted=0)
            else:
                rubriclist = Rubric.objects.filter(clientid=clientid,deleted=0)
            context = {'rubriclist': rubriclist}
            return render(request, 'tsweb/teacher/rubriclistajax.html', context)
