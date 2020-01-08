# -*- coding: utf-8 -*-

# Find all a href links in an html file and extracts it's subdomains by sending request packets
# prerequisites: bs4 and urllib required for this code block
# usage: python crawler.py
# author: Buğra KARACA

import time
from Queue import Queue
import pymysql
from bs4 import BeautifulSoup
import urllib
import re
import requests
import urlparse
from threading import Thread
from fuzzywuzzy import fuzz

ilk_sira = Queue()
ikinci_sira = Queue()

def dbCreateTable():
    sqlCreateTable = "CREATE TABLE fuzzdeneme(url TEXT(3000),keyword TEXT(3000),ie TEXT(30), content TEXT(3000))"
    mycursor.execute(sqlCreateTable)
    db.commit()

def dbUpdate(url, keyword,x, content):
    # Open database connection
    db = pymysql.connect(host="localhost", user="root", password="asdfgASDFG12345ASDFG", database="craw")
    # prepare a cursor object using cursor() method
    mycursor = db.cursor()
    sqlUpdate = "UPDATE sss1 SET url={} , keyword={}, ie={}, content={} where content={}".format(url, keyword,x, content,content)
    mycursor.execute(sqlUpdate)
    db.commit()
    db.close()

def dbDelete():
    sql2 = "DELETE FROM samsung-galaxy-j7-prime"
    sql3 = "ALTER TABLE samsung-galaxy-j7-prime AUTO_INCREMENT = 1"
    mycursor.execute(sql2)
    mycursor.execute(sql3)

def dbWrite(url, keyword,x, content):
    # Open database connection
    db = pymysql.connect(host="localhost", user="root", password="asdfgASDFG12345ASDFG", database="craw")
    # prepare a cursor object using cursor() method
    mycursor = db.cursor()
    sql = "INSERT INTO fuzzdeneme(url, keyword, ie, content) VALUES (%s, %s, %s, %s)"
    val = (url,  keyword,x, content)
    mycursor.execute(sql, val)
    db.commit()
    db.close()

def reSet(comments):
    comments = str(comments)
    re.sub(r'[\x00-\x1f\x7f-\x9f]', " ", str(comments))
    comments=comments.lower()
    comments = comments.replace("\\n", " ")
    comments = comments.replace("\\xc3\\xbc", "u")
    comments = comments.replace("\\xc3\\x9c", "u")
    comments = comments.replace("\\xc3\\xb9", "u")
    comments = comments.replace("\\xc4\\xb1", "i")
    comments = comments.replace("\\xc4\\xb0", "i")
    comments = comments.replace("\\xc5\\x9f", "s")
    comments = comments.replace("\\xc5\\x9e", "s")
    comments = comments.replace("\\xc3\\xb6", "o")
    comments = comments.replace("\\xc3\\x96", "o")
    comments = comments.replace("\\xc4\\x9f", "g")
    comments = comments.replace("\\xc4\\x9e", "g")
    comments = comments.replace("\\xc3\\xa7", "c")
    comments = comments.replace("\\xc3\\x87", "c")
    comments = comments.replace("\\xc2\\xa0", "")
    comments = comments.replace("ü", "u")
    comments = comments.replace("ı", "i")
    comments = comments.replace("İ", "i")
    comments = comments.replace("ç", "c")
    comments = comments.replace("ş", "s")
    comments = comments.replace("ğ", "g")
    comments = comments.replace("ö", "o")
    comments = comments.replace("\\xe2\\x80\\x99", "'")
    comments = comments.replace("\\xe2\\x80\\x9c", "'")
    comments = comments.replace("\\xe2\\x80\\xa6", " ")
    #comments = re.sub(r'[^a-zA-Z]', " ", str(comments))
    #comments = re.sub(r"\b[a-zA-Z]\b", " ", str(comments))
    return comments

def runFuzz(soup1,keywords,keyword):
    soup1 = soup1.lower()
    soup1=soup1.strip()
    fuzres = soup1.split(" ")
    for s in range(len(fuzres)):
        Ratio = fuzz.ratio(fuzres[s].lower(), keyword)
        print Ratio
        print fuzres[s]
        if Ratio >= 100*(len(keyword)-1)/len(keyword):
            print keyword
            if not keywords.__contains__(fuzres[s]):
                keywords.append(fuzres[s])
    return keywords

def splitLinks(i,allSublinks):
    path=urlparse.urlparse(i).path
    if not allSublinks.__contains__(path):
        allSublinks.append(path)
    return allSublinks

