import requests
from bs4 import BeautifulSoup as bs
import discord_bot
import selenium_scrapping
import mmap
import re
from datetime import datetime
import os

## init ##
url = "https://quasarzone.com/bbs/qb_saleinfo"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
past_saleinfo = os.getenv("P_SALEINFO") 

# Get Quasarzone saleinfo : If there is no response using the requests module, re-request using Selenium.
def get_result() :
	res = requests.get(url,headers=headers)
	print('[+] Requests Quasarzone')
	if (res.status_code == 200):
		print('[+] 200, Get Response')
		result = bs(res.text, 'html.parser')

	else :
		print('[-] 403, Requests to Selenium')
		result = bs(selenium_scrapping.get_selenium(url), 'html.parser')

	return result

# File has more than 50 lines => Delete the number of lines from the top of the file
def remove_line(lines,path) :
	
	content = open(path,"r").readlines()
	if (len(content) > 50) :
		del content[:lines]

		f = open(path,"w")
		f.writelines(test)
		f.close()
		print('[+] Remove lines '+str(lines))


def find_newhotdeal(array,path) :
	new_array = [] 
	title_array = []
	for item in array :
		## blind post except
		try :
			#print('[+] Find : title')
			title = item.find('span', class_ ='ellipsis-with-reply-cnt').get_text()
		except:
			print('[-] Find Error : maybe blind post...')
			continue
		with open(path) as f:
			s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
			if s.find(bytes(title,'utf-8')) == -1:
				print('[+] New Info : '+title)
				category = item.find('span', class_ = 'category').get_text()
				price = item.find('span', class_ ='text-orange').get_text()
				link = item.find('a', class_ ='subject-link')['href']
				
				new_array.append([category,'['+title+']('+url+')\n'+price])
				title_array.append(title)

	return [new_array,title_array]


print('\n\n\n[+] Start HOTDEAL')


result = get_result()
hotdeal_list = result.find_all('div', class_ ='market-info-list-cont')
new_hotdeal = find_newhotdeal(hotdeal_list,past_saleinfo)	

with open(past_saleinfo, 'a') as f:
        f.write('\n'.join(new_hotdeal[1]))

now = datetime.now()
date = now.strftime('%Y-%m-%d %H:%M:%S')

if (len(new_hotdeal[0]) != 0 ) :

	print('[+] Found New HOTDEAL Info!')
	print('[+] Send to Discord_bot')
	embed=["NEW Quasarzone saleinfo : "+date,new_hotdeal[0]]
	discord_bot.sendMessage(embed)

else :
	print('[-] Not Found New HOTDEAL Info')

remove_line(len(new_hotdeal),past_saleinfo)
print('[+] END HOTDEAL :' +date)
