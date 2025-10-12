from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from random import choice
import functools

from django.urls import reverse

from all_libs.models import UploadEntryPhoto, Chapter, Lib, Directory, Topic, Entry


def name_generate(n: int) -> str:
    symbols = \
        'qwertyuiopasdfghjklzxcvbnmйцукенгшщфывапролджэячсмитьбюЙЦУКЕНГШЩЗХФЫВАПРОЛДЖЭЯЧСМИТЬБЮQWERTYUIOPASDFJKLZXCVBNM'
    name = ''
    for i in range(n):
        name += choice(symbols)
    return name


def get_entry_create_update_url(entry_object, *args, follow_p=False):
    data = {'text': name_generate(500),
           'form-TOTAL_FORMS': '2',
           'form-INITIAL_FORMS': '0',
           'form-MAX_NUM_FORMS': '8',
           "form-MIN_NUM_FORMS": '0',
           'form-0-id': '',
           'form-1-id': '',
           'form-2-image': '',
           'form-2-id': "",
           'form-0-image': SimpleUploadedFile(name='test_image.jpg', content=b'\x00', content_type='image/jpeg'),
           'form-1-image': SimpleUploadedFile(name='test_image.jpg', content=b'\x00', content_type='image/jpeg')}
    response = entry_object.client.post(reverse("all_libs:entry-create-update", args=args),
         data, follow=follow_p)
    return response


def get_topic_create_update_url(topic_object, *args, follow_p=False):

    response = topic_object.client.post(reverse("all_libs:topic-create-update", args=args)
        , {'name': name_generate(12), }, follow=follow_p)
    return response


def get_lib_create_update_url(lib_object, *args, follow_p=False):
    response = lib_object.client.post(reverse("all_libs:lib-create-update", args=args),
                                {'name': name_generate(12),
                                 'site': 'https://django.fun/docs/django/5.0/topics/testing/tools/'}, follow=follow_p)
    return response


def get_chapter_create_update_url(ch_object, *args, follow_p=False):
    response = ch_object.client.post(reverse("all_libs:chapter-create-update", args=args),
                                {'name': name_generate(12)}, follow=follow_p)
    return response


def get_dir_create_update_url(directory_object, *args, follow_p=False):
    response = directory_object.client.post(
        reverse("all_libs:dir-create-update", args=args),
                {'name': name_generate(12), }, follow=follow_p)
    return response


