# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.http import HttpResponseRedirect


@csrf_protect
def doLogin(request):
    if request.method == "POST":
        uname = request.POST.get( 'username', "")
        passwd = request.POST.get( 'password', "")

        try:
            from django.contrib.auth import authenticate
            user = authenticate(username=uname, password=passwd)
            if user is not None and user.is_active:
                from django.contrib.auth import login
                login(request, user)
                request.session["is_auth_ok"] = '1'

                return HttpResponse('1')
            else:
                request.session["is_auth_ok"] = '0'

                return HttpResponse('0')

        except:
            return HttpResponseRedirect("/accounts/login/")
    else:
        from django.shortcuts import render_to_response
        from django.template import RequestContext
        user = request.user
        return render_to_response('accounts/login.html',{ "user": user }, context_instance = RequestContext( request ))


@csrf_protect
def doLogout(request):
    from django.contrib.auth import logout
    logout(request)
    if request.method == "POST":
        return HttpResponse("1")
    else:
        return HttpResponseRedirect("/login/")
