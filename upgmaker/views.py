# -*- encoding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import os, subprocess,time
from django.views.decorators.csrf import csrf_protect

runBin = "!all.bat"
semFile = "started.txt"
branchPath = { 'bars106105' : "j:/!upgrade_SPO/work12_1_106_105/", 'bars304' : "j:/!upgrade_SPO/work12_1_304/",'bars305' : "j:/!upgrade_SPO/work12_1_305/",'bars302' : "j:/!upgrade_SPO/work12_1_302/",'bars303' : "j:/!upgrade_SPO/work12_1_303/",'KLADR' : "j:/!upgrade_SPO/work_kladr/"}

@login_required
def upgmaker(request):
    line = dict()
    for branch in branchPath:
        if os.path.exists( branchPath[branch]+semFile):
            f = open( branchPath[branch]+semFile, 'r')
            chlist = f.readline()
            f.close()

            whoStarted =  "undef"
            showstring = ""
            if os.path.exists( branchPath[branch]+'starter') and os.path.isfile( branchPath[branch]+semFile):
                if os.path.exists( branchPath[branch]+'error.log'):
                    f = open( branchPath[branch]+'error.log', 'r')
                    whoStarted = f.readline()
                    f.close()
                    showstring = u" ветка не собирается ;-( "+whoStarted
                else:
                    f = open( branchPath[branch]+'starter', 'r')
                    whoStarted = f.readline()
                    f.close()
                    t = os.stat(branchPath[branch]+semFile).st_ctime
                    showstring = u" запущен успешно! текущий changelist: "  + chlist.encode("ascii")+' by '+whoStarted +" in " +time.strftime("%H:%M:%S", time.localtime(t))
            line[branch] =  showstring
        else:
            line[branch] = ""# u" не был запущен"

    context = {'log_lines' : line, "user" : request.user }
    return render_to_response('bd/upgmaker.html', context, context_instance = RequestContext( request ))

#@login_required
def log(request):
    line=[""]
    for branch in branchPath:
        if os.path.exists( branchPath[branch]+semFile):
            f = open( branchPath[branch]+semFile, 'r')
            chlist = f.readline()
            f.close()

            whoStarted =  "undef"

            if os.path.exists( branchPath[branch]+'starter') and os.path.isfile( branchPath[branch]+semFile):
                if os.path.exists( branchPath[branch]+'error.log'):
                    f = open( branchPath[branch]+'error.log', 'r')
                    whoStarted = f.readline()
                    f.close()
                    line.append( u"ветка не собирается: "+branch+ " " + whoStarted)
                else:
                    f = open( branchPath[branch]+'starter', 'r')
                    whoStarted = f.readline()
                    f.close()
                    line.append( branch + u" запущен успешно! текущий changelist: "  + chlist.encode("ascii")+' by '+whoStarted)

        else:
            line.append( branch + u" не был запущен" )

    context = {'log_lines' : line, "user" : request.user }
    return render_to_response('upgmaker.html', context, context_instance = RequestContext( request ))

def getlog(request):
    from django.utils import simplejson

    branchParam = 'branch'
    if request.method == 'GET':
        if 'branchParam' in request.GET:
                print request.GET[branchParam]

    line = dict()
    for branch in branchPath:
        if os.path.exists( branchPath[branch]+semFile):
            f = open( branchPath[branch]+semFile, 'r')
            chlist = f.readline()
            f.close()

            whoStarted =  "undef"

            if os.path.exists( branchPath[branch]+'starter') and os.path.isfile( branchPath[branch]+semFile):
                f = open( branchPath[branch]+'starter', 'r')
                whoStarted = f.readline()
                f.close()
                if branch == 'KLADR':
                    line[branch] = branch + " " +chlist.encode("ascii")+' by '+whoStarted
                else:
                    if os.path.exists( branchPath[branch]+'error.log'):
                        f = open( branchPath[branch]+'error.log', 'r')
                        whoStarted = f.readline()
                        f.close()
                        line[branch] = u"ветка не собирается: "+ whoStarted
                    else:
                        t = os.stat(branchPath[branch]+semFile).st_ctime
                        line[branch] = branch + u" запущен успешно! текущий changelist: "  + chlist.encode("ascii")+' by '+whoStarted +" in " +time.strftime("%H:%M:%S", time.localtime(t))
            else:
                line[branch] = branch + u" не был запущен"
        else:
            line[branch] = branch + u" не был запущен"


    return HttpResponse(simplejson.dumps(line), mimetype = 'application/json')

@login_required
def run(request):
    if request.method == "POST":
        user = request.user
        for branch in branchPath:
             if request.POST.get( branch, False) and not os.path.exists( branchPath[branch]+semFile ):
                 p = subprocess.Popen(branchPath[branch]+runBin, cwd=branchPath[branch])
                 writeStarterEmail( branchPath[branch]+'starter', user.email)
                 while not os.path.exists( branchPath[branch]+semFile ):
                     time.sleep(10)

        print user.email
        return HttpResponseRedirect( "/log/" )
    else:
        user = { "user":request.user }
        return render_to_response('params.html', user, context_instance = RequestContext( request ))


@login_required
def getChlists(request):
    chlist=''
    if request.method == "POST":
        branch = request.POST.get( 'branch', '')
        if branch and branchPath.has_key(branch):
            ofile = branchPath[branch]+'changelist.txt'
            if os.path.exists( ofile ):
                 f = open( ofile, 'r')
                 chlist = f.readlines()
                 f.close()

        return HttpResponse(chlist)
    else:
        return HttpResponse()

'''
Client submitted runbranch button
'''
@login_required
def runbranch(request):
    if request.method == "POST":
        user = request.user
        line=[""]
        branch = request.POST.get( "branch", "")
        if branch:
             if not os.path.exists( branchPath[branch]+semFile ):
                 p = subprocess.Popen(branchPath[branch]+runBin, cwd=branchPath[branch])
                 writeStarterEmail(branchPath[branch]+'/starter', user.email)
                 while not os.path.exists( branchPath[branch]+semFile ):
                     time.sleep(10)

                 f = open( branchPath[branch]+semFile, 'r')
                 chlist = f.readline()
                 f.close()

                 whoStarted =  "undef"

                 if os.path.exists( branchPath[branch]+'starter') and os.path.isfile( branchPath[branch]+semFile):
                     f = open( branchPath[branch]+'starter', 'r')
                     whoStarted = f.readline()
                     f.close()

                 line.append( branch + u" запущен успешно! текущий changelist: "  + chlist.encode("ascii")+' by '+whoStarted)

        return HttpResponse( line )

    else:
        return HttpResponse("not post")

def writeStarterEmail(path, email):
    f = open( path, 'w')
    f.write(email)
    f.close()
    return 0
