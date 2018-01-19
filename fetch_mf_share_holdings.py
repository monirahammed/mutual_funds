from __future__ import print_function
from bs4 import BeautifulSoup
import requests

import sys
import re
import traceback


#link to get direct holdings http://www.moneycontrol.com/india/mutualfunds/mfinfo/portfolio_holdings/MSA031

portfolio_holdings_base_url='http://www.moneycontrol.com/india/mutualfunds/mfinfo/portfolio_holdings/'

base_url='http://www.moneycontrol.com/'

outputDir='/home/monir/mutual_funds/output'

small_mid_cap_url='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/small-and-mid-cap.html'
large_cap_fund_url='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-cap.html'
equity_diversified='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/diversified-equity.html'
elss='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/elss.html'
thematic_infra='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/thematic-infrastructure.html'
pharma_health_care='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/sector-pharma-and-healthcare.html'
fmcg='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/sector-fmcg.html'
technology='http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/sector-technology.html'



mf_fund_type_dict={ 'small-mid-cap': {'url': small_mid_cap_url, 'fundType':'small-mid-cap'},
	    'large-cap': {'url': large_cap_fund_url, 'fundType': 'large-cap'},
	     'equity-diversified' : {'url': equity_diversified, 'fundType': 'equity-diversified'},
	     'elss': {'url': elss, 'fundType':'elss'},
	     'infrastructure' : {'url':thematic_infra, 'fundType': 'infrastructure'},
	     'pharma--healthcare':{'url': pharma_health_care , 'fundType':'pharma-healthcare'},
	     'fmcg': {'url': fmcg,'fundType':'fmcg'},
	     'technology': {'url':technology, 'fundType': 'technology'}
	     }



pattern=re.compile('/mutual-funds/nav/')
pattern_holdings=re.compile('/portfolio-holdings/')


def download_fund_holdings(fundKey):

	url=mf_fund_type_dict[fundKey]['url']
	fund_type=mf_fund_type_dict[fundKey]['fundType']
	outputFile=outputDir+'/'+fund_type+'_holdings.txt'
	infoFile=outputDir+'/'+fund_type+'_mfInfo.info'
	print("Prcessing .....:", url, fund_type,outputFile)

	writeFile=open(outputFile,'w') 
	infoWriteFile=open(infoFile,'w')

	try:
		page = requests.get(url)
		soup = BeautifulSoup(page.content, 'html.parser')
	except Exception as e:
		print("Error : Exception Occured for URL :",url);
		print("Error : Exception Occured :",sys.exc_info()[0]);
		return 1
		

	for links in soup.find_all('a',{'href':pattern}):
		url=links.get('href')
		data=url.split('/')
		mf_code=data[-1]
		indi_url=portfolio_holdings_base_url+mf_code
	#	print("URL IS : ",indi_url, mf_code, fund_type)
		try:

			fund_page=requests.get(indi_url)
			fund_page_soup=BeautifulSoup(fund_page.content,'html.parser')
			table_find=fund_page_soup.find('table',class_='tblporhd')
			rows=table_find.findAll('tr')
			for tr in rows:
				cols = tr.findAll('td')
				if len(cols) < 2 :
					temp_line=fund_page_soup.title.string+'#'+mf_code+'#'+fund_type+'#'
					infoWriteFile.write(temp_line+"\n")
					continue
				#print(temp_line)
				temp_line=fund_page_soup.title.string+'#'+mf_code+'#'+fund_type+'#'
				writeFile.write(temp_line)
				for td in cols:
					temp_line_2=td.find(text=True)+'#'
					#print(temp_line_2)
					writeFile.write(temp_line_2)

			
		
				writeFile.write("\n")
		except Exception as e:
			print("Error : Exception Occured link=",indi_url);
			print("Error : Exception Occured :",sys.exc_info()[0]);
			print(e.__class__, e.__doc__, e.message)
			


	writeFile.close()
	infoWriteFile.close()
	return 0



for key in mf_fund_type_dict:
	download_fund_holdings(key)

