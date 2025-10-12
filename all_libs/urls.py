"""URL для приложения all_libs"""

from django.urls import path

from . import views



app_name = 'all_libs'
urlpatterns = [
    # Домашняя  страница
    path('', views.index, name='index'),

    # Страница с разделами
    path('chapters/', views.ChaptersListView.as_view(), name='chapter-list'),

    # Страница с библиотеками
    path('libs/ch_slug=<slug:ch_slug>/', views.LibListView.as_view(), name='lib-list'),

    # Страница определённой библиотеки
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/', views.DirectoriesListView.as_view(), name='dir-list'),

    # Страница директории. Параметр <str:status> может принимать значения "watching" и "editing" в зависимости от того,
    # какой шаблон мы используем: для редактирования директории (с ссылками на редактирование записей, удаление) и
    # просмотра
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/dir_slug=<slug:dir_slug>/status=<str:status>/', views.DirectoryDetailView.as_view(), name='dir-detail'),

    # Страница для добавления/изм новой библиотеки
    path('ch_slug=<slug:ch_slug>/create_or_update/lib_slug=<slug:lib_slug>/', views.LibCreateUpdateView.as_view(),
         name='lib-create-update'),

    # Страница для добавления и изменения названия новой директории
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/parent_dir_slug=<slug:parent_slug>/dir_slug=<slug:dir_slug>/',
         views.DirectoryCreateUpdateView.as_view(), name='dir-create-update'),

    # Страница для добавления и переименования подзаголовков
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/dir_slug=<slug:dir_slug>/topic_slug=<slug:topic_slug>/',
         views.TopicCreateUpdateView.as_view(),
         name='topic-create-update'),

    # Страница для добавления и редактирования новой записи
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/dir_slug=<slug:dir_slug>/topic_slug=<slug:topic_slug>/entry_slug=<slug:entry_slug>/',
         views.EntryCreateUpdateView.as_view(),
         name='entry-create-update'),

    # Страница для удаления записей
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/dir_slug=<slug:dir_slug>/topic_slug=<slug:topic_slug>/delete_entry/entry_slug=<slug:entry_slug>/',
         views.EntryDeleteView.as_view(), name="entry-delete"),

    # Страница для удаления подзаголовков
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/dir_slug=<slug:dir_slug>/delete_topic/topic_slug=<slug:topic_slug>/',
         views.TopicDeleteView.as_view(), name="topic-delete"),

    # Страница для удаления директории
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/delete_directory/dir_slug=<slug:dir_slug>/',
         views.DirectoryDeleteView.as_view(), name="directory-delete"),

    # Страница для добавления и изменения разделов
    path('ch_slug=<slug:ch_slug>/', views.ChapterCreateUpdateView.as_view(), name="chapter-create-update"),

    # Страница для удаления директории
    path('delete_chapter/ch_slug=<slug:ch_slug>/', views.ChapterDeleteView.as_view(), name="chapter-delete"),

    # Страница для удаления библиотеки
    path('ch_slug=<slug:ch_slug>/delete_lib/lib_slug=<slug:lib_slug>/', views.LibDeleteView.as_view(), name="lib-delete"),

    # Страница с командами для библиотеки
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/commands/', views.CommandsListView.as_view(), name="commands-list"),

    # Удаление команд
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/commands/delete', views.delete_commands, name="delete_commands"),

    # Добавление команд
    path('ch_slug=<slug:ch_slug>/lib_slug=<slug:lib_slug>/commands/command_slug=<slug:command_slug>',
         views.CommandCreateUpdateView.as_view(), name="command-create-update"),

]