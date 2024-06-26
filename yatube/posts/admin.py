from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'author',
        'group',
        'pub_date',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'description',
    )
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
