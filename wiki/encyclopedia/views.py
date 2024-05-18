from django.shortcuts import render
import markdown2
import os


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
        return render(request,"encyclopedia/getentry.html", {
            "name" : name.capitalize(),  # "name" and "html_view" are my variables that need to be inserted
            "html_view": html_view          # into the getentry.html template
        })

def search(request):
    query = request.GET.get('q')
    get_file_names = os.listdir("entries")
    new_file_names = []
    for file in get_file_names:
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
    return render(request, "encyclopedia/new.html")


