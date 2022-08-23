#!/usr/bin/env python
# coding: utf-8

# In[30]:


import numpy as np
import copy


# In[31]:


# Draw a card with CARDVALUE, and then update the cards array and cardsCount array
def hit(cardValue, cards, cardsCount):
    
    # Check if there are any cardValue cards in the pool.
    if cardsCount[cardValue - 1] == 0:
        return None
    
    # Calculate the probability of drawing CARDVALUE, e.g. A.
    prob = cardsCount[cardValue - 1] / np.sum(cardsCount)
    
    # update CARDS and CARDSCOUNT arrays.
    numLeft = cardsCount[cardValue - 1]
    
    
    cards[(cardValue - 1) * 4 + numLeft - 1] = 0  
    cardsCount[cardValue - 1] = cardsCount[cardValue - 1] - 1
    return prob, cards, cardsCount


# In[ ]:





# In[32]:



# In[33]:


## Put back a card with CARDVALUE to the CARDS array and CARDSCOUNT array
def putBack(cardValue, cards, cardsCount):
    cardsIndex = (cardValue - 1) * 4 + cardsCount[cardValue - 1]
    cards[cardsIndex] = 1
    cardsCount[cardValue - 1] += 1
    return cards, cardsCount


# In[34]:



# In[35]:


# Sum of all cards.
# For the dealer, if treating ace as 11 make total value >= 17 but <= 21,
# then must treat ace as 11. Otherwise, it treats all aces as 1.
# For the player, return total when treating ace as 1 and 11 if total <= 21.

# The input DEALER = 1 if it is used to calculate the total
# value for the dealer. 0 otherwise.
def valueSum(cardsHistory, dealer):
    
    cardsHistoryValue = copy.deepcopy(cardsHistory)
    for x in range(0, len(cardsHistoryValue)):
        if cardsHistoryValue[x] >= 10:
            cardsHistoryValue[x] = 10
    
    dealerSum = int(np.sum(np.array(cardsHistoryValue)))
    playerSum1 = int(np.sum(np.array(cardsHistoryValue)))
    playerSum11 = playerSum1 + 10
    
    if dealer == 1:
        if 1 in cardsHistoryValue:
            sumIfAceAs11 = dealerSum + 10
            if sumIfAceAs11 >= 17 and sumIfAceAs11 <= 21:
                dealerSum =  sumIfAceAs11
        return dealerSum        
    else:
        if 1 in cardsHistoryValue:
    
            if playerSum11 <= 21:
                return playerSum1, playerSum11
        return playerSum1
    


# In[36]:


# In[37]:


# Search all paths. If the dealer stands, update the expected value.
# If the dealer bursts, update the burst probability.
# Return the EXPECTEDVALUE, and BURSTPROB.
# CARDSHISTORY is a np.array recording all dealer's cards.
# ENDINGPROB is a np.array recording the probabilities of 
# the player's final results, from 17 to burst, corresponding
# to index 0 to 5.
def step(dealerCardsHistory, cards, cardsCount, pathProb, endingProb):
    
    for x1 in range(1, 14):
        
        hitResult = hit(x1, cards, cardsCount)
        
        if hitResult == None:
            continue
#         print("step - x1, hitResult:", x1, hitResult[2])
        
        dealerCardsHistory = np.append(dealerCardsHistory, x1)
#         print("dealerCardsHistory: ", dealerCardsHistory)
        hitProb = hitResult[0]
        
        cards = hitResult[1]
        cardsCount = hitResult[2]
        
        sumOfAllCards = valueSum(dealerCardsHistory, 1)
#         print("sumOfAllCards: ", sumOfAllCards)
#         print("pathProb: ", pathProb)
        
        if sumOfAllCards < 17:
            ## sumOfAllCards < 17, and the dealer still needs to hit.
            pathProbCurr = pathProb * hitProb
            step(dealerCardsHistory, cards, cardsCount, pathProbCurr, endingProb)
          
        if sumOfAllCards == 17:
            endingProb[0] += pathProb * hitProb
    
        if sumOfAllCards == 18:
            endingProb[1] += pathProb * hitProb
            
        if sumOfAllCards == 19:
            endingProb[2] += pathProb * hitProb
            
        if sumOfAllCards == 20:
            endingProb[3] += pathProb * hitProb
    
        if sumOfAllCards == 21:
            endingProb[4] += pathProb * hitProb

        if sumOfAllCards > 21:
            ## Update burst probability
            endingProb[5] += pathProb * hitProb

        putBackResult = putBack(x1, cards, cardsCount)
        cards = putBackResult[0]
        cardsCount = putBackResult[1]
            
        dealerCardsHistory = dealerCardsHistory[:-1]
        #print("endingProb", endingProb)
    #print("Ending prob for dealer: ", endingProb)
    return endingProb
        


