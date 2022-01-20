#Blackjack game

import random
suits = ('Hearts','Diamonds','Spades','Clubs')

ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace')

values = {"Two":2,"Three":3,"Four":4,"Five":5,"Six":6,"Seven":7,"Eight":8,"Nine":9,"Ten":10,"Jack":10,"Queen":10,"King":10,"Ace":11}

#CLASSES
#card class
class Card():
  def __init__(self,suit,rank):
    self.suit = suit
    self.rank = rank
    self.value = values[rank]

  def __str__(self):
    return self.rank + " of " + self.suit

#deck class: 52 instances of card objects, shuffle, deal one card
class Deck():
  def __init__(self):

    self.deck = []

    for suit in suits:
      for rank in ranks:
        card = Card(suit,rank)
        self.deck.append(card)

  def __str__(self):
    deck = ""
    for card in self.deck:
      deck += "\n" + card.__str__()
    return deck

  def shuffle(self):
    random.shuffle(self.deck)

  def deal(self):
    single_card = self.deck.pop()
    return single_card

#hand class: add card from Deck.deal(), adjust for aces. represents the player and dealer
class Hand():
  def __init__(self):
    self.cards = []
    self.value = 0
    self.aces = 0 #number of aces 

  def add_card(self,card):
    self.cards.append(card)
    self.value += values[card.rank]

    if card.rank == "Ace":
      self.aces += 1

  def adjust_for_ace(self):
    while self.value > 21 and self.aces > 0:

      self.value -= 10
      self.aces -= 1

#chips class: keeps track of starting chips, winning and losing bets
class Chips():
  def __init__(self):
    self.total = 100
    self.bet = 0

  def win_bet(self):
    self.total += self.bet * 1.5
    print(f"Player won {player_chips.bet * 1.5} chips!")

  def lose_bet(self):
    self.total -= self.bet
    print(f"Player lost {player_chips.bet} chips!")

#FUNCTIONS
#to take bets
def take_bet(chips):
  while True:
    try:
      chips.bet = int(input(f"\nYou have {chips.total} chips. Enter your bet: "))

    except:
      print("Sorry, that is not a number (ex. 7). Please try again.")
      continue

    if chips.bet > chips.total:
      print(f"Sorry, you don't have enough chips. Please bet again, you have {chips.total} chips.")

    else:
      print(f"\nYou bet {chips.bet} chips.")
      break

#to take hits
def hit(deck,hand):
  hand.add_card(deck.deal())
  hand.adjust_for_ace()

#to double down: double original bet and recieving only one more card regardless of denomination
def double_down(deck,hand,chips):
  chips.bet *= 2
  print(f"You have doubled your bet to {chips.bet}. You will recieve one more card.")
  lastcard = deck.deal()
  hand.add_card(lastcard)
  hand.adjust_for_ace()
  print(f"You have recieved {lastcard}.")

#for when player wants to do split.
def for_split(chips):
  global if_split
  if_split = True
  print("You now have two hands.")
  print(f"A second bet of {chips.bet} chips has been placed equal to the first on the second hand.")

#ask player if they want to hit stand or dd
def hit_stand_dd(deck,hand,chips):
  global playing

  while True:
    hints(player,dealer)
    answer = input("\nWould you like to hit (h), stand (s), or double down (d)?: ")

    print("–––––––––––" * 6)

    if (answer == "d") and (chips.total < chips.bet * 2):
      print("YOU DON'T HAVE ENOUGH CHIPS TO DOUBLE DOWN. PLEASE SELECT ANOTHER MOVE.")

    elif answer not in ["h","s","d"]:
      print("Invalid, please enter hit (h) , stand (s) or double down (d) exactly.")

    else:
      break
      
  if answer == "h":
    print("PLAYER HITS!")
    hit(deck,hand)

  elif answer == "s":
    print("PLAYER STANDS!\n\nDealer's Turn:")
    if if_split:
      global playing_split1
      global playing_split2
      playing = True
      playing_split1 = False
      playing_split2 = False
    else:
      playing = False

  elif answer == "d":
    print("PLAYER DOUBLE DOWNS!")
    double_down(deck,hand,player_chips)
    if if_split:
      playing = True
      playing_split1 = False
      playing_split2 = False
    else:
      playing = False

