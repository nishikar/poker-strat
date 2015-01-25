# -*- coding: utf-8 -*-

import itertools
import random
import datetime

import sys
import os

import pygame
from pygame.locals import *

from rules import *
from utils import factorial, combination

color = [1,2,3,4]
value = [1,2,3,4,5,6,7,8,9,10,11,12,13]
card = [] #describes all 52 cards in a deck in the form of < list of a (number, color) tuple >

#for displaying to console
#color = { 1 : 'Clubs', 2: 'Spades', 3: 'Diamonds', 4: 'Hearts' }
print_color = { 1 : 'C', 2: 'S', 3: 'D', 4: 'H' }
print_num = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}

deck = [] # current deck
hand = [] # dealt hand

all_possible_holds = []
user_holds = []
index = 0
match_flag = False

no_of_deals = 0
match_cnt = 0

isDeal = True

#for displaying graphics
display_dict = {}

SCREEN_X = 850
SCREEN_Y = 500

IMAGE_WIDTH = 80
IMAGE_HEIGHT = 100

START_X = 50
START_Y = 50

EVAL_BTN = (160,165,80,20)
DEAL_BTN = (270,165,80,20)


def init_cards():
    """ initialize the 52 cards """

    global color
    global value
    global card

    for c in color:
        for v in value:
            card.append((v,c)) 


def init_hand():
    """ initialize the current dealt hand and modify the deck """

    global deck
    global hand
    global all_possible_holds
    global user_holds
    global index
    
    del deck[:]
    del hand[:]
    del all_possible_holds[:]
    del user_holds[:]
    index = 0
    
    #current deck
    for c in card:
        deck.append(c)  
        
    #dealt hand based on random numbers
    while (len(hand) < 5):
        r = random.randint(0, len(card)-1)  
        if card[r] not in hand:
            hand.append(card[r])
            deck.remove(card[r])
    
    #dealt hand based on hardcoded input
    #hand = [(4,3),(10,3),(10,1),(8,1),(13,2)]
    #for each_card in hand:
    #   deck.remove(each_card)
        

def evaluate():
    """ 
        - evaluates the correct hold strategy for the given hand
        - compares whether user hold strategy matches or not
        - updates the stats
    """

    global all_possible_holds
    global index
    global match_flag
    global match_cnt
    global no_of_deals

    print "evaluating...."
    print datetime.datetime.now().time()
    
    del all_possible_holds[:]
    index = 0       
        
    # all 32 possible strategies (hold possibilities) for a dealt hand ( need to calculate expected value for each of these )   
    for i in range(0,len(hand)+1):
        for subset in itertools.combinations(hand,i):
                all_possible_holds.append(subset)   

    # build all possible trial hands by brute force and calculate expected value for all possible hold strategies
    expected_value = [] 
    for item in all_possible_holds:     
        number_of_draws = 5-len(item)
        no_all_possible_draws = combination(len(deck),number_of_draws)      
        payout_running_sum = 0
        sets = itertools.combinations(deck,number_of_draws)
        for subset in sets:              
            trial_hand = item + subset
            payout_running_sum = payout_running_sum + payout(trial_hand)                            
        expected_value.append(payout_running_sum/no_all_possible_draws)     
        

    #find hold strategy with maximum expected value
    max_val = 0.0
    for i in range(0,len(expected_value)):
        if expected_value[i] > max_val:
            max_val = expected_value[i]
            index = i   

    print datetime.datetime.now().time()
    print "hold: "
    for item in all_possible_holds[index]:      
        print print_num[item[0]],
        print print_color[item[1]],
        print ' ',
    print ''    
    
    print "with expected value: ",
    print max_val   
    
    user_match = False
    calc_match = False
    no_of_deals += 1
    for user_item in user_holds:
        if user_item in all_possible_holds[index]:
            user_match = True
        else:
            user_match = False
            break
    for hold_item in all_possible_holds[index]:
        if hold_item in user_holds:
            calc_match = True
        else:
            calc_match = False
            break
    if (user_match and calc_match) or (len(all_possible_holds[index]) == 0 and len(user_holds) == 0):
        print "Correct"
        match_flag = True
        match_cnt += 1
                
    else:
        print "Wrong" 
        match_flag = False      
    
    print match_cnt
    print no_of_deals   
    print float(match_cnt)/float(no_of_deals) * 100
    

