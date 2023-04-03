import numpy as np
from scipy.stats import binom
from math import comb

def Prot_FC(m, faulty = None, mu = 0.272, l = 0.94):
	"""
    Function that carries out one instance of the Monte Carlo type simulation for the protocol. 
    The adversary strategies used here are the same discussed in the paper.

    Parameters
    ----------
    m : integer, the number of four-qubit singlet states used in the protocol.
    
    faulty : integer in {0,1,2}, where 0 corresponds to the no faulty, 1 to the s faulty and 2 to the r0 faulty configuration.
    
    mu : float, the mu parameter of the protocol. The default is 0.272.
    
    l : float, the lambda parameter of the protocol. The default is 0.94.

    Returns
    -------
    type_res: 0 or 1. 0 corresponds to the protocol achieving Weak Broadcast, while 1 corresponds to failure.

    """

	#define the usual quantities
	T = int(np.ceil(mu * m)) #define the T parameter
	Q = T - int(np.ceil(l * T)) + 1 #define the Q parameter
    
	#define arrays that will be used to generate the measurement results for the components
    
	#define the possible measurement results
	states = [[0, 1, 1], [1, 0, 1], [1, 1, 0], [2, 0, 1], [2, 1, 0], [3, 0, 0]]
    
    #define the array that will be used to obtain the correct probabilities during measurement
	statenums = [0, 0, 0, 0, 1, 2, 3, 4, 5, 5, 5, 5]

	#Generation of the random measurements for the components
    #define container for the measurement results
	Qmeas = []
    
    #carry out the measurements
	for i in range(m):
        #pick a random statenum
		statenum = np.random.choice(statenums, size = 1)[0]
        
        #add the corresponding state to the measurement results
		Qmeas.append(states[statenum])
    
    #make a numpy array out of Q
	Qmeas = np.array(Qmeas)

    #Distribute the measurement results among the components
	Qs = Qmeas[:, 0]
	Q0 = Qmeas[:, 1]
	Q1 = Qmeas[:, 2]

    #if the faulty configuration is not specified then generate one randomly
	if faulty == None:
		faulty = np.random.randint(3)

    #now carry out the simulation based on the faulty configuration
    
    #nofaulty configuration
	if faulty == 0: 

		#Step1
		#the correct S generates a bit message and sends it to R0 and R1
		xs = np.random.randint(2)  
		ys = xs
		x0 = xs
		x1 = xs

		#collect the corresponding indices and distribute them
		sigmas = np.array([int(i) for i in range(m) if Qs[i] == 3 * xs], dtype="int")
		sigma0 = sigmas.copy()
		sigma1 = sigmas.copy()

		#Step2
		#the receivers either accept the message of S or not
        #R0 and R1 check both the length condition and the consistency condition
		if (T <= len(sigma0)) and  (len(sigma0) == len([i for i in sigma0 if Q0[i] == 1 - x0])):
			y0 = x0
		else:
			y0 = 2

		if (T <= len(sigma1)) and  (len(sigma1) == len([i for i in sigma1 if Q1[i] == 1 - x1])):
			y1 = x1
		else:
			y1 = 2

		#Step3
        #R0 sends R1 its own data
		rho01 = np.array([int(i) for i in sigma0 if Q0[i] == 1 - y0], dtype="int")
		y01 = y0

		#Step4
		lst = np.array([int(i) for i in rho01 if Q1[i] == 1 - y01], dtype="int")
		#and R1 checks the conditions below according to the protocol
		if ( (y01 != 2) and (y1 != 2) and (y01 != y1) ) and (len(rho01) >= T) and (len(lst) >= l*T + len(rho01) - T):
			y1 = y01

        #the result of the protocol is the list of the three outputs
		result = np.array([ys, y0, y1])
        
        #check whether the protocol achieved Weak Broadcast or not
		type_res = typecheck(result = result, faulty = faulty)
        
        #return 0 or 1 depending on the result of the protocol
		return type_res

    #S faulty configuration
	elif faulty == 1: 

		#Step1
        # S sends conflicting bit values to the components
		xs = np.random.randint(2)
		ys = xs
		x0 = xs
		x1 = 1 - x0

        #correct indices for R0, this set will bet modified
		s0_original = np.array([i for i in range(m) if Qs[i] == 3 * x0], dtype="int")
        
        # correct indices for R1
		sigma1 = np.array([i for i in range(m) if Qs[i] == 3 * x1], dtype="int")
        
		#based on the number of the indices in sigma1 the Event is either in the domain of the s faulty adversary strategy or not
        
		#the bounds on the number of events in sigma1 is (on l3)
		if (len(sigma1) < T) or (len(sigma1) > m - T):
            #return 1 which means that the protocol achieved Failure
			return 1
        
        #there is also a constraint on l1
		if ( len(s0_original) < T - Q ) or (len(s0_original) > (m - len(sigma1)- Q)):
            #return 1 which means that the protocol achieved Failure
			return 1

		#the number of correct messages that S needs to send to R0 is
		c = T - Q
        
		#the number of inconsistent messages that S needs to send to R0 is Q
		ic = Q
        
        #now create the sigma0 set that S sends to R0
        #this set consists of two parts:
        #-a subset which contains only consistent indices
        #-a subset which contains only inconsistent indices
        
		c_sigma0 = np.random.choice(s0_original, size = c, replace = False)

		#construct an index set out of which S chooses the inconsistent indices
		sample = np.array([int(i) for i in range(m) if i not in s0_original if i not in sigma1], dtype="int")
        
		#S selects ic indices out of this sample
		ic_sigma0 = np.random.choice(sample, size = ic, replace = False)
        
		#sigma0 is the sum of these index sets
		sigma0 = np.concatenate((c_sigma0, ic_sigma0))
		sigma0 = sigma0.astype("int")

		#Step2
		#the receivers either accept or not the message of S
        #R0 and R1 check both the length condition and the consistency condition
		if (T <= len(sigma0)) and  (len(sigma0) == len([i for i in sigma0 if Q0[i] == 1 - x0])):
			y0 = x0
		else:
			y0 = 2

		if (T <= len(sigma1)) and  (len(sigma1) == len([i for i in sigma1 if Q1[i] == 1 - x1])):
			y1 = x1
		else:
			y1 = 2

		#Step3
        #R0 sends R1 its own data
		rho01 = np.array([int(i) for i in sigma0 if Q0[i] == 1 - y0], dtype="int")
		y01 = y0

		#Step4
		lst = np.array([int(i) for i in rho01 if Q1[i] == 1 - y01], dtype="int")
		#and R1 checks the conditions below according to the protocol
		if ( (y01 != 2) and (y1 != 2) and (y01 != y1) ) and (len(rho01) >= T) and (len(lst) >= l*T + len(rho01) - T):
			y1 = y01

        #the result of the protocol is the list of the three outputs
		result = np.array([ys, y0, y1])
        
        #check whether the protocol achieved Weak Broadcast or not
		type_res = typecheck(result = result, faulty = faulty)
        
        #return 0 or 1 depending on the result of the protocol
		return type_res


	elif faulty == 2: #R0 faulty configuration

		#Step1
		#the correct S generates a bit message to R0 and R1
		xs = np.random.randint(2)
		ys = xs
		x0 = xs
		x1 = xs

		#collect the corresponding indices and distribute them
		sigmas = np.array([int(i) for i in range(m) if Qs[i] == 3 * xs], dtype="int")
		sigma0 = sigmas.copy()
		sigma1 = sigmas.copy()

		#Step2
		#now as R0 is a faulty component it automatically changes its output to the other value so
		y0 = 1 - x0

		#R1 still checks the values and chooses like previously
		if (T <= len(sigma1)) and  (len(sigma1) == len([i for i in sigma1 if Q1[i] == 1 - x1])):
			y1 = x1
		else:
			y1 = 2

		#Step3
		#check whether the Event is in the domain or not (condition for l1)
		if len(sigma0) > (m - T):
			return 1

		#R0 constructs the index set rho01.

		#l2 indices
		rho01_1 = np.array([int(i) for i in range(m) if i not in sigma0 if Q0[i] == y0], dtype="int")

        # if there are enough l2 indices then the rho01 set is already long enough
		if len(rho01_1) >= T:
			rho01 = rho01_1
            
		else:  #R0 needs more indices
			#construct a sample which contain those indices that R0 can use 
			sample = np.array([int(i) for i in range(m) if i not in sigma0 if i not in rho01_1], dtype="int")

			#R0 chooses randomly a few indices out of these
			rho01_2 = np.random.choice(sample, size = T - len(rho01_1), replace = False)

			#put together these indices
			rho01 = np.concatenate((rho01_1, rho01_2))

        #R0 sends his output to R1
		y01 = y0

		#Step4
		lst = np.array([int(i) for i in rho01 if Q1[i] == 1 - y01], dtype="int")
		#and R1 checks the conditions below according to the protocol
		if ( (y01 != 2) and (y1 != 2) and (y01 != y1) ) and (len(rho01) >= T) and (len(lst) >= l*T + len(rho01) - T):
			y1 = y01

        #the result of the protocol is the list of the three outputs
		result = np.array([ys, y0, y1])
        
        #check whether the protocol achieved Weak Broadcast or not
		type_res = typecheck(result = result, faulty = faulty)
        
        #return 0 or 1 depending on the result of the protocol
		return type_res


