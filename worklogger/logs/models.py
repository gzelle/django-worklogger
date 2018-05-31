# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime
from datetime import timedelta
from django.utils.dateparse import parse_date


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
    total_hours = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)

    def get_week_logs(self, selected_date):
        if parse_date(selected_date).weekday() == 6:
            startdate = parse_date(selected_date)
        else:
            startdate = parse_date(selected_date) - timedelta(days=parse_date(selected_date).weekday()) - timedelta(
                days=1)

        return Log.objects.filter(user=self.user,
                                  log_date__in=[startdate,
                                                startdate + timedelta(days=1),
                                                startdate + timedelta(days=2),
                                                startdate + timedelta(days=3),
                                                startdate + timedelta(days=4),
                                                startdate + timedelta(days=5),
                                                startdate + timedelta(days=6)])

    def get_month_startdate(self, selected_date):
        month = datetime.datetime.strptime(selected_date, "%Y-%m-%d").month
        year = datetime.datetime.strptime(selected_date, "%Y-%m-%d").year
        return datetime.date(year, month, 1)

    def get_month_enddate(self, selected_date):
        month = datetime.datetime.strptime(selected_date, "%Y-%m-%d").month
        year = datetime.datetime.strptime(selected_date, "%Y-%m-%d").year

        if month in (4, 6, 9, 11):
            return datetime.date(year, month, 30)
        elif month == 2:
            if year % 4 == 0:
                return datetime.date(year, month, 29)
            else:
                return datetime.date(year, month, 28)
        else:
            return datetime.date(year, month, 31)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
