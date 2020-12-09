from django.db import models

# Create your models here.

class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.name

class cad_venda(models.Model):
	title = models.CharField(max_length=200, null=True)
	author = models.CharField(max_length=200, null=True)
	genre = models.CharField(max_length=200, null=True)
	field = models.CharField(max_length=200, null=True)
	subject = models.CharField(max_length=200, null=True)
	price = models.CharField(max_length = 50, null=True)

	def __str__(self):
		return self.title

