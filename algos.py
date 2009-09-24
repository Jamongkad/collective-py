from math import sqrt

def sim_distance(person1, person2):
    si = []
    for rating, movie in person1:
        for rating2, movie2 in person2:
            if movie2 == movie:
                si.append(1)

    if len(si) == 0: return 0

    sum_of_values = []
    for r, m in person1:
        for r2, m2 in person2:
            if m == m2:
                sum_of_values.append(pow(r.rating - r2.rating, 2))

    return 1/(1+sum(sum_of_values))

def sim_pearson(person1, person2):
    si = {}
    p1 = []
    p2 = []
    for r, m in person1:
        for r2, m2 in person2:
            if m == m2:
                p1.append(r.rating)       
                p2.append(r2.rating)
                si[m.movie_name] = 1

    n = len(si)

    if n is 0: return 0

    sum1 = sum([i for i in p1])
    sum2 = sum([i for i in p2])

    sum1sq = sum([pow(i, 2) for i in p1])
    sum2sq = sum([pow(i, 2) for i in p2])
    
    p = dict(zip([i for i in p1], [i for i in p2])) 
    pSum = sum([k * v for k, v in p.iteritems()]) 
   
    num = pSum-(sum1*sum2/n) 
    den = sqrt((sum1sq-pow(sum1, 2)/n)*(sum2sq-pow(sum2, 2)/n))
    
    return float(num)/den
