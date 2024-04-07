import requests
import json
# todo optimise codea and format it PROPERLY


# a lot of code needs to be adapted in order for the algorithm to work. (examples would be the for loop, which solely depents on the api response for getting ods)

credentials = "your_api key goes here"
headers = {"input whatever the docs say "}
base_url = "https://www.randomurl.com/api" #see url docs
budget = 500 #placeholder for an api response that contains our budget in euros / dollars
with open('dummyData.json', 'r') as file:
    dummy_data = json.load(file) #placeholder dummy data that is used for now 
odds_response = dummy_data #placeholder for a response which will be used 



# Authentication
# def authenticate():
#     response = requests.post(f"{base_url}/v1/sessions/", headers=headers, json={"username": "your_username", "password": "your_password"})
#     if response.status_code == 200:
#         data = response.json()
#         return data["session_id"]
#     else:
#         print("Authentication failed.")
#         return None



obradjeni = []    

def find_arb_opps(data):
    arb_opps = []
    sports = data.get("sports", {})
    for sport, sport_data in sports.items():
        events = sport_data.get("events", {})
        for event_id, event_data in events.items():
            obradjeni = []
            event_name = event_data.get("event_name", "")
            bookmakers = event_data.get("bookmakers", {})
            for bookmaker_a, odds_a in bookmakers.items():
                obradjeni.append(bookmaker_a)
                # if len(arb_opps) == 1:
                #     break  # Break out of the loop if one arbitrage opportunity is found
                for bookmaker_b, odds_b in bookmakers.items():
                    if obradjeni.__contains__(bookmaker_b):
                        continue
                    # if len(arb_opps) > 0:
                    #     break  # Skip if one arbitrage opportunity is found or if it's the same bookmaker
                    odds_over_a = odds_a.get("odds_over_2.5", 0)
                    odds_under_b = odds_b.get("odds_under_2.5", 0)
                    implied_prob_a = (1 / odds_over_a) * 100
                    implied_prob_b = (1 / odds_under_b) * 100
                    total_implied_prob = implied_prob_a + implied_prob_b
                    limit_bookie_a = odds_a.get("odds_over_2.5_stake_limit", 0)
                    limit_bookie_b = odds_b.get("odds_under_2.5_stake_limit", 0)
                    if implied_prob_a + implied_prob_b < 97:  
                        arb_opportunity = {
                            "sport_id": sport,
                            "event_id": event_id,
                            "event_name": event_name,
                            "bookmaker_over": bookmaker_a,
                            "bookmaker_under": bookmaker_b,
                            "odds_over": odds_over_a,
                            "odds_under": odds_under_b,
                            "implied_prob_over": implied_prob_a,
                            "implied_prob_under": implied_prob_b,
                            "total_implied_prob": total_implied_prob,
                            "limit_for_odds_over": limit_bookie_a,
                            "limit_for_odds_under": limit_bookie_b
                        }
                        arb_opps.append(arb_opportunity)
                        break
    return arb_opps


arb_opps = find_arb_opps(odds_response)
print(arb_opps)

def average_odds(arb_opps, odds_response):
    avg_odds = []
    event_odds = {}
    for arb_opp in arb_opps:
        event_key = f"{arb_opp['sport_id']}_{arb_opp['event_id']}"
        if event_key not in event_odds:
            event_odds[event_key] = {"over": [], "under": []}
        for sport, sport_data in odds_response["sports"].items():
            if sport == arb_opp["sport_id"]:
                events = sport_data.get("events", {})
                for event_id, event_data in events.items():
                    if event_id == arb_opp["event_id"]:
                        bookmakers = event_data.get("bookmakers", {})
                        for bookmaker, odds in bookmakers.items():
                            over_odds = odds.get("odds_over_2.5", None)
                            under_odds = odds.get("odds_under_2.5", None)
                            if over_odds is not None and under_odds is not None:
                                event_odds[event_key]["over"].append(over_odds)
                                event_odds[event_key]["under"].append(under_odds)
                               
    for event_key, odds_data in event_odds.items():
        avg_over = sum(odds_data["over"]) / len(odds_data["over"])
        avg_under = sum(odds_data["under"]) / len(odds_data["under"])
        # print(f"Event: {event_key}, Average Over Odds: {avg_over:.2f}, Average Under Odds: {avg_under:.2f}")
        average_odds_input = {
            "Event_num" : event_key,
            "avg_odds_OVER": avg_over,
            "avg_odds_UNDER" : avg_under
            }
        avg_odds.append(average_odds_input)
        return(avg_odds)
    
avg_odds_returned = average_odds(arb_opps, odds_response)

