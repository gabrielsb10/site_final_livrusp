from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('busca/', views.busca, name="busca"),
    path('cadastrar_livro_venda/', views.cad_venda, name="cad_venda"),
    path('cadastrar_livro_compra/', views.cad_compra, name="cad_compra"),
    path('meus_livros_para_venda/', views.mostrar_livros_venda, name="mostrar_livros_venda")
]