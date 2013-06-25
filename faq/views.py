# -*- encoding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def faq(request):
    if request.method == "POST":
        print 'ssssss'
        return HttpResponse("Здравствуй, мой ч0рный грязный Мир")
    else:
        user = request.user
        return render_to_response('bd/faq.html',{ "user": user }, context_instance = RequestContext( request ))

