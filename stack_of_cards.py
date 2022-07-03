import random
import card

class StackOfCards:

    def __init__(self):
        '''
        Constructor
        '''
        self.cards = []
        
    # returns a string of all the cards in the 'deck'
    def __str__(self):
        s = ''
        for card in self.cards:
            if len(s) == 1:
                s = s + str(card)
            else:
                s = s + '   ' + str(card)
        s = s
        return(s)
    
    # Add card to the 'bottom' of the deck of cards
    def add(self, card):
        self.cards.append(card)
                
    # removes and returns card at position 'pos' of the deck
    def remove(self, pos):
        card = self.cards.pop(pos)
        return card
               
    # Deal card from the 'top' of the deck of cards
    def deal(self):
        return self.cards.pop(0)
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    # returns the size of the stack
    def size(self):
        return(len(self.cards))
    
    # returns the card at position 'pos' of the deck
    def getCard(self, pos):
        return(self.cards[pos])
    
    # replaces the card at position 'pos' with a new 'card'
    def replaceCard(self, pos, card):
        self.cards[pos] = card

    
        
