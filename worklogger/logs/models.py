# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


# Create your models here.


class Project(models.Model):
	project_name = models.CharField(max_length=200)

	def __str__(self):
		return self.project_name

	def get_total_hours(self):
		logs = Log.objects.filter(project=self)
		return logs.aggregate(Sum('duration'))['duration__sum']

class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, blank=False, null=True, on_delete=models.SET_NULL)
    duration = models.IntegerField()
    log_date = models.DateField(auto_now=False, auto_now_add=False)
    date_logged = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
    	return str(self.log_date)