def user_input(coordinate):
    """ mouse input coordinates - check for button click / card click """

    global hand
    global user_holds
    global isDeal       
    
    x = int((coordinate[0]-START_X)/IMAGE_WIDTH)
    y = int((coordinate[1]-START_Y)/IMAGE_HEIGHT)   

    if((x == 0 or x == 1 or x == 2 or x == 3 or x == 4) and y == 0): #get the card selected according to mouse coordinate
        if hand[x] in user_holds:
            user_holds.remove(hand[x])
        else:
            user_holds.append(hand[x])
    
    if(coordinate[0] > EVAL_BTN[0] and coordinate[0] < (EVAL_BTN[0]+EVAL_BTN[2]) and coordinate[1] > EVAL_BTN[1] and coordinate[1] < (EVAL_BTN[1]+EVAL_BTN[3])): #eval button clicked       
        if(isDeal):
            evaluate()
            isDeal = False
    
    elif(coordinate[0] > DEAL_BTN[0] and coordinate[0] < DEAL_BTN[0]+EVAL_BTN[2] and coordinate[1] > DEAL_BTN[1] and coordinate[1] < DEAL_BTN[1]+DEAL_BTN[3]): #deal button clicked
        init_hand()                 
        isDeal = True           
    
    
def input(events):
    """ scan user inputs and decide on action """ 

    global isDeal
    
    for event in events:
        
        if event.type == QUIT:
            sys.exit(0)
        
        elif event.type == KEYDOWN:
            
            if event.key == K_RETURN:
                if(isDeal):
                    evaluate()
                isDeal = False
            
            elif event.key == K_SPACE:                              
                init_hand()                 
                isDeal = True
        
        elif event.type == MOUSEBUTTONDOWN:
        
            user_input(pygame.mouse.get_pos())
            
                
