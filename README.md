# Quasarzone saleinfo Discord Bot
[퀘이사존 핫딜](https://quasarzone.com/bbs/qb_saleinfo)에서 새 글을 지정한 디스코드 채널로 알려줍니다. (갱신 주기 : 1시간)

디스코드 봇 추가

## How To Use
알림을 받을 채널을 선택

채널 편집으로 들어가 채널 주제(topic)에 "run_quasarzonebot"을 입력 후 저장

*****

## Install

### install dependencies
```
pip install requests
pip install discord
pip install beautifulsoup4
pip install selenium
pip install selenium-stealth
sudo apt install chromium-chromedriver
```

### created Storage file 
The user who execute the script must have read, write permission to Storage file
```
ex)
touch /tmp/saleinfo
```

### set environment variable
```
EXPORT TOKEN='[discord bot token]'
EXPORT P_SALEINFO='[Scraped post storage file ex)/tmp/saleinfo]'
```

*****
