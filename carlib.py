#-*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import difflib
#region marki i modele
MARKS = {u'hummer': u'Hummer', u'uaz': u'Uaz', u'bentley': u'Bentley', u'mini': u'Mini', u'tesla': u'Tesla', u'skoda': u'\u0160koda', u'mg': u'MG', u'seat': u'Seat', u'subaru': u'Subaru', u'alfa-romeo': u'Alfa', u'polonez': u'Polonez', u'buick': u'Buick', u'lexus': u'Lexus', u'volvo': u'Volvo', u'opel': u'Opel', u'audi': u'Audi', u'rover': u'Rover', u'mitsubishi': u'Mitsubishi', u'maserati': u'Maserati', u'gmc': u'GMC', u'chevrolet': u'Chevrolet', u'porsche': u'Porsche', u'tata': u'Tata', u'microcar': u'Microcar', u'other': u'Inny', u'saab': u'Saab', u'smart': u'Smart', u'dodge': u'Dodge', u'honda': u'Honda', u'lada': u'Lada', u'pontiac': u'Pontiac', u'isuzu': u'Isuzu', u'cadillac': u'Cadillac', u'dacia': u'Dacia', u'hyundai': u'Hyundai', u'ligier': u'Ligier', u'volkswagen': u'Volkswagen', u'mazda': u'Mazda', u'aixam': u'Aixam', u'lamborghini': u'Lamborghini', u'infiniti': u'Infiniti', u'aston-martin': u'Aston Martin', u'land-rover': u'Land Rover', u'mercedes-benz': u'Mercedes', u'kia': u'Kia', u'ford': u'Ford', u'peugeot': u'Peugeot', u'daewoo': u'Daewoo', u'rolls-royce': u'Rolls-Royce', u'fiat': u'Fiat', u'lincoln': u'Lincoln', u'acura': u'Acura', u'jaguar': u'Jaguar', u'renault': u'Renault', u'jeep': u'Jeep', u'nissan': u'Nissan', u'toyota': u'Toyota', u'daihatsu': u'Daihatsu', u'suzuki': u'Suzuki', u'ferrari': u'Ferrari', u'chrysler': u'Chrysler', u'vw': u'VW', u'citroen': u'Citro\xebn', u'ssangyong': u'SsangYong', u'lancia': u'Lancia', u'bmw': u'BMW'}
MODELS = {u'mini': ['cooper', 'clubman', 'paceman', 'one', 'countryman', '1300', 'cooper-s', '1000'], u'ford': ['transit-connect', 'expedition', 'transit', 'probe', 'crown', 'focus', 'orion', 'kuga', 'escape', 'mustang', 'contour', 'galaxy', 'puma', 'granada', 'scorpio', 'transit-custom', 's-max', 'mondeo', 'cougar', 'capri', 'ecosport', 'fairlane', 'escort', 'sierra', 'ranchero', 'c-max', 'maverick', 'f150', 'festiva', 'explorer', 'courier', 'grand-c-max', 'focus-c-max', 'fiesta', 'windstar', 'taurus', 'ranger', 'fusion', 'streetka', 'f350', 'tourneo-connect', 'tourneo-custom', 'ka', 'taunus', 'f250', 'thunderbird', 'econoline', 'b-max', 'edge', 'tourneo-courier', 'transit-courier', 'excursion'], u'uaz': ['469-b'], u'bentley': ['continental-flying-spur', 'continental-gt', 'bentayga', 'arnage', 'mulsanne', 'turbo-r'], u'tesla': ['model-s', 'roadster', 'model-x'], u'skoda': ['citigo', 'rapid', 'felicia', 'praktik', 'roomster', 'favorit', 'fabia', 'superb', 'kodiaq', '120', 'octavia', 'yeti', '100', 'karoq', 'forman', '105'], u'seat': ['mii', 'ibiza', 'cordoba', 'arona', 'exeo', 'alhambra', 'ateca', 'altea', 'altea-xl', 'arosa', 'leon', 'inca', 'toledo'], u'subaru': ['g3x-justy', 'brz', 'levorg', 'tribeca', 'trezia', 'forester', 'outback', 'legacy', 'b9-tribeca', 'baja', 'svx', 'justy', 'xv', 'wrx', 'impreza'], u'alfa-romeo': ['146', '147', 'mito', '145', '155', 'gtv', '156', '159', 'alfasud', 'spider', 'brera', 'gt', 'giulietta', 'giulia', 'crosswagon', '164', '166', 'stelvio', '4c'], u'buick': ['enclave', 'regal', 'roadmaster', 'rendezvous', 'park-avenue', 'lucerne', 'riviera'], u'lexus': ['gs', 'lc', 'is', 'rx', 'gx', 'nx', 'ls', 'rc', 'sc', 'lx', 'es', 'ct'], u'opel': ['insignia', 'monterey', 'gt', 'movano', 'mokka', 'karl', 'ascona', 'calibra', 'agila', 'sintra', 'crossland-x', 'combo', 'meriva', 'cascada', 'manta', 'frontera', 'antara', 'vectra', 'grandland-x', 'signum', 'zafira', 'omega', 'corsa', 'astra', 'kadett', 'campo', 'tigra', 'vivaro', 'adam', 'rekord', 'senator', 'ampera'], u'audi': ['sq7', 'sq5', 'rs-q3', 'a8', 'rs4', 'rs5', '80', 'rs7', 'rs6', 'rs3', 'q3', 'q2', 'q5', 'q7', 's3', 's2', 's1', 's7', 's6', 's5', 's4', 'tt-s', 'quattro', 'a1', 'tt-rs', 'a3', 'a2', 'a5', 'a4', 'a7', 'a6', 'v8', '90', '100', 'cabriolet', 'a4-allroad', 'r8', 's8', 'a6-allroad', 'tt'], u'rover': ['216', '200', '214', '620', '600', '25', '45', '75', 'streetwise', '414', '416', 'mg', '400', '825', '420', '827', '820', '220'], u'maserati': ['granturismo', 'ghibli', 'biturbo', 'mc-stradale', 'indy', 'coupe', 'grancabrio', 'gransport', 'levante', 'quattroporte', '222'], u'suzuki': ['alto', 'kizashi', 'x-90', 'ignis', 'baleno', 'sj', 'splash', 'sx4-s-cross', 'liana', 'samurai', 'sx4', 'jimny', 'wagon-r', 'xl7', 'celerio', 'swift', 'grand-vitara', 'vitara'], u'gmc': ['envoy', 'acadia', 'typhoon', 'safari', 'savana', 'yukon'], u'chevrolet': ['hhr', 'equinox', 'colorado', 'corvette', 'suburban', 'trailblazer', 'matiz', 'cobalt', 'volt', 'avalanche', 'tacuma', 'captiva', 'chevelle', 'kalos', 'epica', 'lacetti', 'corsica', 'aveo', '1500', 'tahoe', 'silverado', 'malibu', 'monte-carlo', 'express', 'ssr', 'astro', 'rezzo', 'trans-sport', 'apache', 'chevy-van', 'spark', 'evanda', 'k30', 'cruze', 'blazer', 'g', 'orlando', 'nubira', 'caprice', 'camaro', 's-10', 'impala', 'trax'], u'porsche': ['panamera', '911', '944', '718-boxster', '968', '928', '356', 'boxster', 'cayman', '924', '718-cayman', 'macan', 'cayenne'], u'tata': ['indigo', 'safari', 'indica', 'xenon'], u'microcar': ['m-go', 'ligier'], u'other': [], u'saab': ['9-3', '9-5', '900', '99', '9-3x-sportkombi', '9-7x', '9000', '90', '96'], u'smart': ['fortwo', 'roadster', 'forfour'], u'hummer': ['h2', 'h3', 'h1'], u'dacia': ['lodgy', 'logan-van', 'duster', '1310', 'logan', 'dokker-van', 'sandero-stepway', 'dokker', 'sandero'], u'lada': ['samara', 'niva', '2109', '110', '1117', '2103', '2107', '2106'], u'pontiac': ['g6', 'catalina', 'firebird', 'vibe', 'trans-am', 'bonneville', 'montana', 'trans-sport', 'grand-am', 'grand-prix', 'solstice'], u'isuzu': ['pick-up', 'trooper', 'd-max'], u'cadillac': ['brougham', 'allante', 'cts', 'eldorado', 'bls', 'seville', 'dts', 'sts', 'deville', 'fleetwood', 'srx', 'escalade'], u'honda': ['stream', 'civic', 'ridgeline', 'insight', 'nsx', 'logo', 'city', 'odyssey', 'shuttle', 'accord', 'cr-v', 'cr-z', 'jazz', 'prelude', 'legend', 'pilot', 'aerodeck', 'crx', 'hr-v', 's-2000', 'fr-v', 'integra'], u'peugeot': ['605', '604', '607', 'bipper', '308-cc', '307-cc', 'partner', '3008', '4008', 'expert', '207-cc', 'traveller', '4007', '407', '406', '405', '404', '508', '208', '308', '309', '205', '204', '207', '206', '301', '5008', '304', '306', '307', '108', 'boxer', '106', '107', '206-cc', '206-plus', 'rcz', '1007', '2008', '807', '806'], u'hyundai': ['veloster', 'pony', 'ix20', 'galloper', 'kona', 'i25', 'santamo', 'elantra', 'trajet', 'i40', 'xg-350', 'lantra', 'terracan', 'matrix', 'i20', 'accent', 'getz', 'xg-30', 'coupe', 'grand-santa-fe', 'h-1-starex', 'genesis', 'grandeur', 'ix55', 'atos', 'h-1', 'genesis-coupe', 'H-1\\/H300 2497ccm - 168KM 3.1t 08-11 2.5 crdi style+nawigacja', 'sonata', 'equus', 'ix35', 'santa-fe', 'ioniq', 'i30', 'i10', 'tucson', 'h200'], u'ligier': ['optima', 'x-too', 'nova'], u'volkswagen': ['crafter', 'golf', 'tiguan-allspace', 'cc', 'corrado', 't-roc', 'sharan', 'beetle', 'polo', 'multivan', 'eos', 'vento', 'caravelle', 'fox', 'jetta', 'touareg', 'passat', 'golf-sportsvan', 'bora', 'lupo', 'scirocco', 'touran', 'new-beetle', 'tiguan', 'buggy', 'caddy', 'karmann-ghia', 'california', 'arteon', 'transporter', 'phaeton', 'up', 'passat-cc', 'amarok', 'golf-plus', 'garbus', 'golf-sportvan'], u'mazda': ['mx-5', 'mx-6', 'xedos', '626', 'rx-7', 'mx-3', 'rx-8', 'demio', 'bt-50', 'cx-9', 'cx-7', 'cx-5', 'cx-3', '323', '3', '2', '5', '6', 'tribute', 'mpv', '121', 'seria-b', 'millenia', '929', 'premacy', '323f'], u'aixam': ['city', 'crossover', 'roadline', 'a741', 'a751', 'coupe', 'scouty-r', 'gto', 'a721', 'scouty', 'crossline'], u'acura': ['cl', 'tl', 'mdx', 'rsx', 'rl', 'integra'], u'infiniti': ['q50', 'qx30', 'q45', 'g', 'fx', 'qx', 'm', 'qx50', 'q30', 'ex', 'qx70', 'q60', 'q70'], u'aston-martin': ['db9-volante', 'v8-vantage-roadster', 'db11', 'v12-vanquish', 'db9', 'v8-vantage', 'rapide', 'vanquish'], u'land-rover': ['range-rover-sport', 'freelander', 'range-rover', 'range-rover-evoque', 'discovery-sport', 'defender', 'range-rover-velar', 'discovery'], u'mercedes-benz': ['klasa-g', 'klasa-e', 'klasa-b', 'klasa-c', 'klasa-a', 'w124-1984-1993', 'klasa-v', 'klasa-r', 'klasa-s', 'x-klasa', 'vaneo', 'gl', 'citan', 'w123', 'viano', 'vario', 'slk', 'clk', 'sprinter', 'cl', 'cla', 'clc', 'w201-190', '280', 'cls', 'mb-100', 'sl', 'ce-klasa', 'amg-gt', 'glk', 'gla', 'glc', 'gle', 'slr', 'Vito', 'ml', 'vito', 'gls', 'slc'], u'kia': ['pregio', 'magentis', 'carens', 'rio', 'retona', 'venga', 'sportage', 'shuma', 'niro', 'pride', 'sedona', 'optima', 'opirus', 'picanto', 'clarus', 'ceed', 'stonic', 'carnival', 'joice', 'sephia', 'pro-ceed', 'soul', 'stinger', 'sorento', 'cerato'], u'mitsubishi': ['outlander', 'colt', 'space-star', 'santamo', 'starion', 'space-runner', 'lancer-evolution', 'canter', 'l200', 'carisma', 'grandis', 'asx', '3000gt', 'l300', 'montero', 'pajero', 'galant', 'pajero-pinin', 'space-wagon', 'i-miev', 'eclipse', 'space-gear', 'l400', 'lancer', 'sigma'], u'polonez': ['atu', '1-5', 'caro', '1-6'], u'daewoo': ['leganza', 'nexia', 'tico', 'lanos', 'matiz', 'nubira', 'espero', 'chairman', 'kalos', 'korando', 'rezzo', 'evanda', 'lacetti', 'musso', 'tacuma'], u'rolls-royce': ['ghost', 'phantom', 'park-ward', 'silver-shadow', 'silver-cloud'], u'fiat': ['600', 'brava', 'bravo', '500x', 'idea', '132', 'x-1', 'seicento', 'sedici', 'freemont', 'qubo', 'panda', 'fiorino', 'palio', 'stilo', '124-spider', 'grande-punto', 'fullback', 'coupe', 'siena', '500l', 'strada', '500', 'multipla', 'cinquecento', 'marea', 'talento', 'punto', 'ducato', '126', '127', '128', 'barchetta', 'punto-2012', 'punto-evo', 'croma', 'tipo', 'doblo', 'ulysse', 'scudo', '125p', '124', 'albea', 'linea', 'uno'], u'mg': ['mgb', 'mgf', 'zt', 'midget', 'tf', 'zr', 'zs'], u'lamborghini': ['aventador', 'diablo', 'gallardo', 'huracan'], u'jaguar': ['xj', 'f-type', 'xj12', 'xk', 'xf', 'xe', 'f-pace', 'xk8', 'xjsc', 's-type', 'x-type', 'daimler'], u'renault': ['fluence', 'grand-scenic', 'captur', 'kadjar', 'fuego', 'modus', 'talisman', 'clio', 'safrane', '25', '21', 'scenic-conquest', 'coupe', 'trafic', '5', '4', 'latitude', 'master', 'megane', 'twingo', 'vel-satis', 'koleos', 'thalia', 'scenic-rx4', 'laguna', 'zoe', '11', '19', 'scenic', 'grand-espace', 'espace', 'kangoo', 'avantime', 'twizy', 'wind'], u'dodge': ['stratus', 'caliber', 'avenger', 'caravan', 'ram', 'neon', 'durango', 'grand-caravan', 'dart', 'challenger', 'intrepid', 'viper', 'spirit', 'charger', 'dakota', 'magnum', 'journey', 'nitro'], u'nissan': ['king-cab', 'patrol', 'np300-pickup', 'sentra', 'stanza', 'pixo', 'interstar', 'pulsar', 'navara', 'pathfinder', 'leaf', 'serena', '280-zx', '200-sx', 'silvia', 'pickup', 'qashqai-2', 'note', 'murano', 'tiida', 'gt-r', 'vanette', 'juke', 'rogue', 'cube', 'titan', 'altima', 'qashqai', 'sunny', 'nv200', 'xterra', 'x-trail', 'bluebird', '300-zx', 'primastar', '100-nx', 'frontier', '350-z', 'almera', 'primera', 'skyline', 'quest', '370-z', 'terrano', 'maxima', 'almera-tino', 'micra'], u'toyota': ['yaris-verso', '4-runner', 'picnic', 'hilux', 'iq', 'highlander', 'sienna', 'gt86', 'supra', 'venza', 'proace', 'c-hr', 'tacoma', 'avensis-verso', 'hiace', 'matrix', 'carina', 'mr2', 'corolla-verso', 'verso', 'tercel', 'prius', 'avensis', 'rav4', 'urban-cruiser', 'tundra', 'avalon', 'aygo', 'land-cruiser', 'sequoia', 'fj', 'previa', 'auris', 'paseo', 'starlet', 'camry', 'corolla', 'yaris', 'celica', 'verso-s', 'camry-solara'], u'daihatsu': ['copen', 'move', 'rocky', 'cuore', 'feroza', 'materia', 'sirion', 'terios', 'gran-move', 'charade', 'trevis', 'yrv'], u'volvo': ['seria-700', 'v70', 's80', '850', 'c70', 'v40', '340', 's70', 'c30', 'xc-60', 'xc-40', 'xc-70', 'xc-90', 'v60', '245', '262', 's90', 'seria-900', 'seria-200', 'v90', '780', '945', 'seria-300', 'seria-400', 's40', 'v50', 's60'], u'jeep': ['comanche', 'cj', 'patriot', 'renegade', 'cherokee', 'grand-cherokee', 'liberty', 'commander', 'wrangler', 'compass', 'willys'], u'ferrari': ['308', 'mondial', 'ff', 'f550', 'f12berlinetta', 'testarossa', 'f430', 'gtc4lusso', '812-superfast', '599gtb', '488', 'california', '512', '458-italia'], u'lincoln': ['mark-lt', 'mkz', 'continental', 'town-car', 'navigator', 'aviator', 'mkx'], u'chrysler': ['voyager', 'aspen', 'stratus', '300c', '300m', 'caravan', 'le-baron', 'neon', 'concorde', 'crossfire', 'gts', 'pacifica', 'grand-voyager', 'town-country', 'pt-cruiser', 'sebring', 'new-yorker', 'vision'], u'citroen': ['xsara', 'c4-aircross', 'xm', 'c-crosser', 'nemo', 'spacetourer', 'ds3', 'cx', 'zx', 'ax', 'c4-picasso', 'xantia', 'evasion', 'xsara-picasso', 'jumpy-combi', 'c6', 'c4-grand-picasso', 'c-elysee', 'jumper', '2-cv', 'c8', 'c3', 'c2', 'c1', 'saxo', 'bx', 'ds', 'c5', 'c4', 'ds4', 'ds5', 'c3-picasso', 'c3-pluriel', 'c3-aircross', 'berlingo', 'c4-cactus'], u'ssangyong': ['family', 'actyon', 'kyron', 'rodius', 'rexton', 'xlv', 'korando', 'musso', 'tivoli'], u'lancia': ['voyager', 'prisma', 'lybra', 'kappa', 'thema', 'dedra', 'musa', 'thesis', 'ypsilon', 'beta', 'phedra', 'delta', 'zeta', 'fulvia'], u'bmw': ['x5-m', 'x6-m', 'z4', 'm5', 'm4', 'm6', 'm3', 'm2', 'z3', '1m', 'z4-m', 'i8', 'i3', 'x2', 'x3', 'x1', 'x6', 'x4', 'x5', 'seria-1', 'seria-2', 'seria-3', 'seria-4', 'seria-5', 'seria-6', 'seria-7', 'seria-8']}
#endregion
def main():

    string1 = 'Samochód osobowy Ford Fiesta 1.6 D, nr rej. RLA10450, rok prod. 2009, kolor grafit, VIN: WF0JXXWPJJ9 ...Rozwiń nazwęSamochód osobowy Ford Fiesta 1.6 D, nr rej. RLA10450, rok prod. 2009, kolor grafit, VIN: WF0JXXWPJJ9P22238Zwiń nazwę'
    string5 = 'Poznań(wielkopolskie'
    # string2 = '1 875,00 zł'
    # string3 = '/Notice/Details/404585'
    # string4 = '13.07.2018'
    # delete = ['SAM', 'OS']
    # print opis(string1, True)
    # print VIN(opis(string1, True))
    # print cena(string2)
    # print rocznik(opis(string1, True))
    # print link(string3)
    # print data(string4)
    # print silnik(opis(string1, False))
    # print opisout(opis(string1, False))
    # print marka(opis(string1, True))
    # print model(opis(string1, True))
    print miasto(string5)

    # print difflib.SequenceMatcher(None, 'Beny', ['Bentley','Benz']).ratio()*100

