'''
funcion spring_flow is defined below 
with 'current' - as the current sprinf flow based off the previous value
	 'mult' - as factor of decrease over spring flow
	 'i' - being the number of recursions or days since peak flow
'''
discharge=[]
def spring_flow(current, mult,i):
	if current < .0009: #recursion is kicked out once value goes below .009
		print('done')
	else:
		print(i,current) #number of recursions (days) / daily flow being printed 
		return spring_flow (current*mult, mult,i+1) #the recursion, the function calling itseld and using previously calculated value


spring_flow(10000,.9,1) 