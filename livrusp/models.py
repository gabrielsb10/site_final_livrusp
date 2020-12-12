from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	campus = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class Cad_venda(models.Model):
	title = models.CharField(max_length=200, null=True)
	author = models.CharField(max_length=200, null=True)
	genre = models.CharField(max_length=200, null=True)
	field = models.CharField(max_length=200, null=True)
	subject = models.CharField(max_length=200, null=True)
	price = models.CharField(max_length=50, null=True)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="livros_venda")

	def __str__(self):
		return self.title

class Cad_compra(models.Model):
	title = models.CharField(max_length=200, null=True)
	author = models.CharField(max_length=200, null=True)
	genre = models.CharField(max_length=200, null=True)
	field = models.CharField(max_length=200, null=True)
	subject = models.CharField(max_length=200, null=True)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="livros_compra")

	def __str__(self):
		return self.title

class Mensagem(models.Model):
	conteudo = models.CharField(max_length=200, null=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enviadas")
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recebidas")
	date_sent = models.DateTimeField(default=timezone.now)
	livro = models.ForeignKey(Cad_venda, on_delete=models.CASCADE, related_name="mensagens")

