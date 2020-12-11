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


# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "GET":
            return render(request, "registration/register.html")
        elif request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
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
                user = User.objects.create_user(
                    username, email, password)           
                user.save()
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
        results = Cad_venda.objects.filter(title = q)
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