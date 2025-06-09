from django.contrib import admin
from . models import Notas

# Register your models here.
admin.site.register(Notas)
admin.site.site_header = "Painel Administrativo"
admin.site.site_title = "Administração"
admin.site.index_title = "Bem-vindo ao Painel"
