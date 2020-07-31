import requests

from bs4 import BeautifulSoup
import time
import pandas as pd
#Using Yahoo Finance page 'https://finance.yahoo.com' to get Information about stocks and creating a dataset of it.
#Region is chosen as 'India' and volume>10000 to get refined Stocks, as per our desire.
#This is an example.However, we can change the above parameters from the website and provide the link down below.
page = requests.get("https://finance.yahoo.com/screener/unsaved/a8e8f1da-68bb-4ec0-ba14-dab9c8c10c9e")

content = page.content

#This parses the HTML document using the html parser of the Python Standard Library.
soup = BeautifulSoup(content,"html.parser")

#Prior data : Collected from the main page
yahooFinanceUrl = []
symbols = []
names = []
current_Price = []
volume = []
avg_Volume = []
market_cap = []
PE_Ratio = []
listOfInfo=[]
index=0

#Extracting different fields using attributes
 

start = time.time()

for url in soup.find_all("a",attrs={"class":"Fw(600)"}):
	yahooFinanceUrl.append("https://finance.yahoo.com"+str(url.get('href')))

for symb in soup.find_all("a",attrs={"class":"Fw(600)"}):
	symbols.append(symb.text)

for name in soup.find_all("td",attrs={"aria-label":"Name"}):
	names.append(name.text)

for price in soup.find_all("td",attrs={"aria-label":"Price (Intraday)"}):
	current_Price.append(price.text)

for vol in soup.find_all("td",attrs={"aria-label":"Volume"}):
	volume.append(vol.text)

for avg in soup.find_all("td",attrs={"aria-label":"Avg Vol (3 month)"}):
	avg_Volume.append(avg.text)

for market in soup.find_all("td",attrs={"aria-label":"Market Cap"}):
	market_cap.append(market.text)

for pe in soup.find_all("td",attrs={"aria-label":"PE Ratio (TTM)"}):
	PE_Ratio.append(pe.text)


#Now, extracting more information using the individual webpages of 'Statistics' of every company

for url in yahooFinanceUrl:
	
	page = requests.get(url)
	content = page.content
	newSoup = BeautifulSoup(content,"html.parser")
	
	statistics_url = newSoup.find("a",attrs={"data-reactid":"11"})
	print(statistics_url.get('href'))
	
	newPage = requests.get("https://finance.yahoo.com"+str(statistics_url.get('href')))
	newContent = newPage.content
	SoupForStatistics = BeautifulSoup(newContent,"html.parser")
	
	CompleteDict={}
	Priordata={}
	Remainingdata={}

	for ev in SoupForStatistics.find_all("tr",attrs={"class":"Bxz(bb)"}):
		
		if ev.find("td",attrs={'class':'Pos(st)'}).text.strip() in ["52 Week High 3","52 Week Low 3","Return on Equity (ttm)","Profit Margin","Operating Margin (ttm)","Diluted EPS (ttm)"]:
			Remainingdata[ev.find("td",attrs={'class':'Pos(st)'}).text] = ev.find("td",attrs={'class':'Fw(500)'}).text

	
	Priordata["symbols"] = symbols[index]
	Priordata["name"] = names[index]
	Priordata["Current Price"] = current_Price[index]
	Priordata["volume"] = volume[index]
	Priordata["Average volume"] = avg_Volume[index]
	Priordata["Market Cap"] = market_cap[index]
	Priordata["PE Ratio"] = PE_Ratio[index]
	#Merging the data(in the form of dictionaries)
	Priordata.update(Remainingdata)
	listOfInfo.append(Priordata)
	index+=1

end = time.time()

#Creating dataframe of list of dictionaries represented by 'listOfInfo'
df = pd.DataFrame(listOfInfo)
#Storing dataframe in the form of .csv file 
df.to_csv("C:\TheDexterityGlobalGroup\Web Scraping\datasetYahooFinance.csv")
print("Time taken in the whole process of extracting information:",end-start)



