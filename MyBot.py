#!/usr/bin/env python
import sys
import logging
import pickle
from ants import *



# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
  def __init__(self):
      # define class level variables, will be remembered between turns
    self.ants = {} 

  def __str__(self):
    stri = ''
    for key in vars(self).keys():
      stri += 'key: %s\n\n' % vars(self)[key]
    return 'test: ' + stri
    
  def do_setup(self, ants):
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    logging.info('initialized...\n\n')  
      # initialize data structures after learning the game settings
    self.ants = ants  
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    logging.debug(self.ants)

  def do_turn(self, ants):
    self.ants = ants
  # loop through all my ants and try to give them orders
  # the ant_loc is an ant location tuple in (row, col) form

    for ant_loc in self.ants.my_ants():
    # go through ants and let them walk to closest food  and_loc = (row, col)
      #self.log(ant_loc)

      goal_loc = self.closest_food(ant_loc)
      logging.debug('pos: %s ___ goal: %s' % (str(ant_loc), str(goal_loc)))
      if ant_loc and goal_loc:
        path = self.findpath(ant_loc, goal_loc)
        direction = self.ants.direction(ant_loc, goal_loc)[0]
        new_loc = self.ants.destination(ant_loc, direction)
        if (self.ants.passable(new_loc)):
          self.ants.issue_order((ant_loc, direction))
      if self.ants.time_remaining() < 10:
        break

  def closest_food(self, loc):
    dist = 100000
    dest = None
    for food_loc in self.ants.food():
      if self.ants.distance(food_loc, loc) < dist:
        dist = self.ants.distance(food_loc, loc)
        dest = food_loc
    return dest

  def findpath(self, start, goal):  # from, to are loc tuples uses A* from wikipedia
    logging.warning('started findpath')
    logging.warning('started finding %s from %s' % (goal, start))
    closedset = [] # list of already visited location tuples
    openset = [start] # list of location tuples at the border
    came_from = {}
    g_score = {start: 0}
    h_score = {start: self.a_star_h(start, goal)}
    f_score = {start: self.a_star_h(start, goal)} # because a_star_g is 0

    logging.warning((g_score, h_score, f_score))
    while len(openset) > 0:
      a_star_values = {}
      for loc in openset:
        a_star_values[loc] = self.a_star_f(loc, goal, came_from)
      opt_loc = min(a_star_values, key=a_star_values.get) # find next node with lowest f_score value
      logging.debug(str(opt_loc))
      #self.log('opt loc:s a star vlaues:%s', a_star_values)
      if opt_loc == goal:
        return self.a_star_reconstruct_path(came_from, came_from[goal])
      openset.remove(opt_loc)
      closedset.append(opt_loc)
      for loc in self.ants.neighbors(opt_loc):
        if loc in closedset: # already visited
          continue
        tentative_g_score = g_score[opt_loc] + 1
        if not loc in openset:
          openset.append(loc)
          tentative_is_better = True
        else:
          tentative_is_better = False
          
        if tentative_is_better:
          came_from[loc] = opt_loc
          g_score[loc] = tentative_g_score
          h_score[loc] = self.a_star_h(loc, goal)
          f_score[loc] = g_score[loc] + h_score[loc]
    return False      

  def a_star_g(self, came_from, loc):  
    travelled = self.reconstruct_path(came_from, loc)
    if travelled:
      return len(travelled) #number of nodes travelled
    else:
      return 0

  def a_star_h(self, start, goal):
    return self.ants.straight_line_distance(start, goal)

  def a_star_f(self, start, goal, came_from):   
    return self.a_star_g(came_from, start) + self.a_star_h(start, goal)  # start should be the current position in the path

  def reconstruct_path(self, came_from, current_node):
    #if current_node in came_from.keys():
    #  p = self.reconstruct_path(came_from, came_from[current_node])
    #  logging.warning('current path: %s' % p)
    #  return p.append(current_node)
    #else:
    #  return [current_node]
    while current_node in came_from.keys():
      r.append(current_node








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