# In[14]:


# It calculates the expected total value of the dealer if she does not burst.
def dealerExpectedValue(endingProb):
    value = 0
    dealerNotBurstProb = 1 - endingProb[5]
    for x in range(0, 5):
        value += endingProb[x] / dealerNotBurstProb * (17 + x)
    return value


# In[145]:


# Calculate the probability of winning if the player hits.
# The first portion is the probability of dealer not bursting 
# and player's sum greater than dealer's sum.
# The second portion is player not bursting but dealer bursts.
def winProbIfHit(playerSum, cards, cardsCount, expectedValue, burstProb):
    
    
     # If playerSum + 11 <= 17, then winProbHit = dealerBursts.
    if playerSum <= 6:
        winProbHit = burstProb
    else:
        
        # If hitLowerBound/hitUpperBound = 10, consider 
        # hitting 10, 11, 12, and 13. If hitLowerBound/hitUpperBound
        # = 11, then hit 1/A.
        
        hitLowerBound = np.ceil(expectedValue - playerSum)
        hitUpperBound = min(int(21 - playerSum), 11)
        
        # Probability of drawing a card that makes player total value higher than the
        # dealer's expected value but not exceeding 21.
        higherValueProb = 0
        
        hitLowerBound = int(hitLowerBound)
        for x in range(hitLowerBound, hitUpperBound + 1):

            if x == 10:
                for x1 in range(10, 14):
                    hitResult = hit(x1, cards, cardsCount)
                    if hitResult == None:
                        continue
                    # the probability of hitting x1
                    higherValueProb += hitResult[0] 
                    putBack(x1, hitResult[1], hitResult[2])
            elif x == 11:
                hitResult = hit(1, cards, cardsCount)
                if hitResult == None:
                    continue
                # the probability of hitting Ace
                higherValueProb += hitResult[0] 
                putBack(1, hitResult[1], hitResult[2])
            else:
                #print(x)
                hitResult = hit(x, cards, cardsCount)
                if hitResult == None:
                    continue
                higherValueProb += hitResult[0] 
                putBack(x, hitResult[1], hitResult[2])

        # The probability of the player not bursting when hitting
        playerNotBurstProb = 0
        for y in range(1, hitUpperBound + 1):

            if y == 10:
                for y1 in range(10, 14):
                    hitResult = hit(y1, cards, cardsCount)
                    if hitResult == None:
                        continue
                    # the probability of hitting x1
                    playerNotBurstProb += hitResult[0] 
                    putBack(y1, hitResult[1], hitResult[2])
            elif y == 11:
                hitResult = hit(1, cards, cardsCount)
                if hitResult == None:
                    continue
                # the probability of hitting Ace
                playerNotBurstProb += hitResult[0] 
                putBack(1, hitResult[1], hitResult[2])
            else:
                hitResult = hit(y, cards, cardsCount)
                if hitResult == None:
                    continue
                playerNotBurstProb += hitResult[0] 
                putBack(x, hitResult[1], hitResult[2])

        winProbHit = higherValueProb * (1 - burstProb) + playerNotBurstProb * burstProb
        
    return winProbHit


# In[85]:


# winProbIfHit() test case
# step() test case.
# dealerCard1 = 1
# dealerCard2 = 6
# playerCard1 = 5
# playerCard2 = 9

# dealerHistory = np.array([dealerCard1])
# playerHistory = np.array([playerCard1, playerCard2])

# playerSum = valueSum(playerHistory, 0)

# cards = [1] * 52
# cardsCount = [4] * 13

# hit(dealerCard1, cards, cardsCount)

# hit(playerCard1, cards, cardsCount)
# hit(playerCard2, cards, cardsCount)

# endingProb = [0] * 6
# pathProb = 1

# endingProb = step(dealerHistory, cards, cardsCount, pathProb, endingProb)
# expectedValue = dealerExpectedValue(endingProb)
# burstProb = endingProb[5]
# print("dealer's ending probabilities are:", endingProb)
# print("dealer's expected value is: ", expectedValue)
# winProbHit = winProbIfHit(playerSum, cards, cardsCount, expectedValue, burstProb)
# print("player's winning probability if hitting is: ", winProbHit)


# In[86]:


