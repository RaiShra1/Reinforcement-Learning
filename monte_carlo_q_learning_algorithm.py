import numpy as np
import matplotlib.pyplot as plt
from grid_world import std_grid
from utils import max_dict, print_val, print_policy

GAMMA=0.9
EPSILON =0.2
ALL_POSSIBLE_ACTIONS=('Up', 'Down', 'Left', 'Right')
N_EPISODES=10000

#epsilon greedy action selection function:
def epsilon_greedy(a,eps):
	p=np.random.random()
	if p<(1-eps):
		return a
	else:
		return np.random.choice(ALL_POSSIBLE_ACTIONS)

# Function to play the game, gain experience and also returns states and returns-G
def play_the_game(gridEnv, policy): 
	state=(2,0)  # define start point
	gridEnv.set_states(state)
	action=epsilon_greedy(policy[state],EPSILON) #deciding on the action using the epsilon_greedy algorithm
	states_actions_rewards=[(state,action,0)]
	
	while True:
		reward=gridEnv.move(action)
		state=gridEnv.current_state()
		if grid.end_game():
			states_actions_rewards.append((state, None, reward))
			break
		else: 
			action=epsilon_greedy(policy[state],EPSILON)
			states_actions_rewards.append((state,action,reward))
	
	G=0 #initializing G value to 0 for the first iteration
	states_actions_returns=[]
	first_visit=True
	
	for s,a,r in reversed(states_actions_rewards):
		if first_visit:
			first_visit=False
		else:
			states_actions_returns.append((s,a,G))
		G = r + GAMMA * G 
	states_actions_returns.reverse()
	return states_actions_returns
	
def Q_learning(gridEnv):
	policy={}
	#initializing a random policy
	for s in gridEnv.actions.keys():
		policy[s]=np.random.choice(ALL_POSSIBLE_ACTIONS)
	
	#initializing Q(s,a) and returns 
	Q={}
	returns={} 
	states=gridEnv.non_terminal_states()
	for s in states:
		Q[s]={}
		for a in ALL_POSSIBLE_ACTIONS:
			Q[s][a]=0
			returns[(s,a)]=[]
	
	deltas =[]
	
	for t in range(N_EPISODES):
		if t% 1000 ==0:
			print(t)
			
			biggest_change=0
			states_actions_returns=play_the_game(gridEnv,policy)
			
			seen_state_action_pairs=set()
			
			for s,a,G in states_actions_returns:
				sa=(s,a)
				if sa not in seen_state_action_pairs:
					returns[sa].append(G)
					old_q= Q[s][a]
					Q[s][a]=np.mean(returns[sa])
					biggest_change=max(biggest_change, np.abs(old_q-Q[s][a]))
					seen_state_action_pairs.add(sa)
				deltas.append(biggest_change)
			
				for s in policy.keys():
					a,_= max_dict(Q[s])
					policy[s]=a
				
		
		V={}
		for s in policy.keys():
			V[s]=max_dict(Q[s])[1]
			
	return V,policy,deltas
	
	
if __name__ == '__main__':
  grid = std_grid(obey_probability=1.0, step_cost=None)

  # print rewards
  print("rewards:")
  print_val(grid.rewards, grid)

  V, policy, deltas = Q_learning(grid)

  print("final values:")
  print_val(V, grid)
  print("final policy:")
  print_policy(policy, grid)

  plt.plot(deltas)
  plt.show()	
	
	
	
