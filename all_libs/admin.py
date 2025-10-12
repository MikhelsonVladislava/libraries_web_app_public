from django.contrib import admin
from .models import Lib, Topic, Entry, Directory, Chapter, Command

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name', )
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
class LibAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name', )
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class DirectoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'lib', 'parent')
    list_display_links = ('id', 'name', 'lib', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lib, LibAdmin)
admin.site.register(Directory, DirectoryAdmin)
admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Command)
# Register your models here.
