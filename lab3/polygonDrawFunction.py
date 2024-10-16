
def triangulation_draw(polygon):
    """
    Funkcja dokonuje triangulacji wielokąta monotonicznego -> wzdluz osi OY, oraz pokazuje kolejne krotki.
    :param polygon: tablica krotek punktów na płaszczyźnie euklidesowej podanych przeciwnie do ruchu wskazówek zegara - nasz wielokąt
    :return: tablica krotek dodawanych po kolei przekątnych np: [(1,5),(2,3)], oznacza, że triangulacja polega na dodaniu przekątnej pomiędzy wierzchołki 1-5 i 2-3
    """

    visTriangulation = Visualizer()
    visTriangulation.add_title('Triangulation algorithm')
    visTriangulation.add_grid()
    visTriangulation.add_polygon(polygon, fill=False)
    visTriangulation.add_point(polygon, color = "green") #kolor wierzcholkow ktore w ogole nic nie robia

    E = [] #zapis krawedzi
    K = deque() #tymczasowy zapis krawedzi - potrzebene aby efektywnie zwizualizowac ich usuniecie

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

    visTriangulation.add_point(points[0][0], color = "blue") #wierzcholki na stosie
    visTriangulation.add_point(points[1][0], color = "blue")


    while len(Q) > 0 and pointerAct < n:
        top = Q[0] #sprawdzam szczyt stosu
        leftSideTop = top[0] in leftSide
        rightSideTop = top[0] in rightSide
        pointAct = points[pointerAct][0]

        visTriangulation.add_point(pointAct, color = "tomato") #aktualnie rozpatrywany wierzcholek

        if (leftSideTop and pointAct in rightSide) or (rightSideTop and pointAct in leftSide):
            while len(Q) > 1: #nie wyciagamy ostatniego wierzolka
                v = Q.popleft()
                visTriangulation.add_point(v[0], color = "orange")
                edge = visTriangulation.add_line_segment((v[0],pointAct), color = "red")
                E.append(edge)
                K.append(edge)
                if not checkEdge(polygon,v[1],points[pointerAct][1]):
                    D.append((min(v[1],points[pointerAct][1]),max(v[1],points[pointerAct][1])))

                else: visTriangulation.remove_figure(K.pop()) #usuwamy krawedz, jesli sie nie udalo

                visTriangulation.add_point(v[0], color = "paleturquoise")

            Q.popleft() #teraz stos po tej operacji musi byc pusty
            Q.appendleft(points[pointerAct-1])
            Q.appendleft(points[pointerAct])

            visTriangulation.add_point(points[pointerAct-1][0], color = "blue")
            visTriangulation.add_point(points[pointerAct][0], color = "blue")

        elif (leftSideTop and pointAct in leftSide) or (rightSideTop and pointAct in rightSide):
            H = deque()
            H.append(top)
            Q.popleft()
            while len(Q) > 0:
                v = Q.popleft()
                visTriangulation.add_point(v[0], color = "orange")
                edge = visTriangulation.add_line_segment((v[0],pointAct), color = "red")
                E.append(edge)
                K.append(edge)
                if ( leftSideTop and pointAct in leftSide
                        and checkLeftInside(polygon,points[pointerAct][1],top[1],v[1]) ) \
                        or ( rightSideTop and pointAct in rightSide
                        and checkRightInside(polygon,points[pointerAct][1],top[1],v[1]) ):

                    if not checkEdge(polygon,v[1],points[pointerAct][1]):
                        D.append((min(v[1],points[pointerAct][1]),max(v[1],points[pointerAct][1])))
                    else: visTriangulation.remove_figure(K.pop()) #usuwamy krawedz, jesli sie nie udalo

                    visTriangulation.add_point(top[0], color = "paleturquoise")
                    top = v
                    visTriangulation.add_point(top[0], color = "blue")
                    H.popleft()
                    H.appendleft(top)
                else:
                    visTriangulation.remove_figure(K.pop())
                    visTriangulation.add_point(top[0], color = "blue")
                    H.append(v)
                Q.append(points[pointerAct])
                Q.extend(H)

        pointerAct += 1
    return D, visTriangulation