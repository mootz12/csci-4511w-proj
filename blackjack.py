# Defines a Blackjack game
#   4 decks
#   3/2 payout
#   dealer stands on soft 17

import random
import os

deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4*4)
num_dealt = 0

# Define initial cash stack for player
pool = 10000
bet = 2

def main():
    played, money = play_games(deck, 100)
    print("Played " + games + " games for a return of " + money + "\n")

# Helper function to deal 2 cards
def deal(deck):
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
        elif card = 14: #condition where card is an Ace
            if score > 10:
                score += 11
            else:
                score +=1
        else:
            score += card

# Helper functions to eval hand scores
def is_blackjack(hand):
    score = score(hand)
    return score == 21

def is_bust(hand):
    score = score(hand)
    return score > 21

# Player action -> hit
def hit(hand):
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

def play_hand(deck):
    dealer = deal(deck)
    player = deal(deck)
    print("Dealer showing " + dealer[0] + "\n")
    print("You have " + player[0] + player[1] + "\n")
    # PLayer plays hand
    choice = input("Hit or stand? (h or s): ")
    while (choice[0] == "h" or choice[0] == "H"):
        hit(player)
        if (is_bust(player) or is_blackjack(dealer)):
            break
        choice= input("New score is " + score(player) + " hit or stand? (h or s): ")
    # Dealer plays hand
    while score(dealer) < 17:
        hit(dealer)
        if(is_bust(dealer) or is_blackjack(dealer)):
            break
    return payout_hand

def play_game(deck, games):
    random.shuffle(deck)
    num_games = 0;
    while num_games <= games:
        pool += bet*play_hand(deck)
        num_games += 1
        if num_dealt > (sizeof(deck) / 2):
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*(4*4)
            random.shuffle(deck)
            num_dealt = 0
        if pool < 0:
            break
    return num_games, pool
