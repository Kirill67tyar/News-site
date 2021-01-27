from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from . import models
from django import forms




class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = models.News
        fields = '__all__'




class NewsAdmin(admin.ModelAdmin):

    form = NewsAdminForm

    list_display = 'id', 'title', 'category', 'created_it', 'updated_it', 'is_published', 'get_photo',

    list_display_links = 'id', 'title',

    search_fields = 'title', 'content',

    list_editable = 'is_published',

    list_filter = 'is_published', 'category'

    fields = 'title', 'category', 'content', 'photo', 'get_photo', 'is_published', 'views',\
             'created_it', 'updated_it',

    readonly_fields = 'get_photo', 'views', 'created_it', 'updated_it',

    save_on_top = True

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

        return 'Фото не установлено'

    get_photo.short_description = 'Миниатюра'



class CategoryAdmin(admin.ModelAdmin):

    list_display= 'id', 'title'

    list_display_links = 'id', 'title'

    search_fields = 'title',



admin.site.register(models.News, NewsAdmin)
admin.site.register(models.Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
admin.site.site_header = 'Управление новостями'
# Register your models here.
