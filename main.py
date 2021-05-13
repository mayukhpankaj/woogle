from flask import Flask, render_template, redirect , url_for 

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 

import requests
from bs4 import BeautifulSoup

""" 

author: Mayukh Pankaj
date: 10/5/2021

Woogle - a Job scraping web application. 

LEAD 2.0



"""


#initialising global variables
global gdata , lidata , isdata, indata , tdata , usr_input , loc 

gdata =  []
lidata = []
isdata = []
indata = []
tdata =  []



app = Flask(__name__)

app.config['SECRET_KEY'] = 'xyz'  #CSRF token


class searchform(FlaskForm):

    text = StringField('Search',validators=[DataRequired()])

    location = StringField('location')

    submit = SubmitField('SEARCH')


# function for gsearch 

def gsearch(text,loc=""):

    text=text.replace(' ', '+')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }


    if not loc:
        searchurl='https://google.com/search?q='+text+'+jobs'
    else:
        searchurl='https://google.com/search?q='+text+'+jobs+in+'+loc

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

        try:

            title = result.find(class_='LC20lb DKV0Md').string

            link = result.find('a')['href']

            desc = result.next_sibling.text.strip()

            data_item = {

                'title':title,
                'desc':desc,
                'link':link
            }
        except:
            break



        dataframe.append(data_item)



        ctr+=1

    return dataframe




# linkedin search 

def linkedin(text,loc=""):


    text=text.replace(' ', '%20')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    if not loc:

        searchurl='https://www.linkedin.com/jobs/search?keywords='+text+'&location=India&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

    else:

        searchurl='https://www.linkedin.com/jobs/search?keywords='+text+'&location='+loc+'&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    cards = soup.find_all('a',class_='base-card__full-link')

    print(len(cards))

    l = len(cards)

    #linkedin returns different class name sometimes requesting again gives required html.

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
        
        try:
        
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
        
        except:
            break


        dataframe.append(data_item)

        # print(title)
        # print(company)
        # print(location)
        # print(img)
        # print(link) 

        ctr+=1
    

    return dataframe



# internshala search  

def internshala(text,loc=''):

    text=text.replace(' ', '%20')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    if not loc:

        searchurl='https://internshala.com/internships/keywords-'+text

    else:

        searchurl='https://internshala.com/internships/keywords-'+text+'-in-'+loc


    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    cards = soup.find_all(class_='internship_meta')

    cl = len(cards)

    print(cl)


    ctr=0

    dataframe = []

    for card in cards:

        if ctr >=4: 
            break
        
        try:

            try:
                title = card.find(class_='heading_4_5 profile').text.strip()
            except:
                title = ''

            link = card.a['href']
            link = 'https://internshala.com'+link

            company = card.find(class_='heading_6 company_name').text.strip()

            location = card.find(class_='location_link').text.strip()

            el = card.find(class_='internship_other_details_container')

            duration = el.contents[1].find(class_='ic-16-calendar').text.strip()

            stipend = el.find(class_='stipend').text.strip()

            end_date = el.find(class_='apply_by')

            apply_by = end_date.contents[3].text.strip()

            try:
                img = card.find(class_='internship_logo').img['src']
                img = 'https://internshala.com'+img
            
            except:
                img=''

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

        except:
            break




        dataframe.append(card_data)

        ctr+=1
    
    return dataframe



# indeed search 

def indeed(text,loc):



    text=text.replace(' ', '+')

    headers = {

        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    if not loc:

        searchurl='https://in.indeed.com/jobs?q='+text

    else:
         searchurl='https://in.indeed.com/jobs?q='+text+'&l='+loc


    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    cards = soup.find_all(class_='title')

    data = []

    ctr = 0

    for card in cards:

        if ctr >=4:
            break
        
        try:

            title = card.a.text.strip()

            link = card.a['href'].replace('/rc/clk?','')

            # print(len(link))

            if(len(link)>60):
                link='https://in.indeed.com'+link           #indeed's job page & advertised job page have different url
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

        except:
            break


        data.append(data_item)

        ctr+=1
    
    return data


# times job search 

def timesjob(text,loc):
 

    text=text.replace(' ', '%20')

    headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }

    if not loc:

        searchurl='https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords='+text

    else: 

        searchurl='https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords='+text+'+&txtLocation='+loc 




    print(searchurl)

    response = requests.get(searchurl,headers=headers) 

    soup = BeautifulSoup(response.text,'html.parser')

    jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')

    ctr = 0

    data = []

    for job in jobs:

        if ctr >=4:
            break
        
        try:

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
        
        except:
            break


        data.append(data_item)

        ctr +=1

    return data





@app.route('/', methods=['POST','GET'])

def home():

    form = searchform()

    gl=0

    if form.validate_on_submit():

        print('submit clicked')

        global usr_input , loc

        user_input = form.text.data
        usr_input = form.text.data

        loc = form.location.data 

        print(loc)

        print(user_input)

        global gdata , lidata , isdata , indata , tdata 

        gdata =  gsearch(user_input,loc)   #gsearch  

        lidata = linkedin(user_input,loc)  #linkedin

        isdata = internshala(user_input)  #internshala 

        indata = indeed(user_input,loc)    #indeed

        tdata = timesjob(user_input,loc)    #times job 


        return redirect(url_for('result'))   #redirecting to results page  
 
    return render_template('index.html',form=form)


@app.route('/result',methods=['POST','GET']) 

def result():

    return render_template('result.html',gdata=gdata, ldata =lidata , isdata=isdata, indata=indata, tdata=tdata,usri = usr_input,loc=loc)


@app.route('/about')

def about():
    
    return render_template('about.html')




if __name__=='__main__':
     app.run()    