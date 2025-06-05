from django.shortcuts import render, redirect
from notas.models import Notas
from datetime import date, datetime
from django.http import HttpResponse

def home(request):
    return render(request, "home.html")

def notas(request):
    lista_itens = Notas.objects.order_by("-data")
    return render(request, "notas.html",
                  {'lista_itens': lista_itens})

def adiciona(request):
    if request.method == "POST":
        item = Notas()
        item.data = date.today()
        item.hora = datetime.now().time()
        item.titulo = request.POST['titulo']
        item.descricao = request.POST['descricao']
        item.save()
        return redirect("notas")
    return render(request,"adiciona.html")

def edita(request, nr_item):
    try:
        item = Notas.objects.get(pk=nr_item)
    except Notas.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "POST":
        item.data = date.today()
        item.hora = datetime.now().time()
        item.titulo = request.POST['titulo']
        item.descricao = request.POST['descricao']
        item.save()
        return redirect("notas")
    return render(request, "edita.html", {"item": item})

def deleta(request, nr_item):
    try:
        item = Notas.objects.get(pk=nr_item)
    except Notas.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "POST":
        item.delete()
        return redirect("notas")
    return render(request, "deleta.html", {"item": item})

def visualiza(request, nr_item):
    try:
        item = Notas.objects.get(pk=nr_item)
    except Notas.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "POST":
        return redirect("notas")
    return render(request, "visualiza.html", {"item": item})