def opisout(string):
    string =  re.sub('(?i)(SA)\w+', '', string, )
    string = re.sub('Ó.','',string)
    string = re.sub('ó.', '', string)
    return re.sub('(?i)(OS)\w+','', string)

def opis(string, znaki_spec):
    string = re.sub('(?i)r\.',' ',string)       #zeby mercedes nie rozpoznal r klasy
    index1 = string.find('+ inne')
    if index1!=-1:
        string = string[:index1]
    index2 = string.find('wę')  # jesli jest rozwni nazwe, to usuwamy poczatek i zwin nazwe
    if index2!=-1:
        string = string[(index2+3):]
        string = string[:(string.find('Zwi'))]
    if znaki_spec:
        string = re.sub('\W+', ' ', string)
    return string

def rocznik(opis):
    for word in opis.split(' '):
        if len(word) == 4 and word.isdigit():
            if 1950 < int(word) and int(word)<2030:
                return int(word)
    return '-'

def VIN(string):
    string = string.lower()
    vin = string.replace('vin:', '')
    for word in vin.rsplit(' '):
        if len(word) == 17:
            return 'https://www.autodna.pl/vin/'+word.upper()
    return '-'

def cena(string):
    index = string.find('z') -1
    price = string[:index]                  #usun wszystko po zł
    price = price.replace('\xc2\xa0','')    #usun spacje
    price = price.replace(',','.')
    try:
        return float(price)
    except:
        return '-'