def typecheck(result, faulty):
    """
    Function that determines whether a specific result of the protocol is Weak Broadcast or not.

    Parameters
    ----------
    result : list of three integers, the ouputs of the components after the protocol.
    
    faulty : integer in {0,1,2}, characterises the faulty configuration we are dealing with.

    Returns
    -------
    integer, 0 or 1. 0 corresponds to Weak Broadcast, while 1 corresponds to failure.

    """
	#sort the result of the protocol
    ys, y0, y1 = result[0], result[1], result[2]

    # no faulty
    if faulty == 0:  
        if ys == y0 and ys == y1:
            return 0  #weak broadcast
        else:
            return 1
        
    # S faulty
    elif faulty == 1:
        if (y1 == y0) or (y0 != 2 and y1 == 2) or (y1 != 2 and y0 == 2):
            return 0  #weak broadcast
        else:
            return 1
        
    # R0 faulty
    else:
        if y1 == ys:
            return 0  #weak broadcast
        else:
            return 1

def simple_stats(N, m, faulty=None, mu=0.272, l=0.94):
    """
    Function that carries out N random simulations using fixed parameters

    Parameters
    ----------
    N : integer, the number of random simulations used to obtain the failure probabilities.
    
    m : integer, the number of four-qubit singlet states used in the protocol.
    
    faulty : integer in {0,1,2}, where 0 corresponds to the no faulty, 1 to the s faulty and 2 to the r0 faulty configuration.
    
    mu : float, the mu parameter of the protocol. The default is 0.272.
    
    l : float, the lambda parameter of the protocol. The default is 0.94.

    Returns
    -------
    float, the failure probability

    """

    data = [0, 0]
    
    #do the simulation N times
    for i in range(N):
        # increase the number of occurrences for an outcome
        data[(Prot_FC(m=m, faulty=faulty, mu=mu, l=l))] += 1
        
    stat = np.array(data) / N  #obtain the probabilities
    
    # return the failure probability only
    return stat[1]

