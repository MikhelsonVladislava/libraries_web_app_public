from django.test import TestCase

from all_libs.models import Chapter, Directory, Lib, Topic, Entry, Command


class ChapterTestClass(TestCase):

    def test_save(self):
        Chapter(name='Тестовая глава').save()
        Chapter(name='Тестовая глава (ещё одна)').save()
        Chapter(name='My chapter_').save()

class LibTestCase(TestCase):

    def setUp(self) -> None:
        Chapter.objects.create(name='Тестовая глава 1')

    def test_save(self):
        ch1 = Chapter.objects.get(name='Тестовая глава 1')
        Lib(name='Тестовая библиотека (test)', chapter=ch1,
                                 site='http//:site/site/news.ru').save()
        Lib(name='test_library', chapter=ch1,
            site='http//:site/site/news.ru').save()


class DirectoryTestCase(LibTestCase):

    def setUp(self) -> None:
        super(DirectoryTestCase, self).setUp()
        ch1 = Chapter.objects.get(name='Тестовая глава 1')
        Lib.objects.create(name='Тестовая библиотека', chapter=ch1,
                                 site='http//:site/site/news.ru')

    def test_save(self):
        lib1 = Lib.objects.get(name='Тестовая библиотека')
        dir1 = Directory(name='Тестовая директория 1', lib=lib1).save()
        Directory(name='Тестовая директория2', parent=dir1, lib=lib1).save()


class TopicTestCase(DirectoryTestCase):

    def setUp(self) -> None:
        super(TopicTestCase, self).setUp()
        Directory.objects.create(name='Тестовая директория',
                                    lib=Lib.objects.get(name='Тестовая библиотека'))

    def test_save(self):
        dir1 = Directory.objects.get(name='Тестовая директория')
        Topic(name='Тестовый подзаголовок', directory=dir1).save()
        Topic(name='test_()-=', directory=dir1).save()

class EntryTestCase(TopicTestCase):

    def setUp(self) -> None:
        super().setUp()
        Topic.objects.create(name='Тестов. подзаголовок',
                                    directory=Directory.objects.get(name='Тестовая директория'))

    def test_save(self):
        t1 = Topic.objects.get(name='Тестов. подзаголовок')
        Entry(text='Тестовая запись', topic=t1).save()
        Entry(text='_Test', topic=t1).save()

class CommandTestCase(DirectoryTestCase):

    def test_save(self):
        lib1 = Lib.objects.get(name='Тестовая библиотека')
        Command(name='test_command(arg=arg1, *args, **kwargs)', about='Команда', lib=lib1)

# class UploadEntryPhoto(TopicTestCase):
#
#     def setUp(self) -> None:
#         super().setUp()
#         Topic.objects.create(name='Подзаголовок',
#                                     directory=Directory.objects.get(name='Тестовая директория'))
#
#     def test_save(self):
#         topic = Topic.objects.get(name='Подзаголовок')
#         entry = Entry.objects.create(text='Заааапись....', topic=topic)
#         UploadEntryPhoto(image=)