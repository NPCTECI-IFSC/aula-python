# encoding: utf-8
from __future__ import unicode_literals

from django.db import models

class Post(models.Model):
	texto = models.TextField()
	titulo = models.CharField(max_length=150)
	autor = models.ForeignKey('auth.User')
	data_criacao = models.DateTimeField(auto_now_add=True, editable=False)
	data_edicao = models.DateTimeField(auto_now=True, editable=False)
	like = models.IntegerField()

	def __str__(self):
		return self.titulo


class Comentario(models.Model):
	texto = models.TextField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	like = models.BooleanField()
	autor = models.ForeignKey('auth.User')
	data = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.texto
