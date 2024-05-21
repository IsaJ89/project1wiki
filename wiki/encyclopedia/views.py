from django.shortcuts import render
import markdown2
import os
from django import forms
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect
from django.urls import reverse



from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,name):
    entry_md = util.get_entry(name) #trying to get the markdown file
    if entry_md == None:
        return render(request, "encyclopedia/error.html",{
            "name" : name.capitalize()
        })
    else:
        html_view = markdown2.markdown(entry_md)  #converting from .md to .html
        return render(request,"encyclopedia/viewentry.html", {
            "name" : name.capitalize(),  # "name" and "html_view" are my variables that need to be inserted
            "html_view": html_view          # into the viewentry.html template
        })

def search(request):
    query = request.GET.get('q')
    get_file_names = os.listdir("entries")
    new_file_names = []
    for file in get_file_names:
        if file[0] == ".":  # excluding hidden files
            continue
        else:
            file = file.replace(".md","")
            new_file_names.append(file)
    matching_files = []
    for name in new_file_names:
        if query.lower() in name.lower():
            if query.lower() == name.lower():
                return entry(request, query)
            else:
                matching_files += [name]
        
    return render(request, "encyclopedia/search.html", {
        "matching_files" : matching_files
    })

    
def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("newentry")
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            return render(request, "encyclopedia/new.html",{
                "message" : "Sorry, this entry already exists!"
            })
        else:
            default_storage.save(filename, ContentFile(content))
            return HttpResponseRedirect(reverse("entry", args=[title]))
    
    return render(request, "encyclopedia/new.html")

def edit(request):
    if request.method=="POST":
        content = request.POST.get("content")
        name = request.POST.get("name")
        util.save_entry(name, content)
        return HttpResponseRedirect(reverse("entry", args=[name]))
    
    name = request.GET.get("name")
    name_md = util.get_entry(name)
    return render(request, "encyclopedia/edit.html",{
            "name":name,
            "content":name_md
        })
    
