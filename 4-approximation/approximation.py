from math import sqrt

def distance(p,I):
    k = float("inf")
    for x in I:
        if sqrt((x[0]-p[0])**2+(x[1]-p[1])**2) < k:
            k = sqrt((x[0]-p[0])**2+(x[1]-p[1])**2)
    return k 


def UnitDiskCover(rails,rayon):
    C = []
    I = []
    L = sorted(rails, key=lambda tup: tup[1])
    print(L)
    while L != []:
        p = L.pop(0)
        print(p)
        if distance(p,I) > 2*rayon and distance(p,C) > rayon:
            C += [p]
            if distance((p[0]-1.5*rayon,p[1]+0.86*rayon),L) < rayon:
                C += [(p[0]-1.5*rayon,p[1]+0.86*rayon)]
            if distance((p[0]+1.5*rayon,p[1]+0.86*rayon),L) < rayon:
                C += [(p[0]+1.5*rayon,p[1]+0.86*rayon)]
            if distance((p[0],p[1]+1.73*rayon),L) < rayon:
                C += [(p[0],p[1]+1.73*rayon)]            

            I += [p]           
            
    return C