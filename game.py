import re
from card import Card
from datetime import datetime
from stack_of_cards import StackOfCards
from player import Player

class SetStack(StackOfCards):
    
# determine if selected cards are a set or not. 
# return boolean - true if set, false if not a set
    def isSet(self):
        #if more than 3 cards, return false
        if self.size() > 3:
            return False
        
        #get three cards and check if it's a set
        c1 = self.getCard(0)
        c2 = self.getCard(1)
        c3 = self.getCard(2)
        
        # attribute assignment
        
        #color
        color1 = c1.getValueOf('COLOR')
        color2 = c2.getValueOf('COLOR')
        color3 = c3.getValueOf('COLOR')
        
        #value
        value1 = c1.getValueOf('VALUE')
        value2 = c2.getValueOf('VALUE')
        value3 = c3.getValueOf('VALUE')
        
        #count
        count1 = c1.getValueOf('COUNT')
        count2 = c2.getValueOf('COUNT')
        count3 = c3.getValueOf('COUNT')
        
        #shape
        shape1 = c1.getValueOf('SHAPE')
        shape2 = c1.getValueOf('SHAPE')
        shape3 = c1.getValueOf('SHAPE')
        
        
        # individually test attributes, return true if conditions for a set are met
        if(setCalc(color1, color2, color3) == True):
            if(setCalc(value1, value2, value3) == True):
                if(setCalc(count1, count2, count3) == True):
                    if(setCalc(shape1, shape2, shape3) == True):
                        return True
        else:
            return False

