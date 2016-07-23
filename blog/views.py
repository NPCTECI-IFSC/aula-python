from .forms import *
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def create_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.autor = request.user
			post.like = 0
			try:
				post.save()
				return redirect(reverse('blog:list'))
			except Exception as e:
				print(e)
	else:
		form = PostForm()
	return render(request, 'create_post.html', {'form': form})

@login_required
def list_posts(request):
	posts = Post.objects.all()
	return render(request, 'posts.html', {'posts': posts})

def detail_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = ComentarioForm(request.POST)
		comentario = form.save(commit=False)
		comentario.autor = request.user
		comentario.post = post
		comentario.save()
	form = ComentarioForm()
	return render(request, 'post.html', {'post': post, 'form': form})

@login_required
def edit_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			form.save()
			return redirect(reverse('blog:list'))
	else:
		form = PostForm(instance=post)
	return render(request, 'create_post.html', {'form': form})

@login_required
def remove_post(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()	
	return redirect(reverse('blog:list'))

def login_view(request):
	if not request.user.is_anonymous:
		return redirect(reverse('index'))
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username, password=password)
			if user:
				login(request, user)
				return redirect(reverse('blog:list'))
	else:
		form = LoginForm()
	return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
	logout(request)
	return redirect(reverse('index'))
