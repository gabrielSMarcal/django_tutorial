import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Pergunta

class TesteModeloPergunta(TestCase):
    def teste_foi_publicado_recentemente_com_pergunta_futura(self):
        tempo = timezone.now() + datetime.timedelta(days=30)
        pergunta_futura = Pergunta(data_da_publicacao=tempo)
        self.assertIs(pergunta_futura.foi_publicado_recentemente(), False)
        
    def teste_foi_publicado_recentemente_com_pergunta_antiga(self):
        tempo = timezone.now() - datetime.timedelta(days=1, seconds=1)
        pergunta_antiga = Pergunta(data_da_publicacao=tempo)
        self.assertIs(pergunta_antiga.foi_publicado_recentemente(), False)
        
    def teste_foi_puclicado_recentemente_com_pergunta_recente(self):
        tempo = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        pergunta_recente = Pergunta(data_da_publicacao=tempo)
        self.assertIs(pergunta_recente.foi_publicado_recentemente(), True)

def criar_pergunta(texto_da_pergunta, dias):
    tempo = timezone.now() + datetime.timedelta(days=dias)
    return Pergunta.objects.create(texto_da_pergunta=texto_da_pergunta,data_da_publicacao=tempo)

class TestePerguntaIndex(TestCase):
    def teste_sem_perguntas(self):
        resposta = self.client.get(reverse('polls:index'))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Não há pergunta disponível.')
        self.assertQuerySetEqual(resposta.context['lista_das_ultimas_perguntas'], [])
        
    def teste_pergunta_futura(self):
        criar_pergunta(texto_da_pergunta='Pergunta futura', dias=30)
        resposta = self.client.get(reverse('polls:index'))
        self.assertContains(resposta, 'Não há pergunta disponível.')
        self.assertQuerySetEqual(resposta.context['lista_das_ultimas_perguntas'], [])
        
    def teste_pergunta_futura_e_pergunta_antiga(self):
        pergunta = criar_pergunta(texto_da_pergunta='Pergunta antiga.', dias=-30)
        criar_pergunta(texto_da_pergunta='Pergunta futura.', dias=30)
        resposta = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            resposta.context['lista_das_ultimas_perguntas'],
            [pergunta],
        )
    
    def teste_duas_perguntas_antigas(self):
        pergunta1 = criar_pergunta(texto_da_pergunta='Pergunta antiga 1.', dias=-30)
        pergunta2 = criar_pergunta(texto_da_pergunta='Pergunta antiga 2.', dias=-5)
        resposta = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(
            resposta.context['lista_das_ultimas_perguntas'],
            [pergunta2, pergunta1]
        )
        
class TestePerguntaDetalhe(TestCase):
    def teste_pergunta_futura(self):
        pergunta_futura = criar_pergunta(texto_da_pergunta='Pergunta futura.', dias=5)
        url = reverse('polls:detalhe', args=(pergunta_futura.id,))
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 404)
        
    def teste_pergunta_antiga(self):
        pergunta_antiga = criar_pergunta(texto_da_pergunta='Pergunta antiga.', dias=-5)
        url = reverse('polls:detalhe', args=(pergunta_antiga.id,))
        resposta = self.client.get(url)
        self.assertContains(resposta, pergunta_antiga.texto_da_pergunta)