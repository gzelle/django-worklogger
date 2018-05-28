# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.views import generic
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Log, Project
from .forms import LogForm


# Create your views here.
class IndexView(generic.ListView):
	template_name = 'logs/index.html'
	context_object_name = 'logs_list'
	list_filter = 'log_date'

	def get_queryset(self):
		filter_value = self.request.GET.get('filter')
		if filter_value:
			logs = Log.objects.filter(
				user=self.request.user,
				log_date = filter_value
			)
			#self.request.user.profile.total_hours = logs.aggregate(Sum('duration'))['duration__sum']
			return logs
		else:
			logs = Log.objects.filter(user=self.request.user)
			#self.request.user.profile.total_hours = logs.aggregate(Sum('duration'))['duration__sum']
			return logs


class DetailView(generic.DetailView):
	model = Log
	template_name = 'logs/detail.html'


def log_new(request):
	if request.method == "POST":
		form = LogForm(request.POST)
		if form.is_valid():
			log = form.save(commit=False)
			log.user = request.user
			log.duration = request.POST.get('duration')
			log.log_date = request.POST.get('log_date')
			log.save()
			return redirect('logs:index')
	else:
		form = LogForm()
	return render(request, 'logs/new.html', {'form': form})


def home(request):
	return render(request, 'home.html')