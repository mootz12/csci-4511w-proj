# Defines a Blackjack game
#   4 decks
#   3/2 payout
#   dealer stands on soft 17

# Uses a neural net given from main to play

import random
import neat
import os

deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4*4)
num_dealt = 0

# Define initial cash stack for player
pool = 5000
bet = 2

def run_blackjack(nn):
    global deck
    games = 1000
    played, money = play_game(deck, games, nn)
    return played, money
    #print("Played " + str(games) + " games for a return of " + str(money) + "\n")

# Helper functions for NEAT nn

# Translate 2-14 to 0-1 for each card
def get_state(dealer, player):
    inputs = []
    inputs.append(float((dealer[0]-2)/12))
    inputs.append(float((player[0]-2)/12))
    inputs.append(float((player[1]-2)/12))
    return inputs

# Translates a 0-1 move to h, s,
def get_move(move):
    if move <= 0.25:
        return "h"
    elif move <= 0.5:
        return "s"
    elif move <= 0.75:
        return "d"
    else:
        return "p"

# Helper function to deal 2 cards
def deal(deck):
    global num_dealt
    hand = []
    num_dealt += 2
    for i in range(2):
        card = deck.pop()
        hand.append(card)
    return hand

# Helper function to calculate hand score
def score(hand):
    score = 0
    for card in hand:
        if 10 <= card <= 13:
            score += 10
        elif card == 14: #condition where card is an Ace
            if score > 10:
                score += 1
            else:
                score += 11
        else:
            score += card
    return score

# Helper functions to eval hand scores
def is_blackjack(hand):
    value = 0
    value = score(hand)
    return value == 21

def is_bust(hand):
    value = 0
    value = score(hand)
    return value > 21

def can_split(hand):
    return hand[0] == hand[1]

# Player action -> hit
def hit(hand):
    global num_dealt
    card = deck.pop()
    num_dealt += 1
    hand.append(card)
    print("Hit: " + str(card))
    return hand

def hit_dealer(hand):
    global num_dealt
    card = deck.pop()
    num_dealt += 1
    hand.append(card)
    return hand

# Returns a multiple of the bet to add to the players pool
def payout_hand(dealer, player):
    player_score = score(player)
    dealer_score = score(dealer)
    player_bust = is_bust(player)
    dealer_bust = is_bust(dealer)
    player_blackjack = is_blackjack(player)
    dealer_blackjack = is_blackjack(dealer)
    player_out = 0

    # Return -1 if player loses, 1 if player wins, and 3/2 on 21
    if player_bust:
        player_out = -1
    elif dealer_bust:
        if player_blackjack:
            player_out = 1.5
        else:
            player_out = 1
    elif dealer_blackjack:
        if player_blackjack:
            player_out = 0
        else:
            player_out = -1
    elif player_blackjack:
        player_out = 1.5
    elif dealer_score > player_score:
        player_out = -1
    elif player_score > dealer_score:
        player_out = 1
    else:
        player_out = 0

    return player_out

def play_turn(dealer, player, nn):
    stand = False
    valid = True
    payout = 0
    #print("Dealer showing " + str(dealer[0]))
    #print("You have " + str(player[0]) + " - " + str(player[1]))
    # Player plays hand
    while valid and not stand:
        #print("Your score is: " + str(score(player)))
        '''
        if can_split(player):
            choice = input("Hit, stand, double, or split? (h, s, d, p): ")
        else:
            choice = input("Hit, stand, or double? (h, s, d): ")
        '''
        inputs = get_state(dealer, player)
        action = nn.activate(inputs)
        choice = get_move(action)
        if can_split(player) and choice == "p":
            hand1 = [player[0]]
            hit(hand1)
            hand2 = [player[1]]
            hit(hand2)
            return play_turn(dealer,hand1) + play_turn(dealer,hand2)
        elif choice == "d":
            valid = False
            hit(player)
            print("Hand over. Player: " + str(score(player)))
            return 2*payout_hand(dealer, player)
        elif choice == "h":
            hit(player)
            if (is_bust(player) or is_blackjack(dealer)):
                valid = False
        elif choice == "s":
            stand = True
        else:
            print("Invalid input. Please try again.")
    print("Hand over. Player: " + str(score(player)))
    return payout_hand(dealer, player)


def play_hand(deck, nn):
    payout = 0
    dealer = deal(deck)
    player = deal(deck)
    # Play dealer to allow for splits to play against same dealer
    while score(dealer) < 17:
        hit_dealer(dealer)
        if(is_bust(dealer) or is_blackjack(dealer)):
            break
    payout = play_turn(dealer, player)
    print("Dealer: " + str(score(dealer)))
    return payout

def play_game(deck, games):
    global pool
    global bet
    global num_dealt
    random.shuffle(deck)
    num_games = 0;
    while num_games <= games:
        pool += bet*play_hand(deck, nn)
        print("Your total pool is now: " + str(pool))
        print("\n")
        num_games += 1
        if num_dealt > ((4*4*13) / 2):
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4*4)
            random.shuffle(deck)
            num_dealt = 0
        if pool < 0:
            break
    return num_games, pool

if __name__ == "__main__":
    run_blackjack()
