# -*- coding: utf-8 -*-

bet_val = 1.00 #1$

#payout table
ROYAL = 800
ST_FLUSH = 50
FOUR_KIND = 25
FULL_HOUSE = 9
FLUSH = 6
STRAIGHT = 4
THREE_KIND = 3
TWO_PAIR = 2
JACK_BETTER = 1


def isFlush(suits):    
	return suits[0] == suits[1] == suits[2] == suits[3] == suits[4]


def isStraight(ranks):
	if ranks[4] - ranks[0] == 4:
		return True

	#special case of 10,J,Q,K,A
	if(ranks[0] == 1 and ranks[1] == 10 and ranks[2] == 11 and ranks[3] == 12 and ranks[4] == 13):
		return True

	return False	


def isStraightFlush(ranks, suits):
	return isStraight(ranks) and isFlush(ranks)


def isRoyalFlush(ranks, suits):
	return ranks[0] == 1 and ranks[1] == 10 and ranks[2] == 11 and ranks[3] == 12 and ranks[4] == 13 and isStraightFlush(ranks, suits)


def isOfAKind(frequency, k):	
	return k in frequency


def isFullHouse(frequency):	
	return 3 in frequency and 2 in frequency


def isJacksOrBetter(frequency):
	return frequency[0] == 2 or frequency[10] == 2 or frequency[11] == 2 or frequency[12] == 2 #jacks or better pair


def get_sorted_ranks(hand):
	ranks = [c[0] for c in hand]
	ranks.sort()
	return ranks


def get_suits(hand):
	return [c[1] for c in hand]


def get_ranks_frequency(ranks):
	frequency = [0,0,0,0,0,0,0,0,0,0,0,0,0]
	
	for i in xrange(len(ranks)):
		frequency[ranks[i]-1] += 1
	
	return frequency


def get_no_of_pairs(frequency):
	noOfPairs = 0
	for num in frequency:
		if num == 2:
			noOfPairs += 1
	
	return noOfPairs
	

def payout(hand):
	ranks = get_sorted_ranks(hand)
	suits = get_suits(hand)
	frequency = get_ranks_frequency(ranks)
	no_of_pairs = get_no_of_pairs(frequency)

	if isOfAKind(frequency, 4):
		return bet_val * FOUR_KIND
	
	if isFullHouse(frequency):
		return bet_val * FULL_HOUSE

	if isOfAKind(frequency, 3):
		return bet_val * THREE_KIND	

	if no_of_pairs == 2:
		return bet_val * TWO_PAIR

	if isJacksOrBetter(frequency):
		return bet_val * JACK_BETTER

	if no_of_pairs == 1:
		return 0					

	if isRoyalFlush(ranks, suits):
		return bet_val * ROYAL	

	if isStraightFlush(ranks, suits):
		return bet_val * ST_FLUSH				
	
	if isFlush(suits):
		return bet_val * FLUSH
	
	if isStraight(ranks):
		return bet_val * STRAIGHT

	return 0