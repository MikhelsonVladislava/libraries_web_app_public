import random

from django.db import models
from uuid import uuid4
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from modules.services.units import unique_slugify

class Chapter(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения. Слаг.
        """
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('all_libs:lib-list', kwargs={'ch_slug': self.slug})

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "разделы"

    def get_not_delete_url(self):
        return self.get_absolute_url()

    def __str__(self):
        return f"{self.name}"

class Lib(models.Model):
    name = models.CharField(max_length=100, verbose_name="название")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name="раздел")
    site = models.URLField(null=True, max_length=120, verbose_name="Официальный сайт")
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Библиотека"
        verbose_name_plural = "библиотеки"

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения. Слаг.
        """
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('all_libs:dir-list', kwargs={'ch_slug': self.chapter.slug,
                                                    'lib_slug': self.slug})

    def get_not_delete_url(self):
        return self.get_absolute_url()

    def __str__(self):
        return f"{self.name}"

class Directory(MPTTModel):
    """id не должно быть 0"""
    name = models.CharField(max_length=30, unique=True, verbose_name="название")
    lib = models.ForeignKey(Lib, on_delete=models.CASCADE, verbose_name="библиотека")
    parent = TreeForeignKey('self', blank=True,
                                         null=True,
                                         related_name='children',
                                         on_delete=models.CASCADE, verbose_name="родительский заголовок")
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name="URL")

    def get_absolute_url(self):
        return reverse('all_libs:dir-detail', kwargs={'dir_slug': self.slug,
                                                      'lib_slug': self.lib.slug,
                                                      'ch_slug': self.lib.chapter.slug,
                                                      'status': 'watching'})

    def get_not_delete_url(self):
        return reverse('all_libs:dir-detail', kwargs={'dir_slug': self.slug,
                                                      'ch_slug': self.lib.chapter.slug,
                                                      'lib_slug': self.lib.slug,
                                                      'status': 'editing'})

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заголовок"
        verbose_name_plural = "заголовки"

    class MPTTMeta:
        order_insertion_by = ['date_added']


    def __str__(self):
        return f"{self.name}"

class Topic(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE, verbose_name="Родительский заголовок")
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        self.slug = unique_slugify(self, self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('all_libs:dir-detail', kwargs={'dir_slug': self.directory.slug,
                                                      'lib_slug': self.directory.lib.slug,
                                                      'ch_slug': self.directory.lib.chapter.slug,
                                                      'status': 'watching'}) \
               + f'#{self.slug}'

    def get_not_delete_url(self):
        return reverse('all_libs:dir-detail', kwargs={'dir_slug': self.directory.slug,
                                                      'lib_slug': self.directory.lib.slug,
                                                      'ch_slug': self.directory.lib.chapter.slug,
                                                      'status': 'editing'}) \
               + f'#{self.slug}'


    def __str__(self):
        return f"{self.name}"


    class Meta:
        verbose_name = "Подзаголовок"
        verbose_name_plural = "подзаголовки"


class Entry(models.Model):
    text = models.TextField(verbose_name="Текст")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Подзаголовок")
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=256, unique=True, db_index=True, verbose_name="URL")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "записи"

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        self.slug = unique_slugify(self, f"{self.text[:5]}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('all_libs:dir-detail', kwargs={'dir_slug': self.topic.directory.slug,
                                                      'lib_slug': self.topic.directory.lib.slug,
                                                      'ch_slug': self.topic.directory.lib.chapter.slug,
                                                      'status': 'watching'}) + f'#{self.slug}'

    def get_not_delete_url(self):
        return reverse('all_libs:dir-detail',
                       kwargs={'dir_slug': self.topic.directory.slug,
                               'lib_slug': self.topic.directory.lib.slug,
                               'ch_slug': self.topic.directory.lib.chapter.slug,
                               'status': 'editing'}) + f'#{self.slug}'


    def __str__(self):
        return f"{self.text[:200]}..."


class Command(models.Model):
    name = models.CharField(max_length=100, unique=True)
    about = models.TextField()
    lib = models.ForeignKey(Lib, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=256, unique=True)

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения. Слаг.
        """
        name = self.name
        symbols = 'qwertyuiopasdfghjklzxcvbnm-_'
        symbols_to_delete = '.(), !@\'"/\\&?#^:$;*~`[]{}<>%'
        for s in symbols_to_delete:
            name = name.replace(s, '')
        while self.__class__.objects.filter(slug=name).exists():
            random_string = ''
            for i in range(12):
                random_string+= random.choice(symbols)
            name = f"{name}-{random_string}"
        self.slug = name

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " - " + self.about[:15] + "..."

    def get_absolute_url(self):
        return reverse('all_libs:commands-list', kwargs={'lib_slug': self.lib.slug,
                                                         'ch_slug': self.lib.chapter.slug}) + f'#{self.slug}'


class UploadEntryPhoto(models.Model):
    image = models.ImageField(upload_to='upload_images/%Y/%m/%d', default=None)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)





# Create your models here.
