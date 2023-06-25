from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# define o módulo de configuração padrão do Django para 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fbite.settings')

app = Celery('fbbite')

# Aqui, 'CELERY' significa a configuração do Celery será definida em 'settings.py'.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar módulos de tarefa de todos os aplicativos registrados.
app.autodiscover_tasks()