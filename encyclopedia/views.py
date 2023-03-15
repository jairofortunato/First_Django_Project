from django.shortcuts import render, redirect
from django.urls import reverse 
from . import util
from .util import get_entry, list_entries, save_entry
from django import forms
import markdown2
from django.http import HttpResponseNotFound
import random

# Converter markdown para html 

def convert_md_to_html(title):
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdown2.markdown(content)

# Página inicial 

def index(request):
    entries = util.list_entries()
    css_file = util.get_entry("CSS")
    coffee = util.get_entry("coffee")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Página do conteúdo 

def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", { 
            "message": "This entry does not exist"
        })
    else: 
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
# Mecanismo de busca 

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content =  convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entry_search,
            "content": html_content
            })
        else:
            allEntries = util.list_entries()
            recommendation = []
            for entry in allEntries:
                if entry_search.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recommendation": recommendation
            })

# Criação novo conteúdo

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}))

def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = list_entries()
            if title.lower() in [entry.lower() for entry in entries]:
                return render(request, "encyclopedia/new_entry.html", {
                    "form": form,
                    "existing_title": True
                })
            else:
                save_entry(title, content)
                return redirect("entry", title=title)
    else:
        form = NewEntryForm()
        return render(request, "encyclopedia/new_entry.html", {
            "form": form,
            "existing_title": False
        })

# Editar conteúdo


def edit(request, title):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

      
def save_edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
        })




# Botão de conteúdo aleatório

def random_entry(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    html_content = convert_md_to_html(random_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })
