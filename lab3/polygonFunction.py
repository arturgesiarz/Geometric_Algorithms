def triangulation(polygon):
    """
    Funkcja dokonuje triangulacji wielokąta monotonicznego -> wzdluz osi OY.
    :param polygon: tablica krotek punktów na płaszczyźnie euklidesowej podanych przeciwnie do ruchu wskazówek zegara - nasz wielokąt
    :return: tablica krotek dodawanych po kolei przekątnych np: [(1,5),(2,3)], oznacza, że triangulacja polega na dodaniu przekątnej pomiędzy wierzchołki 1-5 i 2-3
    """
    n = len(polygon)
    D = []
    points = []

    for i in range(n):
        points.append((polygon[i],i))

    points.sort(key = lambda point:point[0][1], reverse=True)

    leftSide, rightSide = createSides(polygon)
    Q = deque()
    Q.appendleft(points[0])
    Q.appendleft(points[1])
    pointerAct = 2

    while len(Q) > 0 and pointerAct < n:
        top = Q[0] #sprawdzam szczyt stosu
        leftSideTop = top[0] in leftSide
        rightSideTop = top[0] in rightSide
        pointAct = points[pointerAct][0]

        if (leftSideTop and pointAct in rightSide) or (rightSideTop and pointAct in leftSide):
            while len(Q) > 1: #nie wyciagamy ostatniego wierzolka
                v = Q.popleft()
                if not checkEdge(polygon,v[1],points[pointerAct][1]):
                    D.append((min(v[1],points[pointerAct][1]),max(v[1],points[pointerAct][1])))

            Q.popleft() #teraz stos po tej operacji musi byc pusty
            Q.appendleft(points[pointerAct-1])
            Q.appendleft(points[pointerAct])

        elif (leftSideTop and pointAct in leftSide) or (rightSideTop and pointAct in rightSide):
            H = deque()
            H.append(top)
            Q.popleft()
            while len(Q) > 0:
                v = Q.popleft()
                if ( leftSideTop and pointAct in leftSide
                        and checkLeftInside(polygon,points[pointerAct][1],top[1],v[1]) ) \
                        or ( rightSideTop and pointAct in rightSide
                        and checkRightInside(polygon,points[pointerAct][1],top[1],v[1]) ):

                    if not checkEdge(polygon,v[1],points[pointerAct][1]):
                        D.append((min(v[1],points[pointerAct][1]),max(v[1],points[pointerAct][1])))
                    top = v
                    H.popleft()
                    H.appendleft(top)
                else:
                    H.append(v)
            Q.append(points[pointerAct])
            Q.extend(H)

        pointerAct += 1
    return D