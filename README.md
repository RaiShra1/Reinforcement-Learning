# Reinforcement-Learning

grid_world.py : Sets up the 3x4 grid for the classic example for Reinforcement Learning. 
The grid shape is: 
-------------------
| . | . | . | +1 |
| . | x | . | -1 |
| s | . | . |  . |
-------------------

s denotes the starting point and if the agent reaches grid position (0,3) the agent gets a reward of +1 
and if the agent reaches grid position (1,3) then it receives a penality of -1 

utils.py: It is only used for displaying the Reward, Value and Policy

value_iteration_algorithm.py: This implments finds the Value table based on the optimal actions that is already known. 
This is developed using the Dynamic Programming principle and is based on the Bellman eqaution

monte_carlo_Q_learning.py : This implements the Q learning algorithm of Reinforcement learning to solve the grid world problem. 
