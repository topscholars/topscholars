from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson
from django.core.mail import send_mail

from tsweb.models import *

class LOGINAJAX():
    def sendhint(self,request):
        username=request.POST.get('username',False)
        if username == False:
            data_json = {'status': 'Invalid Username.',}
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                user= Login.objects.get(loginname=username,deleted=0)
            except (KeyError, Login.DoesNotExist):
                data_json = {'status': 'Invalid Username.',}
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                body = 'Your password is: ' + user.password
                email = [username]
##                if user.usertypeid == 2:
##                    userdetails = Studentlist.objects.get(id=user.recid)
##                    email = [userdetails.emailaddress1]
##                elif user.usertypeid == 3:
##                    email = [username]
##                else:
##                    userdetails = Userlist.objects.get(id=user.recid)
##                    email = [userdetails.emailaddress]
                send_mail('Topscholar Education: Password', body , 'noreply@writability.org',email, fail_silently=False)
                data_json = {'status': 'Email Sent.',}
##                try:
##                    send_mail('Topscholar Education: Password Hint', body , settings.EMAIL_HOST_USER,[email], fail_silently=False)
##                except  smtplib.SMTPException:
##                    data_json = {'status': 'Fail to Send Email.',}
##                else:
##                    data_json = {'status': 'Email Sent.',}
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')

    def checkUserPassword(self,request):
        try:
            username=request.POST.get('username',False)
            password=request.POST.get('password',False)
        except KeyError:
            data_json = { 'status': 'error', }
            data = simplejson.dumps(data_json)
            return HttpResponse(data, mimetype='application/json')
        else:
            try:
                login = Login.objects.get(loginname=username)
            except Login.DoesNotExist:
                data_json = { 'status': 'no_user', }
                data = simplejson.dumps(data_json)
                return HttpResponse(data, mimetype='application/json')
            else:
                try:
                    login = Login.objects.get(loginname=username, password=password)
                except Login.DoesNotExist:
                    data_json = { 'status': 'password_wrong', }
                    data = simplejson.dumps(data_json)
                    return HttpResponse(data, mimetype='application/json')
                else:
                    data_json = { 'status': 'success', }
                    data = simplejson.dumps(data_json)
                    return HttpResponse(data, mimetype='application/json')