def total_stats(N, ms, faulty=None, mu=0.272, l=0.94): 
    """
    Function that carries out the fixed parameter simulation N times for each m in ms.

    Parameters
    ----------
    N : integer, the number of random simulations used to obtain the failure probabilities.
    
    ms : list of integers, list of the possible number of four-qubit singlet states used in the protocol.
    
    faulty : integer in {0,1,2}, where 0 corresponds to the no faulty, 1 to the s faulty and 2 to the r0 faulty configuration.
    
    mu : float, the mu parameter of the protocol. The default is 0.272.
    
    l : float, the lambda parameter of the protocol. The default is 0.94.

    Returns
    -------
    totalstatistics: list of floats, the failure probabilities as a function of m.

    """
    
    #create container for the probabilities
    totalstatistics = []
    
    #iterate through all m values
    for m in ms:
        #obtain the sime_statistics for all the m values
        ss = simple_stats(N = N, m = m, faulty = faulty, mu = mu, l = l)
        
        #add the probablity of Weak Broadcast to the totalstatistics list
        totalstatistics.append(ss)
    
    totalstatistics = np.array(totalstatistics)
    
    return totalstatistics


def mn2(m,p1,p2,p3,i,j,k):
    """
    Function that calculates a specific combination of binomial coefficients and probabilities

    Parameters
    ----------
    m : integer, the number of four-qubit singlet states used in the protocol.

    p1 : float, probability.
    
    p2 : float, probability.
    
    p3 : float, probability.
    
    i : integer, i < m.
    
    j : integer, j < m.
    
    k : integer, k < m. The condition  that i+j+k=m must hold.

    Returns
    -------
    float, probability. Trinomial distribution.

    """
    return comb(m,i) * comb(m - i, j) * ( p1**i ) * ( p2**j ) * ( p3**k )



