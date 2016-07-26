from .forms import *
from .models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404

@login_required
# Decorator para restringir apenas para usuários logados
# Mais sobre Decorators: http://wiki.python.org.br/Decoradores_Python_(Pyt)m)ncihon_Decorators)
def create_post(request):
# Função para a página de criação de Posts, recebe a requisição como parametro
    if request.method == 'POST': # Caso a requisição seja do tipo POST (envio de formulário) precisamos processar o formulário
	form = PostForm(request.POST) # Instanciamos o formulário passando a requisição
	if form.is_valid(): # Verificamos se o formulário é válido conforme as validações da classe
	    post = form.save(commit=False) # Criamos uma instancia de Post, mas ainda não salvamos no banco de dados
	    post.autor = request.user # Definimos o usuário logado atualmente como autor do Post
	    post.like = 0 # Definimos o número de likes como 0 (gambiarras)
	    try:
		post.save() # Salvamos o Post no banco de dados
		return redirect(reverse('blog:list')) # Redirecionamos para a lista de Posts
	    except Exception as e:
		print(e)
    else:
        # Caso a requisição não seja do tipo POST, quer dizer que estamos só acessando a página
        form = PostForm() # Portanto instanciamos um formulário vazio a ser mostrado na página
    return render(request, 'create_post.html', {'form': form}) # Retornamos a página HTML injetando o formulário vazio

@login_required
def list_posts(request):
# Função para a página de listagem de Posts
    posts = Post.objects.all()
    # Recuperamos todos os Posts do banco de dados através da ORM do Django
    # Mais sobre ORM: http://turing.com.br/material/acpython/mod3/django/orm1.html
    return render(request, 'posts.html', {'posts': posts}) # Retornamos a página HTML injetando os Posts

def detail_post(request, pk):
# Função para a página de detalhes de um Post, recebe a requisição e uma chave como parametros
    # Procura pelo Post escolhido através da chave ou devolve um erro HTTP 404 caso não encontre
    # Mais sobre HTTP 404: https://pt.wikipedia.org/wiki/HTTP_404
    post = get_object_or_404(Post, pk=pk)
    # Novamente temos um formulário, portanto quando a requisição for de envio de dados precisamos processa-lo
    if request.method == 'POST':
	form = ComentarioForm(request.POST) # Instanciamos um formulário com a requisição
	comentario = form.save(commit=False) # Instanciamos um Comentário, mas ainda não salvamos no banco de dados
	comentario.autor = request.user # Definimos como autor do Comentário o usuário logado
	comentario.post = post # Definimos como Post do comentário o Post que está sendo visualizado
	comentario.save() # Salvamos o comentário no banco de dados
    form = ComentarioForm() # Caso a requisição não seja de envio de dados, novamente criamos um formulário vazio
    # Retornamos a página HTML injetando o Post que foi buscado no banco de dados, e o formulário de comentários
    return render(request, 'post.html', {'post': post, 'form': form})

@login_required
def edit_post(request, pk):
# Função para a página de edição de Posts, recebendo a requisição e uma chave como parametros
    # Novamente, procura pelo Post através da chave passada ou retorna um erro HTTP 404
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # Novamente temos que processar um formulário, mas dessa vez declaramos que a instancia é o Post buscado do banco
	form = PostForm(request.POST, instance=post)
	if form.is_valid():
	    form.save()
	    return redirect(reverse('blog:list'))
    else:
        # Caso não estejamos processando um formulário, não passamos a requisição como parametro
        # Mas passamos a instancia ainda sim, porque estaremos mostrando o formulário com os dados de um Post já cadastrado
	form = PostForm(instance=post)
    return render(request, 'create_post.html', {'form': form})

@login_required
def remove_post(request, pk):
# Função para a página de exclusão de um Post através da chave passada por parametro
    post = get_object_or_404(Post, pk=pk)
    post.delete() # Exclui do banco de dados o Post
    return redirect(reverse('blog:list'))

def login_view(request):
# Função para a página de login
    if not request.user.is_anonymous: # Verifica se o usuário já não está logado no sistema
	return redirect(reverse('index')) # Caso já esteja, redirecionamos imediatamente para a página inicial
    if request.method == 'POST':
	form = LoginForm(request.POST) # Novamente, processamos um formulário com a requisição
	if form.is_valid():
	    username = request.POST.get('username') # Recuperamos o username enviado no formulário
	    password = request.POST.get('password') # Recuperamos a senha enviada no formulário
            # Procuramos por um usuário no banco de dados que tenha este nome e esta senha
	    user = authenticate(username=username, password=password)
	    if user: # Caso encontremos um usuário com o usuário e a senha no banco
		login(request, user) # Autenticamos este usuário
		return redirect(reverse('blog:list')) # Redirecionamos para a lista de Posts
    else: # Caso a requisição seja simplesmente um acesso à página (GET)
	form = LoginForm() # Criamos um formulário vazio
    return render(request, 'login.html', {'form': form}) # Retornamos a página HTML injetando o formulário

@login_required
def logout_view(request):
# Função para logout, auto-explicativa
    logout(request)
    return redirect(reverse('index'))