class TestUrls(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        ch1 = Chapter.objects.create(name=name_generate(12))
        lib1 = Lib.objects.create(name=name_generate(12), chapter=ch1)
        dir = Directory.objects.create(name=name_generate(12), lib=lib1)
        topic = Topic.objects.create(name=name_generate(12), directory=dir)
        self.chapters = Chapter.objects.all()
        self.dirs = Directory.objects.all()
        self.libs = Lib.objects.all()
        self.topics = Topic.objects.all()
        en = Entry.objects.create(text=name_generate(225), topic=topic)
        im = SimpleUploadedFile(name='test_image.jpg', content=b'\x00', content_type='image/jpeg')
        upload = UploadEntryPhoto.objects.create(image=im, entry=en)

        self.images = UploadEntryPhoto.objects.all()
        self.entries = Entry.objects.all()

    def test_chapter_list(self):
        res = self.client.get(reverse('all_libs:chapter-list'), follow=True)
        self.assertEqual(res.status_code, 200)

    def test_lib_lists(self):
        for ch in self.chapters:
            response = self.client.get(reverse('all_libs:lib-list', args=(ch.slug,)), follow=True)
            self.assertEqual(response.status_code, 200)

    def test_list_of_dirs(self):
        for lib in self.libs:
            response = self.client.get(reverse('all_libs:dir-list', args=(lib.chapter.slug, lib.slug,)), follow=True)
            self.assertEqual(response.status_code, 200)

    def test_dir_detail(self):
        for directory in self.dirs:
            response = self.client.get(reverse('all_libs:dir-detail', args=(directory.lib.chapter.slug,
                                                                            directory.lib.slug,
                                                                            directory.slug, 'watching',)), follow=True)
            self.assertEqual(response.status_code, 200)
            response = self.client.get(reverse('all_libs:dir-detail', args=(directory.lib.chapter.slug,
                                                                            directory.lib.slug,
                                                                            directory.slug, 'editing',)), follow=True)
            self.assertEqual(response.status_code, 200)

    def test_lib_create_update(self):
        for chapter in self.chapters:
            response = functools.partial(get_lib_create_update_url)(self, chapter.slug, 'new_object')
            self.assertEqual(response.status_code, 302)
            response = functools.partial(get_lib_create_update_url)(self, chapter.slug, 'new_object', follow_p=True)
            self.assertEqual(response.status_code, 200)
        for lib in self.libs:
            response = functools.partial(get_lib_create_update_url)(self, chapter.slug, lib.slug)
            self.assertEqual(response.status_code, 302)
            # response = functools.partial(get_lib_create_update_url)(self, chapter.slug, lib.slug, follow_p=True)
            # self.assertEqual(response.status_code, 200)

    def test_dir_create_update(self):
        for lib in self.libs:
            response = functools.partial(get_dir_create_update_url)(self, lib.chapter.slug, lib.slug, 'no-slug', 'new_object')
            self.assertEqual(response.status_code, 302)
            response = functools.partial(get_dir_create_update_url)(self, lib.chapter.slug, lib.slug, 'no-slug', 'new_object', follow_p=True)
            self.assertEqual(response.status_code, 200)
            for dir in self.dirs:
                response = functools.partial(get_dir_create_update_url)(self, lib.chapter.slug, dir.lib.slug, dir.slug, 'new_object')
                self.assertEqual(response.status_code, 302)
                response = functools.partial(get_dir_create_update_url)(self, lib.chapter.slug, dir.lib.slug, dir.slug, 'new_object',
                                             follow_p=True)
                self.assertEqual(response.status_code, 200)
                if dir.parent:
                    pare_slug = dir.parent.slug
                else:
                    pare_slug = 'no-slug'
                response = functools.partial(get_dir_create_update_url)(self, lib.chapter.slug, lib.slug, pare_slug, dir.slug)
                self.assertEqual(response.status_code, 302)
                # response = functools.partial(get_dir_create_update_url)(self, lib.chapter.slug, lib.slug, pare_slug, dir.slug, follow_p=True)
                # self.assertEqual(response.status_code, 200)

    def test_topic_create_update(self):
        for dir in self.dirs:
            response = functools.partial(get_topic_create_update_url)(self, dir.lib.chapter.slug,
                                                                      dir.lib.slug, dir.slug, 'new_object')
            self.assertEqual(response.status_code, 302)
            response = functools.partial(get_topic_create_update_url)(self, dir.lib.chapter.slug, dir.lib.slug,
                                                                      dir.slug, 'new_object', follow_p=True)
            self.assertEqual(response.status_code, 200)
            for top in self.topics:
                response = functools.partial(get_topic_create_update_url)(self, dir.lib.chapter.slug,
                                                                      dir.lib.slug, dir.slug, top.slug)
                self.assertEqual(response.status_code, 302)
                # response = functools.partial(get_topic_create_update_url)(self, dir.lib.chapter.slug,
                #                                                       dir.lib.slug, dir.slug, top.slug, follow_p=True)
                # self.assertEqual(response.status_code, 200)

    def test_chapter_create_update(self):
        for chapter in self.chapters:
            response = functools.partial(get_chapter_create_update_url)(self, chapter.slug)
            self.assertEqual(response.status_code, 302)
            # response = functools.partial(get_chapter_create_update_url)(self, chapter.slug, follow_p=True)
            # self.assertEqual(response.status_code, 200)

        response = functools.partial(get_chapter_create_update_url)(self, 'new_object')
        self.assertEqual(response.status_code, 302)
        response = functools.partial(get_chapter_create_update_url)(self, 'new_object', follow_p=True)
        self.assertEqual(response.status_code, 200)

    def test_entry_create_update(self):
        for entry in self.entries:
            response = functools.partial(get_entry_create_update_url)(self, entry.topic.directory.lib.chapter.slug,
                                                                      entry.topic.directory.lib.slug,
                                                                      entry.topic.directory.slug,
                                                                      entry.topic.slug, entry.slug)
            self.assertEqual(response.status_code, 302)
            # response = functools.partial(get_entry_create_update_url)(self, entry.topic.directory.lib.chapter.slug,
            #                                                           entry.topic.directory.lib.slug,
            #                                                           entry.topic.directory.slug,
            #                                                           entry.topic.slug, entry.slug, follow_p=True)
            # self.assertEqual(response.status_code, 200)
        for topic in self.topics:

            response = functools.partial(get_entry_create_update_url)(self, topic.directory.lib.chapter.slug,
                                                                      topic.directory.lib.slug,
                                                                      topic.directory.slug, topic.slug, 'new_object')
            self.assertEqual(response.status_code, 302)
            response = functools.partial(get_entry_create_update_url)(self, topic.directory.lib.chapter.slug,
                                                                      topic.directory.lib.slug,
                                                                      topic.directory.slug,
                                                                      topic.slug, 'new_object', follow_p=True)
            self.assertEqual(response.status_code, 200)

    def test_lib_delete(self):
        ch = Chapter.objects.get(pk=1)
        lib = Lib.objects.create(name=name_generate(12), chapter=ch)
        response = self.client.post(reverse("all_libs:lib-delete", args=(ch.slug, lib.slug, )))
        self.assertEqual(response.status_code, 302)
        lib = Lib.objects.create(name=name_generate(12), chapter=ch)
        response = self.client.post(reverse("all_libs:lib-delete", args=(ch.slug, lib.slug, )), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_chapter_delete(self):
        ch = Chapter.objects.create(name=name_generate(12))
        response = self.client.post(reverse("all_libs:chapter-delete", args=(ch.slug,)))
        self.assertEqual(response.status_code, 302)
        ch = Chapter.objects.create(name=name_generate(12))
        response = self.client.post(reverse("all_libs:chapter-delete", args=(ch.slug,)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_directory_delete(self):
        lib = Lib.objects.get(pk=1)
        directory = Directory.objects.create(name=name_generate(12), lib=lib)
        response = self.client.post(reverse("all_libs:directory-delete", args=(lib.chapter.slug, lib.slug, directory.slug)))
        self.assertEqual(response.status_code, 302)
        directory = Directory.objects.create(name=name_generate(12), lib=lib)
        response = self.client.post(reverse("all_libs:directory-delete", args=(lib.chapter.slug, lib.slug, directory.slug)), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_topic_delete(self):
        directory = Directory.objects.get(pk=1)
        topic = Topic.objects.create(directory=directory, name=name_generate(12))
        response = self.client.post(reverse("all_libs:topic-delete", args=(directory.lib.chapter.slug,
                                                                           directory.lib.slug,
                                                                           directory.slug, topic.slug,)))
        self.assertEqual(response.status_code, 302)
        topic = Topic.objects.create(directory=directory, name=name_generate(12))
        response = self.client.post(reverse("all_libs:topic-delete", args=(directory.lib.chapter.slug,
                                                                           directory.lib.slug,
                                                                           directory.slug, topic.slug,)), follow=True)
        self.assertEqual(response.status_code, 200)
