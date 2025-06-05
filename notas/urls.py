from django.urls import path
from notas import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notas', views.notas, name='notas'),
    path('adiciona/', views.adiciona, name='adiciona'),
    path("edita/<nr_item>", views.edita, name='edita'),
    path("deleta/<nr_item>", views.deleta, name='deleta'),
    path("visualiza/<nr_item>", views.visualiza, name='visualiza'),
]
