from django.db import models
from datetime import date, datetime


class Notas(models.Model):
    data = models.DateField(default=date.today)
    hora = models.TimeField(default=datetime.now().time())
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.titulo

