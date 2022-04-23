from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import PortHoldings
from django.urls import reverse
from .scrape import scrapeData

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