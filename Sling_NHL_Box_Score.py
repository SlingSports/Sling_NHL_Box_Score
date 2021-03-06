# -*- coding: utf-8 -*-
# Author: John Freed - @jtf323

from colorama import init, Fore, Style
import datetime
import json
import os
import platform
import sys
import time
import requests

refresh_time = 60  # Refresh time (seconds), as per NHL API
api_url = 'http://live.nhle.com/GameData/RegularSeasonScoreboardv3.jsonp?loadScoreboard=jQuery110105207217424176633_1428694268811&_=1428694268812'
api_headers = {'Host': 'live.nhle.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36', 'Referer': 'http://www.nhl.com/ice/scores.htm'}

show_today_only = False


def main():
    clear_screen()

    # Format dates to match NHL API style:

    # Today's date
    t = datetime.datetime.now()
    todays_date = "" + t.strftime("%A") + " " + "%s/%s" % (t.month, t.day)
    
    # Yesterday's date
    y = t - datetime.timedelta(days=1)
    yesterdays_date = "" + y.strftime("%A") + " " + "%s/%s" % (y.month, y.day)

    while True:
        clear_screen()

        r = requests.get(api_url, headers=api_headers)
        
        # We get back json data with some JS around it, gotta remove the JS
        json_data = r.text

        # Remove the leading JS
        json_data = json_data.replace('loadScoreboard(', '')

        # Remove the trailing ')'
        json_data = json_data[:-1]

        data = json.loads(json_data)
        for key in data:
            if key == 'games':
                for game_info in data[key]:

                    # Assign more meaningful names    
                    game_clock = game_info['ts']
                    game_stage = game_info['tsc']
                    status = game_info['bs']

                    away_team_locale = game_info['atn']
                    away_team_name = game_info['atv'].title()
                    away_team_score = game_info['ats']
                    away_team_result = game_info['atc']

                    home_team_locale = game_info['htn']
                    home_team_name = game_info['htv'].title()
                    home_team_score = game_info['hts']
                    home_team_result = game_info['htc']

                    # Fix strange names / locales returned by NHL
                    away_team_locale = fix_locale(away_team_locale)
                    home_team_locale = fix_locale(home_team_locale)
                    away_team_name = fix_name(away_team_name)
                    home_team_name = fix_name(home_team_name)

                    # Show games from Yesterday and today or just today
                    if (yesterdays_date in game_clock.title() and not show_today_only) or todays_date in game_clock.title() or 'TODAY' in game_clock or 'LIVE' in status:

                        header_text = away_team_locale + ' ' + away_team_name + ' @ ' + home_team_locale + ' ' + home_team_name
                        
                        # Different displays for different states of game:
                        # Game from yesterday, ex: on YESTERDAY, MONDAY 4/20 (FINAL 2nd OT)
                        # Game from today finished, ex: TODAY (FINAL 2nd OT)
                        if 'FINAL' in status:
                            if yesterdays_date in game_clock.title():
                                header_text += '\nYESTERDAY, ' + game_clock + ' '
                            elif todays_date in game_clock.title() or 'TODAY' in game_clock:
                                header_text += '\nTODAY '
                            header_text += '(' + status + ')'

                        # Upcoming game, ex: TUESDAY 4/21, 7:00 PM EST)
                        elif 'DAY' in game_clock:
                            header_text += Fore.YELLOW + '\n(' + game_clock + ', ' + status + ' EDT)' + Fore.RESET

                        # Last 5 minutes of game and overtime, ex: (1:59 3rd PERIOD) *in red font*
                        elif 'critical' in game_stage:
                            header_text += '\n(' + Fore.RED + game_clock + ' PERIOD' + Fore.RESET + ')'

                        # Any other time in game, ex: (10:34 1st PERIOD)
                        else:
                            header_text += Fore.YELLOW + '\n(' + game_clock + ' PERIOD)' + Style.RESET_ALL

                        print header_text


                        # Highlight the winner of finished games in green, and games underway in blue:
                        # Away team wins
                        if away_team_result == 'winner':
                            print Style.BRIGHT + Fore.GREEN + away_team_name + ': ' + away_team_score + Style.RESET_ALL
                            print home_team_name + ': ' + home_team_score

                        # Home team wins
                        elif home_team_result == 'winner':
                            print away_team_name + ': ' + away_team_score
                            print Style.BRIGHT + Fore.GREEN + home_team_name + ': ' + home_team_score + Style.RESET_ALL

                        # Game still underway
                        elif 'progress' in game_stage or 'critical' in game_stage:
                            print Fore.CYAN + away_team_name + ': ' + away_team_score
                            print home_team_name + ': ' + home_team_score + Fore.RESET

                        # Game hasn't yet started
                        else:
                            print away_team_name + ': ' + away_team_score
                            print home_team_name + ': ' + home_team_score

                        print ''
                    
        # Perform the sleep
        time.sleep(refresh_time)


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def print_help():
    print 'By default games from yesterday and today will be displayed.'
    print ''
    print 'If you want to see games from just today run the program with '
    print 'the "--today-only" flag.'


def fix_locale(team_locale):
    # NHL API forces team name in locale for both New York teams, i.e. locale + name == "NY Islanders islanders"
    if 'NY ' in team_locale:
        return 'New York'

    if 'Montr' in team_locale:
        return u'Montréal'
        
    return team_locale


def fix_name(team_name):
    # Change "redwings" to "Red Wings"
    if 'wings' in team_name:
        return 'Red Wings'

    # Change "bluejackets" to "Blue Jackets"
    if 'jackets' in team_name:
        return 'Blue Jackets'

    # Change "mapleleafs" to "Maple Leafs"
    if 'leafs' in team_name:
        return 'Maple Leafs'

    return team_name


def parse_arguments(arguments):
    global show_today_only
    for x in range(1, len(arguments)):
        argument = arguments[x]

        if argument == '--help' or argument == '-h':
            print_help()
            sys.exit(0)
        elif argument == '--today-only':
            show_today_only = True


if __name__ == '__main__':
    # Initialize Colorama
    init()

    # Parse any arguments provided
    parse_arguments(sys.argv)

    # Start the main loop
    main()
