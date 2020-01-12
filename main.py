#!Python 3.8 | 2:48 PM | 10-01-2020


import json
import re

import requests
from bs4 import BeautifulSoup
from colorama import init
from colorama import Fore, Back, Style

def get_html(url):
    respone = requests.get(url)#.respone
    if respone.ok:
        return respone.content.decode()
    else:
        return None
        
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

        if "An error has occurred." in html:
            print("Invalid Summoner Name or Press 'q' to exit")
            return None
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
        matches = matches_list.findAll("div",{"class":"GameItemWrap"})
        data = {}
        for m in matches:
            game_data = {}
            game_id = m.div["data-game-id"]
            game_data["result"] = m.div["data-game-result"]
            content = m.find("div",{"class":"Content"})

            ##GameStats
            #gamestats_container = content.find("div",{"class":"GameStats"}) 
            game_data["type"] = content.find("div",{"class":"GameType"}).text.strip()
            game_data["time"] = content.find("div",{"class":"TimeStamp"}).find("span").text.strip()
            game_data["length"] = content.find("div",{"class":"GameLength"}).text.strip()

            ##GameSettingInfo

            ##KDA
            kda_container = content.find("div",{"class":"KDA"})
            KDA = kda_container.find("div",{"class":"KDA"})#.text.strip()
            game_data["Kill"] = KDA.find("span",{"class":"Kill"}).text.strip()
            game_data["Death"] = KDA.find("span",{"class":"Death"}).text.strip()
            game_data["Assist"] = KDA.find("span",{"class":"Assist"}).text.strip()
            ##Stats
            ##Items
            ##FollowPlayers Names
            players_container = content.find("div",{"class":"FollowPlayers Names"})
            teams = players_container.findAll("div",{"class":"Team"})
            team1_summoners = teams[0].findAll("div",recursive=False)
            team2_summoners = teams[1].findAll("div",recursive=False)

            team1 , team2 = {},{}
            for sm in team1_summoners:
                stt = str(team1_summoners.index(sm))
                champion = sm.find("div",{"class","ChampionImage"}).div.text.strip()
                sm_name = sm.find("div",{"class":"SummonerName"}).text.strip()
                team1.setdefault(stt,{"name":sm_name,"champion":champion})
                if "Requester" in sm["class"]:
                    team1.setdefault("rq",stt) # Summoner Requester Index
                    team1.setdefault("team","team1") # Summoner Requester Team
            for sm in team2_summoners:
                stt = str(team2_summoners.index(sm))
                champion = sm.find("div",{"class","ChampionImage"}).div.text.strip()
                sm_name = sm.find("div",{"class":"SummonerName"}).text.strip()
                team2.setdefault(stt,{"name":sm_name,"champion":champion})
                if "Requester" in sm["class"]:
                    #print("Summoner Requester")
                    team2.setdefault("rq",stt) # Summoner Requester Index
                    team2.setdefault("team","team2") # Summoner Requester Team
                # else:
                #     print(sm["class"])

            #game_data["teams"] = [team1,team2]######################IMPORTANT LINE

            if team1.get("rq"):
                rq = team1.get("rq")
                team = team1.get("team")
            else:
                rq = team2.get("rq")
                team = team2.get("team")

            if team == "team1":
                game_data["summoner_champ"] = team1.get(rq)['champion']
                game_data["opponent_name"] = team2.get(rq)['name']
                game_data["opponent_champ"] = team2.get(rq)['champion']
            elif team == "team2":
                game_data["summoner_champ"] = team2.get(rq)['champion']
                game_data["opponent_name"] = team1.get(rq)['name']
                game_data["opponent_champ"] = team1.get(rq)['champion']
            data.setdefault(game_id,game_data)
        return data

def intro(summoner):
    intro_message = "Recent matches %s" % summoner
    print(intro_message.center(60,"-"))

def outro():
    outro_message = ""
    print("")

def show_content(data):
    #Format:
    # #length matches of user:
    #Ranked Solo 14 Jan 2020 (31min32s):
    #       TwistedFate vs Zed (Sof13)(SNG SOFM)
    init(autoreset=True)
    for d in data:
        type_ = data[d]["type"]
        time = data[d]["time"]
        length = data[d]["length"]
        Kill = data[d]["Kill"]
        Death = data[d]["Death"]
        Assist = data[d]["Assist"]
        summoner_champ = data[d]["summoner_champ"]
        opponent_champ = data[d]["opponent_champ"]
        opponent_name = data[d]["opponent_name"]
        result = data[d]["result"]
        if result == "win":
            print(Back.BLUE + "{} {} ({}):".format(type_,time,length) )

            print("\t\t"+Fore.WHITE+"%s (" % summoner_champ \
                +Fore.GREEN+"%s" % Kill \
                +Fore.WHITE +"/"\
                +Fore.RED+"%s" % Death\
                +Fore.WHITE +"/"\
                +Fore.GREEN + "%s" % Assist\
                +Fore.WHITE + ") vs %s (%s)" % (opponent_champ, opponent_name))

        else:
            print(Back.RED + "{} {} ({}):".format(type_,time,length) )

            print("\t\t"+Fore.WHITE+"%s (" % summoner_champ \
                +Fore.GREEN+"%s" % Kill \
                +Fore.WHITE +"/"\
                +Fore.RED+"%s" % Death\
                +Fore.WHITE +"/"\
                +Fore.GREEN + "%s" % Assist\
                +Fore.WHITE + ") vs %s (%s)" % (opponent_champ, opponent_name))


def main():
    while True:
        summoner = input("Summoner:\n")
        if summoner == 'q':
            quit()
        summoner_id = OPGG().find_summoner_id(summoner)
        if summoner_id:
            break

    html = OPGG().matches_html(summoner_id)
    intro(summoner)
    data = OPGG().extract_info(html)
    show_content(data)
if __name__ == "__main__":
    main()
