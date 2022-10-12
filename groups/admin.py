from django.contrib import admin
from .models import Group


class GroupAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "slug", "description")
    empty_value_display = "-пусто-"


admin.site.register(Group, GroupAdmin)