def link(string):
    string = 'http://www.licytacje.komornik.pl'+string
    # return '=HIPERŁĄCZE("'+string+'"; "link")'
    return string

def data(string):
    dmy = string.split('.')
    return map(int, dmy)

def silnik(string):
    string = string.replace(',','.')
    try:
        string = re.search('\W\d\.\d', string).group()[1:]
        return float(string)
    except:
        if search_mark(marka(string)) == 'mercedes-benz':
            return (mercedes_silnik(string))
        return '-'

# def miasto(string):
#     index = string.find('(')
#     if index != -1:
#         return string[:index].lower().capitalize()
#     else:
#         return string
def miasto(string):
    string = string.replace(')','')
    list = string.split('(')
    if len(list)==2:
        return list[0], list[1]
    else:
        return string, ''

def marka(string):
    mark = '-'
    string = string.lower()
    words = string.split(' ')
    max = 0.0
    sim ={}
    for m in MARKS:
        similar = difflib.get_close_matches(MARKS[m].lower(), words, n=1, cutoff=0.7)
        if len(similar) != 0:
            sim[MARKS[m]] = similar[0]
    for s in sim:
        ratio = difflib.SequenceMatcher(None, sim[s], s.lower()).ratio()
        if ratio > max:
            max = ratio
            mark = search_mark(s)
    if mark == 'vw':
        mark = 'volkswagen'
    try:
        return MARKS[mark]
    except:
        return '-'