# displays upCards in table
    def displayInRows(self): 
        
        cardList = self.size()
        
        #center number text
        for i in range(1, cardList//3 + 1):
            print("\t" + "  ", i, end = "")
            
        # filling in the table
        num = 0
        for j in ["A:", "B:", "C:"]:
            print("\n", j, end = "")
            for k in range(cardList//3):
                print("\t", self.getCard(k*3 + num), end = "")
            num = num + 1
        
# Input:
#   deck - SetStack which is the deck to draw new cards from
#   upCards - SetStack that are face up
#   players - list of Player
# Return boolean: True to continue game, False to end game
def playRound(deck, upCards, player, playerNum = 0): 
    
    upCards.displayInRows()
    setVal = str(input("\n" + "Can you find a set? (yes/no/quit)"))
    
    # If not a set, should add 3 cards. User loses if no more cards in deck and if there are less than 21 upCards.
    # Console prompts user to try again if 21 cards are face up
    if(setVal == "no" or setVal == 'n'):
        if(deck.size() == 0 and upCards.size() < 21):
              print("No more cards can be added at this time. You lose.")
              return False
        
        elif(upCards.size() >= 12 and upCards.size() < 21):
            for i in range(3):
              upCards.add(deck.deal())
            return True
        
        elif(upCards.size() == 21):
            print("\n" + "Keep trying to find the set!")
            return True
    
    # "Yes" conditions:  
    elif(setVal == "yes" or setVal == "y"):
        cards = input("What is the set? [ex. A2 B3 C1]:")
        
        # Check for invalid user from the input. Ask to enter cards if invalid input or if user enters nothing.
        inputCheck(cards) 
        while(cards == ""):
          print("Enter card location values")
          cards = input("What is the set? [ex. A2 B3 C1]:")
          
        cardCoord1 = cards[0:2]
        cardCoord2 = cards[3:5]
        cardCoord3 = cards[6:8]
        selectedDeck = SetStack()
        cardList = []
        findCard(cardCoord1, cardCoord2, cardCoord3, cardList, selectedDeck, upCards) # Converts card coordinates to location value
        
        # If the user's selected cards for set is a set, remove 3 cards, and add 3 cards if upCards less than 12.
        # Add user score by 1.
        if(selectedDeck.isSet() == True):
          player[playerNum].addScore(1)
          print("- Yes this is a set!!" + "\t", player[playerNum])
          
          for k in cardList:
            upCards.remove(k)
          
          # Add cards to upCards if it falls under 12. If no more cards to add, user is close to or has won the game.
          if(upCards.size() < 12 and deck.size() >= 3):
            for l in range(3):
                upCards.add(deck.deal())
          elif(deck.size() == 0 and (upCards.size() < 12 and upCards.size() > 0)):
            print("There are no more cards in the deck to add. There may still be more sets!")
          elif(deck.size() == 0 and upCards.size() == 0):
            print("You won the game and found all the sets!")
            return False
        
        #If selected cards aren't a set, subtract score from user.
        else:
            player[playerNum].addScore(-1)
            print("- This is not a set. Keep trying!" + "\t", player[playerNum])
            
        return True
    
    # End game and display final score
    elif(setVal == "quit" or setVal == "q"):
        print("\n" + "Great game!", "\n" + str(player[playerNum]))
        return False
    
    # Input checking for "Can you find a set" question. 
    # If answer isn't yes, no, or quit, ask user to enter an answer
    else:
      print("Please enter a valid input.")
      return True  
   
# Input:
#   deck - SetStack which is the deck to draw new cards from
#   players - list of Player
# No return value
def playSetGame(deck, player, playerNum):
    # deal 12 cards from the deck
    # repeatedly call playRound until the game is over
    upCards = SetStack()
    
    for k in range(12):
        upCards.add(deck.deal())
    
    gameOn = playRound(deck, upCards, player, playerNum = 0) # Calls playRound for the first time
    
    # Continue calling playRound until playRound is false
    while(gameOn == True):
        gameOn = playRound(deck, upCards, player, playerNum = 0)
   
   
def play(): 
    # get player(s) name
    # make deck & shuffle it
    # call playSetGame
    # see if player want to play another game 
    playerName = input("Please enter your name:") 
   
   # If user enters nothing, ask them to enter a name
    while(playerName == ""):
        print("Please enter a name.")
        playerName = input("Please enter your name:") 
   
    p = Player(playerName)
    players = [p]
    n = input("Enter the number of additional players (if you wish to play in single player mode, enter 0):") # Allows for more than 1 player to play
    
    # Checking input and prompting user to type number of additional players again if input isn't a positive number or 0
    while(n.isdigit() == False):
      print("Please enter a positive number or 0.")
      n = input("Enter the number of additional players (if you wish to play in single player mode, enter 0):")
    
    n = int(n)
    # Asking user to enter names of additional players
    for i in range(n): 
      x = str(input("Please enter name of player {num}:".format(num = i+2)))
    
    # Ask user to enter names again if no input is put in
      while(x == ""): 
          print("Please enter a name.")
          x = str(input("Please enter name of player {num}:".format(num = i+2)))
      y = Player(x)
      players.append(y)
      
    deck = SetStack()
    att = [0, 1, 2]
    for j in att:
        for k in att:
            for l in att:
                for m in att:
                    deck.add(Card(j, k, l, m))
    
    # Each player goes until they quit and don't want to continue anymore 
    for playerNum in range(n + 1):
        print("\n", "It is", str(players[playerNum].name) + "'s turn:")
        endVal = "yes" 
        
        while(endVal == "yes" or endVal == "Yes"): 
            players[playerNum].score = 0
            deck.shuffle()
            startTime = datetime.now() # Mark when the user starts to play game 
            playSetGame(deck, players, playerNum)
            endTime= datetime.now() # Mark when the user stops playing game to find total time spent playing
            timeTaken = (endTime-startTime)
            print("\n" + "The time you took to finish the game is", int(timeTaken.total_seconds()), "seconds")
            
            #Asks if user wants to play again
            endVal = str(input("\n" + "Would you like to play again?"))
            
            # Input checking - ask user to enter a valid input if endVal isn't yes or no
            while(endVal != "yes" and endVal != "Yes" and endVal != "no" and endVal != "No"):
                print("Please provide a valid input.")
                endVal = str(input("Would you like to play again?")) 
        
        # End game if use doesn't want to play again
        if(endVal == "no" or endVal == "No"):
            print("\n" + "Game over for you.")

# Input: attributes of cards
# Determine if inputed attributes are all same and all different
# Returns boolean - if true then the card's attribute is either all the same or all different
def setCalc(att1, att2, att3):
    if(att1 == att2 == att3 or (att1 != att2 and att2 != att3 and att3 != att1)):
       return True

'''
If input of cards isn't in (letterNumber) format or if the total length of the input isn't equal to 8 or if any of the inputs
are the same, prompt user to enter a valid input.
input -  cards inputed by user
'''
def inputCheck(cardInput):
    for p in range(-1, 2):
          while(cardInput[(3*p) + 3] not in "ABCabc" or cardInput[(3*p) + 4] not in "1234567" or len(cardInput) != 8 
                or (cardInput[0:2].lower() == cardInput[3:5].lower() or cardInput[0:2].lower() == cardInput[6:8].lower() 
                    or cardInput[3:5].lower() == cardInput[6:8].lower())): 
            print("Please provide a valid input (i.e. A1 B1 C1)")
            cardInput = input("What is the set? [ex. A2 B3 C1]:")


'''
Find the actual index of the card 
Input: card1, card2, card3 (card coordinates chosen by user), cardList (empty list of user inputs)
selectedDeck (selected deck by the user), upCards
Output: cardList (cards inputed by the user)
'''
def findCard(card1, card2, card3, cardList, selectedDeck, upCards):
    num = 0
    for j in [card1, card2, card3]:
        cardList.append("ABC".find(j[0].upper()) + (int(j[1]) - 1) * 3)
        selectedDeck.add(upCards.getCard(cardList[num]))
        num = num + 1
    return(cardList)
    
    
def main(): 
    
    # sample code using Card, StackOfCards, Player classes
    x = Card(1, 2, 2, 2)
    y = Card(2, 0, 2, 1)

   
    
    
    
    
    c = Card(0, 1, 2, 0)
          # make a Set card with attributes of
                            # value: 0
                            # color: 1
                            # count: 2
                            # shape: 0                        # will print out x x x

    deck = SetStack()                  # make a stack of cards
    deck.add(c)                        # add the card to the deck
    deck.add(y)        # add another card to the deck
    deck.add(x)  
    deck.isSet()
           # add another card to the deck    # add another card to the deck
  
    


    player = Player("Mark")         # make a player called Mark
    players = [ player ]
    
    play()
    
    
if __name__ == "__main__":
    main()