#ask player if want to hit stand dd or split. will only be run if player can split(starting cards are the same vaue)
def hit_stand_dd_split(deck,hand,chips):
  global playing

  while True:
    hints(player,dealer)
    answer = input("\nWould you like to hit (h), stand (s), double down (d), or split(p)?: ")

    print("–––––––––––" * 6)

    if (answer == "d") and (chips.total < chips.bet * 2):
      print("YOU DON'T HAVE ENOUGH CHIPS TO DOUBLE DOWN. PLEASE SELECT ANOTHER MOVE.")

    elif answer == "s" and (chips.total < chips.bet * 2):
      print("YOU DON'T HAVE ENOUGH CHIPS TO SPLIT. PLEASE SELECT ANOTHER MOVE.")

    elif answer not in ["h","s","d","p"]:
      print("Invalid, please enter hit (h), stand (s), double down (d) or split (p)")

    else:
      break
      
  if answer == "h":
    print("PLAYER HITS!")
    hit(deck,hand)

  elif answer == "s":
    print("PLAYER STANDS!\n\nDealer's Turn:")
    playing = False

  elif answer == "d":
    print("PLAYER DOUBLE DOWNS!")
    double_down(deck,hand,player_chips)
    playing = False

  elif answer == "p":
    print("PLAYER SPLITS!")
    for_split(player_chips)

#to display 1 of the dealer's cards when still playing
def show_some(player,dealer):

  print("\nDealer's hand: (one card is hidden)")
  print(dealer.cards[0])
  
  print("\nPlayer's hand:")
  for card in player.cards:
    print(card)
  player.adjust_for_ace()
  print(f"Value: {player.value}")

#to display all cards at the end to see the results
def show_all(player,dealer):
  print("–––––––––––" * 6)
  print("\nFINAL RESULTS:")
  print("\nDealer's hand:")
  for card in dealer.cards:
    print(card)
  dealer.adjust_for_ace()
  print(f"Value: {dealer.value}")

  print("\nPlayer's hand:")
  for card in player.cards:
    print(card)
  player.adjust_for_ace()
  print(f"Value: {player.value}")

#functions for end of game scenarios

#player busts
def player_busts(player,dealer,chips):
  print("\nPlayer BUSTS!")
  chips.lose_bet()

#player wins
def player_wins(player,dealer,chips):
  print("\nPlayer WINS!")
  chips.win_bet()

#dealer busts
def dealer_busts(player,dealer,chips):
  print("\nDealer BUSTS!")
  chips.win_bet()
    
#dealer wins
def dealer_wins(player,dealer,chips):
  print("\nDealer WINS!")
  chips.lose_bet()

#tie
def push(player,dealer):
  print("\nPUSH! Player and Dealer tie!")

#hints depending on value of player's hand
def hints(player,dealer):
  print("\nHINT:")

  if player.value <= 8:
    print("Highly recommended: hit (h)")

  elif player.value == 9:
    print("If dealer shows 3–6: You should double down (d)")
    print("If dealer shows 2 or 7+: You shoud hit (h)")

  elif player.value == 10:
    print("If dealer shows 2-9: You should double down (d)")
    print("If dealer shows 10 or Ace: You should hit (h)")

  elif player.value == 11:
    print("If dealer shows 2-10: You should double down (d)")
    print("If dealer shows Ace: You should hit (h)")

  elif player.value == 12:
    print("If dealer shows 2, 3, or 7+: You should hit (h)")
    print("If dealer shows 4-6: You should stand (s)")

  elif 16 >= player.value >= 13:
    print("If dealer shows 7+: You should hit (h)")
    print("If dealer shows 2-6: You should stand (s)")

  elif 21 >= player.value >= 17:
    print("Highly recommended: stand (s)")

