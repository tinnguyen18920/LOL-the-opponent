#!Python 3.8 | 2:48 PM | 10-01-2020

#SYSTEM PACKAGES:
import json
import re
#LOCAL PACKAGES:

#Installed PACKAGES (Need install):
import requests
from bs4 import BeautifulSoup

#TODO: BeautifulSoup function


def get_html(url):
    respone = requests.get(url)#.respone
    if respone.ok:
        return respone.content.decode()
    else:
        return None
# def convert_html_to_json():
#     html = get_html("https://www.op.gg/summoner/matches/ajax/averageAndList/summonerId=83714156")
#     data = json.loads(html)
#     return data
# convert_html_to_json()
class OPGG:
    """docstring for OPGG"""
    def __init__(self):
        pass
    def matches_html(self,summoner_id):
        html = get_html("https://www.op.gg/summoner/matches/ajax/averageAndList/summonerId={}".format(summoner_id))
        data = json.loads(html)
        return data.get("html")
    def find_summoner_id(self,user_name):
        url = "https://www.op.gg/summoner/header/userName={}".format(user_name)
        html = get_html(url)
        #print(html)
        if "An error has occurred." in html:
            print("Invalid User name")
            quit()
        try:
            summoner_id = re.search(r"\'(\d+)\'\)\;",html).group(1)
        except:
            soup = BeautifulSoup(html)
            summoner_id_button = soup.find("button",{"id":"SummonerRefreshButton"})
            summoner_id = re.search(r"\d+",html)
        return summoner_id
    def extract_info(self,html):
        soup = BeautifulSoup(html,'html.parser')
        matches_list = soup.find("div",{"class":"GameItemList"})
        return matches_list
html = OPGG().matches_html("4460427")
data = OPGG().extract_info(html)
print(data)


#TODO: Listen sys arguments