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

    #Sites where data is scraped from
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
    bitcoinPrice = soup3.find('span', class_="currency-value__amount")
    vdhgPrice = soup4.find('div', class_="YMlKec fxKbKc")
    vesgPrice = soup5.find('div', class_="YMlKec fxKbKc")
    vanguardPrice = soup6.find_all('span', class_="YMWpadright")
    hbarPrice = soup7.find('div', class_="priceValue")

    #Convert airbus euro stock price to AUD
    euro = soup1.find('span', class_ ='ccOutputRslt')
    conversion = euro.text
    rates = re.findall(r'\d+\.\d+', conversion)
    rate = rates[0]
    totalPrice = float(rate) * float(airbusHoldings)
    airbusAUDTotal = float(totalPrice)
    
    holdingsDatabase = PortHoldings.objects.all().values()
    output = ""
    for x in holdingsDatabase:
        output += x['nameFund']        

    #Get value of different holdings
    VDHGAmt = PortHoldings.objects.get(nameFund="VDHG", institution="CommSec")
    VDHGValue = float(VDHGAmt.numHoldings) * float(vdhgPrice.text.replace(',','').strip('$'))
    VESGAmt = PortHoldings.objects.get(nameFund="VESG")
    VESGValue = float(VESGAmt.numHoldings) * float(vesgPrice.text.replace(',','').strip('$'))
    VanguardAmt = PortHoldings.objects.get(institution="Vanguard")
    VanguardValue = float(VanguardAmt.numHoldings) * float(vanguardPrice[4].text.replace(',','').strip('$'))
    BitAmt = PortHoldings.objects.get(nameFund="Bitcoin")
    BitValue = float(BitAmt.numHoldings) * float(bitcoinPrice.text.replace(',','').strip('$'))
    EthAmt = PortHoldings.objects.get(nameFund="Etherium")
    EthValue = float(EthAmt.numHoldings) * float(ethPrice.text.replace(',','').strip('$'))
    HbarAmt = PortHoldings.objects.get(nameFund="Hbar")
    HbarValue = float(HbarAmt.numHoldings) * float(hbarPrice.text.replace(',','').strip('$'))
    AirAmt = PortHoldings.objects.get(nameFund="Airbus")
    AirValue = float(AirAmt.numHoldings) * airbusAUDTotal
    totalValue = (AirValue + EthValue + BitValue + VanguardValue + VESGValue + VDHGValue + HbarValue)

    holdings = {'funds':[{'fundName': VESGAmt.nameFund, "value": VESGValue},
                    {'fundName': VDHGAmt.nameFund, "value": VDHGValue},
                    {'fundName': EthAmt.nameFund, "value": EthValue},
                    {'fundName': BitAmt.nameFund, "value": BitValue},
                    {'fundName': AirAmt.nameFund, "value": AirValue},
                    {'fundName': VanguardAmt.institution, "value": VanguardValue},
                    {'fundName': HbarAmt.nameFund, "value": HbarValue},]
                } 
    
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