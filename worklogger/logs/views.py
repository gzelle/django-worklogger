# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template, forms
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from .models import Log, Project
from .forms import LogForm


# Create your views here.
class LogIndexView(generic.ListView):
    template_name = 'logs/index.html'
    context_object_name = 'logs_list'

    def get_queryset(self):
        user = self.request.user
        filter_value = self.request.GET.get('filter')
        view = self.request.GET.get('view')
        logs = Log.objects.filter(user=user)

        # If a date is selected, filter to that date
        if filter_value:

            if view == 'week':
                logs = user.profile.get_week_logs(filter_value)

            elif view == 'month':
                startdate = user.profile.get_month_startdate(filter_value)
                enddate = user.profile.get_month_enddate(filter_value)
                logs = logs.filter(log_date__gte=startdate).filter(log_date__lte=enddate)

            else:
                logs = Log.objects.filter(log_date=filter_value)

        user.profile.total_hours = logs.aggregate(Sum('duration'))['duration__sum']

        return logs


class LogDetail(generic.DetailView):
    model = Log
    template_name = 'logs/detail.html'


class LogDelete(DeleteView):
    model = Log
    success_url = reverse_lazy('logs:index')
    template_name = 'logs/delete.html'


class LogUpdate(UpdateView):
    model = Log
    fields = ['log_date']
    template_name_suffix = '_update'
    success_message = "Log updated"

    def get_success_url(self):
        return reverse('logs:detail', kwargs={'pk': self.object.pk})


class LogNew(CreateView):
    model = Log
    template_name = 'logs/new.html'
    form_class = LogForm


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ('project', 'duration', 'log_date')
        widgets = {'log_date': forms.DateField()}


def home(request):
    return render(request, 'home.html')
