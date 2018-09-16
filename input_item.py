# Oujing Liu input item into checklist

import requests
import bs4
import pprint
import urllib, codecs, datetime, os, smtplib

#read and update the textfile
file = open("text.filecopy.txt", "a+")

# get_price1 (url) extracts item name and price from given url(Aritzia)
def get_price1 (url): 
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    pair =[]
    # search meta tag to find required data
    for meta in soup.select('meta'):
        if meta.get('property')=='og:title':
            name=meta.get('content')
            pair.append(name)
            
        if meta.get('itemprop') == 'price':
            price = meta.get('content')
            pair.append(price)
            
    # show users data have been input successfully
    pprint.pprint(pair)
    file.write('/'.join(pair)+'('+url+')'+'\n')
        
# get_price2 (url) extracts item name and price from given url (Ssense)
def get_price2 (url): 
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    pair =[]
    # search meta tag to find required data
    for meta in soup.select('meta'):
        if meta.get('name') == 'twitter:title':
            name = meta.get('content')
            pair.append(name)

        if meta.get('itemprop') == 'price':
            price = meta.get('content')
            pair.append(price)

    # show users data have been input successfully
    pprint.pprint(pair)
    file.write('/'.join(pair)+'('+url+')'+'\n')

# main() 
def main():
    # ask users for number of items waiting to be added
    n = input ('how many items do you want to put into checklist:')
    lst = list()
    # ask users to input url
    for i in range (0,int(n)):
           url= input('input the website: (please omit www. )')
           lst.append(url)
    #pprint.pprint(lst)
    file.seek(0)
    for i in range (0, len(lst)):
        
        # remind users when items are already in the list
        if lst[i] in file.read():
            print("item from "+url+" already in the list\n")
            continue

        else:
            if "aritzia" in lst[i] :
               get_price1(lst[i])
                    
            elif "ssense" in lst[i]:
                get_price2(lst[i])
            
            else:
                continue
    file.close()
    


# call main function
main()

