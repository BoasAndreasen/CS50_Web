from django.shortcuts import render, redirect
from markdown2 import Markdown
from random import choice
from django import forms

from . import util
from .util import save_entry

markdowner = Markdown()


def index(request):
    all_entries = util.list_entries()

    if "Error" in all_entries:
        all_entries.remove("Error")

    return render(request, "encyclopedia/index.html", {
        "entries": all_entries
    })


def wiki(request, page):
    if not util.get_entry(page):
        return render(request, "encyclopedia/page.html", {
            "entry": markdowner.convert(util.get_entry("Error"))
        })
    else:
        return render(request, "encyclopedia/page.html", {
            "page": page,
            "entry": markdowner.convert(util.get_entry(page))
        })


def edit_wiki(request, page):
    if request.method == "POST":
        save_entry(page, request.POST['textarea'])

        return redirect(f'/wiki/{page}')

    else:
        return render(request, "encyclopedia/edit_wiki.html", {
            "entry": util.get_entry(page)
        })


def search(request):
    param = request.POST['q']

    if param in util.list_entries():
        return render(request, "encyclopedia/page.html", {
            "entry": markdowner.convert(util.get_entry(param))
        })

    substr = [el for el in util.list_entries() if param in el]

    if "Error" in substr:
        substr.remove("Error")

    return render(request, "encyclopedia/index.html", {
        "entries": substr
    })


def random(request):
    all_entries = util.list_entries()
    if "Error" in all_entries:
        all_entries.remove("Error")

    page = choice(all_entries)

    return render(request, "encyclopedia/page.html", {
        "entry": markdowner.convert(util.get_entry(page))
    })


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Name")


def new_page(request):
    if request.method == "POST":
        if util.get_entry(request.POST['title']):
            return render(request, "encyclopedia/page.html", {
                "entry": markdowner.convert(util.get_entry("Error"))
            })
        else:
            save_entry(request.POST['title'], request.POST['textarea'])
            return wiki(request, request.POST['title'])
    else:
        return render(request, "encyclopedia/new_page.html")
