#!/usr/bin/env python
import sys
import logger
import pickle
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
  def __init__(self):
      # define class level variables, will be remembered between turns
    self.log = logger.Logger().log 
  
  def __str__(self):
    stri = ''
    for key in vars(self).keys():
      stri += 'key: %s\n\n' % vars(self)[key]
    return 'test: ' + stri
    
  def do_setup(self, ants):
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    self.log('initialized...\n\n')  
      # initialize data structures after learning the game settings
      
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
  def do_turn(self, ants):
  # loop through all my ants and try to give them orders
  # the ant_loc is an ant location tuple in (row, col) form

    for ant_loc in ants.my_ants():
    # go through ants and let them walk to closest food  and_loc = (row, col)
      self.log(ant_loc)

      goal_loc = self.closest_food(ants, ant_loc)
      self.log('goal: %s' % str(goal_loc))
      if ant_loc and goal_loc:
        direction = ants.direction(ant_loc, goal_loc)[0]
        self.log('direction: %s' % str(direction[0]))
        new_loc = ants.destination(ant_loc, direction)
        self.log('new loc: %s' % str(new_loc))
        if (ants.passable(new_loc)):
          ants.issue_order((ant_loc, direction))
      if ants.time_remaining() < 10:
        break

  def closest_food(self, ants, loc):
    dist = 100000
    dest = None
    for food_loc in ants.food():
      if ants.distance(food_loc, loc) < dist:
        dist = ants.distance(food_loc, loc)
        dest = food_loc
    return dest


  def findpath(self, start, goal):  # from, to are loc tuples uses A* from wikipedia
    closedset = [] # sets of location tuples
    openset = [start]
    came_from = []
    g_score = {}
    h_score = {start: self.a_star_h(start, goal)}
    f_score = {start: g_score + h_score}

    while len(openset) > 0:
      temp_dict = {}  
      opt_loc = ()
      opt_loc = max(
      for loc in openset:    # find optimal loc in openset
        temp_dict[loc] = self.a_star_f(loc, goal)
        if temp_dict[loc] < opt_f_score: # we found a lower value
          opt_f_score = temp_dict[loc]
          opt_loc = loc
      if x == goal:
        return a_star_reconstruct_path(came_from, came_from[goal])

      openset.remove(opt_loc)
      closedset.append(opt_loc)
      for loc in self.neighbors(opt_loc):
        if loc in closedset:
          continue
        tentative_g_score = g_score[opt_loc] + 1
        if not loc in openset:
          openset.append(loc)
          tentative_is_better = True
        elif tentative_g_score < g_score[loc]:
          tentative_is_better = True
        else:
          tentative_is_better = False
          
        if tentative_is_better:
          came_from[loc] = opt_loc
          g_score[loc] = tentative_g_score
          h_score[loc] = a_star_h(loc, goal)
          f_score[loc] = g_score[loc] + h_score[loc]
    return False      

  def a_star_g(self, start, goal):
    pass

  def a_star_h(self, start, goal):
    pass

  def a_star_f(self, start, goal):
    return a_star_g(start. goal) + a_star_h(start, goal)

  def reconstruct_path(came_from, current_node):
    if current_node in came_from:
      p = reconstruct_path(came_from, came_from[current_node])
      return p + current_node
    else:
      return current_node









"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""

if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
