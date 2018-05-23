# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import generic

from .models import Log, Project

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'logs/index.html'
    context_object_name = 'logs_list'

    def get_queryset(self):
    	logs = Log.objects.filter(user=self.request.user)
        return Log.objects.all


class DetailView(generic.DetailView):
    model = Log
    template_name = 'logs/detail.html'


class ResultsView(generic.DetailView):
    model = Log
    template_name = 'logs/results.html'
