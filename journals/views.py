from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Journal


def index(request):
    journals = Journal.objects.order_by('name')
    template = loader.get_template('journals/index.html')
    request.session['1'] = 1
    request.session.modified = True
    context = {
            'journals': journals,
    }
    return HttpResponse(template.render(context, request))

def add_to_cart(request, journal_id):
    if Journal.objects.filter(id=journal_id).exists():
        request.session[journal_id] = 1
    request.session.modified = True
    journals = Journal.objects.order_by('name')
    template = loader.get_template('journals/index.html')
    context = {
            'journals': journals,
    }
    return HttpResponse(template.render(context, request))

