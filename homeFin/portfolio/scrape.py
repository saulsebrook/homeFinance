from webbrowser import get
import re
from .models import PortHoldings
from .web_scrape import WebScrape

headers = {'User-agent': 'your bot 0.1'}

def get_airbus_value():
    #Get beautiful soup objects

    airbus = WebScrape('https://markets.businessinsider.com/stocks/airbus-stock?op=1', {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        })
    airbusPrice = airbus.scraper.find('span', class_="price-section__current-value")
    airbusHoldings = float(airbusPrice.text)
    #Convert to AUD
    eur_audConverter = WebScrape('https://www.x-rates.com/calculator/?from=EUR&to=AUD&amount=1', headers)
    euro = eur_audConverter.scraper.find('span', class_ ='ccOutputRslt').text
    rates = re.findall(r'\d+\.\d+', euro)
    airbusAUDTotal = float(rates[0]) * float(airbusHoldings)
    #airbusAUDTotal = float(totalPrice)
    AirAmt = PortHoldings.objects.get(nameFund="Airbus")
    AirValue = float(AirAmt.numHoldings) * float(airbusAUDTotal)

    return AirAmt, AirValue

def get_etherium_value():
    etherium = WebScrape('https://www.independentreserve.com/market/eth', headers)
    ethPrice = etherium.scraper.find('span', class_="currency-value__amount")
    EthAmt = PortHoldings.objects.get(nameFund="Etherium")
    EthValue = float(EthAmt.numHoldings) * float(ethPrice.text.replace(',','').strip('$'))

    return EthAmt, EthValue

def get_bitcoin_value():
    bitcoin = WebScrape('https://www.independentreserve.com/market/btc', headers)
    bitcoinPrice = bitcoin.scraper.find('span', class_="currency-value__amount")
    BitAmt = PortHoldings.objects.get(nameFund="Bitcoin")
    BitValue = float(BitAmt.numHoldings) * float(bitcoinPrice.text.replace(',','').strip('$'))
    
    return BitAmt, BitValue

def get_VDHG_value():
    vdhg = WebScrape('https://www.google.com/finance/quote/VDHG:ASX', headers)
    #Scrape stock price value from page
    vdhgPrice = vdhg.scraper.find('div', class_="YMlKec fxKbKc")
    #Calculate total price
    VDHGAmt = PortHoldings.objects.get(nameFund="VDHG", institution="CommSec")
    VDHGValue = float(VDHGAmt.numHoldings) * float(vdhgPrice.text.replace(',','').strip('$'))

    return VDHGAmt, VDHGValue

def get_VESG_value():
    vesg = WebScrape('https://www.google.com/finance/quote/VESG:ASX', headers)
    vesgPrice = vesg.scraper.find('div', class_="YMlKec fxKbKc")
    VESGAmt = PortHoldings.objects.get(nameFund="VESG")
    VESGValue = float(VESGAmt.numHoldings) * float(vesgPrice.text.replace(',','').strip('$'))

    return VESGAmt, VESGValue

def get_vanguard_value():
    vanguard = WebScrape('https://www.morningstar.com.au/Fund/FundReportPrint/5402', headers)
    vanguardPrice = vanguard.scraper.find_all('span', class_="YMWpadright")
    VanguardAmt = PortHoldings.objects.get(institution="Vanguard")
    VanguardValue = float(VanguardAmt.numHoldings) * float(vanguardPrice[4].text.replace(',','').strip('$'))

    return VanguardAmt, VanguardValue

def get_hbar_value():
    hbar = WebScrape('https://coinmarketcap.com/currencies/hedera/hbar/aud/', headers)
    hbarPrice = hbar.scraper.find('div', class_="priceValue")
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