def clearData(allSublinks,lna,host,visited):
    sublinks=[]
    for a in allSublinks:
        host = re.sub("/$", "", host)
        a = host + a
        a = re.sub("/$", "", a)
        if not (sublinks.__contains__(a) or lna.__contains__(a) or visited.__contains__(a) ):
            sublinks.append(a)
    return sublinks

def getHtmlData(soup,li):
    allSublinks=[]
    k = urlparse.urlparse(li).hostname
    for s in soup.findAll('div', {}):
        s1 = s.findAll('a', href=True)
        for s2 in s1:
            i = s2['href'].encode('utf-8')

            j=urlparse.urlparse(i).hostname
            if k == j :
                allSublinks=splitLinks(i, allSublinks)
            elif re.search("^/",i):
                allSublinks = splitLinks(i, allSublinks)
    return allSublinks

def openUrl(host,visited,keyword):
    theHtml = """       < !DOCTYPE
            html >
            < html >
            < head > < meta
            content = "text/html; charset=UTF-8"
            http - equiv = "Content-Type" / > < meta
            charset = "utf-8" / > < meta
            content = "width=device-width, initial-scale=1"
            name = "viewport" / >
            < title > İGA
            TUR & Ccedil;
            ekiliş < / title >
            < link
            href = "https://fonts.googleapis.com/css?family=Open+Sans:400,700"
            rel = "stylesheet"
            type = "text/css" / >
            < style
            type = "text/css" > body, html
            {
                padding: 0;
            margin: 0;
            }
            body
            {
                font - family: 'Open Sans', sans - serif;
            background - color:  # e6edef;
            background: url('/system/content_images/uploads/45e/5aa/10-/original/bg-3-grayscale.png')
            no - repeat
            center
            center
            fixed;
            -webkit - background - size: cover;
            -moz - background - size: cover;
            -o - background - size: cover;
            background - size: cover;
            }
            html
            {
                width: 100 %;
            height:  100 %;
            }
            .wrapper
            {
                height: 100 %;
            }
            h1
            {
                color:  # FFFFFF;
                    margin: 0;
            font - size: 55
            px;
            line - height: 1
            em;
            }
            h2
            {
                font - size: 18px;
            color:  # FFFFFF;
            }
            .login
            {
                position: relative;
            display: block;
            height: auto;
            max - width: 960
            px;
            margin: auto;
            background:  # ffffff;
            margin - top: 100
            px;
            box - shadow: 0
            px
            30
            px
            100
            px - 5
            px
            rgba(0, 0, 0, 0.2);
            overflow: hidden;
            -webkit - border - radius: 1
            px;
            -moz - border - radius: 1
            px;
            border - radius: 1
            px;
            }
            input
            {
                width: 100 %;
            margin - bottom: 10
            px;
            background:  # eeeeee;
            border: none;
            outline: none;
            padding: 15
            px;
            font - size: 16
            px;
            color:  # 222222;
            -webkit - border - radius: 2
            px;
            -moz - border - radius: 2
            px;
            border - radius: 2
            px;
            display: block;
            }

            input[type = submit] {
                color:  # FFFFFF;
            }
            .btn
            {
                width: 100px;
            background - color:  # 6B0103;
            margin - top: 10
            px;
            cursor: pointer;
            }
            .btn2
            {
                width: 325px;
            background - color:  # 6B0103;
            margin - top: 10
            px;
            margin - left: 30
            px;
            cursor: pointer;
            }
            .btn:hover
            {
                background - color:  # 3498db;
            }
            .onerow
            {
                clear: both;
            padding: 0
            10
            px;
            }
            / *Columns
            ** ** ** ** ** ** ** ** ** ** ** ** * /

            .col1,.col2,.col3,.col4,.col5,.col6,.col7,.col8,.col9,.col10,.col11,.col12
            {
                float: left;
            margin: 0
            0
            0
            0;
            }
            .col6
            {
                width: 46 %;
            padding: 15
            px;
            }

            @media


            all and (min - width: 1024px)
            {
                .onerow
            {
                padding: 0;
            }
            }

            input[type = checkbox] {
                display: inline;
            width: 15
            px;
            background:  # fff;
            }
            .header
            {
                position: relative;
            height: auto;
            max - width: 960
            px;
            }
            .footer
            {
                position: relative;
            height: auto;
            max - width: 960
            px;
            margin: auto;
            text - align: center;
            }
            .footer
            p
            {
                font - size: 10px;
            }
            .leftcol
            {
                height: 400px;
            / *background - image: url( / system / content_images / uploads / 249 / e7d / 42 - / original / bg.png); * /

            background:  # 6b0103; /* Old browsers */
            background: -moz - linear - gradient(45
            deg,  # 6b0103 0%, #a30006 100%); /* FF3.6-15 */
            background: -webkit - linear - gradient(45
            deg,  # 6b0103 0%,#a30006 100%); /* Chrome10-25,Safari5.1-6 */
            background: linear - gradient(45
            deg,  # 6b0103 0%,#a30006 100%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
            filter: progid:DXImageTransform.Microsoft.gradient(startColorstr='#6b0103', endColorstr='#a30006',
                                                               GradientType=1); / *IE6 - 9
            fallback
            on
            horizontal
            gradient * /
            }
            .icon
            {
                width: 70px;
            height: auto;
            padding - bottom: 20
            px;
            }

            table
            {
                width: 92 %;
            border: 0;
            }
            / *Small
            Devices
            ** ** ** ** ** ** ** ** ** ** ** ** * /

            @media


            all and (max - width: 640px)
            {
                .onerow
            {
            }
                .col1,.col2,.col3,.col4,.col5,.col6,.col7,.col8,.col9,.col10,.col11
            {
                float: none;
            width: auto;
            }
            .login
            {
                margin - top: 10px;
            width: 100 %;
            }
            .leftcol
            {
                height: auto;
            }
            input
            {
                width: 90 %;
            }
            h1
            {
                font - size: 45px;
            }
            }
            < / style >
                < / head >
                    < body > <!-- Login
            container -->
            < div


            class ="login" > < !-- Left Column -->

            < div


            class ="col6 leftcol" > < img alt="" src="https://www.igairport.com/MultimediaData1/2019-home-2.jpg" style="width: 100%; height: 208px;" / > < br / >

            < !-- Main
            heading -->
            < h1 > İGATUR
            4
            dam < / h1 >
            < !-- Subheading -->

            < h2 > İstanbul
            Havalimanından
            Yurti & ccedil;
            i - Yurtdışı
            adbm
            Gidiş
            D & ouml;
            n & uuml;
            ş
            U & ccedil;
            ak
            Bileti
            Kazanma
            Fırsatı < / h2 >
            < !-- Left
            Column
            paragraph(Security
            info) --> < img
            alt = ""
            height = "116"
            src = "/system/content_images/uploads/a59/c95/4b-/original/icon_password.png"
            style = "display: inline; width: 10px; height: auto;"
            width = "141" / >
            < p
            style = "font-size: 12px; color: #ffffff; display:inline;" > & Ouml;
            NEMLİ
            UYARI! L & uuml;
            tfen
            Şifrenizi
            Kimseyle
            adam
            Paylaşmayınız < / p >
            < / div >
            < !-- End
            Left
            Column --> < !-- Right
            Column -->

            < form
            action = ""
            autocomplete = "off"
            id = "landing_form1"
            method = "post"
            name = "landing_form1"
            style = "margin: 0px; padding: 0px;" >
            < div


            class ="col6" > < !-- Login Form -->

            < table >
            < tbody >
            < tr >
            < td > <!--[ if IE
            7] >
            < label
            for ="Username" > Username < / label >
            < ![endif] --> < !--[ if IE
            8] >
            < label
            for ="Username" > Username < / label >
            < ![endif] --> < !--[ if IE
            9] >
            < label
            for ="Username" > Username < / label >
            < ![endif] --> < input
            id = "name"
            name = "UserName"
            placeholder = "Ad Soyad"
            type = "text"
            style = "width: 100%" / > < / td >
            < / tr >
            < tr >
            < td > <!--[ if IE
            7] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < !--[ if IE
            8] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < !--[ if IE
            9] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < input
            id = "mailadress"
            name = "Password"
            placeholder = "Kurumsal E-Posta Adresiniz"
            type = "text"
            style = "width: 100%" / > < / td >
            < / tr >
            < tr >
            < td > <!--[ if IE
            7] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < !--[ if IE
            8] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < !--[ if IE
            9] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < input
            id = "adres"
            name = "adres"
            placeholder = "Adresiniz"
            type = "text"
            style = "width: 100%" / > < / td >
            < / tr >
            < tr >
            < td > <!--[ if IE
            7] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < !--[ if IE
            8] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < !--[ if IE
            9] >
            < label
            for ="Username" > Password < / label >
            < ![endif] --> < input
            id = "telefon"
            name = "telefon"
            placeholder = "Telefon Numaranız"
            type = "text"
            style = "width: 100%" / > < / td >
            < / tr >
            < / tbody >
            < / table >
            < table >
            < tbody >
            < tr >
            < td > <!-- [[FORMFIELDS]] --> < input


            class ="btn" name="submit" type="submit"  value="Kaydet" style="width: 130%" / > & nbsp; < / td >

            < td > <!-- [[FORMFIELDS]] --> < input


            class ="btn2" name="submit" type="submit" value="Değişiklik yapmak istemiyorum" style="width: 100%" / > & nbsp; < / td >

            < / tr >
            < / tbody >
            < / table >
            < !-- End
            Login
            Form --> < / div >
            < / form >
            < / div >
            < !-- Footer -->

            < div


            class ="footer" > < !-- Copyright -->

            < p > All
            images and logos
            copyright & copy;
            their
            respective
            owners.Redistribution
            of
            images is strictly
            prohibited and will
            be
            prosecuted
            to
            the
            fullest
            extent
            of
            the
            law. < / p >
            < / div >
            < !-- End
            Footer --> < / body >
            < / html > """
    while True:
        theUrl = ilk_sira.get()
        if theUrl:
            thePage = urllib.urlopen(theUrl)
            response = requests.get(theUrl)
            x = re.search(".pdf$|.doc$|.docx$|.xml$|.xmls$|.ppt$|.pptx$|.txt$", theUrl)
            if response != 404 and x==None:
                #soup = BeautifulSoup(thePage, "html.parser")

                soup = BeautifulSoup(theHtml, "html.parser")
                x = re.search("HTTP ERROR 500|HTTP ERROR", soup.encode('utf-8'))
                soup1 = str(soup.text.encode("utf-8"))
                keywords=[]
                results = []
                keywords.append(keyword)
                keywords=runFuzz(soup1,keywords,keyword)
                res = re.findall('.*(?i){0}.*'.format(keyword), soup1)
                for r in res:
                    r=reSet(r)
                    if not results.__contains__(r):
                        results.append(r)
                        dbWrite(theUrl, keyword,"includes", str(r))
                for key in keywords:
                    res=re.findall('.*(?i){0}.*'.format(key),soup1)
                    for r in res:
                        r=reSet(r)
                        h=re.search("{}".format(key),r)
                        if h!=None:
                            if not results.__contains__(r):
                                results.append(r)
                                dbWrite(theUrl, key,"exact", str(r))
                            else:
                                #dbUpdate(theUrl, key,"exact", str(r))
                                pass
                    #print 'Found the word "{0}" {1} times\n'.format(key, len(results))


                if not x:
                    allSublinks=getHtmlData(soup, theUrl)
                    sublinks=clearData(allSublinks,lna,host,visited)
                    sublinks = list(set(sublinks))
                    sublinks = list(dict.fromkeys(sublinks))
                    sublinks = sorted(sublinks)
                    for a in sublinks:
                        ilk_sira.put(a)
                        lna.append(a)
                    lna.remove(theUrl)
                    visited.append(theUrl)
            else:
                print ("404 not found")
        #print ("lna : %d", len(lna))

        print theUrl
        ilk_sira.task_done()

if __name__ == "__main__":

    # Open database connection
    db = pymysql.connect(host="localhost", user="root", password="asdfgASDFG12345ASDFG", database="craw")
    # prepare a cursor object using cursor() method
    mycursor = db.cursor()

    try:
        dbCreateTable()
    except:
        pass
    db.close()

    #host = raw_input("url giriniz: \n Örnek: forum.shiftdelete.net ")
    host="https://forum.shiftdelete.net/"
    #host="https://"+host+"/"
    keyword=raw_input("keyword gir:")

    lna=[]
    visited=[]
    lna.append(host)
    ilk_sira.put(host)
    keyword=(str.lower(keyword))

    for i in range(0,8):
        t = Thread(target=openUrl, args=(host,visited,keyword,))
        t.daemon = True
        t.start()
    time.sleep(10)

    ilk_sira.join()

    f = open("fuzzdeneme", "a")
    for a in visited:
        f.write(a)
        f.write("\n")



#02.08.2019 cuma en son sql update yazmaya çalışıyordum. includes olan kelimelerde exact olan varsa değiştirmek için
