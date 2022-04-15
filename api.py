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

#import libsearch
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def dlinker(link):
    req = Request(link)
    html_page = urlopen(req)
    soup = BeautifulSoup(html_page,features="lxml")
    links = []
    for link in soup.findAll('a'):
        links.append(link.get('href'))
    return links[0];

def linksResolver(res,s):
	download_links = s.resolve_download_links(res);
	return download_links["GET"];

@app.route('/download/<fname>', methods = ['POST'])	
@cross_origin()
def downloadBook(fname: str):
	url=request.headers.get('dlink');
	fname2=fname
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
	portBookToKindle(fname2);
	return "200";

@cross_origin()
@app.route('/search/<name>', methods = ['GET'])
def getBooks(name):
	s = LibgenSearch()
	title_filters = {"Extension": "pdf","Language": "English"}
	results = s.search_title_filtered(name,title_filters,exact_match=True);
	i=1;
	links=[];
	for res in results:
		print(i,") ",res['Author'],"||",res['Title'],"||",res['Size'],"||",res['Extension']);
		templink=linksResolver(res,s)
		print(templink)
		links.append({'index':i,'Author':res['Author'],'Title':res['Title'],'size':res['Size'],'download_link':templink});
		i+=1;
	return jsonify({'data': links})

def portBookToKindle(book_name):
	print("Sending book: "+ book_name +" to kindle");
	fromaddr="bookkeeper61611@yahoo.com";
	toaddr="vivekvarma175_juo0vg@kindle.com";
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
	s = smtplib.SMTP('smtp.mail.yahoo.com', 587)
	s.starttls()
	password = "jlazkhixseoxzppo"
	s.login(fromaddr, password);
	text = msg.as_string()
	s.sendmail(fromaddr, toaddr, text)
	s.quit()
	os.remove(filename)
if __name__ == '__main__':
    app.run(debug = True)
