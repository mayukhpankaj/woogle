from bs4 import BeautifulSoup
import requests 


text1 = input('Enter Job title  ')


def internshala(text):

    text=text.replace(' ', '%20')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    searchurl='https://internshala.com/internships/keywords-'+text

    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    cards = soup.find_all(class_='internship_meta')

    ctr=0

    dataframe = []

    for card in cards:

        if ctr >=4: 
            break

        title = card.find(class_='heading_4_5 profile').text.strip()

        link = card.a['href']
        link = 'https://internshala.com'+link

        company = card.find(class_='heading_6 company_name').text.strip()

        location = card.find(class_='location_link').text.strip()

        el = card.find(class_='internship_other_details_container')

        duration = el.contents[1].find(class_='ic-16-calendar').text.strip()

        stipend = el.find(class_='stipend').text.strip()

        end_date = el.find(class_='apply_by')

        apply_by = end_date.contents[3].text.strip()

        img = card.find(class_='internship_logo').img['src']
        img = 'https://internshala.com'+img

        # print(title,company,location,duration,stipend,apply_by,img,link)

        card_data = {
            
            'title':title,
            'company':company,
            'location':location,
            'duration':duration,
            'stipend':stipend,
            'apply_by':apply_by,
            'img':img,
            'link':link

        }

        dataframe.append(card_data)

        ctr+=1
    
    return dataframe
    
    



result = internshala(text1)

print(result[1]['link'])