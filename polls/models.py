import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone

class Pergunta(models.Model):
    texto_da_pergunta = models.CharField(max_length=200)
    data_da_publicacao = models.DateTimeField('data publicada')
    
    def __str__(self):
        return self.texto_da_pergunta
    
    @admin.display(
        boolean=True,
        ordering='data_da_publicacao',
        description='Publicado recentemente?',
    )
    
    def foi_publicado_recentemente(self):
        agora = timezone.now()
        return agora - datetime.timedelta(days=1) <= self.data_da_publicacao <= agora
    
class Alternativa(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    texto_da_alternativa = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)
    
    def __str__(self):
        return self.texto_da_alternativa