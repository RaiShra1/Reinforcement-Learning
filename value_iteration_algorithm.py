import numpy as np 
from grid_world import std_grid
from utils import * 

THETA=1e-3
GAMMA=0.9
ALL_POSSIBLE_ACTIONS=('Up', 'Down', 'Left', 'Right')

def best_action_value(gridEnv, V, s):
	#returns the action and value after finding max value out of all possible actions
	best_action=None
	best_value=float('-inf')
	gridEnv.set_states(s)
	#loop through all possible actions to find best action for that state
	for a in ALL_POSSIBLE_ACTIONS: 
		transition_probs=gridEnv.get_transition_probs(a)
		expected_value=0
		expected_reward=0
		
		for (prob,r,next_state) in transition_probs:
			expected_reward=expected_reward+ prob*r
			expected_value=expected_value+ prob* V[next_state]
		v=expected_reward + GAMMA * expected_value
		
		if v > best_value:
			best_value=v
			best_action=a
			
	return best_action, best_value

def calc_values(gridEnv): 
	V={} #initializing the value table
	states= gridEnv.all_states()
	for s in states:
		V[s]=0
	while True:
		biggest_change=0
		for s in gridEnv.non_terminal_states():
			old_value=V[s]
			_, new_value=best_action_value(gridEnv,V,s)
			V[s]=new_value
			biggest_change= max(biggest_change, np.abs(old_value-new_value))
			
		if biggest_change < THETA:
			break
	return V
	
def init_random_policy(gridEnv): 
	#policy is a lookup table : given state, it gives the best action
	# we'll first initialize a random table and update it as we learn
	policy={}
	for s in gridEnv.non_terminal_states():
		policy[s]=np.random.choice(ALL_POSSIBLE_ACTIONS)
	return policy
	
def control_policy(gridEnv,V):
	policy= init_random_policy(gridEnv)
	for s in policy.keys(): 
		gridEnv.set_states(s)
		#loop through all possible actions to find the best current action
		best_action,_=best_action_value(gridEnv,V,s)
		policy[s]=best_action
	return policy
	

if __name__ == '__main__': 
  # this grid gives you a reward of -0.1 for every non-terminal state
  # we want to see if this will encourage finding a shorter path to the goal
  grid =std_grid(obey_probability=0.5, step_cost=None)

  # print rewards
  print("rewards:")
  print_val(grid.rewards, grid)

  # calculate accurate values for each square
  V = calc_values(grid)

  # calculate the optimum policy based on our values
  policy = control_policy(grid, V)

  # our goal here is to verify that we get the same answer as with policy iteration
  print("values:")
  print_val(V, grid)
  print("policy:")
  print_policy(policy, grid)






















