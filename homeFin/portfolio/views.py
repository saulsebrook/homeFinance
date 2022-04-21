from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import bs4, requests, re, sys, os, pasteboard, json
from .models import PortHoldings
from django.urls import reverse

def index(request):
   
    #Get beautiful soup objects
    airbus = 'https://markets.businessinsider.com/stocks/airbus-stock?op=1'
    response = requests.get(airbus, headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        })
    #Used for debugging, will raise an error code if anything other than 200
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, features="html.parser")


    eur_aud = 'https://www.x-rates.com/calculator/?from=EUR&to=AUD&amount=1'
    res1 = requests.get(eur_aud, headers = {'User-agent': 'your bot 0.1'})
    res1.raise_for_status()
    soup1 = bs4.BeautifulSoup(res1.text, features="html.parser")

    eth = 'https://www.independentreserve.com/market/eth'
    res2 = requests.get(eth, headers = {'User-agent': 'your bot 0.1'})
    res2.raise_for_status()
    soup2 = bs4.BeautifulSoup(res2.text, features="html.parser")

    bitcoin = 'https://www.independentreserve.com/market/btc'
    res3 = requests.get(bitcoin, headers = {'User-agent': 'your bot 0.1'})
    res3.raise_for_status()
    soup3 = bs4.BeautifulSoup(res3.text, features="html.parser")

    vdhg = 'https://www.google.com/finance/quote/VDHG:ASX'
    res4 = requests.get(vdhg, headers = {'User-agent': 'your bot 0.1'})
    res4.raise_for_status()
    soup4 = bs4.BeautifulSoup(res4.text, features="html.parser")

    vesg = 'https://www.google.com/finance/quote/VESG:ASX'
    res5 = requests.get(vesg, headers = {'User-agent': 'your bot 0.1'})
    res5.raise_for_status()
    soup5 = bs4.BeautifulSoup(res5.text, features="html.parser")

    vanguard = 'https://www.morningstar.com.au/Fund/FundReportPrint/5402'
    res6 = requests.get(vanguard, headers = {'User-agent': 'your bot 0.1'})
    res6.raise_for_status()
    soup6 = bs4.BeautifulSoup(res6.text, features="html.parser")

    hedera = 'https://coinmarketcap.com/currencies/hedera/hbar/aud/'
    res7 = requests.get(hedera, headers = {'User-agent': 'your bot 0.1'})
    res7.raise_for_status()
    soup7 = bs4.BeautifulSoup(res7.text, features="html.parser")

    Bitcoins = 0.02947755
    Etheriums = 1.00141391
    Hbar = 	1052.12285742

    #Get stock prices
    airbusPrice = soup.find('span', class_="price-section__current-value")
    airbusHoldings = float(airbusPrice.text)
    ethPrice = soup2.find('span', class_="currency-value__amount")
    ethereumHolding = float(ethPrice.text.replace(',','').strip('$'))  * Etheriums
    bitcoinPrice = soup3.find('span', class_="currency-value__amount")
    bitcoinHolding = float(bitcoinPrice.text.replace(',','').strip('$'))  * Bitcoins
    vdhgPrice = soup4.find('div', class_="YMlKec fxKbKc")
    vdhgHolding = float(vdhgPrice.text.replace(',','').strip('$')) * 48
    vesgPrice = soup5.find('div', class_="YMlKec fxKbKc")
    vesgHolding = float(vesgPrice.text.replace(',','').strip('$')) * 65
    vanguardPrice = soup6.find_all('span', class_="YMWpadright")
    vanguardHolding = float(vanguardPrice[4].text.replace(',','').strip('$')) * 3212.25
    hbarPrice = soup7.find('div', class_="priceValue")
    #hbarHolding = 21
    hbarHolding = float(hbarPrice.text.replace(',','').strip('$')) * Hbar
  
    

    #Convert airbus euro stock price to AUD
    euro = soup1.find('span', class_ ='ccOutputRslt')
    conversion = euro.text
    rates = re.findall(r'\d+\.\d+', conversion)
    rate = rates[0]
    totalPrice = float(rate) * float(airbusHoldings)
    airbusAUDTotal = float(totalPrice) * 34

    #Calculate total investment value
    totalHoldings = int(vesgHolding + vdhgHolding + ethereumHolding + bitcoinHolding + airbusAUDTotal + vanguardHolding + hbarHolding)
    
    holdings = {'funds':[{'fundName': 'VESG', "value": int(vesgHolding)},
                    {'fundName': 'VDHG', "value": int(vdhgHolding)},
                    {'fundName': 'Ethereum', "value": int(ethereumHolding)},
                    {'fundName': 'Bitcoin', "value": int(bitcoinHolding)},
                    {'fundName': 'Airbus', "value": int(airbusAUDTotal)},
                    {'fundName': 'Vanguard', "value": int(vanguardHolding)},
                    {'fundName': 'HBar', "value": int(hbarHolding)},]
                } 
    holdingsDatabase = PortHoldings.objects.all().values()
    output = ""
    for x in holdingsDatabase:
        output += x['nameFund']        
    template = loader.get_template('index.html')
    #Create dictionary of all variables you want to pass to template
    context = {'holdings': holdings,
            'totalHoldings': totalHoldings,
            'holdingsDatabase': holdingsDatabase,
    }




    
    return HttpResponse(template.render(context, request))
    #Other way to do it
    #return render(request, 'myfirst.html', context)

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