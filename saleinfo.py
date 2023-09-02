import requests
from bs4 import BeautifulSoup as bs
import discord_bot
import selenium_scrapping
import mmap
import re
from datetime import datetime
import os
import sys

## init ##
url = "https://quasarzone.com/bbs/qb_saleinfo"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
past_saleinfo = "./data/quasarzone_info"

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
		f.writelines(content)
		f.close()
		print('[+] Remove lines {}'.format(str(lines)))


def find_newhotdeal(array,path) :
	new_array = [] 
	title_array = []
	num =1
	for item in array :
		# blind post except
		try :
			title = item.find('span', class_ ='ellipsis-with-reply-cnt').get_text()
		except :
			print('[-] Find Error : maybe blind post...')
			continue

		try : 
			with open(path) as f:
				try : 
					s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ).find(bytes(title,'utf-8'))
				except ValueError: 
					s = -1
				if s == -1:
					category = item.find('span', class_ = 'category').get_text()
					price = item.find('span', class_ ='text-orange').get_text()
					link = item.find('a', class_ ='subject-link')['href']
					if(title.find('래플') != -1 or ( title.find('적립') != -1 and float(re.sub(r'[^0-9\.]', '', price)) < 100 ) ) :
						print('[-] Filter info : {}'.format(title))
					else :
						print('[+] New Info : {}'.format(title))
						new_array.append(['','{}\. [`{}`]{}\n{} [(게시글 링크)](https://quasarzone.com{})\n\n'.format(str(num),category,title,price,link)])
						num +=1
					title_array.append(title)
		except FileNotFoundError:
			with open(path,"x") as f:
				print('[-] Not found FIle : Create New file')

	return [new_array,title_array]


def get_notice(args) :
	title = []
	content = []
	for item in args:
		if (item[:2] == "t=") :
			title.append(item[2:])	
		elif (item[:2] == "c="):
			content.append(item[2:])

	b = len(title) if len(title) > len(content) else len(content) #len(title),len(content))
	if(len(title) < b) :
		for i in range(0,b-len(title)) :
			title.append('')
	else :
		for i in range(0,b-len(content)) :
			content.append('')

	res = list(map(lambda x,y: [x,y], title, content))

	if (len(res) != 0 ) :
		embed=["NOTICE : "+date,res]
		discord_bot.sendMessage(embed)

def saleinfo() :
	print('[1] Get saleinfo data')
	result = get_result()
	print('[------------------------------]')
	print('[2] Parse saleinfo')
	hotdeal_list = result.find_all('div', class_ ='market-info-list-cont')
	new_hotdeal = find_newhotdeal(hotdeal_list,past_saleinfo)	
	print('[------------------------------]')
	with open(past_saleinfo, 'a') as f:
		f.write('\n'.join(new_hotdeal[1]))

	now = datetime.now()
	date = now.strftime('%Y-%m-%d %H:%M:%S')

	if (len(new_hotdeal[0]) != 0 ) :

		print('[+] Found New HOTDEAL Info!')
		print('[------------------------------]')
		print('[3] Send to Discord_bot')
		embed=["NEW Quasarzone saleinfo : {}".format(date),new_hotdeal[0]]
		discord_bot.sendMessage(embed)

	else :
		print('[-] Not Found New HOTDEAL Info')

	remove_line(len(new_hotdeal[0]),past_saleinfo)

if __name__ == "__main__":

	now = datetime.now()
	date = now.strftime('%Y-%m-%d %H:%M:%S')

	print('\n\n\n[------------------------------]\n[+] Start HOTDEAL\n[------------------------------]')

	try:
		# saleinfo.py notice t="title" c="content" t="title2" ...
		if (sys.argv[1] == 'notice') :
			args = sys.argv
			del args[:2]
			get_notice(args)

	except IndexError:
		saleinfo()

	print('[+] END HOTDEAL :' +date)
	print('[------------------------------]')
