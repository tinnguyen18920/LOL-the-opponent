#!Python 3.8 | 8:44 PM | 12-01-2020

import json

import requests
from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Back, Style

from main import get_html

def main():
    html = get_html("https://www.op.gg/spectate/pro/")
    soup = BeautifulSoup(html,"html.parser")
    container = soup.find("div",{"class":"SpectateSummonerList"})
    summoners_ct = container.findAll("div",{"class":"Item"},recursive=False)
    total = len(summoners_ct)
    for sm in summoners_ct:
        sm_name = sm.find("span",{"class":"SummonerName"}).text.strip()
        sm_champ = sm.find("span",{"class":"ChampionName"}).text.strip()
        type = sm.find("div",{"class":"GameType"}).text.strip()
        time = sm.find("div",{"class":"GameTime"}).text.strip()
        team = sm.find("div",{"class":"TeamName"}).text.strip()
        player = sm.find("div",{"class":"Extra"}).text.strip()
        show_lives(sm_name,sm_champ,type,time,team,player)
def show_lives(sm_name,sm_champ,type,time,team,player):
    init(autoreset=True)
    print(Fore.YELLOW + team + " " +Fore.CYAN + player)
    print("\t" + Fore.MAGENTA + sm_champ + Fore.WHITE +" "+type + " (%s)" % time)
    print("\tInGame: " + Fore.GREEN + sm_name)
if __name__ == "__main__":
    main()

