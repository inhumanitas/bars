# Create your views here.

from django.template import RequestContext
from django.shortcuts import render_to_response

def about(request):
    user = request.user
    return render_to_response('about.html',{ "user": user }, context_instance = RequestContext( request ))
