#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 17:58:48 2020

@author: hannousse
"""
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import whois
import time
import re


#################################################################################################################################
#               Domain registration age 
#################################################################################################################################

def domain_registration_length(domain):
    try:
        res = whois.whois(domain)
        expiration_date = res.expiration_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        # Some domains do not have expiration dates. The application should not raise an error if this is the case.
        if expiration_date:
            if type(expiration_date) == list:
                expiration_date = min(expiration_date)
            return abs((expiration_date - today).days)
        else:
            return 0
    except:
        return -1

def domain_registration_length1(domain):
    v1 = -1
    v2 = -1
    try:
        host = whois.whois(domain)
        hostname = host.domain_name
        expiration_date = host.expiration_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        if type(hostname) == list:
            for host in hostname:
                if re.search(host.lower(), domain):
                    v1 = 0
            v1= 1
        else:
            if re.search(hostname.lower(), domain):
                v1 = 0
            else:
                v1= 1  
        if expiration_date:
            if type(expiration_date) == list:
                expiration_date = min(expiration_date)
            return abs((expiration_date - today).days)
        else:
            v2= 0
    except:
        v1 = 1
        v2 = -1
        return v1, v2
    return v1, v2

#################################################################################################################################
#               Domain recognized by WHOIS
#################################################################################################################################

 
def whois_registered_domain(domain):
    try:
        hostname = whois.whois(domain).domain_name
        if type(hostname) == list:
            for host in hostname:
                if re.search(host.lower(), domain):
                    return 0
            return 1
        else:
            if re.search(hostname.lower(), domain):
                return 0
            else:
                return 1     
    except:
        return 1

#################################################################################################################################
#               Unable to get web traffic (Page Rank)
#################################################################################################################################
import urllib

def web_traffic(short_url):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + short_url).read(), "xml").find("REACH")['RANK']
        except:
            return 0
        return int(rank)


#################################################################################################################################
#               Domain age of a url
#################################################################################################################################

import json
from datetime import datetime, timezone
from dateutil.parser import isoparse

def domain_age(url_string):
    pattern = r"(?:http[s]?://)?(?:[a-zA-Z0-9]+\.)*([a-zA-Z0-9-]+\.[a-zA-Z]{2,})"
    match = re.search(pattern, url_string)

    if match:
        domain = match.group(1)
    else:
        return "Domain name could not be extracted"

    # domain = url_string.split("//")[-1].split("/")[0].split('?')[0].split('.')[-2] +\
    #     '.' + url_string.split(".")[-1]

    # show = "https://input.payapi.io/v1/api/fraud/domain/age/" + url
    # r = requests.get(show)

    url = "https://whois40.p.rapidapi.com/whois"
    querystring = {"q":domain}
    headers = {
        "X-RapidAPI-Key": "190b82c316mshc9184c61d2f5a8cp19d976jsnd9a7b2d25c3a",
        "X-RapidAPI-Host": "whois40.p.rapidapi.com"
    }

    r = requests.get(url, headers=headers, params=querystring)
    # print(r.status_code)
    if r.status_code == 200:
        data = r.text
        # print(data)
        jsonToPython = json.loads(data)
        try:
            creation_date = jsonToPython['creationDate']
            creation_date = isoparse(creation_date)
            today = datetime.now(timezone.utc)
            difference = today - creation_date
            result = difference.days
            # print(result)
            return result
        except:
            # print(-2)
            return -2
    else:    
        # print(-1)   
        return -1

    
# address = 'https://support-appleld.com.secureupdate.duilawyeryork.com/ap/89e6a3b4b063b8d/?cmd=_update&dispatch=89e6a3b4b063b8d1b&locale=_'
# domain_age(address)
#################################################################################################################################
#               Global rank
#################################################################################################################################

def global_rank(domain):
    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })
    
    try:
        return int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        return -1


#################################################################################################################################
#               Google index
#################################################################################################################################


from urllib.parse import urlencode

def google_index(url):
    #time.sleep(.6)
    user_agent =  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent' : user_agent}
    query = {'q': 'site:' + url}
    google = "https://www.google.com/search?" + urlencode(query)
    data = requests.get(google, headers=headers)
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), "html.parser")
    try:
        if 'Our systems have detected unusual traffic from your computer network.' in str(soup):
            return -1
        check = soup.find(id="rso").find("div").find("div").find("a")
        #print(check)
        if check and check['href']:
            return 0
        else:
            return 1
        
    except AttributeError:
        return 1

#print(google_index('http://www.google.com'))
#################################################################################################################################
#               DNSRecord  expiration length
#################################################################################################################################

import dns.resolver

def dns_record(domain):
    try:
        nameservers = dns.resolver.query(domain,'NS')
        if len(nameservers)>0:
            return 0
        else:
            return 1
    except:
        return 1

#################################################################################################################################
#               Page Rank from OPR
#################################################################################################################################


def page_rank(key, domain):
    url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domain
    try:
        request = requests.get(url, headers={'API-OPR':key})
        result = request.json()
        result = result['response'][0]['page_rank_integer']
        if result:
            return result
        else:
            return 0
    except:
        return -1