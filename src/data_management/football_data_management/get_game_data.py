from bs4 import BeautifulSoup
import urllib3
import certifi
import re
from bld.project_paths import project_paths_join as ppj

def scrapping(temp_url, i, game_dict, matchdays_df):    
    
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    
    try:
        r = http.request("GET", temp_url)
        game_dict.at[i, "href"] = temp_url
        soup = BeautifulSoup(r.data, 'lxml')
    except:
        pass

    
    # Summary Statistics
    try:
        date_soup = soup.find("div", {"class":"spielbericht_tipp_status"})
        game_dict.at[i, "league"] = date_soup.div.span.text
        date_text = date_soup.div.text
        game_dict.at[i, "date"] = re.search(r'\d{2}.\d{2}.\d{2}', date_text).group(0)
        game_dict.at[i, "time"] =  re.search(r'\d{2}:\d{2}', date_text).group(0)
        game_dict.at[i, "matchday"] = re.search(r'[|]\d+', date_text).group(0)[1:]
    except:
        pass       
    
    game_dict.at[i, "result"] = soup.find("div", {"class":"stand"}).text
    
    try:
        game_dict.at[i, "referee"] = soup.find("span", {"class":"schiri_link"}).text
    except:
        pass
    
    smmry_container = soup.find("div", {"class":"spielbericht_ergebnis_wrapper"})
    club_title = smmry_container.find_all("img")
    team_title = smmry_container.findAll("div", {"class":"teaminfo"})
    
    teams = {"home_", "away_"}
    
    for j, team in enumerate(teams):
        game_dict.at[i, team + "team"] = team_title[j].a["title"]
        game_dict.at[i, team + "team_url"] = team_title[j].a["href"]
        game_dict.at[i, team + "club"] = club_title[j]["title"]
     
     # Player names   
    try:
        hmsd = soup.findAll("div", {"class": "aufstellung_ausgabe_block homeside"})[0]
        plyrs_hmsd = hmsd.findAll("a", {"class": "spieler_linkurl"})
    except:
        pass
    
    try:
        awsd = soup.findAll("div", {"class": "aufstellung_ausgabe_block awayside"})[0]
        plyrs_awsd = awsd.findAll("a", {"class": "spieler_linkurl"})
    except:
        pass
    
    for j in range(11):
        try:
            game_dict.at[i, "home_" + str(j+1)] = plyrs_hmsd[j].text
            game_dict.at[i, "home_" + str(j+1) + "_url"] = plyrs_hmsd[j]["href"]
        except:
            pass
        try:
            game_dict.at[i, "away_" + str(j+1)] = plyrs_awsd[j].text
            game_dict.at[i, "away_" + str(j+1) + "_url"] = plyrs_awsd[j]["href"]
        except:
            pass
    
    try:
        game_dict.at[i, "avg_hmsd"] = hmsd.div.a.text[-5:]
        game_dict.at[i, "avg_awsd"] = awsd.div.a.text[-5:]
    except AttributeError as e:
        pass
    
    # Cards
    try:
        cards_soup = soup.find("table", {"class":"content_table_std spielerstrafen"})
        cards = cards_soup.findAll("div", {"class":"tn_item"})
        
        for j, card in enumerate(cards):
            game_dict.at[i, "card_plyr_" + str(j)] = card.a.text
            game_dict.at[i, "card_min_" + str(j)] = card.find("span", {"class":"klammerzahl"}).text[:-1]
        
    
            if card.div["style"] == "color:#FBDB04;":
                game_dict.at[i, "card_clr_" + str(j)] = 1 # yellow = 1         
            elif card.div["style"] == "color:#D7110C;":
                game_dict.at[i, "card_clr_" + str(j)] = 2 # red = 2
            elif card.div["class"][0] == "icon_gelbrot":
                game_dict.at[i, "card_clr_" + str(j)] = 3 # yellow / red = 3
            else:
                game_dict.at[i, "card_clr_" + str(j)] = "unknown card_clr"
    except:
        pass
        
    # Goals
    try:    
        goals_soup = soup.find("table", {"class":"content_table_std torschuetzen"})
        goals = goals_soup.findAll("div", {"class":"tn_item torschuetzen_ausgabe"})
        
        for j, goal in enumerate(goals):
            game_dict.at[i, "goal_" + str(j)] = goal.find("span", {"class":"spielstand"}).text
            game_dict.at[i, "goal_plyr_" + str(j)] = goal.img["title"]
            game_dict.at[i, "goal_min" + str(j)] = goal.find("span", {"class":"klammerzahl"}).text[:-1]
    except:
        pass
    
    # Coach
    try:
        coach_hmsd = soup.findAll("div", {"class": "aufstellung_ausgabe_block homeside"})[2]
        game_dict.at[i, "coach_hmsd"] = coach_hmsd.a.text
        coach_awsd = soup.findAll("div", {"class": "aufstellung_ausgabe_block awayside"})[2]
        game_dict.at[i, "coach_awsd"] = coach_awsd.a.text
    except:
        pass

    # set to done
    matchdays_df.loc[matchdays_df["href"] == temp_url, "done"] = 1