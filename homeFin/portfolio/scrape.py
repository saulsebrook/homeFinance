from webbrowser import get
import bs4, requests, re, sys, os
from .models import PortHoldings

def get_airbus_value():
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
    airbusPrice = soup.find('span', class_="price-section__current-value")
    airbusHoldings = float(airbusPrice.text)
    #Convert to AUD
    eur_aud = 'https://www.x-rates.com/calculator/?from=EUR&to=AUD&amount=1'
    res1 = requests.get(eur_aud, headers = {'User-agent': 'your bot 0.1'})
    res1.raise_for_status()
    soup1 = bs4.BeautifulSoup(res1.text, features="html.parser")
    euro = soup1.find('span', class_ ='ccOutputRslt').text
    rates = re.findall(r'\d+\.\d+', euro)
    rate = rates[0]
    totalPrice = float(rate) * float(airbusHoldings)
    airbusAUDTotal = float(totalPrice)
    AirAmt = PortHoldings.objects.get(nameFund="Airbus")
    AirValue = float(AirAmt.numHoldings) * airbusAUDTotal

    return AirAmt, AirValue

def get_etherium_value():
    eth = 'https://www.independentreserve.com/market/eth'
    res2 = requests.get(eth, headers = {'User-agent': 'your bot 0.1'})
    res2.raise_for_status()
    soup2 = bs4.BeautifulSoup(res2.text, features="html.parser")
    ethPrice = soup2.find('span', class_="currency-value__amount")
    EthAmt = PortHoldings.objects.get(nameFund="Etherium")
    EthValue = float(EthAmt.numHoldings) * float(ethPrice.text.replace(',','').strip('$'))

    return EthAmt, EthValue

def get_bitcoin_value():
    bitcoin = 'https://www.independentreserve.com/market/btc'
    res3 = requests.get(bitcoin, headers = {'User-agent': 'your bot 0.1'})
    res3.raise_for_status()
    soup3 = bs4.BeautifulSoup(res3.text, features="html.parser")
    bitcoinPrice = soup3.find('span', class_="currency-value__amount")
    BitAmt = PortHoldings.objects.get(nameFund="Bitcoin")
    BitValue = float(BitAmt.numHoldings) * float(bitcoinPrice.text.replace(',','').strip('$'))
    
    return BitAmt, BitValue

def get_VDHG_value():
    vdhg = 'https://www.google.com/finance/quote/VDHG:ASX'
    res4 = requests.get(vdhg, headers = {'User-agent': 'your bot 0.1'})
    res4.raise_for_status()
    soup4 = bs4.BeautifulSoup(res4.text, features="html.parser")
    #Scrape stock price value from page
    vdhgPrice = soup4.find('div', class_="YMlKec fxKbKc")
    #Calculate total price
    VDHGAmt = PortHoldings.objects.get(nameFund="VDHG", institution="CommSec")
    VDHGValue = float(VDHGAmt.numHoldings) * float(vdhgPrice.text.replace(',','').strip('$'))

    return VDHGAmt, VDHGValue

def get_VESG_value():
    vesg = 'https://www.google.com/finance/quote/VESG:ASX'
    res5 = requests.get(vesg, headers = {'User-agent': 'your bot 0.1'})
    res5.raise_for_status()
    soup5 = bs4.BeautifulSoup(res5.text, features="html.parser")
    vesgPrice = soup5.find('div', class_="YMlKec fxKbKc")
    VESGAmt = PortHoldings.objects.get(nameFund="VESG")
    VESGValue = float(VESGAmt.numHoldings) * float(vesgPrice.text.replace(',','').strip('$'))

    return VESGAmt, VESGValue

def get_vanguard_value():
    vanguard = 'https://www.morningstar.com.au/Fund/FundReportPrint/5402'
    res6 = requests.get(vanguard, headers = {'User-agent': 'your bot 0.1'})
    res6.raise_for_status()
    soup6 = bs4.BeautifulSoup(res6.text, features="html.parser")
    vanguardPrice = soup6.find_all('span', class_="YMWpadright")
    VanguardAmt = PortHoldings.objects.get(institution="Vanguard")
    VanguardValue = float(VanguardAmt.numHoldings) * float(vanguardPrice[4].text.replace(',','').strip('$'))

    return VanguardAmt, VanguardValue

def get_hbar_value():
    hedera = 'https://coinmarketcap.com/currencies/hedera/hbar/aud/'
    res7 = requests.get(hedera, headers = {'User-agent': 'your bot 0.1'})
    res7.raise_for_status()
    soup7 = bs4.BeautifulSoup(res7.text, features="html.parser")
    hbarPrice = soup7.find('div', class_="priceValue")
    HbarAmt = PortHoldings.objects.get(nameFund="Hbar")
    HbarValue = float(HbarAmt.numHoldings) * float(hbarPrice.text.replace(',','').strip('$'))

    return HbarAmt, HbarValue
    
def scrapeData():    

    AirAmt, AirValue = get_airbus_value()
    EthAmt, EthValue = get_etherium_value()
    VESGAmt, VESGValue = get_VESG_value()
    VDHGAmt, VDHGValue = get_VDHG_value()
    BitAmt, BitValue = get_bitcoin_value()
    VanguardAmt, VanguardValue = get_vanguard_value()
    HbarAmt, HbarValue = get_hbar_value()
    
    holdingsDatabase = PortHoldings.objects.all().values()
    output = ""
    for x in holdingsDatabase:
        output += x['nameFund']        

    totalValue = (AirValue + EthValue + BitValue + VanguardValue + VESGValue + VDHGValue + HbarValue)

    holdings = {'funds':[{'fundName': VESGAmt.nameFund, "value": VESGValue},
                    {'fundName': VDHGAmt.nameFund, "value": VDHGValue},
                    {'fundName': EthAmt.nameFund, "value": EthValue},
                    {'fundName': BitAmt.nameFund, "value": BitValue},
                    {'fundName': AirAmt.nameFund, "value": AirValue},
                    {'fundName': VanguardAmt.institution, "value": VanguardValue},
                    {'fundName': HbarAmt.nameFund, "value": HbarValue},]
                } 
    return holdings, totalValue, holdingsDatabase

if __name__ == '__main__':
    scrapeData()
