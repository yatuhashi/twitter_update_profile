# -*- coding: utf-8 -*-
import urllib
import urllib2
import requests
"""
まずログイン前のページをGETしcookie情報を貰う
GETした時に貰った情報とusername&passwordをつけてログインする
したい事をする
終わったら/logout
"""

username=""
password=""
new_name=""

login_url="https://twitter.com/"
proxy={'http': 'http://cache.ccs.kogakuin.ac.jp:8080','https': 'https://cache.ccs.kogakuin.ac.jp:8080'}
s = requests.session()

try :
    r = s.get(login_url, proxies=proxy)
    auth_index=r.text.find('authenticity_token')
    auth_token=r.text[auth_index-48:auth_index-8]
    ID=r.headers['set-cookie'].split(" ")
    token=[x  for x in ID if(x.find('sess') !=-1 or x.find('guest_id') !=-1)]
except:
    print("Can not Access!")

print(r.status_code)

params={"session[username_or_email]":username,
        "session[password]":password,
        "remember_me":"1",
        "return_to_ssl":"true",
        "scribe_log":"",
        "redirect_after_login":"/",
        "authenticity_token":str(auth_token)
        }

header={
        'HOST':"twitter.com",
        'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0",
        'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language':"ja,en-US;q=0.7,en;q=0.3",
        'Accept-Encoding':"gzip, deflate, br",
        'Referer':"https://twitter.com/",
        'Cookie':token[1]+
                "remember_checked_on=1;"+
                "eu_cn=1;"+
                token[0]+
                "lang=ja; "+
                "dnt=1; "+
                "_gat=1 ",
        'Connection':"keep-alive"
        }

login_url="https://twitter.com/sessions"
try :
    r = s.post(login_url, headers=header, params=params, proxies=proxy)
except:
    print("Can not Access!")

print(r.status_code)

profile_url="https://twitter.com/"+username
try :
    r = s.get(profile_url, proxies=proxy)
except:
    print("Can not Access!")


print(r.status_code)

html=r.text.encode('utf-8')
index=html.find('sms-confirmation-begin-form')
au_token=html[index+155:index+195]


params ={
        'authenticity_token':au_token,
        'page_context':"me",
        'section_context':"profile",
        'user[name]':new_name
#        'user[description]':"お知らせ",
#        'user[location]':"新宿"
        }

s.headers.update({
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Referer":"https://twitter.com/"+username
    })
geo_profile_url='https://twitter.com/account/geo_profile'
update_url='https://twitter.com/i/profiles/update'
try :
    r = s.post(update_url, params=params, proxies=proxy)
except:
    print("Can not Access!")

print(r.status_code)
