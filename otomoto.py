#region import
#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import re
import carlib as car
from datetime import date
import difflib
import time
from mechanize import Browser
import ast
import requests
import traceback
#endregion

def makes():
    url = "https://www.otomoto.pl"
    MAKES = {}
    make_name = ''
    webs = urllib2.urlopen(url)
    soup = BeautifulSoup(webs, "html.parser")
    makes = soup.find('select', class_='custom searchFormParam')
    makes = makes.find_all('option')
    for make in makes:
        make_value = make['value']
        make_text = make.text
        num = re.search('\d+', make_text)
        if num:
            num = int(num.group())
        index = make_text.find('(')
        if index != -1:
            make_name = make_text[:(index-1)]
        if num > 10:
            MAKES[make_value] = make_name
    return MAKES

def models(marks):
    i=0
    url = "https://www.otomoto.pl"
    MODELS = {}

    br = Browser()
    for make in marks:
        MODEL_MAKE = []
        print make,'\t\t',(100*i/len(marks)),'%'
        if make:
            br.open(url)
            br.form = list(br.forms())[0]
            br.form["search[filter_enum_make]"] = [make,]
            response = br.submit()
            soup = BeautifulSoup(response, "html.parser")
            models = soup.find('section')['data-facets']
            index = models.find('filter_enum_model')
            models = models[index:]
            index1 = models.find('{')
            index2 = models.find('}')
            models = models[index1:(index2+1)]
            models = ast.literal_eval(models)
            for m in models:
                if m != 'other':
                    MODEL_MAKE.append(m)
            MODELS[make] = MODEL_MAKE
        print MODELS[make]
        i += 1
    return MODELS

def cena_otomoto(make, model,rok, silnik):
    try:
        print 'd0'
        t = time.time()
        print 'd1', round(time.time() - t, 2)
        CENA=[]
        avg = 0
        ua = 'Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/20100101 Firefox/18.0 (compatible;)'
        url = 'https://www.otomoto.pl/osobowe/?search%5Bnew_used%5D=on'
        br = Browser()
        br.addheaders = [('User-Agent', ua), ('Accept', '*/*')]
        br.set_handle_robots(False)
        br.open(url)
        print 'd2', round(time.time() - t, 2)
        br.form = list(br.forms())[0]
        print 'd3', round(time.time() - t, 2)
        print br.form
        br.form["search[filter_enum_make]"] = [make, ]
        print 'd4', round(time.time() - t, 2)
        print br.form
        if rok != '-':
            br.form["search[filter_float_year:from]"] = str(int(rok)-1)
            br.form["search[filter_float_year:to]"] = str(int(rok)+1)
        if silnik != '-':
            br.form["search[filter_float_engine_capacity:from]"] = str(int(float(silnik)*1000*0.75))
            br.form["search[filter_float_engine_capacity:to]"] = str(int(float(silnik)*1000*1.25))
        br.form["search[filter_enum_damaged]"] = ['0']
        br.form["search[filter_enum_no_accident]"] = ['0']
        response = br.submit()
        print 'd5', round(time.time() - t, 2)
        new_url = response.geturl()
        print 'd6', round(time.time() - t, 2)
        url_list = new_url.split('/?')
        if len(url_list) == 2:
            new_url = url_list[0]+'/'+model+'/?'+url_list[1]+'&page='
            for page in range(1, 2):
                newest_url = new_url+str(page)
                print 'd7', round(time.time() - t, 2)
                webs = br.open(newest_url)
                print 'd8', round(time.time() - t, 2)
                if re.search("search%5", webs.geturl()):
                    print 'd9', round(time.time() - t, 2)
                    soup = BeautifulSoup(webs, "html.parser")
                    print 'd10', round(time.time() - t, 2)
                    oferty = soup.find_all('article')
                    print 'd11', round(time.time() - t, 2)
                    for oferta in oferty:
                        print 'd12', round(time.time() - t, 2)
                        cena = oferta.find('span', class_ = 'offer-price__number').get_text(strip=True)
                        print 'd13', round(time.time() - t, 2)
                        cena = cena.replace(' ','').replace('PLN', '')
                        print 'd14', round(time.time() - t, 2)
                        try:
                            print 'd15', round(time.time() - t, 2)
                            CENA.append(int(cena))
                        except:
                            pass
                else:
                    break
            if len(CENA):
                print 'd16', round(time.time() - t, 2)
                avg = reduce(lambda x, y: x + y, CENA) / len(CENA)
            print 'd17', round(time.time() - t, 2)
            new_url = new_url + '1'
            if len(new_url) > 245:
                new_url = requests.get("http://tinyurl.com/" + "api-create.php?url=" + new_url).text
            print 'd18', round(time.time() - t, 2)
            return avg, new_url
        else:
            return 0, ''
    except:
        traceback.print_exc()
        return 0, ''


    # makes = makes.find_all('option')

# print cena_otomoto('volkswagen', 'passat', 2015, 1.9)

# print makes()
# print models(makes())




