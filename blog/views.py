from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from .forms import PostForm
from .models import Post

def create_post(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.like = 0
			try:
				post.save()
				return redirect(reverse('blog:list'))
			except Exception as e:
				print(e)
	else:
		form = PostForm()
	return render(request, 'create_post.html', {'form': form})

def list_posts(request):
	posts = Post.objects.all()
	return render(request, 'posts.html', {'posts': posts})

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
