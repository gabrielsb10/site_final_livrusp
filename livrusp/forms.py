from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django import forms
from .models import *


class FormLivroVenda(ModelForm):
    class Meta:
        model = cad_venda
        fields = "__all__"

