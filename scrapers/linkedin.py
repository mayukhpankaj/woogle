from bs4 import BeautifulSoup
import requests 



text1 = input('Enter Job title  ')


def linkedin(text):


    text=text.replace(' ', '%20')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    searchurl='https://www.linkedin.com/jobs/search?keywords='+text+'&location=India&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    cards = soup.find_all('a',class_='base-card__full-link')

    print(len(cards))

    l = len(cards)

    while(not(l)):
        response = requests.get(searchurl,headers=headers) 

        soup = BeautifulSoup(response.text,'html.parser')

        cards = soup.find_all('a',class_='base-card__full-link')

        l = len(cards)


    ctr = 0

    dataframe =[]

    
    for card in cards:
        
        if ctr >=4:
            break
        

        link = card['href']

        card = card.next_sibling.next_sibling

        img = card.img['data-delayed-url']

        card = card.next_sibling.next_sibling

        title = card.h3.text.strip()

        company = card.h4.text.strip()

        location = card.find(class_='base-search-card__metadata').span.text.strip()

        data_item = {

            'title': title,
            'company': company,
            'location': location,
            'img':img,
            'link':link
        }

        dataframe.append(data_item)

        # print(title)
        # print(company)
        # print(location)
        # print(img)
        # print(link) 

        ctr+=1
    

    return dataframe


result = linkedin(text1)

print(result[3])

# print(len(results))

# print(soup)