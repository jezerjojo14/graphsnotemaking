from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render

import json

import os
from django.conf import settings

from pathlib import Path

import subprocess, os, platform

from os import listdir

from django.views.decorators.csrf import csrf_exempt

papers_path = settings.BASE_DIR.parent.parent / "Papers" / "Active"


# Create your views here.

def refresh_papers():
    with open("paper_links.json") as f:
        # This json file will contain the filenames of all the papers as keys
        # Values will be of the form {"title": ..., "author": ..., "link": ..., "parent": ...}
        paper_links=json.load(f)
    papers = listdir(papers_path)
    for paper in papers:
        if paper not in paper_links.keys():
            paper_links[paper]={"title": paper, "author": "", "link": "/", "parent": ""}
    
    with open("paper_links.json", 'w', encoding='utf-8') as f:
        json.dump(paper_links, f, ensure_ascii=False, indent=4)
    

def index(request):
    refresh_papers()
    with open("paper_links.json") as f:
        # This json file will contain the filenames of all the papers as keys
        # Values will be of the form {"title": ..., "author": ..., "link": ..., "parent": ...}
        paper_links=json.load(f)
    return render(request, "graphnotes/index.html", context={"papers_json_str":json.dumps(paper_links)})

@csrf_exempt
def open_paper(request):

    post_data = json.loads(request.body.decode("utf-8"))
    print(post_data)
    filename=post_data["filename"]

    filepath=papers_path / filename
    
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', filepath))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(filepath)
    else:                                   # linux variants
        subprocess.call(('xdg-open', filepath))

    return HttpResponse(status="201")
