from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView
from .forms import FormLivroVenda, FormLivroCompra
from .models import *
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "GET":
            return render(request, "registration/register.html")
        elif request.method == "POST":
            name = request.POST["name"]
            username = request.POST["username"]
            campus = request.POST["campus"]
            email = request.POST["email"]
            phone = request.POST["phone"]
            password = request.POST["password"]
            password2 = request.POST["password2"]

            if '' in [username, email, password, password2]:
                messages.error(request, 'Preencha todos os campos.')
                return render(request, "registration/register.html")

            if password != password2:
                messages.error(request, 'As senhas digitadas são diferentes.')
                return render(request,  "registration/register.html")

            arroba = email.index("@")
            if email[arroba:] != "@usp.br":
                messages.error(request, 'Utilize seu email USP.')
                return render(request,  "registration/register.html")

            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)           
                user.save()
                c = Customer(user= user, name = name , phone = phone, campus = campus)
                c.save() 
            except IntegrityError:
                messages.error(request, 'Usuário já existe.')
                return render(request, "registration/register.html")
            login(request, user)
            return redirect("home")	


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Usuário ou senha incorretos')

        context = {}
        return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def busca(request):
    if request.GET.get('q'):
        q = request.GET.get('q')
        results = Cad_venda.objects.filter(Q(title__icontains = q) | Q(author__icontains = q) | Q(genre__icontains = q) | Q(field__icontains = q) | Q(subject__icontains = q))
        return render(request, 'busca.html', {
            'results': results
        })
    return render(request, 'busca.html')  


def cad_venda(request):
    form = FormLivroVenda(request.POST or None)


    if request.method == 'POST':
        if form.is_valid():
            livro_venda = Cad_venda()
            livro_venda.title = form.cleaned_data['title']
            livro_venda.author = form.cleaned_data['author']
            livro_venda.genre = form.cleaned_data['genre']
            livro_venda.field = form.cleaned_data['field']
            livro_venda.subject = form.cleaned_data['subject']
            livro_venda.price = form.cleaned_data['price']
            f = form.save(commit=False)
            f.usuario = request.user
            f.save()
            messages.success(request, 'Livro cadastrado!')
        else:
            messages.error(request, 'Erro.')
    
    return render(request, 'cad_venda.html')


def cad_compra(request):
    form = FormLivroCompra(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            livro_compra = Cad_compra()
            livro_compra.title = form.cleaned_data['title']
            livro_compra.author = form.cleaned_data['author']
            livro_compra.genre = form.cleaned_data['genre']
            livro_compra.field = form.cleaned_data['field']
            livro_compra.subject = form.cleaned_data['subject']
            f = form.save(commit=False)
            f.usuario = request.user
            f.save()
            messages.success(request, 'Livro cadastrado!')
        else:
            messages.error(request, 'Erro.')
    
    return render(request, 'cad_compra.html')


def mostrar_livros_venda(request):
    return render(request, 'meus_livros_venda.html', {
        'meus_livros_venda': Cad_venda.objects.filter(usuario = request.user)
    })

def mostrar_livros_compra(request):
    return render(request, 'meus_livros_compra.html', {
        'meus_livros_compra': Cad_compra.objects.filter(usuario = request.user)
    })

def chat(request):
    if request.method == 'GET':
        livros = Mensagem.objects.values_list('livro', flat=True).filter(receiver = request.user).distinct()
        chats = []
        for livro in livros:
            chats_livro = []
            senders = Mensagem.objects.values_list('sender', flat=True).filter(receiver = request.user, livro = livro).distinct()
            for sender in senders:
                sender_receiver = []
                recebidas = Mensagem.objects.filter(receiver = request.user, livro = livro, sender = sender)
                enviadas = Mensagem.objects.filter(sender = request.user, livro = livro, receiver = sender)
                sender_receiver.append(recebidas)
                sender_receiver.append(enviadas)
                chats_livro.append(sender_receiver)
            chats.append(chats_livro)
        return render(request, 'chat.html', {
            'chats': chats
        })
    
    elif request.method == 'POST':
        conteudo = request.POST['mensagem']
        receiver = request.POST['receiver']
        livro = request.POST['livro']
        sender = request.user

        receiver = User.objects.get(pk = receiver)
        livro = Cad_venda.objects.get(pk = livro)

        m = Mensagem(
            conteudo = conteudo, 
            receiver = receiver,
            sender = sender,
            livro = livro
        )
        m.save()

        messages.success(request, 'Mensagem enviada')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))