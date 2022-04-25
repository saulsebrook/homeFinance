from json import load
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import PortHoldings
from django.urls import reverse
from .scrape import scrapeData
from .web_scrape import WebScrape

def index(request):

    holdings, totalValue, holdingsDatabase = scrapeData()
  
    #Dictionary of variables created to be passed to template
    context = {'holdings': holdings,
            'totalValue': totalValue,
            'holdingsDatabase': holdingsDatabase,

            }
    
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request)) #Other way to do it => return render(request, 'myfirst.html', context)
    
def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))

def addrecord(request):
        x = request.POST['nameFund']
        y = request.POST['numHoldings']
        z = request.POST['institution']

        portfolio = PortHoldings(nameFund=x, numHoldings=y, institution=z)
        portfolio.save()

        return HttpResponseRedirect(reverse('index'))

def delete(request, id):
    portEntry = PortHoldings.objects.get(id=id)
    portEntry.delete()
    return HttpResponseRedirect(reverse('index'))

def pop(request):
    portEntry = PortHoldings.objects.all().values()
    template = loader.get_template('pop.html')
    context = {
        'portEntry': portEntry
        }
    return HttpResponse(template.render(context, request))

def modify(request, id):
    portEntry = PortHoldings.objects.get(id=id)
    template = loader.get_template('modify.html')
    context = {
        'portEntry': portEntry
    }
    return HttpResponse(template.render(context, request))

def modifyRecord(request, id):
    fund = request.POST['fund']
    holdings = request.POST['holdings']
    institution = request.POST['institution']
    portfolio = PortHoldings.objects.get(id=id)
    portfolio.fundName = fund
    portfolio.numHoldings = holdings
    portfolio.institution = institution
    portfolio.save()
    return HttpResponseRedirect(reverse('index'))