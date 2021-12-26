from django.core.files.base import ContentFile
from django.forms.widgets import Textarea
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
import markdown2
import random

from . import util
from django import forms

class NewPageForm(forms.Form):
    title=forms.CharField(label="New Page")
    content=forms.CharField(label="content", widget=forms.Textarea(attrs={'class':'fieldform'}))

class ChangePageForm(forms.Form):
    content=forms.CharField(label="content", widget=forms.Textarea(attrs={'class':'fieldform'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, title):
    art=util.get_entry(title)
    if art is None:
        return HttpResponse("Error. The required article was not found")

    return render(request, "encyclopedia/article.html", {
        "title": title, "content": markdown2.markdown(art)
    })

def search(request):
    if request.method == "POST":
        title=request.POST.get("q")
        art=util.get_entry(title)
        entries=util.list_entries()
        if art is None:
            results=[ ]
            for entry in entries:
                if title in entry:
                    results.append(entry)

            if results:
                return render(request, "encyclopedia/index.html", {
                    "entries":results})             

            return HttpResponse("No matches found")
        else:
            return HttpResponseRedirect(reverse ("article", kwargs={"title": title}))

    else:
        return render (request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def newpage(request):
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })


def savepage(request):
    if request.method == "POST":
        title=request.POST.get("title")
        content=request.POST.get("content")
        name=util.get_entry(title)
        if name is None:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse ("article", kwargs={"title": title}))
        else:
            return HttpResponse("Error. An article with this title already exists")
    else:
        return render (request, "encyclopedia/newpage.html", {
            "form": NewPageForm()
        })

def changepage(request, title):
    content=util.get_entry(title)
    return render(request, "encyclopedia/changepage.html", {
        "title": title, "form": ChangePageForm(initial={'content': content})
    })

def editpage(request, title):
    if request.method == "POST":
        content=request.POST.get("content")
        title=title
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse ("article", kwargs={"title": title}))
    else:
        content=util.get_entry(title)
        return render (request, "encyclopedia/changepage.html", {
            "title": title, "form": ChangePageForm(initial={'content': content})
        })


def randompage(request):
    entries=util.list_entries()
    title=random.choice(entries)
    return HttpResponseRedirect(reverse ("article", kwargs={"title": title}))

