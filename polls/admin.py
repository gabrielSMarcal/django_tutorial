from django.contrib import admin

from .models import Alternativa, Pergunta

class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 3

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['texto_da_pergunta']}),
        ('Informação de Data', {'fields': ['data_da_publicacao'], 'classes': ['colapso']}),
    ]
    inlines = [AlternativaInline]
    list_display = ['texto_da_pergunta', 'data_da_publicacao', 'foi_publicado_recentemente']
    list_filter = ['data_da_publicacao']
    search_fields = ['texto_da_pergunta']
    
    

admin.site.register(Pergunta, PerguntaAdmin)
