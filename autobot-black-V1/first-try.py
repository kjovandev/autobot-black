import requests
import json
import time
import datetime

credentials = "your_api_key_here"
headers = {"Authorization": f"Basic {credentials}"}
base_url = "https://api.mollybet.com"

# Authentication
def authenticate():
    response = requests.post(f"{base_url}/v1/sessions/", headers=headers, json={"username": "your_username", "password": "your_password"})
    if response.status_code == 200:
        data = response.json()
        return data["session_id"]
    else:
        print("Authentication failed.")
        return None

def retrieve_odds(session_id):
    # this is a placeholder for a get api request for getting data which is returning dummy data temporarely
    with open('dummyData.json', 'r') as file:
        odds_data = json.load(file)
    return odds_data

def find_arbitrage_opportunities(data):
    arbitrage_opportunities = []
    sports = data.get("sports", {})
    for sport, sport_data in sports.items():
        events = sport_data.get("events", {})
        for event_id, event_data in events.items():
            event_name = event_data.get("event_name", "")
            bookmakers = event_data.get("bookmakers", {})
            for bookmaker_a, odds_a in bookmakers.items():
                for bookmaker_b, odds_b in bookmakers.items():
                    if bookmaker_a != bookmaker_b:  
                        odds_over_a = odds_a.get("odds_over_2.5", 0)
                        odds_under_b = odds_b.get("odds_under_2.5", 0)
                        implied_prob_a = 1 / odds_over_a
                        implied_prob_b = 1 / odds_under_b
                        if implied_prob_a + implied_prob_b < 0.97:  
                            arb_opportunity = {
                                "event_id": event_id,
                                "event_name": event_name,
                                "bookmaker_over": bookmaker_a,
                                "bookmaker_under": bookmaker_b,
                                "odds_over": odds_over_a,
                                "odds_under": odds_under_b,
                                "implied_prob_over": implied_prob_a,
                                "implied_prob_under": implied_prob_b,
                                "total_implied_prob": implied_prob_a + implied_prob_b
                            }
                            arbitrage_opportunities.append(arb_opportunity)
    return arbitrage_opportunities

# Using the dummy data
dummy_data = retrieve_odds(authenticate())

arbitrage_opportunities = find_arbitrage_opportunities(dummy_data)

print(len(arbitrage_opportunities))

def dump_to_json(data):
    with open("odds_data.json", "w") as f:
        json.dump(data, f, indent=4)

# def main():
#     session_id = authenticate()
#     if session_id:
#         odds_data = retrieve_odds(session_id)
#         if odds_data:
#             arbitrage_opportunities = find_arbitrage_opportunities(odds_data)
#             dump_to_json(arbitrage_opportunities)
#         else:
#             print("No odds data retrieved.")
#     else:
#         print("Authentication failed.")

# if __name__ == "__main__":
#     main()
