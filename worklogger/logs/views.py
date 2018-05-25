# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum
from django.shortcuts import render, redirect
from django.views import generic

from .models import Log, Project
from .forms import LogForm

# Create your views here.
total_hours = 0

class IndexView(generic.ListView):
	template_name = 'logs/index.html'
	context_object_name = 'logs_list'
	list_filter = 'log_date'

	def get_queryset(self):
		global total_hours
		filter_value = self.request.GET.get('filter')
		if filter_value:
			logs = Log.objects.filter(
				user=self.request.user,
				log_date = filter_value
			)
			total_hours = logs.aggregate(Sum('duration'))['duration__sum']
		else:
			logs = Log.objects.filter(user=self.request.user)
			total_hours = logs.aggregate(Sum('duration'))['duration__sum']
		return logs


class DetailView(generic.DetailView):
	model = Log
	template_name = 'logs/detail.html'


class ResultsView(generic.DetailView):
	model = Log
	template_name = 'logs/results.html'


def log_new(request):
	if request.method == "POST":
		form = LogForm(request.POST)
		if form.is_valid():
			log = form.save(commit=False)
			log.user = request.user
			log.duration = request.POST.get('duration')
			log.log_date = request.POST.get('log_date')
			log.save()
			return redirect('logs:detail', pk=log.pk)
	else:
		form = LogForm()
	return render(request, 'logs/new.html', {'form': form})
