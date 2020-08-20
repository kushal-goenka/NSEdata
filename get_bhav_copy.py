import pandas as pd

import requests
import zipfile
import os

def get_range(year):
    from datetime import timedelta, date

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)

    dates = []

    for single_date in daterange(start_date, end_date):
    #     print(single_date.strftime("%Y-%m-%d"))
    #     print(single_date.strftime("%d%b%Y").upper())
        day = single_date.strftime("%d").upper()
        month = single_date.strftime("%b").upper()
        year = single_date.strftime("%Y").upper()

        if(single_date.strftime("%a").upper()=='SUN' or single_date.strftime("%a").upper()=='SAT'):
    #         print("Weekend")
            a = 1
        else:
            dates.append((day,month,year))
            
    return dates

def download_file(date):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
    print("Starting Download for date: ",date)
    day,month,year = date
    
    fileName = "cm{}{}{}bhav.csv".format(day,month,year)

    url = "https://archives.nseindia.com/content/historical/EQUITIES/{}/{}/{}.zip".format(year,month,fileName)
    
#     print(url)
#     print(requests.get(url,header,timeout=5))

    try:
        r = requests.get(url,header,timeout=5)
#         print(r)
        open("bhav/"+fileName+'.zip', 'wb').write(r.content)

        with open('bhav/'+fileName+'.zip', 'rb') as fileobj:
            z = zipfile.ZipFile(fileobj)
            z.extractall('bhav/')
            z.close()
        os.remove('bhav/'+fileName+'.zip')
    except:
        print("Didn't work: ",date)


years = [2008,2010]

for year in years:
    dates = get_range(year)
    for date in dates:
        download_file(date)