def fprob_nofaulty(m, mu, l):
    """
    Function that calculates the exact failure probability for the no faulty configuration

    Parameters
    ----------
    m : integer, the number of four-qubit singlet states used in the protocol.
    
    mu : float, the mu parameter of the protocol.
    
    l : float, the lambda parameter of the protocol.

    Returns
    -------
    prob : float, the failure probability.

    """
    #define T
    T = int(np.ceil(mu*m))
    
    #evaluate the failure probability formula in the paper
    
    prob = 0
    
    #iterate through all l1
    for i in range(0, T):
        
        #add the binomial distribution with the given parameters
        prob += binom.pmf(i, m, 1/3)
        
    #return the failure probability
    return prob


def fprob_sfaulty(m, mu, l):
    """
    Function that calculates the upper bound of the failure probability for the s faulty configuration

    Parameters
    ----------
    m : integer, the number of four-qubit singlet states used in the protocol.
    
    mu : float, the mu parameter of the protocol.
    
    l : float, the lambda parameter of the protocol.

    Returns
    -------
    prob : float, the failure probability.

    """
	#define the usual quantities
    T = int(np.ceil(mu * m)) #define the T parameter
    Q = T - int(np.ceil(l * T)) + 1 #define the Q parameter
    
    #evaluate the upper bound formula in the paper
    
    #we can readily evaluate the following quantity and use it
    probfact = 2**(- 1 * Q)
    
    #set the initial probability to 1
    prob = 1
    
    #for each l3 between T and m-T
    for i in range(T, m - T + 1):
        
        #for each l1 between T-Q and m-Q-l3
        for j in range(T - Q, m - Q - i + 1):
            
            #the probability of the Event is 
            Eprob = mn2(m, 1/3, 1/3, 1/3, i, j, m-i-j) 
            
            #then the failure probability should be decreased by Eprob*(1-probfact)
            prob -= Eprob*(1-probfact)
            
    #return the failure probability
    return prob


