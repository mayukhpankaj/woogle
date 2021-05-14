from bs4 import BeautifulSoup
import requests 



text1 = input('Enter Job title  ')


def gsearch(text):

    text=text.replace(' ', '+')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    searchurl='https://google.com/search?q='+text+'+jobs'

    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    results = soup.find_all(class_='yuRUbf')

    r_no = min(3,len(results))
    ctr = 0

    dataframe =[]

    for result in results:
        if(ctr>=r_no):
            break
        title = result.find(class_='LC20lb DKV0Md')
        title = title.text
        link = result.find('a')['href']

        desc = result.next_sibling.text.strip()

        data_item = {

            'title':title,
            'desc':desc,
            'link':link
        }

        dataframe.append(data_item)



        ctr+=1

    return dataframe


result = gsearch(text1)

print(result[1])