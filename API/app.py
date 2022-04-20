from lib2to3.pgen2 import token
from flask import Flask, jsonify, request
import numpy as np
import sys
from libgen_api import LibgenSearch
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import urllib.request as urllib2
from fake_useragent import UserAgent
import requests
import os
from tqdm import tqdm

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from getpass import getpass
from flask_cors import CORS, cross_origin
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
nextToken = 0
userObjectStorage = {}

def dlinker(link):
    req = Request(link)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page, features="lxml")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links[0];


@app.route('/download/<fname>', methods=['POST'])
@cross_origin()
def downloadBook(fname: str):
    userToken = request.headers['Token']
    bookID = request.headers['bookID']
    name=request.headers['search4']
    global userObjectStorage
    s = LibgenSearch()
    title_filters = {"Extension": "pdf", "Language": "English"}
    results = s.search_title_filtered(name, title_filters, exact_match=True);
    todown = None
    for res in userObjectStorage[userToken]:
        if res['ID'] == bookID:
            todown = res
    url = s.resolve_download_links(todown)
    fname2 = fname
    fname = fname + ".pdf"
    headers = {'User-Agent': 'Mozilla/5.0'}

    resp = requests.get(url["GET"], stream=True, headers=headers,verify=False)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)
    portBookToKindle(fname2)
    return "200"


@cross_origin()
@app.route('/search/<name>', methods=['GET'])
def getBooks(name):
    s = LibgenSearch()
    title_filters = {"Extension": "pdf", "Language": "English"}
    results = s.search_title_filtered(name, title_filters, exact_match=True);
    i = 1;
    links = []
    for res in results:
        print(res['ID']);
        print(i, ") ", res['Author'], "||", res['Title'], "||", res['Size'], "||", res['Extension'], "||", res['Year'])
        temp=res
        temp['search4']=name
        links.append(temp)
        i += 1
    temp = request.headers['Token']
    temp = str(temp)
    global userObjectStorage
    userObjectStorage[temp] = results
    return jsonify({'data': links})


@cross_origin()
@app.route('/getToken', methods=['GET'])
def assignToken():
    global nextToken
    nextToken += 1;
    return str(nextToken);


def portBookToKindle(book_name):
    print("Sending book: " + book_name + " to kindle");
    fromaddr = "bookkeeper61611@yahoo.com";
    toaddr = "vivekvarma175_juo0vg@kindle.com";
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    filename = book_name + ".pdf";
    attachment = open(os.getcwd() + "/" + filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    sd = smtplib.SMTP('smtp.mail.yahoo.com', 587)
    sd.starttls()
    password = "jlazkhixseoxzppo"
    sd.login(fromaddr, password);
    text = msg.as_string()
    sd.sendmail(fromaddr, toaddr, text)
    sd.quit()
    os.remove(filename)


if __name__ == '__main__':
    app.run(debug=True)
