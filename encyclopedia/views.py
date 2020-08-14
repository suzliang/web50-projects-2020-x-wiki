from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from . import util
from .util import *
from .models import *

from markdown2 import Markdown 
markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    e = get_entry(title)
    if e is None:
        raise Http404("Error: entry does not exist")
    return render(request, "encyclopedia/entry.html", {'title': title, 'content': markdowner.convert(e)})

def search(request):
    if request.method == "POST":
        q = request.POST['q']
        a = util.list_entries()
        matching = []
        for i in a:
            if q.lower() == i.lower():
                return HttpResponseRedirect(reverse('entry', args=[i]))
            if q.lower() in i.lower():
                matching.append(i)
        return render(request, "encyclopedia/search.html", {'matching': matching})

def create(request):
    if request.method == "POST":
        form = New(request.POST)
        if form.is_valid():
            e = form.save(commit=False)
            s = get_entry(e.title)
            if s is None:
                save_entry(e.title, e.content)
                return HttpResponseRedirect(reverse('entry', args=[e.title]))
            raise Http404("Error: encyclopedia entry already exists")

    if request.method == "GET":
        form = New()
        return render(request, "encyclopedia/create.html", {'form': form})

def edit(request):
    if request.method == "POST":
        form = New(request.POST)
        if form.is_valid():
            e = form.save(commit=False)
            save_entry(e.title, e.content)
            return HttpResponseRedirect(reverse('entry', args=[e.title]))
        
    if request.method == "GET":
        title = request.GET['title']
        e = get_entry(title)
        form = New(initial={'title': title, 'content': e})
        return render(request, "encyclopedia/edit.html", {'form': form, 'title': title})

def random(request):
    import random
    a = util.list_entries()
    c = random.choice(a)
    e = get_entry(c)
    return render(request, "encyclopedia/entry.html", {'title': c, 'content': markdowner.convert(e)})