# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Log, Project
from django.contrib.auth.models import User

class LogInline(admin.TabularInline):
	model = Log
	extra = 1

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Information',	{'fields': ['first_name', 'last_name', 'email']}),
    ]
    inlines = [LogInline]
    list_display = ('first_name', 'last_name', 'email')

class ProjectAdmin(admin.ModelAdmin):
	fields = ['project_name', 'get_total_hours']
	readonly_fields = ['get_total_hours']

	def get_total_hours(self, obj):
		return obj.get_total_hours()

admin.site.register(Project, ProjectAdmin)
admin.site.register(Log)