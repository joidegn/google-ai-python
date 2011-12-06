import math

class Pathfinder:
  def findpath(self, start, goal):  # from, to are loc tuples uses A* from wikipedia
    print('started findpath')
    print('started finding %s from %s' % (goal, start))
    closedset = [] # list of already visited location tuples
    openset = [start] # list of location tuples at the border
    came_from = {}
    g_score = {start: 0}
    h_score = {start: self.a_star_h(start, goal)}
    f_score = {start: self.a_star_h(start, goal)} # because a_star_g is 0

    print((g_score, h_score, f_score))
    while len(openset) > 0:
      a_star_values = {}
      for loc in openset:
        a_star_values[loc] = self.a_star_f(loc, goal, came_from)
      opt_loc = min(a_star_values, key=a_star_values.get) # find next node with lowest f_score value
      print(str(opt_loc))
      if opt_loc == goal:
        return self.reconstruct_path(came_from, came_from[goal])
      openset.remove(opt_loc)
      closedset.append(opt_loc)
      for loc in neighbors(opt_loc):
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
    return distance(start, goal)

  def a_star_f(self, start, goal, came_from):   
    return self.a_star_g(came_from, start) + self.a_star_h(start, goal)  # start should be the current position in the path

  def reconstruct_path(self, came_from, current_node):
    print('came_from:')
    print(came_from)
    print('current node:')
    print(current_node)
    #if current_node in came_from.keys():
    #  p = self.reconstruct_path(came_from, came_from[current_node])
    #  print('current path: %s' % p)
    #  return p.append(current_node)
    #else:
      #return [current_node]
    p = []
    end = 0
    while not end:
      if current_node in came_from.keys():
        p.append(came_from[current_node])
        current_node = came_from[current_node]
      else:
        end = 1
    return p

def distance(loc1, loc2):
  return math.sqrt((loc1[0]-loc2[0])**2 + (loc1[0]-loc2[0])**2)
def neighbors(loc):
  n = []
  for x in (-1,0,1):
    for y in (-1,0,1):
      if (x+y) % 2 > 0 and loc[0]+x>=0 and loc[1]+y>=0:
        if passable((loc[0]+x, loc[1]+y)):
          n.append((loc[0]+x, loc[1]+y))
  return n 
def passable(loc):
  for dim in loc:
    if dim >= 10:
      return False
  return map[loc] >= 0

map = {}
for x in range(10):
  for y in range(10):
    map[(x,y)] = 0

for x in range(9):
  map[(8,x)] = -1
for x in range(9):
  map[(5,x+1)] = -1
for x in range(9):
  map[(3,x)] = -1

map[(9,9)] = 1
pathfinder = Pathfinder()
path = pathfinder.findpath((0,0),(9,9))
print ('path with length %s found: %s' % (len(path), path))