def fprob_r0faulty(m, mu, l):
    """
    Function that calculates the upper bound of the failure probability for the r0 faulty configuration

    Parameters
    ----------
    m : integer, the number of four-qubit singlet states used in the protocol.
    
    mu : float, the mu parameter of the protocol.
    
    l : float, the lambda parameter of the protocol.

    Returns
    -------
    prob : float, the failure probability.

    """
    #define the usual quantities
    T = int(np.ceil(mu * m)) #define the T parameter
    Q = T - int(np.ceil(l * T)) + 1 #define the Q parameter
    
    #evaluate the upper bound formula in the paper

    prob = 0
    
    #last term in pf_downarrow
    #for all l1 between 0 and T
    for i in range(0, T):
        
        #add binomial
        prob += binom.pmf(i, m, 1/3 )

    #second term in pf_downarrow
    #for all l1 between T and m-T
    for i in range(T, m - T + 1):
        
        #and for all l2 between T-Q+1 and m-l1
        for j in range(T - Q + 1, m - i + 1):
            
            prob += mn2(m, 1/3, 1/6, 1/2, i, j, m-i-j)

    #first term in pf_downarrow
    #for all l1 between T and m-T
    for i in range(T , m - T + 1):
        
        #for all l2 between 0 and T-Q
        for j in range(0, T - Q + 1):
            
            #for all possible number of correctly guessed indices 
            for k in range(T - Q + 1 - j, T - j + 1):
                
                prob += mn2(m, 1/3, 1/6, 1/2, i, j, m - i - j) * binom.pmf(k, T - j, 2/3)

    #upper bound term
    for i in range(m -T + 1, m + 1):
        prob += binom.pmf( i, m, 1/3)

    #return the failure probability
    return prob

#Now let's add the possibility to make the twoD grid plots

def maximal_fprob(m, mu, l):
    """
    Function that determines the maximal failure probability for fixed parameters 

    Parameters
    ----------
    m : integer, the number of four-qubit singlet states used in the protocol.
    
    mu : float, the mu parameter of the protocol.
    
    l : float, the lambda parameter of the protocol.

    Returns
    -------
    prob : float, the maximal failure probability.

    """
    
    #calculate the failure probability for all the faulty configurations independently
    p0 = fprob_nofaulty(m = m, mu = mu, l = l)
    p1 = fprob_sfaulty(m = m, mu = mu, l = l)
    p2 = fprob_r0faulty(m = m, mu = mu, l = l)

    #return the maximal failure probability
    return max(p0,p1,p2)


def optimal_m_for_parametervalues_finder(ms, mu, l, fprobtreshhold = 0.05):
    """
    Function that determines m_min for errprobthreshhold.

    Parameters
    ----------
    ms : list of integers, list of the possible number of four-qubit singlet states used in the protocol.

    mu : float, the mu parameter of the protocol.
    
    l : float, the lambda parameter of the protocol.
    
    fprobtreshhold : float, the failure probability threshhold. The default is 0.05.

    Returns
    -------
    m : integer, the minimal number of states for which the maximal failure probability is lower than the threshhold value.

    """
    #for each m
    for m in ms:
        #if the maximal p_f is lower than the threshhold then return that m
        if maximal_fprob(m = m, mu = mu, l = l) < fprobtreshhold: 
            return m
    
    #if none of the m satisfy the condition than return the last value
    return m

def optimalizator(ms, mus, ls, fprobtreshhold = 0.05):
    """
    For each point defined by all the combinations of mus and ls find m_min.

    Parameters
    ----------
    ms : list of integers, list of the possible number of four-qubit singlet states used in the protocol.
    
    mus : list of floats, list of the possible mu values used in the protocol.
    
    ls : list of floats, list of the possible lambda values used in the protocol.
    
    fprobtreshhold : float, the failure probability threshhold. The default is 0.05.

    Returns
    -------
    points: list of lists containing three numbers, each entry is a list containg [mu, lambda, m_min]

    """
    #container for the possible m values
    points = []
    
    #for each mu value
    for mu in mus:
    
        #for each lambda value
        for l in ls:
            
            #optimal value of m for the given parameters
            z = optimal_m_for_parametervalues_finder(ms = ms, mu = mu, l = l, fprobtreshhold = fprobtreshhold)
            
            #add the three numbers to points
            points.append([mu, l, z])
        
    #returns the values
    return np.array(points) 