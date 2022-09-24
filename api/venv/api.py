from math import fabs
import time
from flask import Flask
from flask_cors import CORS
from flask import request
import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from urllib.request import Request, urlopen
from googlesearch import search
from collections import Counter

app = Flask(__name__)
CORS(app)

howManyWebsitesToScrape = 10


textAllWebsites = ""


def scrapingHTML(url):
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True) 
    return text
 
 
def getH1(url): 
    get_url = requests.get(url)
    get_text = get_url.text
    soup = BeautifulSoup(get_text, "html.parser")

    h1text = soup.find('h1')
    return h1text.text.strip()


def countWord(html, yourHTML):
    text = html
    yourText = yourHTML
    raw_html_output = ''
    yourRaw_html_output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',
        'input',
        'div',
    ]

    for t in text:
        if t.parent.name not in blacklist:
            raw_html_output += t.replace("\n","").replace("\t","")

    for t in yourText:
        if t.parent.name not in blacklist:
            yourRaw_html_output += t.replace("\n","").replace("\t","")


 

    return{"yourWords": yourRaw_html_output.split(), "allWords": raw_html_output.split()}
    

def keywordDensity(html, yourHTML):
    text = html
    yourText = yourHTML
    stopwords = ['w','na', 'się','z','a','i', 'oraz', 'od', 'to', 'do', 'lub', 'jest']
    raw_html_output = ''
    yourRaw_html_output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'style',
        'input',
        'div',
    ]
    ban_charsx1 = ['|','/','&','<p>','</p>', '\r', '–', 'a', 'i', 'jak', '-', 'że', 'dla', 'o', 'są', 'nie', 'tak', 'który', 'które', 'przez', 'za', 'co', 'może', 'ze', 'np']
    ban_chars = ['|','/','&','<p>','</p>', '\r', '–']
    for t in text:
        if t.parent.name not in blacklist:
            raw_html_output += t.replace("\n","").replace("\t","")

    for t in yourText:
        if t.parent.name not in blacklist:
            yourRaw_html_output += t.replace("\n","").replace("\t","")
    
    #x1 output
    outputx1 = raw_html_output
    outputx1 = outputx1.split(" ")

  

    outputx1 = [x for x in outputx1 if not x=='' and not x[0] =='#' and x not in ban_charsx1] 
    outputx1 = [x.lower() for x in outputx1]
    outputx1 = [word for word in outputx1 if word not in stopwords]

    youroutputx1 = yourRaw_html_output
    youroutputx1 = youroutputx1.split(" ") 

    youroutputx1 = [x for x in youroutputx1 if not x=='' and not x[0] =='#' and x not in ban_charsx1] 
    youroutputx1 = [x.lower() for x in youroutputx1]
    youroutputx1 = [word for word in youroutputx1 if word not in stopwords]

    countsX1 = Counter(outputx1).most_common(10)
    for i in range(10):
        yourCounter = 0
        for y in youroutputx1:
            if countsX1[i][0] == y:
                yourCounter = yourCounter + 1

        diff = fabs(int(countsX1[i][1]/howManyWebsitesToScrape) - yourCounter)
        diff = int(round(diff, 0))
        countsX1[i] = (countsX1[i][0], int(countsX1[i][1]/howManyWebsitesToScrape), yourCounter, diff)
         


    #x2 output 
    outputx2 = raw_html_output
    outputx2 = outputx2.split(" ") 
    lenghtX2 = len(outputx2)
    outputx2 = [x for x in outputx2 if not x=='' and not x[0] =='#' and x not in ban_chars] 
    outputx2 = [x.lower() for x in outputx2]
    outputx2 = [word for word in outputx2 if word not in stopwords]

    for index, element in enumerate(outputx2):
        if (index+1 < len(outputx2) and index - 1 >= 0): 
            outputx2[index] = outputx2[index] + " " + outputx2[index+1]

    yourOutputx2 = yourRaw_html_output
    yourOutputx2 = yourOutputx2.split(" ") 
    lenghtX2 = len(yourOutputx2)
    yourOutputx2 = [x for x in yourOutputx2 if not x=='' and not x[0] =='#' and x not in ban_chars] 
    yourOutputx2 = [x.lower() for x in yourOutputx2]
    yourOutputx2 = [word for word in yourOutputx2 if word not in stopwords]

    for index, element in enumerate(yourOutputx2):
        if (index+1 < len(yourOutputx2) and index - 1 >= 0): 
            yourOutputx2[index] = yourOutputx2[index] + " " + yourOutputx2[index+1]


    countsX2 = Counter(outputx2).most_common(10)

    for i in range(10):
        yourCounter = 0
        for y in yourOutputx2:
            if countsX2[i][0] == y:
                yourCounter = yourCounter + 1

        diff = fabs(int(countsX2[i][1]/howManyWebsitesToScrape) - yourCounter)
        diff = int(round(diff, 0))
        countsX2[i] = (countsX2[i][0], int(countsX2[i][1]/howManyWebsitesToScrape), yourCounter, diff)

    return{"x1": countsX1, "x2": countsX2}




