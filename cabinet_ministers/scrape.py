import requests, json
from bs4 import BeautifulSoup

url ="https://www.india.gov.in/my-government/whos-who/council-ministers"               

page = requests.get(url)                                                               

soup = BeautifulSoup(page.content) 

tbody = soup.findAll('tbody')

data = []

for tb in tbody:
	tds = tb.findAll('td')
	for td in tds:
		min_data = {
			'name': '',
			'contact': '',
			'facebook': '',
			'twitter': ''
		}

		divs = td.findAll('div')
		if len(divs)>1:
			min_data['name'] = divs[2].text
		
		links = td.findAll('a')

		#d = []
		for link in links:
			if link.text=='Twitter Account ':
				min_data['twitter'] = link['href']
			elif link.text == 'Facebook Account ':
				min_data['facebook'] = link['href']
			elif link.text == 'Contact ':
				min_data['contact'] = link['href']
		    
		    #d.append([, link['href']])

		print min_data
		
		data.append(min_data)

json