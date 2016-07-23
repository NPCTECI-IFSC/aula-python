from django.shortcuts import render
from blog import models

def index(request):
	objects = models.Post.objects.all().order_by('-data_edicao')
	return render(request, 'base.html', {'objects' : objects})
