from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from django import template
from .models import Rubric, Article

register = template.Library()


admin.site.register(Rubric, DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',

    ),
    list_display_links=(
        'indented_title',
    ),)
admin.site.register(Article)




