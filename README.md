# LicytacjeKomorniczeSamochody-webScrapper
Gathers information about car bailiff auctions and compare it with prices at OTOMOTO(car ads web).

## Getting started
Run licytacje-samochody.py with Python 2.7(it may take some time)

 Markup : 1. Gathers information using BeautifulSoup from http://www.licytacje.komornik.pl/Notice/Filter/24?page=
          2. Process information with RegEx to get car detail
          3. Find this kind of cars (mark, make, year of production, engine) at Otomoto
          4. Get the avarage price and compare it with auction price
          5. Store all the data in excel using Pandas
          
## Results
![screenshot][output.png]
          

