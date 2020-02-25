# has the functions to print out values and the policy
def max_dict(d):
  # returns the argmax (key) and max (value) from a dictionary
  max_key = None
  max_val = float('-inf')
  for k, v in d.items():
    if v > max_val:
      max_val = v
      max_key = k
  return max_key, max_val

def print_val(V,g):
	for i in range(g.width):
		print("---------------------------")
		for j in range(g.height): 
			v=V.get((i,j),0)
			if v>=0: 
				print("%.2f|"% v, end=" ")
			else: 
				print("%.2f|" % v, end =" ")
			
		print("")

def print_policy(P,g):
	for i in range(g.width):
		print("---------------------------")
		for j in range(g.height):
			a=P.get((i,j), ' ')
			print(" %s |" %a, end=" ")
		print("")

