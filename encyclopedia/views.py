from django.shortcuts import render, redirect

from . import util
from markdown2 import Markdown
import random

def convert_md_to_html(content):
    markdowner = Markdown()
    return markdowner.convert(content)
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    try:
        title = name
        content = util.get_entry(title)
        html_content = convert_md_to_html(content)
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        } )
    except:
        return render(request, "encyclopedia/error.html",{
            "error_title":"404 Not Found",
            "message":"Page not found"
        })

def search(request):
    query = request.GET.get('q')
    if not query:
        return render(request, "encyclopedia/error.html", {
            "error_title": "Empty Search",
            "message": "Please enter a valid search term."
        })
    entry_list = util.list_entries()
    reco_list =[]
    for entry in entry_list:
        if query.lower() == entry.lower():
            return render(request, "encyclopedia/entry.html",{
                "title":entry,
                "content":convert_md_to_html(util.get_entry(entry))
            })
        elif query.lower() in entry.lower():
            reco_list.append(entry)
    if reco_list:
        return render(request, "encyclopedia/search.html",{
                    "entries":reco_list
                })   
    else:
        return render(request, "encyclopedia/error.html",{
            "error_title":"No Results",
            "message":"There are no related entries"
        })

def new_page(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST["content"]

        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
                "error_title": "Page already exists!",
                "message":"A page with the same title already exists."
                })
        
        elif title == "" or content == "":
            return render(request, "encyclopedia/error.html", {
                "error_title": "Title and content are required!",
                "message":"" 
                })
        
        util.save_entry(title, content)

        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":convert_md_to_html(content)
        })
    return render(request, "encyclopedia/new_page.html", {
    })

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method =="POST":
        title = request.POST['title']
        content = request.POST['content']
        content = content.strip()
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":convert_md_to_html(content)
        })
   
def rand(request):
    entries = util.list_entries()
    title = random.choice(entries)
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title":title,
        "content":convert_md_to_html(content)
    })