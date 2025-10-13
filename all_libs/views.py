from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import BaseUpdateView
from django.db import transaction

from .models import Lib, Topic, Entry, Directory, Chapter, Command, UploadEntryPhoto
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from .forms import DirectoryForm, TopicForm, EntryForm, LibForm, ChapterForm, CommandForm, ImageFormSet
from .services import get_object_slug, get_order_objects, get_filter_objects, get_object, get_field, set_field, \
    save_object



def get_kwargs_to_context(view, context):
    """Дополняе контекст представления переменными, передающимися из представления"""
    for kwarg in view.kwargs.keys():
        if not (kwarg in list(context.keys())):
            context[kwarg] = view.kwargs[kwarg]
    return context


class CreateUpdateView(PermissionRequiredMixin, LoginRequiredMixin, SingleObjectTemplateResponseMixin, BaseUpdateView):

    object_slug = 'new_object'

    def get_object(self):
        """Чтобы разделить createview и updateview"""
        slug = self.kwargs.get(self.slug_url_kwarg)
        if slug == 'new_object':
            return None

        return super().get_object(queryset=None)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.object:
            self.object_slug = get_object_slug(self.object)
        context['object_slug'] = self.object_slug
        return context


class CustomDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    """Удаление экземпляров моделей, редактируемых и создаваемых из страницы изменения директории"""
    template_name = "all_libs/delete.html"

    def get_success_url(self):
        return reverse('all_libs:dir-detail', args=(self.kwargs['ch_slug'], self.kwargs['lib_slug'], self.kwargs['dir_slug'], "editing"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'dir_slug' in self.kwargs.keys():
            context['dir_slug'] = self.kwargs['dir_slug']
        return context


@login_required
def index(request):
    """Домашняя страница приложения all_libs"""
    return render(request, 'all_libs/index.html')


class ChaptersListView(LoginRequiredMixin, ListView):
    model = Chapter
    template_name = "all_libs/chapters.html"
    context_object_name = 'chapters'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return get_order_objects(Chapter.objects, 'name')


class ChapterDeleteView(CustomDeleteView):
    model = Chapter
    slug_url_kwarg = 'ch_slug'
    permission_required = 'all_libs.delete_chapter'

    def get_success_url(self):
        return reverse('all_libs:chapter-list')


class LibDeleteView(CustomDeleteView):
    model = Lib
    slug_url_kwarg = 'lib_slug'
    permission_required = 'all_libs.delete_lib'

    def get_success_url(self):
        return reverse('all_libs:lib-list', args=(self.kwargs["ch_slug"], ))


class LibListView(LoginRequiredMixin, ListView):
    """Список библиотек"""
    model = Lib
    template_name = "all_libs/libs.html"
    context_object_name = 'libs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapter'] = get_object(Chapter.objects, slug=self.kwargs['ch_slug'])
        context['ch_slug'] = get_object_slug(context['chapter'])
        return context

    def get_queryset(self):
        return get_order_objects(get_filter_objects(Lib.objects, chapter__slug=self.kwargs['ch_slug']), 'name')


class DirectoriesListView(LoginRequiredMixin, ListView):
    model = Directory
    template_name = "all_libs/directories.html"
    context_object_name = 'directories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lib'] = get_object(Lib.objects, slug=self.kwargs['lib_slug'])
        context = get_kwargs_to_context(self, context)
        return context

    def get_queryset(self):
        return get_filter_objects(Directory.objects, lib__slug=self.kwargs['lib_slug'])


class DirectoryDetailView(LoginRequiredMixin, DetailView):
    model = Directory
    context_object_name = 'directory'
    template_name = None
    slug_url_kwarg = 'dir_slug'

    def get_template_name(self):
        if self.kwargs['status'] == "editing" and (self.request.user.groups.contains(Group.objects.get(name='moderator')) or self.request.user.is_superuser):
            return "all_libs/edit_directory.html"
        elif self.kwargs['status'] == "watching" or self.kwargs['status'] == "editing":
            return "all_libs/directory.html"

    def get(self, request, *args, **kwargs):
        self.template_name = self.get_template_name()
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_kwargs_to_context(self, context)
        context['topics'] = get_filter_objects(Topic.objects, directory__slug=self.kwargs['dir_slug']).all()
        context['lib'] = get_object(Lib.objects, slug=self.kwargs['lib_slug'])
        if self.object and self.object.parent:
            context['parent_slug_or_no_slug'] = get_field(get_field(self.object, 'parent'), 'slug')
        else:
            context['parent_slug_or_no_slug'] = 'no-slug'
        return context


class LibCreateUpdateView(CreateUpdateView):
    model = Lib
    template_name = "all_libs/new_lib.html"
    slug_url_kwarg = 'lib_slug'
    permission_required = ('all_libs.add_lib', 'all_libs.change_lib')
    form_class = LibForm

    def form_valid(self, form):
        self.object = save_object(form, commit=False)
        set_field(self.object, 'chapter', get_object(Chapter.objects, slug=self.kwargs['ch_slug']))
        save_object(self.object)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_kwargs_to_context(self, context)
        return context

    def get_success_url(self):
        return reverse('all_libs:dir-list', args=(self.kwargs['ch_slug'], get_object_slug(self.object)))


class ChapterCreateUpdateView(CreateUpdateView):
    form_class = ChapterForm
    template_name = "all_libs/new_chapter.html"
    model = Chapter
    slug_url_kwarg = 'ch_slug'
    permission_required = ('all_libs.add_chapter', 'all_libs.change_chapter')

    def get_success_url(self):
        return reverse('all_libs:lib-list', args=(get_field(self.object, 'slug'), ))


