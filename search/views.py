from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse

from all_libs.models import Chapter, Directory, Lib, Topic, Entry, Command
from .forms import SearchRequest
from itertools import chain


@login_required
def search_request(request):
    if request.method == 'GET' and 'request_field' in request.GET.keys():
        form = SearchRequest(request.GET)
        if form.is_valid():
            search = form.cleaned_data['request_field']
            result = search_list(request, search)
            return result
    form = SearchRequest()
    context = {'form': form}
    return render(request, 'search/search_window.html', context)


@login_required
def search_list(request, search):
    chapters = Chapter.objects.filter(name__icontains=search)
    libs = Lib.objects.filter(name__icontains=search)
    directories = Directory.objects.filter(name__icontains=search)
    topics = Topic.objects.filter(name__icontains=search)
    entries = Entry.objects.filter(text__icontains=search)
    commands = Command.objects.filter(Q(name__icontains=search) | Q(about__icontains=search))
    form = SearchRequest()
    context = {'chapters': chapters, 'libs': libs, 'directories': directories, 'form': form,
               'topics': topics, 'entries': entries, 'commands': commands}

    return render(request, 'search/search_window.html', context)




# Create your views here.
