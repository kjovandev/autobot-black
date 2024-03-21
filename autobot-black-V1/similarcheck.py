# in order to find the mistake we need to turn diff_bet_one and two to positive numbers 



def betting(arbOppsSoccer):
    if len(arbOppsSoccer) > 0:
        for bet in arbOppsSoccer:
            bookie1Key = bookie1.bookieOnekey
            bookie1 = bet.bookieOne
            betOne = bookie1.odds
            bookie2 = bet.bookieTwo
            betTwo = bookie2.odds
            
            # Calculate the average odds for the event from other bookies
            other_bookies_avg = (bookie1.avg_odds + bookie2.avg_odds) / 2
            
            # Calculate the difference between each bet and the average odds
            diff_bet_one = abs(betOne - other_bookies_avg)
            diff_bet_two = abs(betTwo - other_bookies_avg)
            
            # Determine which bet is closer to the average odds
            if diff_bet_one < diff_bet_two:
                # Place bet on bookieTwo
                place_bet(bookie2, betTwo)
            else:
                # Place bet on bookieOne
                place_bet(bookie1, betOne)

def place_bet(bookie, bet):
    # Implement bet placement logic here
    pass  # Placeholder for actual bet placement logic

