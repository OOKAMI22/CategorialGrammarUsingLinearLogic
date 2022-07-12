import matplotlib as plt

import json
exemple = ('eqv',
('and', ('imp', ('var', 'x'), ('var', 'y')),
('imp', ('var', 'y'), ('var', 'z'))
),
('imp', ('var', 'x'), ('var', 'z')))


def left(f): return f[1]
def right(f): return f[2]
symbol = {'not': '-', 'and': '.', 'or': '+', 'imp': '->', 'eqv': '<->'}
prio = {'var': 15, 'not': 10, 'and': 8, 'or': 6, 'imp': 4, 'eqv': 2}
def paren(s, f1, f):
    if prio[f1[0]] <= prio[f[0]]: return '(' + s + ')'
    else: return s


def to_string(f):
    if f[0] == 'var':
        return f[1]
    elif f[0] == 'not':
        f1 = left(f)

        s1 = to_string(f1)
        return '-' + paren(s1, f1, f)
    else:
        smb = symbol[f[0]]
        f1 = left(f)
        f2 = right(f)
        s1 = to_string(f1)
        s2 = to_string(f2)
        return paren(s1, f1, f) + smb + paren(s2, f2, f)


def draw_aux(f, rect, dy):
    x1, x2, y1, y2 = rect
    xm = (x1 + x2) // 2
    if f[0] == 'var':
        noeud = f[1]
    else:
        noeud = symbol[f[0]]
        plt.text(xm + 3, y2, noeud, fontsize=12, horizontalalignment='left')
    if f[0] == 'var': return
    if f[0] == 'not':
        draw_aux(left(f), (x1, x2, y1, y2 - dy), dy)
        a, b = ((xm, xm), (y2, y2 - dy))
        plt.plot(a, b, 'k', marker='o')
    else :
        draw_aux(left(f), (x1, xm, y1, y2 - dy), dy)
        draw_aux(right(f), (xm, x2, y1, y2 - dy), dy)
        a, b = ((xm, (x1 + xm) // 2), (y2, y2 - dy))
        plt.plot(a, b, 'k', marker='o')
        c, d = ((xm, (x2 + xm) // 2), (y2, y2 - dy))
        plt.plot(c, d, 'k', marker='o')

def hauteur(f):
    if f[0] == 'var': return 0
    elif f[0] == 'not' : return 1 + hauteur(left(f))
    else:
        h1 = hauteur(left(f))
        h2 = hauteur(right(f))
        return 1 + max([h1, h2])
def draw(f):
    d = 512
    pad = 20
    dy = (d - 2 * pad) / (hauteur(f))
    draw_aux(f, (pad, d - pad, pad, d - pad), dy)
    plt.axis([0, d, 0, d])
    plt.axis('off')
    plt.show()

plt.rcParams['figure.figsize'] = (12, 8)
draw(exemple)

print(to_string(exemple))
























def sansTriangle(n,matAdj):
    for i in range(n):
        voisins = []
        for j in range(n):
            if matAdj[i][j] == 1 :
                voisins.append(j)

        for v in voisins:
            for commun in range(n):
                if matAdj[v][commun] == 1 and commun in voisins:
                    return False
    return True




def sansTrianglrBis(n,m,listeArrete,MatAdj):
    for j in range(m):
        x = listeArrete[j][0]
        y = listeArrete[j][1]
        # une arrete xy
        #je vais chercher un z tq yz zx
        for z in range(n):
            zx = MatAdj[z][x]
            yz = MatAdj[y][z]
            if zx == 1  and  yz == 1:
                return False
    return True

def sansTriangle3(M):
    for i in range(len(M)):
        for j in range(len(M)):
            if M[i][j] == 1:
                for k in range(len(M)):
                    if M[j][k] == 1 and M[i][k] == 1:
                        return False


verbe = {"complexe" : False, "quantifier": Node("forAll", "x0", "_", "-"), "left": Node("np", "x0", 1, "+"),
         "right": Node("s", "x0", 2, "-"), "connect": "--o -"}


