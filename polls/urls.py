from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('<int:pk>/', views.Detalhe.as_view(), name='detalhe'),
    path('<int:pk>/resultados/', views.Resultados.as_view(), name='resultados'),
    path('<int:pergunta_id>/voto/', views.voto, name='voto'),
]