from django.contrib import admin

from tags import models
from tags.models import Tagged_Item


# Register your models here.



class TagsAdmin(admin.ModelAdmin):
    list_display = ['label']
    list_filter = ['label']
    list_per_page = 15
    search_fields = ['label']

admin.site.register(models.Tag, TagsAdmin)

@admin.register(Tagged_Item)
class Tagged_ItemAdmin(admin.ModelAdmin):
    list_display = ['object_id', 'tag', 'content_type', 'content_object']
    list_filter = ['tag', 'content_type',]
    list_per_page = 15
    search_fields = ['object_id', 'tag', 'content_type']
