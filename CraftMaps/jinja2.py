from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment, FileSystemLoader

def environment(**options):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    env.globals.update({
    'static': staticfiles_storage.url,
    'url': reverse,
    })
    return env
