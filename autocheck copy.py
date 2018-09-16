# Oujing Liu (Autocheck, run every 10 min, send notification when detecting price changes)


import requests
import bs4
import pprint
import urllib,codecs, datetime, os,smtplib

#Aritzia, Ssense
def update_price1 (url,ori_price): 
    check=[]
    # skip invalid url
    try :    
        response = requests.get(url, timeout=3) 
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text,"html.parser")
        # extract price data
        for meta in soup.select('meta'):
            if meta.get('itemprop') == 'price': 
                    price = meta.get('content')
                    # compare price with the original one
                    if (price == ori_price): 
                        return check
                        
                    else:
                        check.append(price)
                        #return the new price back to main function
                        return check 
    except Exception:
        check.append("invalid")
        return check # add mark to the check list and return back
                
                
        
def send_email (lst): # 
    print('sending')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    from_addr = 'l389819@gmail.com'
    to_addr = 'estella980927@gmail.com'
    msg=""
    for i in lst:
        url = i[0];
        old_price=i[1];
        new_price=i[2];
        item=i[3];
        msg += "The price of " + item + " has changed from "+ old_price+ " to " + new_price+ "\n visit here for change " + url+"\n" # can convert to original version
    username='l389819@gmail.com'
    password= 'loj123456'
    server.login(username,password)
    server.sendmail(from_addr,to_addr,msg)
    server.quit()

             
    
def main():
    file = open("/Users/estellaliu/Desktop/web-scraping/text.filecopy.txt", "r+")
    contents = file.readlines() #make a copy of text file
    file.seek(0)
    file.truncate()
    email_list =[]
    #print(contents)
    for line in contents:
        my_tuple = []
        segment = line.strip().split('/')
        item = segment[0]
        #print(item+'\n')
        ori_price = segment[1].split('(')[0]
        
        #print (ori_price+'\n')
        website = line.strip().split('(')[1].split(')')[0]
        
        #print (website+'\n')
        
        price_same= update_price1(website,ori_price)

        if (len (price_same) != 0):
            if (price_same[0]=="invalid"):
                print("reached")
                
            else:
                my_tuple.extend([website, ori_price,price_same[0],item])
                email_list.append(my_tuple)
                file.write(line.replace(ori_price,price_same[0]))            
        else:
            file.write(line)
        
    pprint.pprint(email_list)
    if ((len(email_list))!=0):
        send_email(email_list)
        
    
    



main()        
