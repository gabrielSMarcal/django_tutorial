from typing import Any
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Alternativa, Pergunta

class Index(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lista_das_ultimas_perguntas'
    
    def get_queryset(self):
        return Pergunta.objects.filter(data_da_publicacao__lte=timezone.now()).order_by('-data_da_publicacao')[
            :5
        ]
    

class Detalhe(generic.DetailView):
    model = Pergunta
    template_name = 'polls/detalhe.html'
    
    def get_queryset(self):
        return Pergunta.objects.filter(data_da_publicacao__lte=timezone.now())
    


class Resultados(generic.DetailView):
    model = Pergunta
    template_name = 'polls/resultados.html'

def voto(request, pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    try:
        alternativa_selecionada = pergunta.alternativa_set.get(pk=request.POST['alternativa'])
    except (KeyError, Alternativa.DoesNotExist):
        return render(
            request,
            'polls/detalhe.html',
            {
                'pergunta': pergunta,
                'mensagem_de_erro': 'Você não selecionou uma alternativa',
            }
        )
    else:
        alternativa_selecionada.votos = F('votos') + 1
        alternativa_selecionada.save()
        return HttpResponseRedirect(reverse ('polls:resultados', args=(pergunta.id,)))