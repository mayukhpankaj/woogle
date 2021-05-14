from bs4 import BeautifulSoup
import requests 



text1 = input('Enter Job title  ')


def indeed(text):

    text=text.replace(' ', '+')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    searchurl='https://in.indeed.com/jobs?q='+text

    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    cards = soup.find_all(class_='title')

    data = []

    ctr = 0

    for card in cards:

        if ctr >=4:
            break
        
        title = card.a.text.strip()

        link = card.a['href'].replace('/rc/clk?','')

        # print(len(link))

        if(len(link)>60):
            link='https://in.indeed.com'+link
        else:
            link='https://in.indeed.com/viewjob?'+link
        
        card = card.parent

        company = card.find(class_='company').text.strip()

        location = card.find(class_='location accessible-contrast-color-location').text.strip()

        description = card.find(class_='summary').text 

        # print(title,company,location,link,description)

        data_item = {

            'title':title,
            'company':company,
            'location':location,
            'description': description,
            'link':link
        }

        data.append(data_item)

        ctr+=1
    
    return data



result = indeed(text1)

print(result[0])