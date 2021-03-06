#-*- coding: utf-8 -*-
from django.shortcuts import render
import urllib.request
from bs4 import BeautifulSoup

def index(request, platform, btag):

    # fix Makkukurīmī#1513 btag (non ascii character)
    # accept btags with hash (minor)
    # main page with select for platform and input for btag
    # better rwd view

    if platform not in ['pc', 'psn', 'xbl']:
        return notFound(request)

    urlopen = urllib.request.urlopen('http://playoverwatch.com/pl-pl/career/' + platform + '/' + btag)
    person = Person(btag)
    soup = BeautifulSoup(urlopen, 'html.parser')

    isOK = soup.find('div', attrs={'class':'u-center'})
    if isOK is None:
        return render(request, '404.html')

    level = soup.find('div', attrs={'class':'u-center'}).text
    total = getTotal(soup)
    shotcaller = getShotcaller(soup)
    teammate = getTeammate(soup)
    sportsmanship = getSportsmanship(soup)

    endorsement = Endorsement(total, level, shotcaller, sportsmanship, teammate)

    return render(request, 'index.html', {'endorsement': endorsement, 'person': person})


def getTotal(soup):
    total = soup.find('svg', attrs={'class':'EndorsementIcon-border--shotcaller'})
    if total is None:
        return 0
    else:
        return total['data-total']

def getShotcaller(soup):
    total = soup.find('svg', attrs={'class':'EndorsementIcon-border--shotcaller'})
    if total is None:
        return 0
    else:
        return total['data-value']

def getTeammate(soup):
    total = soup.find('svg', attrs={'class':'EndorsementIcon-border--teammate'})
    if total is None:
        return 0
    else:
        return total['data-value']

def getSportsmanship(soup):
    total = soup.find('svg', attrs={'class':'EndorsementIcon-border--sportsmanship'})
    if total is None:
        return 0
    else:
        return total['data-value']

class Endorsement(object):
    total = 0
    level = 0
    shotcaller = 0
    sportsmanship = 0
    teammate = 0

    def __init__(self, total, level, shotcaller, sportsmanship, teammate):
        self.total = total
        self.level = level
        self.shotcaller = shotcaller
        self.sportsmanship = sportsmanship
        self.teammate = teammate

class Person(object):
    btag = ""
    def __init__(self, btag):
        self.btag = btag

def notFound(request):
    return render(request, '404.html')
