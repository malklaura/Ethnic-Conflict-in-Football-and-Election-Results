import re
import urllib3
import certifi
import numpy as np

from bs4 import BeautifulSoup


def scrape_game_data(game_url):
    """
    Returns a dictionary containing all relevant game data 
    from a prespecified game URL.
    """
    try:
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

        # Get game soup object.
        game_request = http.request("GET", game_url)
        soup = BeautifulSoup(game_request.data, 'lxml')

        # Store game data in dictionary.
        game_dict = {"game_url": game_url}
        game_dict = get_smmry_data(soup, game_dict)
        game_dict = get_player_data(soup, game_dict)
        game_dict = get_card_data(soup, game_dict)

        return game_dict
    except MaxRetryError:
        pass


def get_card_data(soup, game_dict):
    """
    Returns cards for both the home- and away team from a 
    soup object and writes that information in the corresponding 
    game dictionary. Recorded are card color, player name, and 
    minute of the card.
    """

    try:
        # Get container storing card information.
        cards_soup = soup.find(
            "table", {"class": "content_table_std spielerstrafen"})
        cards_soup = cards_soup.find_all("td", {"valign": "top"})

        # Loop through home- and away-team.
        for i, team in enumerate(["home", "away"]):
            # Get cards soup for every team.
            team_cards = cards_soup[i].findAll("div", {"class": "tn_item"})

            # Initalize values for card counting.
            game_dict["{}_card_yllw".format(team)] = 0
            game_dict["{}_card_red".format(team)] = 0

            # Get card color.
            game_dict = get_card_color(team_cards, game_dict, team)

    except AttributeError:
        pass

    return game_dict


def get_card_color(team_cards, game_dict, team):
    """
    Scrapes card color by team and continuously counts cards.
    """

    # Loop through cards by team.
    for j, card in enumerate(team_cards):
        # Loop through all cards of respective team.
        try:
            # Get player name and minute of card.
            player = card.a.text
            minute = card.find("span", {"class": "klammerzahl"}).text[:-1]

            game_dict["{}_card_plyr_{}".format(team, j)] = player
            game_dict["{}_card_min_{}".format(team, j)] = int(minute)

            # Scrape card colors and count cards.
            if team_cards[j].div["style"] == "color:#FBDB04;":
                game_dict["{}_card_clr_{}".format(team, j)] = 1  # yellow = 1
                game_dict["{}_card_yllw".format(team)] += 1

            elif team_cards[j].div["style"] == "color:#D7110C;":
                game_dict["{}_card_clr_{}".format(team, j)] = 2  # red = 2
                game_dict["{}_card_red".format(team)] += 1

            elif team_cards[j].div["class"][0] == "icon_gelbrot":
                game_dict["{}_card_clr_{}".format(team, j)] = 3  # yellow/red=3
                # Counted as two yellow.
                game_dict["{}_card_yllw".format(team)] += 2

            else:
                game_dict["{}_card_clr_{}".format(team, j)] = np.nan

        except AttributeError:
            pass

    return game_dict


def get_player_data(soup, game_dict):
    """
    Returns player data for both the home- and away team
    from a soup object and writes that information in the respective 
    game dictionary. Besides the player names, also the corresponding player
    URLs are retrieved.
    """

    # Loop through teams to store information by team.
    for i, team in enumerate(["home", "away"]):
        try:
            plyrs_soup = soup.findAll(
                "div", {"class": "aufstellung_ausgabe_block {}side".format(team)})[0]
            plyr_data = plyrs_soup.findAll("a", {"class": "spieler_linkurl"})

            # Loop through players by team.
            for j, plyr in enumerate(plyr_data):
                try:
                    game_dict["{}_plyr_{}".format(team, j)] = plyr.text
                    game_dict["{}_plyr_url_{}".format(team, j)] = plyr["href"]
                except AttributeError:
                    pass
        except (AttributeError, IndexError):
            pass

    return game_dict


def get_smmry_data(soup, game_dict):
    """
    Given a soup object, this function returns the general game data,
    ranging from date of the game, the result, the referee as well as the
    name and URL of both teams.
    """

    # Get date and time data.
    try:
        date_soup = soup.find("div", {"class": "spielbericht_tipp_status"})
        league = date_soup.div.span.text
        date_string = date_soup.div.text
        date = re.search(r'\d{2}.\d{2}.\d{2}', date_string).group(0)
        time = re.search(r'\d{2}:\d{2}', date_string).group(0)
        matchday = re.search(r'[|]\d+', date_string).group(0)[1:]

        game_dict["league"] = league
        game_dict["fb_date"] = date
        game_dict["fb_time"] = time
        game_dict["matchday"] = matchday
    except AttributeError:
        pass

    # Get game result.
    try:
        result = soup.find("div", {"class": "stand"}).text
        game_dict["result"] = result
    except AttributeError:
        pass

    # Try to get the referee name.
    try:
        referee = soup.find("span", {"class": "schiri_link"}).text
        game_dict["referee"] = referee
    except AttributeError:
        pass

    # Get team, club name and repective url by team.
    try:
        smmry_soup = soup.find(
            "div", {"class": "spielbericht_ergebnis_wrapper"})
        club_title = smmry_soup.find_all("img")
        team_title = smmry_soup.findAll("div", {"class": "teaminfo"})

        # Loop through teams.
        for j, team in enumerate(["home_", "away_"]):
            game_dict[team + "team"] = team_title[j].a["title"]
            game_dict[team + "team_url"] = team_title[j].a["href"]
            game_dict[team + "club"] = club_title[j]["title"]
    except (AttributeError, TypeError):
        pass

    return game_dict
