from bs4 import BeautifulSoup
import requests 



text1 = input('Enter Job title  ')


def timesjob(text):
 

    text=text.replace(' ', '%20')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    searchurl='https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords='+text

    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')

    ctr = 0

    data = []

    for job in jobs:

        if ctr >=4:
            break

        title = job.find('h2').text.strip()

        company= job.find('h3',class_='joblist-comp-name').text.strip()

        skills = job.find('span',class_='srp-skills').text.strip()

        datalabel = job.find('ul',class_='top-jd-dtl clearfix')

        # using navigation for years & location without any class or id

        years = datalabel.next_element.next_element.next_element.next_sibling

        location = datalabel.contents[3].span.text

        link = job.header.h2.a['href']

        data_item = {

            'title': title,
            'company': company,
            'duration': years,
            'location': location,
            'skills': skills,
            'link' : link

        }

        data.append(data_item)

        ctr +=1

    return data 


result = timesjob(text1)
    
print(result[1])