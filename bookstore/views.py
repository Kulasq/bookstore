from django.http import HttpResponse
from django.views import View
import subprocess
import os


class UpdateServerView(View):
    def post(self, request, *args, **kwargs):
        try:
            commands = [
                'cd /home/kulasq/bookstore',
                'git pull origin main',
                'source /home/kulasq/env/bin/activate',
                'pip install -r requirements.txt',
                'python manage.py collectstatic --noinput',
            ]

            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True)

            return HttpResponse('Deploy realizado com sucesso!', status=200)
        except Exception as e:
            return HttpResponse(f'Erro no deploy: {str(e)}', status=500)


def update_server(request):
    return UpdateServerView.as_view()(request)


def hello_world(request):
    return HttpResponse('Hello, World! v1 - Deploy Automático Funcionando!')