def winProbIfStand(playerSum, endingProb):
    
    burstProb = endingProb[5]
    winProbStand = 0
    
    if isinstance(playerSum, int) == False:
        
        # When ace is treated as 11 and not bursting, winProbStand is greater.
        playerSum = playerSum[1]
    
    # If the player stands, the probability of winning if the player's 
    # total value is greater than dealer's expected value.
    if playerSum > 17:
    
        # Calculate the winning probability if player stands.
        for i in range(0, 5):
            # Probability of player's value greater than expected dealer value
            # when the player stands.
            if playerSum > (17 + i):
                winProbStand += endingProb[i]
            # Probability of dealer bursting.
        winProbStand += burstProb
    
    # If the player's sum is smaller than
    else:
        winProbStand += burstProb
    return winProbStand


# In[18]:


# winProbIfStand(playerSum, endingProb) test case.
playerSum = 19
endingProb = np.array([.2, .2, .2, .2, .1, .1])
winProbIfStand(playerSum, endingProb)


# In[138]:


# This function takes in the player's cards history, the dealer's card on the table,
# the card set the player sees prior drawing the table cards, 
# and the counts for each card value. 
# It outputs the probabilities of the player winning if she stands or hits.
# It outputs the strategy of the player for this step.

# The general strategy is that the player will stand if her sum is greater
# or equal to the dealer's expected sum (conditional on dealer not bursting).

# change to a simple strategy for test cases.

def playerStrategy(dealerCard1, playerHistory, cards, cardsCount):
    
    dealerHistory = np.array([dealerCard1])
    
    playerSum = valueSum(playerHistory, 0)
    #print("player sum is: ", playerSum)
    if isinstance(playerSum, int) == True and playerSum > 21:
        return 0, 0, 0
    
    # Initiate dealer bursting probability.
    burstProb = 0
    
    # Initiate player's winning probability if she stands.
    winProbStand = 0
    
    pathProb = 1
    
    expectedValue = 0
    
    # Create a data set which the player sees.
    
    cards1 = copy.deepcopy(cards)
    cardsCount1 = copy.deepcopy(cardsCount)
    
    hit(dealerCard1, cards1, cardsCount1)
    for i in range(0, len(playerHistory)):
        hit(playerHistory[i], cards1, cardsCount1)
    #print("cards count before step() is: ", cardsCount1)
    
    # Initiate the ending probability array for the player. It records the 
    # probabilities of the player's final results, from 17 to burst, 
    # corresponding to index 0 to 5, given the player only knows the cards on
    # the table. So we will create a full data set with only the table
    # cards drawn out.
    endingProb = [0] * 6
    endingProb = step(dealerHistory, cards1, cardsCount1, pathProb, endingProb)
    #print("cards count after step():  ", cardsCount1)
    #print("dealer's ending probability is: ", endingProb)
    expectedValue = dealerExpectedValue(endingProb)
    #print("dealer's expected value is: ", expectedValue)
    burstProb = endingProb[5]
    #print("dealer's burst probability is: ", burstProb)
    
    winProbStand = winProbIfStand(playerSum, endingProb)
    
    # Calculate the winning probability if hitting.

    if isinstance(playerSum, int) == False:
        playerSum1 = playerSum[0]
        playerSum11 = playerSum[1]
        #print("player's sum is: ", playerSum)
        winProbHit1 = winProbIfHit(playerSum1, cards1, cardsCount1, expectedValue, burstProb)
        winProbHit11 = winProbIfHit(playerSum11, cards1, cardsCount1, expectedValue, burstProb)
        winProbHit = max(winProbHit1, winProbHit11)
    else:
        winProbHit = winProbIfHit(playerSum, cards1, cardsCount1, expectedValue, burstProb)
        
    if winProbHit > winProbStand:
        strategy = 1
    else: 
        strategy = 0
        
    return strategy, winProbHit, winProbStand
    



# In[144]:


# Randomly select a card from the card sets, but not actually draw it, just
# output its value
def randomValue(cards):
    counter = 1
    randomTemp = np.random.randint(1, 53)
    #print("randomTemp", counter, ": ", randomTemp)# 1-52 inclusive
    while cards[randomTemp - 1] == 0:
        counter += 1
        randomTemp = np.random.randint(1, 53)
        #print("randomTemp", counter, ": ", randomTemp)
    value = int(np.ceil(randomTemp / 4))
    return value


# In[148]:


# Fixing dealerCard1, dealerCard2, playerCard1 and playerCard2, we played one game to see who
# wins and who lose.