def display():
    """ displays all objects """

    screen.fill((34,139,34))
    
    #evaluation indicator - (right/wrong)
    pygame.draw.circle(screen, (0,50,0), (240,30), 10)
    pygame.draw.circle(screen, (50,0,0), (270,30), 10)
    
    #boundary of payout table
    pygame.draw.rect(screen,(160,82,45),(500,40,300,300))
    
    #deal,eval buttons
    pygame.draw.rect(screen,(60,60,60),EVAL_BTN)
    pygame.draw.rect(screen,(0,0,255),EVAL_BTN,2)
    pygame.draw.rect(screen,(60,60,60),DEAL_BTN)
    pygame.draw.rect(screen,(0,0,255),DEAL_BTN,2)
    
    btn_font_surface_e = btn_font.render("EVAL",2,(255,255,0))
    screen.blit(btn_font_surface_e, (179,168))
    btn_font_surface_d = btn_font.render("DEAL",2,(255,255,0))
    screen.blit(btn_font_surface_d, (289,168))
    
    #key info
    info_font_surface = info_font.render("[Click on card to hold] [Space to deal new hand] [Enter to evaluate hold]",2,(0,0,255))
    screen.blit(info_font_surface, (50,470))
    
    #paytable info
    pay_font_surface_royal = pay_font.render( "Royal Flush : "+str(ROYAL), 3, (255, 255, 0) )
    pay_font_surface_stFlush = pay_font.render( "Straight Flush : "+str(ST_FLUSH), 3, (255, 255, 0) )
    pay_font_surface_four = pay_font.render( "Four of a Kind : "+str(FOUR_KIND), 3, (255, 255, 0) )
    pay_font_surface_fh = pay_font.render( "Full House : "+str(FULL_HOUSE), 3, (255, 255, 0) )
    pay_font_surface_flush = pay_font.render( "Flush : "+str(FLUSH), 3, (255, 255, 0) )
    pay_font_surface_st = pay_font.render( "Straight : "+str(STRAIGHT), 3, (255, 255, 0) )
    pay_font_surface_three = pay_font.render( "Three of a Kind : "+str(THREE_KIND), 3, (255, 255, 0) )
    pay_font_surface_two = pay_font.render( "Two Pair: "+str(TWO_PAIR), 3, (255, 255, 0) )
    pay_font_surface_jb = pay_font.render( "Jacks or Better : "+str(JACK_BETTER), 3, (255, 255, 0) )
    pay_font_surface_bet = pay_font.render( "Bet : $"+str(bet_val), 3, (0,0,0) )
    
    screen.blit(pay_font_surface_royal, (520,50))
    screen.blit(pay_font_surface_stFlush, (520,80))
    screen.blit(pay_font_surface_four, (520,110))
    screen.blit(pay_font_surface_fh, (520,140))
    screen.blit(pay_font_surface_flush, (520,170))
    screen.blit(pay_font_surface_st, (520,200))
    screen.blit(pay_font_surface_three, (520,230))
    screen.blit(pay_font_surface_two, (520,260))
    screen.blit(pay_font_surface_jb, (520,290))
    screen.blit(pay_font_surface_bet, (520,380))
    
    stat_font_surface_correct = stat_font.render( "correct: "+str(match_cnt), 2, (0,0,0) )
    stat_font_surface_total =   stat_font.render( "total hands: "+str(no_of_deals), 2, (0,0,0) )
    if no_of_deals > 0:
        stat_font_surface_acc = stat_font.render( "accuracy: "+str(round(float(match_cnt)/float(no_of_deals) * 100,2))+"%", 2, (0,0,0) )
    else:
        stat_font_surface_acc = stat_font.render( "accuracy: ", 2, (0,0,0) )    
    
    screen.blit(stat_font_surface_correct, (50,360))
    screen.blit(stat_font_surface_total, (50,390))
    screen.blit(stat_font_surface_acc, (50,420))
       
    x = START_X
    y = START_Y
    for item in hand:
        screen.blit(display_dict[item],(x,y))       
        if(item in user_holds):             
            pygame.draw.rect(screen,(0,0,255),(x,y,IMAGE_WIDTH,IMAGE_HEIGHT),3)
        x += IMAGE_WIDTH    
    
    x = 50
    y = 200
    if len(all_possible_holds) > 0:     
        for item in all_possible_holds[index]:          
            if item in display_dict.keys():             
                screen.blit(display_dict[item],(x,y))
            x += IMAGE_WIDTH
        if match_flag: 
            pygame.draw.circle(screen, (0,255,0), (240,30), 10)
            pygame.draw.circle(screen, (50,0,0), (270,30), 10)
        else:
            pygame.draw.circle(screen, (0,50,0), (240,30), 10)
            pygame.draw.circle(screen, (255,0,0), (270,30), 10)         
        
    pygame.display.flip()
        

if __name__ == "__main__":

    init_cards()
    init_hand()

    print "dealt hand: "
    for i in range(0, len(hand)):
        print print_num[hand[i][0]],
        print print_color[hand[i][1]],
        print ' ',
    print ''

    os.environ['SDL_VIDEO_CENTERED'] = '1'             
    pygame.init()

    window = pygame.display.set_mode((SCREEN_X,SCREEN_Y))
    pygame.display.set_caption("PokerStrat")
    screen = pygame.display.get_surface()

    
    #initializing all card image files
    IMG_FILES = []
    for i in range(0,len(card)):
        inx = i+1
        inx_file = str(inx)+".jpg"
        IMG_FILES.append(os.path.abspath(os.path.join('../data',inx_file)))

    
    #initializing all card image objects
    img_objs = []
    for image_file in IMG_FILES:
        img_objs.append(pygame.image.load(image_file).convert())    

    for i in range(0, len(img_objs)):
        display_dict[card[i]] = img_objs[i]
        
    
    #fonts
    STAT_FONT_FILE = os.path.abspath(os.path.join("../data", "256BYTES.TTF"))
    stat_font = pygame.font.Font( STAT_FONT_FILE, 26)
    PAY_FONT_FILE = os.path.abspath(os.path.join("../data", "ARCADE.TTF"))
    pay_font = pygame.font.Font( PAY_FONT_FILE, 26)
    btn_font = pygame.font.Font( PAY_FONT_FILE, 20)
    info_font = pygame.font.Font( PAY_FONT_FILE, 20)

    display()

    while True:
        input(pygame.event.get())    
        display()

