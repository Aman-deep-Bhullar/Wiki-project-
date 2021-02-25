
from django.shortcuts import render,reverse
from django.http import  HttpResponseRedirect
from django import forms
from . import util
import random
import markdown2


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "randompage":random.choice(util.list_entries())
    })

def title(request, title):
     details =util.get_entry(title)
     if not details:
       details="There is no contents"
     return render(request,"encyclopedia/details.html", {
      "title":title,
      "details":markdown2.markdown(details),
     "randompage":random.choice(util.list_entries())

    })

class Newentryform(forms.Form):
     title = forms.CharField(label="Add title")
     content = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "cols": 5}))




def search(request):
     query = request.GET.get('q')
     if not util.get_entry(query):

        entries = []
        for entry in util.list_entries():
          if query.upper() in entry.upper():
            entries.append(entry)
     else:
          return HttpResponseRedirect(reverse("details",kwargs={'title':query}))


     return render(request, "encyclopedia/index.html", {
     "entries": entries,
      "randompage": random.choice(util.list_entries())
})
def addentry(request):


    if request.method == 'POST':
        form =Newentryform (request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content= form.cleaned_data["content"]

            if  util.get_entry(title):
                return render(request,"encyclopedia/error.html",{
                              "form":form, 'message':'page exist', "randompage":random.choice(util.list_entries())})

            else:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("details", kwargs={'title': title}))

    return render(request, "encyclopedia/add.html",{
                    "form": Newentryform(),
                    "randompage": random.choice(util.list_entries())
    })


class editentryform(forms.Form):

    content = forms.CharField(widget = forms.Textarea(attrs={"rows": 3, "cols": 7}))

def editentry(request, title):

    # That code will be excuted when the save button will be pressed and it will save the new content given
    if request.method == "POST":
        form = editentryform(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("details", kwargs={'title': title}))
    #The end
    # that code below will be excuted if you visted the link first time.
        #first thing check if the parameter on url exist on entries and render the edit page, else it will show error page
    if util.get_entry(title):
        content = util.get_entry(title)
        form = editentryform(request.POST or None, initial={'content': content})
    else:
        return render(request, "encyclopedia/error.html",{'message': 'page doesnot exist'})
    return render(request, "encyclopedia/edit.html", {"form": form})
























