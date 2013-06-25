# -*- encoding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import os

def hello(request):
    user = request.user
    return render_to_response('index.html',{ "user": user }, context_instance = RequestContext( request ))

#@login_required
def news(request):
    xmlfile = "j:\\site\\bars\\static\\news.xml"

    if not os.path.exists( xmlfile ):
        print "no file here"+xmlfile
        context = {'log_lines' : dict(), "user" : request.user }
        return render_to_response('bd/news.html',    context, context_instance = RequestContext( request ))

    import xml.etree.ElementTree as etree
    tree = etree.parse(xmlfile)
    root = tree.getroot()
    line = dict()

    for child in root:
        tags = dict()
        for block in child.iter():
            tags[block.tag] = block.text
        line[child.attrib['name']] = tags

    from collections import  OrderedDict

    line = OrderedDict(sorted(line.items(), key=lambda t: t[0]))

    context = {'log_lines' : line, "user" : request.user }
    return render_to_response('bd/news.html',    context, context_instance = RequestContext( request ))