class TopicCreateUpdateView(CreateUpdateView):
    slug_url_kwarg = 'topic_slug'
    model = Topic
    permission_required = ('all_libs.add_topic', 'all_libs.change_topic')
    form_class = TopicForm
    template_name = "all_libs/new_topic.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        directory = get_object(Directory.objects, slug=self.kwargs['dir_slug'])
        context['directory'] = directory
        context = get_kwargs_to_context(self, context)
        return context

    def form_valid(self, form):
        self.object = save_object(form, commit=False)
        set_field(self.object, 'directory', self.get_context_data()['directory'])
        save_object(self.object)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('all_libs:dir-detail', args=(self.kwargs['ch_slug'], self.kwargs['lib_slug'],
                                                    self.kwargs['dir_slug'], "editing"))


class DirectoryCreateUpdateView(CreateUpdateView):
    model = Directory
    slug_url_kwarg = 'dir_slug'
    template_name = "all_libs/new_directory.html"
    permission_required = ('all_libs.add_directory', 'all_libs.change_directory')
    form_class = DirectoryForm

    def get_success_url(self):
        return reverse('all_libs:dir-detail',
                       args=(get_field(get_field(get_field(self.object, 'lib'), 'chapter'), 'slug'),
                             get_field(get_field(self.object, 'lib'), 'slug'),
                             get_field(self.object, 'slug'), "editing"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['parent_slug_or_no_slug'] = self.kwargs['parent_slug']
        context = get_kwargs_to_context(self, context)
        context['lib'] = get_object(Lib.objects, slug=self.kwargs['lib_slug'])
        return context

    def form_valid(self, form):
        """parent_slug='no-slug' когда нет родителя"""
        self.object = save_object(form, commit=False)
        set_field(self.object, 'lib', self.get_context_data()['lib'])
        parent_slug = self.get_context_data()['parent_slug_or_no_slug']
        if parent_slug != 'no-slug':
            set_field(self.object, 'parent', get_object(Directory.objects, slug=parent_slug))
        save_object(self.object)

        return super().form_valid(form)

class EntryCreateUpdateView(CreateUpdateView):
    model = Entry
    form_class = EntryForm
    permission_required = ('all_libs.add_entry', 'all_libs.change_entry')
    template_name = "all_libs/new_entry.html"
    slug_url_kwarg = 'entry_slug'

    @transaction.atomic
    def form_valid(self, form, **kwargs):
        context = self.get_context_data()
        images = context['image_form']

        if not self.object:
            self.object = save_object(form, commit=False)
            set_field(self.object, 'topic', get_object(Topic.objects, slug=self.kwargs['topic_slug']))
        save_object(self.object)

        if images.is_valid():
            for img in images:
                if 'DELETE' in img.cleaned_data.keys() and img.cleaned_data['DELETE']:
                    img.instance.delete()
                elif img.cleaned_data.keys():
                    img = save_object(img, commit=False)
                    set_field(img, 'entry', self.object)
                    save_object(img)

        return super(EntryCreateUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = get_object(Topic.objects, slug=self.kwargs['topic_slug'])
        context['directory'] = get_field(topic, 'directory')
        context = get_kwargs_to_context(self, context)
        if self.request.POST:
            context['image_form'] = ImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_form'] = ImageFormSet(queryset=UploadEntryPhoto.objects.filter(entry=self.object))
        return context

    def get_success_url(self):
        return reverse('all_libs:dir-detail', args=(self.kwargs['ch_slug'], self.kwargs['lib_slug'],
                                                    self.kwargs['dir_slug'], "editing"))


class EntryDeleteView(CustomDeleteView):
    model = Entry
    permission_required = 'all_libs.delete_entry'
    slug_url_kwarg = 'entry_slug'


class TopicDeleteView(CustomDeleteView):
    permission_required = 'all_libs.delete_topic'
    model = Topic
    slug_url_kwarg = 'topic_slug'


class DirectoryDeleteView(CustomDeleteView):
    permission_required = 'all_libs.delete_directory'
    model = Directory
    slug_url_kwarg = 'dir_slug'

    def get_success_url(self):
        return reverse('all_libs:dir-list', args=(self.kwargs['ch_slug'], self.kwargs['lib_slug'], ))


class CommandsListView(LoginRequiredMixin, ListView):
    model = Command
    template_name = 'all_libs/commands_list.html'
    context_object_name = 'commands'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lib'] = get_object(Lib.objects, slug=self.kwargs['lib_slug'])
        context = get_kwargs_to_context(self, context)
        return context

    def get_queryset(self):
        return get_filter_objects(Command.objects, lib__slug=self.kwargs["lib_slug"])


@login_required
def delete_commands(request, lib_slug, ch_slug):
    lib = get_object(Lib.objects, slug=lib_slug)
    commands = get_filter_objects(Command.objects, lib=lib)
    for command in commands:
        if request.method == "POST":
            if request.POST.get(command.name):
                command.delete()
    url = reverse('all_libs:commands-list', kwargs={'lib_slug': lib_slug, 'ch_slug': ch_slug})
    return HttpResponseRedirect(url)


class CommandCreateUpdateView(CreateUpdateView):
    model = Command
    slug_url_kwarg = 'command_slug'
    form_class = CommandForm
    template_name = "all_libs/new_command.html"

    def form_valid(self, form):
        self.object = save_object(form, commit=False)
        set_field(self.object, 'lib', get_object(Lib.objects, slug=self.kwargs['lib_slug']))
        save_object(self.object)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = get_kwargs_to_context(self, context)
        return context