def model(string):
    mark = search_mark(marka(string))
    string = string.lower()
    words = string.split(' ')
    if mark:
        for w in words:
            sim = difflib.get_close_matches(w, MODELS[mark], n=1, cutoff=0.8)
            if len(sim) != 0:
                return sim[0]
    if mark == u'mercedes-benz':
        return(mercedes(string))
    return '-'

def mercedes(string):
    if re.search('[sgebcavrx]\d\d[0]\D', string):
        return 'klasa-'+re.search('[sgebcavrx]\d\d[0]\D', string).group()[0]
    words = string.split(' ')
    for w in words:
        for klasa in ['s','g','e','b','c','a','v','r','x']:
            if w == klasa:
                return 'klasa-'+klasa
    return '-'

def mercedes_silnik(string):
    string = string.lower()
    silnik =''
    if re.search('[sgebcavrx]\d\d[0]\W', string):
        silnik = re.search('[sgebcavrx]\d\d[0]\W', string).group()[1:4]
    if re.search('\W\d\d[0]\W', string):
        silnik = re.search('\W\d\d[0]\W', string).group()[1:4]
    if re.search(('\W\d\d[0][dc]'), string):
        silnik = re.search(('\W\d\d[0][dc]'), string).group()[1:4]
    try:
        return float(silnik)/100
    except:
        return '-'

    # if re.search
    # if re.search('[sgebcavrx]\d\d\d', string):
    #     print re.search('[sgebcavrx]\d\d\d', string).group()

def search_mark(key):
    for k, v in MARKS.items():
        if v == key:
            return k

if __name__ == "__main__":
    main()