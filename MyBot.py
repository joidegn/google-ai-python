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
    self.move_registry = {} # every ant should register the field it is moving and maybe the goal that it wants to reach
    self.stats = {} # store some stats for me to evaluate the algorithm
    self.stats['path'] = 0
    self.stats['path_lengths'] = []
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    logging.debug(self.ants)
    

  def do_turn(self, ants):
    self.ants = ants
    self.stats['path'] = 0 #reset stats
    logging.warning('\n\nstarting turn, seeing %s food' % self.ants.food())
    for ant_loc in self.ants.my_ants():
      logging.warning('Time left: %s' % (self.ants.time_remaining()))
      goal_loc = self.closest_food(ant_loc)
      if ant_loc and goal_loc:
        distance = self.ants.distance(ant_loc, goal_loc)
        if distance < 100:
          path = self.findpath(ant_loc, goal_loc)
          logging.warning('ant at %s is going to go to %s via:\n%s\n that is %s steps' % (ant_loc, goal_loc, path, len(path)))
          new_loc = path.pop() 
          direction = self.ants.direction(ant_loc, new_loc)[0]
          if (self.ants.isloc(new_loc) and self.ants.passable(new_loc)): 
            logging.warning('move order issued: ant at %s going %s to reach %s' % (ant_loc, direction, new_loc))
            self.ants.issue_order((ant_loc, direction))
      if self.ants.time_remaining() < 100:
        break
    if self.ants.time_remaining() > 100:  # we have enought time to do some stuff, so we should do it
      logging.warning('There is still plenty of time')

  def closest_food(self, loc):
    dist = 100000
    dest = None
    for food_loc in self.ants.food():
      if self.ants.distance(food_loc, loc) < dist:
        dist = self.ants.distance(food_loc, loc)
        dest = food_loc
    return dest

  def findpath(self, start, goal):  # from, to are loc tuples uses A* from wikipedia
    logging.warning('started finding %s from %s that is %s steps. Time left: %s' % (goal, start, self.ants.distance(start, goal), self.ants.time_remaining()))
    self.stats['path'] = self.stats['path'] + 1
    logging.warning('found %s paths' % self.stats['path'])
    
    closedset = [] # list of already visited location tuples
    openset = [start] # list of location tuples at the border
    came_from = {}
    g_score = {start: 0}
    h_score = {start: self.a_star_h(start, goal)}
    f_score = {start: self.a_star_h(start, goal)} # because a_star_g is 0

    while len(openset) > 0:
      a_star_values = {}
      for loc in openset:
        a_star_values[loc] = self.a_star_f(loc, goal, came_from)
      opt_loc = min(a_star_values, key=a_star_values.get) # find next node with lowest f_score value
      if opt_loc == goal:
        #logging.warning('path found reconstructing:%s' % came_from)
        #logging.warning('reconstruction:%s' % self.reconstruct_path(came_from, came_from[goal]))
        p = [goal]
        for loc in  self.reconstruct_path(came_from, came_from[goal]):
          p.append(loc)
        return p
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
    #logging.warning('reconstructing %s from %s' % (came_from, current_node))
    #p = []
    #steps = 0
    #while current_node in came_from.keys(): # finishes once we reach the location to which we didnt come
    #  steps = steps + 1
    #  p.append(current_node)
    #  current_node = came_from[current_node] # set current_node to next element
    #  if steps > 100:
    #    logging.warning('reconstructing %s from %s' % (came_from, current_node))
    #return p
    if current_node in came_from.keys():
      p = self.reconstruct_path(came_from, came_from[current_node])
      if p:
        return p.append(current_node)
      else:
        logging.warning('something went wrong: came_from:%s current_node:%s' % (came_from, current_node))
    else:
      return [current_node]

     






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