# cards and cardsCount datasets are 

# Return game statistics: who wins? Any bursts? Player's cards, and dealer's cards,
# player's winning probability if hit/stand at each step.

def oneGame(dealerCard1, dealerCard2, playerCard1, playerCard2, cards, cardsCount):

    # playerBurstDummy = 1 if the player bursts.
    playerBurstDummy = 0
    dealerBurstDummy = 0
    
    playerStrategyRecord = []
    
    # dealerWin = 1 if the dealer wins. 0 otherwise.
    dealerWin = 0
    
    # GAMERESULT = -1 if the dealer wins, = 1 if the player wins,
    # and = 0 if they draw.
    gameResult = 0
    
    dealerHistory = [dealerCard1, dealerCard2]
    dealerSum = valueSum(dealerHistory, 1)
    
    playerHistory = [playerCard1, playerCard2]
    playerSum = valueSum(playerHistory, 0)

    cards1 = copy.deepcopy(cards)
    cardsCount1 = copy.deepcopy(cardsCount)


    hit(dealerCard1, cards1, cardsCount1)

    hit(playerCard1, cards1, cardsCount1)
    hit(playerCard2, cards1, cardsCount1)

    # CARDS and CARDSCOUNT are supposed not to change after this function.
    # Inside playerStrategy(), all cards on the table would be
    # drawn out from CARDS and CARDSCOUNT datasets.
    playerStrategyResult = playerStrategy(dealerCard1, playerHistory, cards, 
                                          cardsCount)
    strategy = playerStrategyResult[0]
    winProbHit = playerStrategyResult[1]
    winProbStand = playerStrategyResult[2]
    
    playerStrategyRecord.append(playerStrategyResult)
    
    while strategy == 1:
        #print("cardsCount before hitting: ", cardsCount1)
        value = randomValue(cards1)
        
        # We use cards1 and cardsCount1 to record the datasets
        # which will be changed in the process.
        hitResult = hit(value, cards1, cardsCount1)
        cards1 = hitResult[1]
        cardsCount1 = hitResult[2]
        #print("cardsCount after hitting: ", cardsCount1)
        
        playerHistory = np.append(playerHistory, value)
        
        #print("playerHistory", playerHistory)

        # Player bursts
        playerSum = valueSum(playerHistory, 0)
        if isinstance(playerSum, int) == True and playerSum > 21:
            playerBurstDummy = 1
            break
            
        # return strategy, winProbHit, winProbStand
        playerStrategyResult = playerStrategy(dealerCard1, playerHistory, 
                                              cards, cardsCount)
        strategy = playerStrategyResult[0]
        winProbHit = playerStrategyResult[1]
        winProbStand = playerStrategyResult[2]
        playerStrategyRecord.append(playerStrategyResult)

    if isinstance(playerSum, int) == True and playerSum > 21:
        gameResult = -1
        # continue to the second game
        return playerBurstDummy, dealerBurstDummy, playerHistory, dealerHistory, gameResult, playerStrategyRecord, cards1, cardsCount1
    
    # print("cards1", cards1)
    # The player stands. The dealer reveals its second card, and she starts to hit or stand

    while dealerSum < 17:

        value = randomValue(cards1)
        hitResult = hit(value, cards1, cardsCount1)
        cards1 = hitResult[1]
        cardsCount1 = hitResult[2]

        dealerHistory = np.append(dealerHistory, value)
        dealerSum = valueSum(dealerHistory)

    if dealerSum > 21:
        dealerBurstDummy = 1
        gameResult = 1
        
    elif dealerSum < playerSum:
        gameResult = 1

    elif dealerSum > playerSum:
        gameResult = -1

    elif dealerSum == playerSum:
        gameResult = 0

    return playerBurstDummy, dealerBurstDummy, playerHistory, dealerHistory, gameResult, playerStrategyRecord, cards1, cardsCount1



# In[149]:


# oneGame() test case:
# dealerCard1 = 1
# dealerCard2 = 6
# playerCard1 = 5
# playerCard2 = 9

# dealerHistory = np.array([dealerCard1])
# playerHistory = np.array([playerCard1, playerCard2])

# cards = [1] * 52
# cardsCount = [4] * 13

# oneGameTest = oneGame(dealerCard1, dealerCard2, playerCard1, playerCard2, cards, cardsCount)

# print("one game result: ", oneGameTest[0], oneGameTest[1], oneGameTest[2], oneGameTest[3], oneGameTest[4], oneGameTest[5])


