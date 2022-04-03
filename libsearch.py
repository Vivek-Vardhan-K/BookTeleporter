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


#dont use this code for automated testing as it may hammer the server -vivek (author).

def dlinker(link):
    req = Request(link)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page,features="lxml")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links[0];
def downloadBook(url: str, fname: str):
	fname=fname+".pdf"
	headers = {'User-Agent': 'Mozilla/5.0'}
	resp = requests.get(url, stream=True, headers=headers)
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
def portBookToKindle(book_name):
	print("Sending book: "+ book_name +"to kindle");
	fromaddr=input("Enter your email address : ");
	toaddr=input("Enter your kindle address to send book : ");
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	filename = book_name+".pdf";
	attachment = open(os.getcwd()+"/"+filename, "rb")
	p = MIMEBase('application', 'octet-stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	msg.attach(p)
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	password = getpass('please enter your email password || incase of two factor auth use generated app password from google : ')
	s.login(fromaddr, password);
	text = msg.as_string()
	s.sendmail(fromaddr, toaddr, text)
	s.quit()
s = LibgenSearch()
text=input("Enter Book Name or Keyword : ");
title_filters = {"Extension": "pdf","Language": "English"}
results = s.search_title_filtered(text,title_filters,exact_match=True);
i=1;
links=[];
for res in results:
    print(i,") ",res['Author'],"||",res['Title'],"||",res['Size'],"||",res['Extension']);
    templink=dlinker(res['Mirror_1'])
    links.append(templink);
    i+=1;
book_idx=input("EnterBookIndex: ");
book_idx=int(book_idx);
book_name=results[book_idx-1]['Title'];
downloadBook(links[book_idx-1],book_name);
portBookToKindle(book_name);
