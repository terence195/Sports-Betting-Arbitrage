import json
import pandas as pd
import requests

def main():
    response = requests.get(" https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=70c051405978b54ce300c050c2be62f5&regions=us&markets=h2h,spreads&oddsFormat=american")

    formatted_result = reFormatJSON(response)
    reformatted_result(formatted_result)

def reformatted_result(formatted_result):
    for games in formatted_result:
        bet = [games['Game']]
        for sportsbooks in games['SportsBooks']:
            bet.append(sportsbooks['title'])
            for bets in sportsbooks['Bet']:
                bet.append(bets['price'])
        findArbitrage(bet)

def findArbitrage(bet):
    game = bet[0].split(' vs ')
    for j in range(1, len(bet), 3):
        for i in range (6, len(bet), 3):
            arb1 = arbritage(bet[j+1], bet[i])
            arb2 = arbritage(bet[j+1], bet[i-1])
            if arb1:
                s1, s2 = calculateStake(bet[j+1], bet[i])  
                print(f"Bet on {bet[0]} with ${s1} on {game[0]} on {bet[j]} and ${s2} on {game[1]} on {bet[i-2]}")
            if arb2:
                s1, s2 = calculateStake(bet[j+1], bet[i-1])  
                print(f"Bet on {bet[0]} with ${s1} on {game[1]} on {bet[j]} and ${s2} on {game[0]} on {bet[i-2]}")
                


def arbritage(bet1, bet2):
    bet1 = odd(bet1)
    bet2 = odd(bet2)
    odds = round(bet1 + bet2, 0)
    if odds > 1:
        return False 
    elif odds == 1:
        return False
    else: 
        return True


def calculateStake(bet1, bet2):
    bet1 = odd(bet1)
    bet2 = odd(bet2)
    odds = bet1 + bet2
    s1 = round((bet1*100)/odds, 2)
    s2 = round((bet2*100)/odds, 2)
    return s1, s2
        
    

def odd(odds):
    if odds > 0:
        return 100 / (odds + 100)
    else:
        return -odds / (-odds + 100)
    

def reFormatJSON(response):
    formatted_result = []

    for event in response.json():
        away_team = event.get('away_team')
        home_team = event.get('home_team')
        game = f"{away_team} vs {home_team}"

        sportsbooks = []

        for bookmaker in event.get('bookmakers', []):
            title = bookmaker.get('title')
            bets = []

            for market in bookmaker.get('markets', []):
                for outcome in market.get('outcomes', []):
                    if 'point' not in outcome:
                        bet = {
                            'name': outcome.get('name'),
                            'price': outcome.get('price')
                        }
                        bets.append(bet)

            if bets:
                sportsbooks.append({
                    'title': title,
                    'Bet': bets
                })

        if sportsbooks:
            formatted_result.append({
                'Game': game,
                'SportsBooks': sportsbooks
            })
            
    return formatted_result

if __name__ == "__main__":
    main()
