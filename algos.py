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

    def square_minus(square, sum, n):
        return square-pow(sum, 2)/n

    def sum_person(person):
        return sum([person[it] for it in si]) 

    def pow_sum_person(person):
        return sum([pow(person[it], 2) for it in si])
    
    sum1 = sum_person(firstPerson) 
    sum2 = sum_person(secondPerson)
  
    sum1Sq = pow_sum_person(firstPerson)
    sum2Sq = pow_sum_person(secondPerson)
    
    pSum = sum([firstPerson[it] * secondPerson[it] for it in si])

    num = pSum - (sum1*sum2/n)
    den = sqrt(square_minus(sum1Sq, sum1, n) * square_minus(sum2Sq, sum2, n))
    
    if den == 0: return 0

    r=num/den
    return r
