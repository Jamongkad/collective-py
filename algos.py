from math import sqrt

#ten times better algorithm
def sim_distance(prefs, person1, person2):
    #fetch prefs only once.
    firstPerson = prefs(person1)
    secondPerson = prefs(person2)
    si = [] 

    for movie1 in firstPerson:
        if movie1 in secondPerson:
            si.append(1)
        
    n = len(si)
    if n is 0: return 0

    sum_of_squares = sum([pow(firstPerson[item] - secondPerson[item], 2) 
                         for item in firstPerson if item in secondPerson])
    
    return 1/(1+sum_of_squares)

def sim_pearson(prefs, person1, person2):
    si = {}

    firstPerson = prefs(person1)
    secondPerson = prefs(person2)

    for item in firstPerson:
        if item in secondPerson:
            si[item] = 1

    n = len(si)
    if n is 0: return 0

    sum1 = sum([firstPerson[it] for it in si])
    sum2 = sum([secondPerson[it] for it in si])
    
    sum1Sq = sum([pow(firstPerson[it], 2) for it in si])
    sum2Sq = sum([pow(secondPerson[it], 2) for it in si])
    
    pSum = sum([firstPerson[it] * secondPerson[it] for it in si])

    num = pSum - (sum1*sum2/n)
    den = sqrt((sum1Sq-pow(sum1, 2)/n) * (sum2Sq-pow(sum2, 2)/n))
    
    if den == 0: return 0

    r=num/den

    return r
