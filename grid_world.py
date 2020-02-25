import numpy as np

# creating class for grid environment
class gridEnv: 
	def __init__(self, width, height,start): 
		self.width=width
		self.height=height
		#consider i is for rows and j is for columns
		self.i=start[0]
		self.j=start[1]
		
		
	# rewards should be a dictionary: r[row, col]: reward
	#actions is also a dictionary: A[row,col]: list of all actions possible
	def set(self, rewards,actions,obey_probability):
		self.rewards=rewards
		self.actions=actions
		self.obey_prob=obey_probability
	
	
	def non_terminal_states(self): 
		return self.actions.keys()
		
	
	def set_states(self, s):
		self.i=s[0]
		self.j=s[1]
	
	def current_state(self):
		return (self.i, self.j)
	
	def is_terminal(self, s):
		return s not in self.actions
		
	def stochastic_move(self, action):
		p = np.random.random()
		if p <= self.obey_prob:
			return action
		if action == 'Up' or action == 'Down':
			return np.random.choice(['Left', 'Right'])
		elif action == 'Left' or action == 'Right':
			return np.random.choice(['Up', 'Down'])
	  
	
		
	def move(self, action):
		actual_action = self.stochastic_move(action)
		if actual_action in self.actions[(self.i, self.j)]:
			if actual_action == 'Up':
				self.i = self.i - 1
			elif actual_action == 'Down':
				self.i= self.i+1
			elif actual_action == 'Right':
				self.j =self.j + 1
			elif actual_action == 'Left':
				self.j = self.j - 1
		return self.rewards.get((self.i, self.j), 0)
		
		
	#returns the next state and the reward we would recieve 
	#by performing the action
	def move_check(self, action):
		i=self.i
		j=self.j
		# check if move is allowed
		if action in self.actions[(self.i,self.j)]:
			#perform the action
			if action== 'Up':
				i=i-1
			elif action == 'Down':
				i=i+1
			elif action == 'Right':
				j=j+1
			elif action == 'Left': 
				j=j-1
		#reward for reaching the next state
		reward= self.rewards.get((i,j),0)
		return ((i,j), reward)
		
	# to find the probabilities of taking an action and going to state s'
	
	def get_transition_probs (self, action):
		#returns the tuple (prob, reward, next state)
		probs=[]
		next_state,reward=self.move_check(action)
		probs.append((self.obey_prob,reward,next_state))
		disobey_prob=1-self.obey_prob
		
		if disobey_prob < 0.0: 
			return probs
		
		if action == 'Up' or action == 'Down': 
			next_state, reward= self.move_check('Left')
			probs.append((disobey_prob/2, reward,next_state))
			next_state,reward=self.move_check('Right')
			probs.append((disobey_prob/2, reward,next_state))
			
		elif action == 'Left' or action == 'Right': 
			next_state, reward= self.move_check('Up')
			probs.append((disobey_prob/2, reward,next_state))
			next_state,reward=self.move_check('Down')
			probs.append((disobey_prob/2, reward,next_state))
		
		return probs
		
		
	def end_game (self): 
	# returns true if game is over, else false
	# it becomes true if we are in a state where no actions are possible 
		return (self.i, self.j) not in self.actions
	
	def all_states(self):
    # possibly buggy but simple way to get all states
    # either a position that has possible next actions
    # or a position that yields a reward
		return set(self.actions.keys()) | set(self.rewards.keys())
	
def std_grid(obey_probability=1.0, step_cost= None): 
# defining a typical 3x4 grid like the traditional problem 
# .  .  .  1 - goal
# .  x  . -1 - game over
# s  .  .  .
# obey_probability : the probability of obeying the command
#step_cost: a penality applied at each step to minimize the number of moves (-0.1 usually)
	g= gridEnv(3,4,[2,0])
	rewards= {(0,3):1, (1,3): -1}
	actions={
		(0,0): ('Down', 'Right'),
		(0,1): ('Left', 'Right'),
		(0,2): ('Left','Down', 'Right'),
		(1,0): ('Up','Down'),
		(1,2): ('Up','Down', 'Right'),
		(2,0): ('Up','Right'),
		(2,1): ('Left','Right'),
		(2,2): ('Left','Up','Right'),
		(2,3): ('Left','Up'),
	}
	
	g.set(rewards, actions, obey_probability)
	if step_cost is not None:
		g.rewards.update({
		  (0, 0): step_cost,
		  (0, 1): step_cost,
		  (0, 2): step_cost,
		  (1, 0): step_cost,
		  (1, 2): step_cost,
		  (2, 0): step_cost,
		  (2, 1): step_cost,
		  (2, 2): step_cost,
		  (2, 3): step_cost,
		})
	return g