def search_and_return(keyword, yourSiteURL):
    query = keyword
    links_array = []
    for j in search(query, tld="co.in", num=10, stop=howManyWebsitesToScrape, pause=2):
        print(j)
        links_array.append(j)
    
    return links_array
 

def get_img_cnt(url): 
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    return len(soup.find_all('img'))


@app.route('/querry' , methods=['GET', 'POST'])
def getQuerry():
    # handle the POST request
    if request.method == 'POST':
        content = request.json
        keyword = content['querry']["keyword"]
        url = content['querry']["url"]
        print("Searched keyword: " + keyword)
        print("Main url: " + url)
        urls = search_and_return(keyword, url)
        print(urls)
        score = 100
        yourHTML = scrapingHTML(url)
        newHTML = scrapingHTML(urls[0])
        allHTML = newHTML
        h1Text = getH1(url)
        h1Correct = "False"
        if h1Text.lower() == keyword.lower():
            h1Correct = "True"

        urls.pop()
        for x in urls:
            newHTML = scrapingHTML(x)
            allHTML += newHTML

        # print(allHTML)
        words1 = countWord(allHTML, yourHTML)
        wordsAverage = len(words1.get('allWords')) / howManyWebsitesToScrape
        yourWords = len(words1.get('yourWords'))
         
        keywords = keywordDensity(allHTML, yourHTML) 
        
        keywordDiff = 10


        keywordDiffAv = 0.001
        keywordDiffMy = 0.001

        keywordsDiffHelp = keywords.get("x1")
        for i in keywordsDiffHelp:
            print(i)
            keywordDiffAv = keywordDiffAv + i[1] 
            keywordDiffMy = keywordDiffMy + i[2] 

        keywordsDiffHelp = keywords.get("x2")
        for i in keywordsDiffHelp:
            print(i)
            keywordDiffAv = keywordDiffAv + i[1] 
            keywordDiffMy = keywordDiffMy + i[2] 


        print('kd def av - jd def my')
        print(keywordDiffAv)
        print(keywordDiffMy)

        kdPer100wAV = keywordDiffAv / (wordsAverage / 100)
        kdPer100wMY = keywordDiffMy / (yourWords / 100)

        print('per100')
        print(kdPer100wAV)
        print(kdPer100wMY)

        diffKDPer100Words = fabs(kdPer100wAV - kdPer100wMY)

        print("kdPer100")
        print(diffKDPer100Words)

        if keywordDiffMy == 0.001:
            score = score - 50
        else:
            if diffKDPer100Words < 1:
                score = score
            elif diffKDPer100Words < 2:
                score = score - 5
            elif diffKDPer100Words < 4:
                score = score - 10
            elif diffKDPer100Words < 8:
                score = score - 20
            elif diffKDPer100Words < 12:
                score = score - 30
            elif diffKDPer100Words < 16:
                score = score - 40
            else:
                score = score - 50


        print(score)


        print("kd def per 100 av")
        print(kdPer100wAV)

        
        print("kd def per 100 av")
        print(kdPer100wMY)

 

        yourIMG = get_img_cnt(url)
        imgMIN = wordsAverage / 250
        imgMIN = int(imgMIN)

        imgMAX = wordsAverage / 40
        imgMAX = int(imgMAX)

       

        
        print("pierwszy score")
        print(score)


        if h1Correct == "False":
            score = score - 20

        if wordsAverage > yourWords:
            pointsForWords = (1 - (yourWords / wordsAverage)) * 30
        else:
            pointsForWords = (1 - (wordsAverage / yourWords)) * 10
  
        print("points for words")
        print(pointsForWords)
        
        score = score - pointsForWords
        
       # score = score - fabs((wordsAverage/yourWords))

        print("zdjecia")
        print(yourIMG)
        print(imgMAX)
        print(imgMIN)

        if yourIMG < imgMIN:
            print("zle zdjecia")
            score = score - 10

        if yourIMG > imgMAX:
            print("zle zdjecia")
            score = score - 10
 

        score = int(score)

        return {'score': score,'keywords': keywords, 'words': wordsAverage, 'yourWords': yourWords, 'yourKeyword': keyword,  'yourUrl': url, 'yourH1': h1Text, 'yourH1Correct': h1Correct, 'yourIMG': yourIMG, 'imgMIN': imgMIN, 'imgMAX': imgMAX}

    # otherwise handle the GET request
    return {'time': time.time()}
 
 