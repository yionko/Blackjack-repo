## Blackjack.py 

This file contains codes that outputs the optimal strategy of Blackjack card game based on the statistical calculations of winning probability conditional on "hitting" or "standing". It simulates a whole Blackjack game and records the winner, cards history and the actions of dealer and player.

It contains useful methods that are imported by the following files. For example, "hit" method randomly draws a card and output the probability of drawing this card. "valueSum" method calculates the value of all cards at hand, taking into account of Ace being 1 and 11.

Note: This simulation only allows player actions of hitting and standing. Each game has the same amount of bet. Only one player in a game.

## Blackjack Simple Simulation.ipynb

This file also outputs the player's winning probability conditional on "hitting" or "standing" but with a main difference. It repeatively simulates the game for many times to obtain the average winning probability of a strategy. This result confirms the correctness of the calculations in Blackjack.py.

It also contains a fun simulation in which the player takes on the same strategy as the player. We can see that the player will lose on average.

## Blackjack Common Strategy.ipynb

This file takes in the common Blackjack strategy used by most players in the world (link at below), and simulates Blackjack applying this strategy.

Note: Player actions of only hitting, standing and double are allowed.

