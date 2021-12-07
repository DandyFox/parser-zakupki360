from bs4 import BeautifulSoup # library for parsing func
import requests               # make request to main url
import pandas as pd           # make a spreadsheet and converting in XLSX file
import re                     
import datetime               # add date in table when your parsing and giving date for name file
from time import sleep        # delay of requests
from random import randint    # random seconds for delay


### Name of parametrs marks and link on site ###


main_url = input('Input page link:')
date_time = datetime.date.today()
df = pd.DataFrame(columns = ['Date','Name','Price','Link','Actuality','Category','Start date','End date','Customer','Delivery area','Sourse link'])
filtered_url = []
x = 1
print('Searching...')


#### Getting links of offers ####


while x <= 20:
    if x == 1:
        url = main_url
    else:
        url = f'{main_url}?page={str(x)}'
    
    
    request = requests.get(url)
    #sleep(randint(3, 5))
    data = BeautifulSoup(request.text, "html.parser")
    divs = data.find_all("div", class_="card-container ng-star-inserted")
    
    
    for div in divs:          
        links = data.find_all('a', class_='app-passive-link')
        for link in links:
            link = "https://zakupki360.ru" + link['href']
            if 'https://zakupki360.ru/tender' in link:
                filtered_url.append(link)
            else:
                pass
    x += 1


unique_url = list(set(filtered_url))


### Getting data from every once offer ####


y = 0
print('Getting offers...')
for line in unique_url:
    id_index = line.rfind('/')
    id = f"ZC-{date_time.year}-{line[id_index+1:]}"
    
    
    request = requests.get(line)
    #sleep(randint(3, 5))
    data = BeautifulSoup(request.text, "html.parser")
    divs = data.find_all("div", class_="dossier")
    
    
    for div in divs:    
        header_search = data.find('h1', class_='dossier__title').text
        rub_find = header_search.find('₽')
        if rub_find > -1:
            head_bad_index = header_search.rfind('(')
            header = header_search[0:head_bad_index]
        else:
            header = header_search
            
        
        theme = data.find('a', class_='link ng-star-inserted').text


        try:
            time_data = data.find('div', class_='dossier__column data ng-star-inserted')
            time = time_data.find('span', class_='ng-star-inserted').text
            time_search = re.findall('\d\d\S\d\d\S\d{4}',time)
            time_start = time_search[0]
            time_end = time_search[1]
        except:
            time_placement_search = data.find('div', class_='dossier__column data').text
            time_placement = time_placement_search[10:]


        place_search = data.find('div', class_='dossier__column data', itemtype='http://schema.org/PostalAddress').text
        place = place_search[1:]


        price_search = data.find('div', class_='data info__data').text
        price1 = price_search.replace('₽', '')
        price = ''.join(price1.split())


        contacts = data.find('div', class_='contacts')
        customer_search = contacts.find('div', class_='title').text
        cust_bad_index = customer_search.find('(Заказчик)')
        if cust_bad_index > -1:
            customer = customer_search[0:cust_bad_index]
        else:
            customer = customer_search


        #source_link = data.find('a', class_='participate')
        #source_link = source_link['href']
        source_link = "None"
        

        df.loc[id] = [date_time,header, price, line, '', theme, time_start, time_end, customer, place, source_link]
        
        
        y += 1
        print('DONE!', line)


### Writing data in file ####


df.to_excel(f'ZC-{date_time}.xlsx', sheet_name='Zakupki360-all', index=True)


print('Found offers:', len(unique_url))
print('Loaded offers:', y)
print(f'Data has been successfully written to file "ZC-{date_time}.xlsx".')
exit = input('Press "Enter" for exit')

