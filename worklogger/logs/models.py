# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
	duration = models.DecimalField(max_digits=10, decimal_places=3)
	log_date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date.today)
	date_logged = models.DateField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return str(self.project) + " - " + str(self.duration) + " - " + str(self.log_date)


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	total_hours = models.DecimalField(max_digits=10, decimal_places=3)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
