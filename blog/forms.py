# encoding: utf-8
from django import forms
from django.contrib.auth import authenticate
from .models import Post, Comentario


class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('titulo', 'texto')


class ComentarioForm(forms.ModelForm):

	class Meta:
		model = Comentario
		fields = ('texto', 'like')


class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

	def clean(self):
		super(LoginForm, self).clean()
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user:
			raise forms.ValidationError(u'Login ou senha inválidos')
		return self.cleaned_data