def human_error(avg_odds_returned_data, arb_opps_data):
    final_arb_data = []
    avg_odd_over = avg_odds_returned[0].get("avg_odds_OVER", 0)
    avg_odd_under = avg_odds_returned[0].get("avg_odds_UNDER", 0)
    arb_opp_under =  arb_opps_data[0].get("odds_under_2.5", 0)
    arb_opps_over =  arb_opps_data[0].get("odds_over_2.5", 0)
    dif_under = abs(avg_odd_under - arb_opp_under)
    dif_over = abs(avg_odd_over - arb_opps_over)
    if dif_under > dif_over:
        final_calcs = {
                        "sport_id": avg_odds_returned[0].get("sport_id", 0),
                        "event_id": avg_odds_returned[0].get("event_id", 0),
                        "event_name": avg_odds_returned[0].get("event_name", 0),
                        "bookmaker_over": avg_odds_returned[0].get("bookmaker_over", 0),
                        "bookmaker_under": avg_odds_returned[0].get("bookmaker_under", 0),
                        "odds_over": avg_odds_returned[0].get("odds_over", 0),
                        "odds_under": avg_odds_returned[0].get("odds_under", 0),
                        "implied_prob_over": avg_odds_returned[0].get("implied_prob_over", 0),
                        "implied_prob_under": avg_odds_returned[0].get("implied_prob_under", 0),
                        "total_implied_prob": avg_odds_returned[0].get("total_implied_prob", 0),
                        "limit_for_odds_over": avg_odds_returned[0].get("limit_for_odds_over", 0),
                        "limit_for_odds_under": avg_odds_returned[0].get("limit_for_odds_under", 0), 
                        "first to play is ": "UNDER"
                        }
    elif dif_over > dif_under:
         if dif_over > dif_under:
             final_calcs = { 
                        "sport_id": avg_odds_returned[0].get("sport_id", 0),
                        "event_id": avg_odds_returned[0].get("event_id", 0),
                        "event_name": avg_odds_returned[0].get("event_name", 0),
                        "bookmaker_over": avg_odds_returned[0].get("bookmaker_over", 0),
                        "bookmaker_under": avg_odds_returned[0].get("bookmaker_under", 0),
                        "odds_over": avg_odds_returned[0].get("odds_over", 0),
                        "odds_under": avg_odds_returned[0].get("odds_under", 0),
                        "implied_prob_over": avg_odds_returned[0].get("implied_prob_over", 0),
                        "implied_prob_under": avg_odds_returned[0].get("implied_prob_under", 0),
                        "total_implied_prob": avg_odds_returned[0].get("total_implied_prob", 0),
                        "limit_for_odds_over": avg_odds_returned[0].get("limit_for_odds_over", 0),
                        "limit_for_odds_under": avg_odds_returned[0].get("limit_for_odds_under", 0) ,
                        "first_to_play_is: ": "OVER"
                        }
         else:
             print("error in finding first to play")
    final_arb_data.append(final_calcs)
    return(final_arb_data)
    
final_data_to_bet = human_error(avg_odds_returned, arb_opps)
    



print("..................")
print("final data to bet is: ")
print(final_data_to_bet)

def calc_bets(arb_opps_data, budget_data):

    budget_safe = budget * 0.9
    odds_under =  arb_opps_data[0].get("odds_under_2.5", 0)
    odds_over =  arb_opps_data[0].get("odds_over_2.5", 0)
    limit_under = arb_opps_data[0].get( "limit_for_odds_under", 0)
    limit_over = arb_opps_data[0].get( "limit_for_odds_over", 0)
    total_probability = arb_opps_data[0].get("total_implied_prob", 0)
    implied_prob_under = arb_opps_data[0].get("implied_prob_under", 0)
    implied_prob_over = arb_opps_data[0].get("implied_prob_over", 0)
    limit_over_safe = limit_over *0.9
    limit_under_safe = limit_under * 0.9
    bet_over_where_limit_under_is_budget_for_under = (limit_under_safe / implied_prob_under) * implied_prob_over
    bet_under_where_limit_over_is_budget_for_over = (limit_over_safe / implied_prob_over) * implied_prob_under
    if budget_data < limit_under and budget_data < limit_over:
        bet_stake_under = (budget_safe / total_probability) * implied_prob_under
        bet_stake_over = (budget_safe / total_probability) * implied_prob_over
    elif bet_over_where_limit_under_is_budget_for_under < limit_over_safe:
        bet_stake_under = limit_under_safe
        bet_stake_over = bet_over_where_limit_under_is_budget_for_under
    elif bet_under_where_limit_over_is_budget_for_over < limit_under_safe:
        bet_stake_over = limit_over_safe
        bet_stake_under = bet_under_where_limit_over_is_budget_for_over
    else:
        print("CLUSTERFUCK")
    # print("bet stake for under is:", bet_stake_under)
    # print("bet stake for over is:", bet_stake_over)
    print("limit for under is: ", limit_under)
    print("limit for over is: ", limit_over)
    print("odds for over are: ", odds_over)
    print("odds for under are: ", odds_under)

calc_bets(arb_opps, budget)

with open("found-arbs.json", "w") as f:
    json.dump(arb_opps, f, indent=4)


def placing_priority_bet():
    requests.post("API DOCS, but place priority bet first")
response_priority_bet = "api placeholder"
response_about_placed_bets = "whatever"
def placing_second_bet():
    if response_priority_bet == "success" and response_about_placed_bets != "watever the bet isnt placed already" :# see the api docs
        requests.post("api docs, place non priority bet")
    else: 
        print("first bet denied, wont place second")
        print("ERROR ERROR ERROR ERROR ERROR")
        


# def main():
#     session_id = authenticate()
#     if session_id:
#         odds_data = retrieve_odds(session_id)
#         if odds_data:
#             arb_opps = find_arb_opps(odds_data)
#             dump_to_json(arb_opps)
#         else:
#             print("No odds data retrieved.")
#     else:
#         print("Authentication failed.")

# if __name__ == "__main__":
#     main()