#LOGIC
gameon = True
while gameon:
  print("\n")
  print("–––––––––––" * 6)
  print("Hi! Welcome to BlackJack!")

  #create deck and shuffle
  deck = Deck()
  deck.shuffle()

  #deal 2 cards each to player and dealer
  player = Hand()
  card1 = deck.deal()
  card2 = deck.deal()
  player.add_card(card1)
  player.add_card(card2)

  dealer = Hand()
  dealer.add_card(deck.deal())
  dealer.add_card(deck.deal())

  #make another instance of hand for a second dealer to play against a second hand for split
  dealer2 = Hand()
  dealer2.add_card(deck.deal())
  dealer2.add_card(deck.deal())

  #make 2 instances of hands for if player makes a split with old cards
  split_player1 = Hand()
  split_player1.add_card(card1)

  split_player2 = Hand()
  split_player2.add_card(card2)

  #set up player's chips and ask take bet
  player_chips = Chips()
  take_bet(player_chips)

  #create 2 separate instance of player's chips in event of split, and put the same bet on both new hands
  split_chips1 = Chips()
  split_chips2 = Chips()
  split_chips1.total = player_chips.total
  split_chips2.total = player_chips.total
  split_chips1.bet = player_chips.bet
  split_chips2.bet = player_chips.bet

  #later player_chips will = split_chips1 + split_chips2 for the total chips after both are finished 

  print("–––––––––––" * 6)
  #show cards, but keep one dealer card hidden
  show_some(player,dealer)

  playing = True
  if_split = False

  while playing:
    
    #if can run split (starting cards have equal value)
    if card1.value == card2.value:
      hit_stand_dd_split(deck,player,player_chips)

    #if the player choses split. basically remake game in here

    while if_split:

      print("–––––––––––" * 6)

      print("\nHAND 1:")
      playing_split1 = True
      while playing_split1:

        show_some(split_player1,dealer)
        hit_stand_dd(deck,split_player1,split_chips1)

        if split_player1.value > 21:
          show_all(split_player1,dealer)
          player_busts(split_player1,dealer,split_chips1)
          break

      if split_player1.value <= 21:
        while dealer.value < 17:
          print("\nDEALER HITS!")
          hit(deck,dealer)

        show_all(split_player1,dealer)

        if split_player1.value > dealer.value:
          player_wins(split_player1,dealer,split_chips1)

        elif dealer.value > 21:
          dealer_busts(split_player1,dealer,split_chips1)
      
        elif dealer.value > split_player1.value:
          dealer_wins(split_player1,dealer,split_chips1)

        elif split_player1.value == dealer.value:
          push(split_player1,dealer)

      print("–––––––––––" * 6)
      
      print("\nHAND 2:")
      playing_split2 = True
      while playing_split2:
        show_some(split_player2,dealer2)
        hit_stand_dd(deck,split_player2,split_chips2)

        if split_player2.value > 21:
          show_all(split_player2,dealer2)
          player_busts(split_player2,dealer2,split_chips2)
          break

      if split_player2.value <= 21:
        while dealer2.value < 17:
          print("\nDEALER HITS!")
          hit(deck,dealer2)

        show_all(split_player2,dealer2)

        if split_player2.value > dealer2.value:
          player_wins(split_player2,dealer2,split_chips2)

        elif dealer2.value > 21:
          dealer_busts(split_player2,dealer2,split_chips2)
      
        elif dealer2.value > split_player2.value:
          dealer_wins(split_player2,dealer2,split_chips2)

        elif split_player2.value == dealer2.value:
          push(split_player2,dealer2)

      total_chips = 100 + (split_chips1.total - 100) + (split_chips2.total - 100)
      print(f"\nWith the results from both hands, Player has {total_chips} chips.")

      print("\nThank you for playing!")

      quit()

    #prompt player to hit stand or dd
    hit_stand_dd(deck,player,player_chips)

    #show cards, but keep one dealer card hidden
    show_some(player,dealer)

    #If player's hand exceeds 21 they BUST. Show final results. break out of loop
    if player.value > 21:
      show_all(player,dealer)
      player_busts(player,dealer,player_chips)
      break

  #If Player hasn't busted, play Dealer's hand until Dealer reaches 17
  if player.value <= 21:
    while dealer.value < 17:
      print("\nDEALER HITS!")
      hit(deck,dealer)

    #show all cards (final result)
    show_all(player,dealer)

    #run different winning scenarios

    #if player wins
    if player.value > dealer.value:
      player_wins(player,dealer,player_chips)

    #if dealer busts
    elif dealer.value > 21:
      dealer_busts(player,dealer,player_chips)
    
    #if dealer wins
    elif dealer.value > player.value:
      dealer_wins(player,dealer,player_chips)

    #if there's a tie
    elif player.value == dealer.value:
      push(player,dealer)

  #inform player of total chips
  print(f"\nPlayer has {player_chips.total} chips.")

  #ask to play again
  answer = "wrong"

  while answer not in ["Yes","No"]:
    answer  = input("\nWould you like to play again? (Yes or No): ")
    if answer not in ["Yes","No"]:
      print("Invalid. Please write Yes or No exactly.")

  if answer == "Yes":
    playing = True
    continue

  elif answer == "No":
    print("\nOk, thanks for playing! Goodbye!")
    break