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
import otomoto as ot
import xlsxwriter
#endregion
#region variables
NUM = []
FOT = []
DATA = []
OPIS = []
MIASTO = []
CENA = []
C_OT = []
L_OT = []
ROZN = []
LINK = []
VIN = []
ROK = []
SIL = []
MARK = []
MODEL = []
LAST = []
i = 0
oto = []
url = "http://www.licytacje.komornik.pl/Notice/Filter/24?page="
file_name = "licytacje_poznan.xlsx"
#endregion
for page in range(1, 5):
    print(page)
    url_p = url + str(page)
    webs = urllib2.urlopen(url_p)
    soup = BeautifulSoup(webs, "html.parser")
    right_table = soup.find('table', class_='wMax')
    rows = right_table.find_all('tr')
    if not re.search(r'\d+', rows[1].find('td').string):        #break jesli w tabeli None
        print('last page = ', page-1)
        break
    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 7:
            if car.miasto(tds[4].get_text(strip=True))[1] == 'wielkopolskie':
                opis = car.opis(tds[3].get_text(strip=True), True)
                data = car.data(tds[2].get_text(strip=True))
                NUM.append(int(tds[0].get_text(strip=True)))
                FOT.append(car.link(tds[6].find('a').get('href')) if len(tds[1].find('img').get('src'))<39 else '-')
                DATA.append(date(data[2],data[1],data[0]))
                OPIS.append(car.opis(tds[3].get_text(strip=True), False))
                MIASTO.append(car.miasto(tds[4].get_text(strip=True))[0])
                CENA.append(car.cena(tds[5].get_text(strip=True)))
                LINK.append(car.link(tds[6].find('a').get('href')))
                VIN.append(car.VIN(opis))
                ROK.append(car.rocznik(opis))
                SIL.append(car.silnik(OPIS[i]))
                MARK.append(car.marka(opis))
                MODEL.append(car.model(opis))
                LAST.append('-')
                print(MARK[i], MODEL[i])
                if MARK != '-' and MODEL[i] != '-':
                    oto = ot.cena_otomoto(car.search_mark(MARK[i]), MODEL[i], ROK[i],SIL[i])
                    C_OT.append(oto[0])
                    L_OT.append(oto[1])
                    if oto[0]:
                        ROZN.append(oto[0]-int(CENA[i]))
                    else:
                        ROZN.append(0)
                else:
                    C_OT.append(0)
                    L_OT.append('-')
                    ROZN.append(0)

                print(C_OT[i], L_OT[i], ROZN[i])
                i += 1


#region table-create
df=pd.DataFrame(NUM, columns=['No'])
df['Fot'] = FOT
df['Link'] = LINK
df['Marka'] = MARK
df['Model'] = MODEL
df['Rok'] = ROK
df['Silnik'] = SIL
df['Cena'] = CENA
df['Cena OT'] = C_OT
df['OTO'] = L_OT
df['Różnica'] = ROZN
df['Data'] = DATA
df['Miasto'] = MIASTO
df['Opis'] = OPIS
df['VIN'] = VIN
df['-'] = LAST


#endregion

#region excel-create
os.system("TASKKILL /F /IM excel.exe")
writer = pd.ExcelWriter(file_name, engine='xlsxwriter', date_format='dd.mmm.yyyy')
df.to_excel(writer, sheet_name='Sheet1', index=False, freeze_panes=(1, 0))
workbook = writer.book
worksheet = writer.sheets['Sheet1']
#endregion

#region excel-format
format1 = workbook.add_format({'num_format': '#,###'})
format2 = workbook.add_format({'align': 'center'})
format3 = workbook.add_format({'num_format': '0.0'})
worksheet.set_column('A:A', 4.6)                #numeracja
worksheet.set_column('B:B', 4)                  #foto
worksheet.set_column('C:C', 4)                  #link
worksheet.set_column('D:E', 12.5)                #marka/model
worksheet.set_column('F:F', 4.6)                #rocznik
worksheet.set_column('G:G', 4.6, format3)       #silnik
worksheet.set_column('H:H', 11, format1)        #cena
worksheet.set_column('I:I', 11, format1)        #cena otomoto
worksheet.set_column('J:J', 4)                  #link otomoto
worksheet.set_column('K:K', 8, format1)         #roznica cena
worksheet.set_column('L:L', 11.5)               #data
worksheet.set_column('M:M', 23, format2)        #miasto
worksheet.set_column('N:N', 23)                 #opis
worksheet.set_column('O:O', 4)                  #link

#endregion
writer.save()
os.startfile(file_name)
