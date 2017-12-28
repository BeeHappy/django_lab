from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views import View
from .models import Journal


def process_request(request):
    if not 'cart' in request.session:
        request.session['cart'] = []
    if 'subscribe' in request.POST:
        journal_id = int(request.POST['subscribe'])
        if Journal.objects.filter(id=journal_id).exists():
            request.session['cart'].append(journal_id)
            request.session.modified = True
    elif 'cancel' in request.POST:
        journal_id = int(request.POST['cancel'])
        if Journal.objects.filter(id=journal_id).exists():
            request.session['cart'] = [x for x in request.session['cart'] if not x == journal_id]
            request.session.modified = True


class Index(View):
    template_name = "journals/index.html"

    def get(self, request):
        if not 'cart' in request.session:
            request.session['cart'] = []
        journals = Journal.objects.order_by('name')
        subscribed = [(journal.id in request.session['cart']) for journal in journals]
        prices = [journal.subscription_fee for journal in journals if journal.id in request.session['cart']]
        journals_zipped = zip(subscribed, journals)
        journals = [{'in_cart': in_cart, 'info': journal} for in_cart, journal in journals_zipped] 
        template = loader.get_template(self.template_name)
        context = {'journals': journals, 'items': len(prices), 'price': sum(prices)}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        process_request(request)
        return HttpResponseRedirect('/journals/')


class Cart(View):
    template_name = "journals/cart.html"

    def get(self, request):
        if not 'cart' in request.session:
            request.session['cart'] = []
        journals = Journal.objects.order_by('name')
        subscribed = [(journal.id in request.session['cart']) for journal in journals]
        prices = [journal.subscription_fee for journal in journals if journal.id in request.session['cart']]
        journals_zipped = zip(subscribed, journals)
        journals = [{'in_cart': in_cart, 'info': journal} for in_cart, journal in journals_zipped if journal.id in request.session['cart']] 
        template = loader.get_template(self.template_name)
        context = {'journals': journals, 'items': len(prices), 'price': sum(prices)}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        process_request(request)
        return HttpResponseRedirect('/journals/cart/')


class Info(View):
    template_name = "journals/info.html"

    def get(self, request, journal_id):
        if not 'cart' in request.session:
            request.session['cart'] = []
        journals = Journal.objects.order_by('name')
        subscribed = [(journal.id in request.session['cart']) for journal in journals]
        prices = [journal.subscription_fee for journal in journals if journal.id in request.session['cart']]
        journal = None
        publisher = None
        if Journal.objects.filter(id=journal_id).exists():
            journal = Journal.objects.get(id=journal_id)
            publisher = journal.publisher
        in_cart = (journal_id in request.session['cart'])
        template = loader.get_template(self.template_name)
        context = {'journal': journal, 'in_cart': in_cart, 'publisher': publisher, 'items': len(prices), 'price': sum(prices)}
        return HttpResponse(template.render(context, request))

    def post(self, request, journal_id):
        process_request(request)
        return HttpResponseRedirect('/journals/journal/' + str(journal_id))


def index(request):
    if not 'cart' in request.session:
        request.session['cart'] = []
    journals = Journal.objects.order_by('name')
    subscribed = [(journal.id in request.session['cart']) for journal in journals]
    journals_zipped = zip(subscribed, journals)
    journals = [{'in_cart': in_cart, 'info': journal} for in_cart, journal in journals_zipped] 
    template = loader.get_template('journals/index.html')
    context = {'journals': journals}
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

