from django import forms

from .custom_widgets import CustomClearableFileInput, CustomBaseFormSet, CustomBaseModelFormSet
from .models import Lib, Topic, Directory, Entry, Chapter, Command, UploadEntryPhoto
from django.forms import modelformset_factory


class CommandForm(forms.ModelForm):

    class Meta:
        model = Command
        fields = ['name', 'about']
        labels = {'name': 'Название/синтаксис', 'about': 'Описание'}


class LibForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "add_name_field"})
        self.fields["site"].widget.attrs.update({"class": "add_site_field"})

    class Meta:
        model = Lib
        fields = ['name', 'site']
        labels = {'name': 'Название', 'site': 'Официальный сайт'}


class ChapterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "add_name_field"})

    class Meta:
        model = Chapter
        fields = ['name']
        labels = {'name': 'Название'}


class DirectoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "add_name_field"})

    class Meta:
        model = Directory
        fields = ['name']
        labels = {'name': 'Название',}


class TopicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "add_name_field"})

    class Meta:
        model = Topic
        fields = ['name',]
        labels = {'name': 'Название'}


class EntryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update({"class": "add_text_field"})

    class Meta:
        model = Entry
        fields = ['text',]
        labels = {'text': '',}


class EntryImageForm(forms.ModelForm):
    class Meta:
        model = UploadEntryPhoto
        fields = ['image',]
        labels = {'image': '', }


ImageFormSet = modelformset_factory(UploadEntryPhoto, fields=('image', ), labels={'image': ''}, extra=1, max_num=8,
                                    validate_max=True, absolute_max=9, can_delete=True, formset=CustomBaseModelFormSet,
                                    widgets={'image': CustomClearableFileInput()}) # max_num вдвое больше необходимого,
# чтобы при редактировании до сохранения сохранялись формы, отмеченные на удаление