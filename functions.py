import stanza
import copy
import pickle
import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
from classes import *
from jeux2Mots import *


# Grammar Formulas:

def getFormules():
    with open('formulesGrammaire', 'rb') as f1:
        formulesGrammaire = pickle.load(f1)
        return formulesGrammaire


# Data-Traitements' functions
def copySurface(formule):
    result = {"complexe": "", "quantifier": "",
              "left": "",
              "right": "", "connect": ""}
    result["complexe"] = formule["complexe"]
    result["quantifier"] = Node(formule["quantifier"].name, formule["quantifier"].start, formule["quantifier"].end,
                                formule["quantifier"].sign)
    result["connect"] = Node(formule["connect"].name, formule["connect"].start, formule["connect"].end,
                             formule["connect"].sign)
    if formule["complexe"]:
        result["left"] = Node(formule["left"].name, formule["left"].start, formule["left"].end,
                              formule["left"].sign)
        result["right"] = copySurface(formule["right"])
    else:
        result["complexe"] = formule["complexe"]
        result["left"] = Node(formule["left"].name, formule["left"].start, formule["left"].end,
                              formule["left"].sign)
        result["right"] = Node(formule["right"].name, formule["right"].start, formule["right"].end,
                               formule["right"].sign)

    return result


def getPOSStanza(phrase):
    nlp = stanza.Pipeline('fr')  # initialize French neural pipeline
    doc = nlp(phrase)  # run annotation over a sentence
    result = {"phrase": phrase, "np": [], "n": [], "verbe": [], "article": []}
    phrase = phrase.split(" ")
    pos = [f'word: {word.text}\tupos: {word.upos}' for sent in doc.sentences for word in sent.words]
    print(pos)
    for i in range(len(pos)):
        if "PROPN" in pos[i]:
            result["np"].append(phrase[i])
        elif "DET" in pos[i]:
            result["article"].append(phrase[i])
        elif "NOUN" in pos[i]:
            result["n"].append(phrase[i])
        elif "VERB" in pos[i]:
            result["verbe"].append(phrase[i])

    return result


# phrase = "Le petit chat mange"
# info = getPOS(phrase)


def getPositions(informations):
    print("ici commence getPosition")
    position = {}
    phrase = informations["phrase"].split(" ")
    for mot in phrase:
        position.update({mot: []})
    for i in range(len(phrase)):
        position[phrase[i]].append([i, i + 1])

    print(position)

    return position


# info = {"phrase": "Lambek killed Lambek but Lambek did not kill Lambek"}
# print(getPositions(info))


def getBasicNodes(informations, positions):
    # positions = getPositions(informations)
    nodes = []
    np = informations["np"]
    n = informations["n"]
    nodes.append(Node("s", 0, len(informations["phrase"].split(" ")), "+"))
    for key in positions.keys():
        if key in np:
            for position in positions[key]:
                nodes.append(Node("np", position[0], position[1], "-"))
        if key in n:
            for position in positions[key]:
                nodes.append(Node("n", position[0], position[1], "-"))
    return nodes


def getEdgesFromFormula(formule):
    if formule["complexe"]:
        grapheEdges = [[formule.get("quantifier"), formule.get("connect")],
                       [formule.get("connect"), formule.get("left")],
                       [formule.get("connect"), formule.get("right").get("quantifier")]] + getEdgesFromFormula(
            formule.get("right"))
    else:
        grapheEdges = [[formule.get("quantifier"), formule.get("connect")],
                       [formule.get("connect"), formule.get("left")],
                       [formule.get("connect"), formule.get("right")]]
    return grapheEdges


def replaceVar(var1, val1, var2, val2, formule):
    if formule["complexe"]:
        if formule["left"].start == var1:
            formule["left"].start = val1
        elif formule["left"].start == var2:
            formule["left"].start = val2
        if formule["left"].end == var1:
            formule["left"].end = val1
        elif formule["left"].end == var2:
            formule["left"].end = val2
        replaceVar(var1, val1, var2, val2, formule["right"])
    else:
        if formule["left"].start == var1:
            formule["left"].start = val1
        elif formule["left"].start == var2:
            formule["left"].start = val2
        if formule["left"].end == var1:
            formule["left"].end = val1
        elif formule["left"].end == var2:
            formule["left"].end = val2

        if formule["right"].start == var1:
            formule["right"].start = val1
        elif formule["right"].start == var2:
            formule["right"].start = val2
        if formule["right"].end == var1:
            formule["right"].end = val1
        elif formule["right"].end == var2:
            formule["right"].end = val2
    return formule


# print(replaceVar("ci", 1, "cj", 2, verbeTransitifs))
# edges = getEdgesFromFormula(verbeTransitifs)


def getEdgesFromData(informations):
    positions = getPositions(informations)
    basicNodes = getBasicNodes(informations, positions)
    edges = []
    formules = getFormules()
    for node in basicNodes:
        edges.append([node, None])
    for article in informations["article"]:
        for positionA in positions[article]:
            myArticle = copySurface(formules["articles"])
            replaceVar("ci", positionA[0], "cj", positionA[1], myArticle)
            edges = edges + getEdgesFromFormula(myArticle)
            # replaceVar(position[0], "ci", position[1], "cj", articles)
    for verbe in informations["verbe"]:
        for positionV in positions[verbe]:
            myVerb = copySurface(formules["verbesTransitifs"])
            replaceVar("ci", positionV[0], "cj", positionV[1], myVerb)
            edges = edges + getEdgesFromFormula(myVerb)
    for adverbe in informations["adverbe"]:
        for positionAdv in positions[adverbe]:
            myAdv = copySurface(formules["adverbe"])
            replaceVar("ci", positionAdv[0], "cj", positionAdv[1], myAdv)
            edges = edges + getEdgesFromFormula(myAdv)

    return edges


# Solvers' functions
def isMatch(node1, node2):
    if type(node1) == Node and type(node2) == Node and node1.name == node2.name and node1.sign != node2.sign:
        if node1.start == node2.start and node1.end == node2.end:
            return True
        elif node1.start == node2.start and node1.end != node2.end:
            if type(node1.end) == str or type(node2.end) == str:
                return True
        elif node1.end == node2.end and node1.start != node2.start:
            if type(node1.start) == str or type(node2.start) == str:
                return True
        elif type(node1.start) != str and type(node2.start) == str and type(node1.end) == str and type(
                node2.end) != str:
            return True
        elif type(node1.start) == str and type(node2.start) != str and type(node1.end) != str and type(
                node2.end) == str:
            return True
        elif type(node1.start) != str and type(node2.start) == str and type(node1.end) != str and type(
                node2.end) == str:
            return True
        elif type(node2.start) != str and type(node1.start) == str and type(node2.end) != str and type(
                node1.end) == str:
            return True
        elif type(node1.start) == str and type(node2.start) != str and type(node1.end) == str and type(node2.end) == str:
            return True
        elif type(node1.start) != str and type(node2.start) == str and type(node1.end) == str and type(node2.end) == str:
            return True


    else:
        return False


def isPerfectMatch(node1, node2):
    if node1.name == node2.name and node1.sign == node2.sign:
        if node1.start == node2.start and node1.end == node2.end:
            return True
    else:
        return False


def findUnification(node1, node2):
    result = []
    if type(node1.start) == str and type(node2.start) == str:
        result.append([node1.start, node2.start])
    if type(node1.end) == str and type(node2.end) == str:
        result.append([node1.end, node2.end])
    elif type(node1.start) == str and node1.end == node2.end:
        result.append([node1.start, node2.start])
    elif type(node2.start) == str and node2.end == node1.end:
        result.append([node2.start, node1.start])
    elif type(node1.end) == str and node1.start == node2.start:
        result.append([node1.end, node2.end])
    elif type(node1.start) != str and type(node2.start) == str:
        result.append([node2.start, node1.start])
        if type(node1.end) != str and type(node2.end) == str:
            result.append([node1.end, node2.end])
    print("this is findUni")
    print(result)
    return result


def findPossibleSolutionsIndex(node, edges):
    res = []
    for n in range(len(edges)):
        if (edges[n][1] == None):
            if (isMatch(node, edges[n][0])):
                # J'enregistre les indexes des solutions possibles
                edges[n][0].toString()
                res.append(n)
    return res


def findPossibleSolutions(node, nodes):
    res = []
    for n in nodes:
        if isMatch(node, n):
            res.append(n)
    return res


def findNodeByVariable(var, edges):
    res = []
    for e in range(len(edges)):
        if type(edges[e][0]) == Node:
            if (edges[e][0].start == var or edges[e][0].end == var):
                res.append((e, 0))
        if type(edges[e][1]) == Node:
            if (edges[e][1].start == var or edges[e][1].end == var):
                res.append((e, 1))
    return res


def remplaceVar(var, value, nodes):
    for n in nodes:
        if n.start == var:
            n.start = value
        if n.end == var:
            n.end = value
    return nodes


def getNodes(edges):
    res = []
    print("je commence getNodes")
    for e in edges:
        # print("["+e[0].toString() +", "+e[1].toString())
        if type(e[0]) == Node and e[0].name != "forAll" and e[0].name != "imp":
            print(e[0].toString())
            res.append(e[0])
        if type(e[1]) == Node and e[1].name != "forAll" and e[1].name != "imp":
            print(e[1].toString())
            res.append(e[1])
    print(res)
    return res
    # return list(set(res))


def getNodesSp(nodes):
    res = []
    print(printListNodes(nodes))
    for n in nodes:
        print(n.toString())
        print(printListNodes(findPossibleSolutions(n, nodes)))
        res.append([n, findPossibleSolutions(n, nodes)])
    return sorted(res, key=lambda x: len(x[1]), reverse=False)


def match(node, edges, nodes):
    SP = findPossibleSolutions(node, edges, nodes)
    if len(SP) == 0:
        return False
    else:
        return True


def afficher(edges):
    tmp = copy.copy(edges)
    for i in range(len(tmp)):
        if type(tmp[i][0]) == Node:
            tmp[i][0] = tmp[i][0].toString()
        if type(tmp[i][1]) == Node:
            tmp[i][1] = tmp[i][1].toString()
    return tmp


def formePrenexe(formule):
    if not formule.get("complexe"):
        return (formule.get("quantifier").toString(),
                (formule.get("connect"), (formule.get("left").toString(), None),
                 (formule.get("right").toString(), None)))
    else:
        return (formule.get("quantifier").toString(),
                (formule.get("connect"), (formePrenexe(formule.get("left")), None),
                 (formePrenexe(formule.get("right")), None)))


def getNodesByUni(uni, nodes):
    res = []
    print("Ici commencegetNodeByUni  uni : ")
    print(uni)

    for u in uni:
        for n in nodes:
            if n.start == u[0] or n.end == u[0]:
                res.append(n)
    return res


def unifier(uni, nodes):
    uniNodes = getNodesByUni(uni, nodes)
    for u in uni:
        print("Unify ")
        print(u)
        for n in uniNodes:
            print(n.start)
            if n.start == u[0]:
                n.start = u[1]
            if n.end == u[0]:
                n.end = u[1]
                print(n.end)


def undo(uni, backup):
    uniNodes = getNodesByUni(uni, backup)
    for u in uni:
        for n in uniNodes:
            if n.start == u[1]:
                n.start = u[0]
            if n.end == u[1]:
                n.end = u[0]



def getVoisins(node, edges):
    res = []
    for e in edges:
        if e[0] == node:
            res.append(e[1])
        if e[1] == node:
            res.append(e[0])
    return res


def hasCycle(edges, edge):
    liste1 = getVoisins(edge[0], edges)
    liste2 = getVoisins(edge[1], edges)
    set1 = set(liste1)
    set2 = set(liste2)
    if len(set1.intersection(set2)) > 0:
        return True
    else:
        return False


def solve(nodes, edges):
    if len(nodes) == 0:
        return True
    print("Ici commence Solve")
    nodesSP = getNodesSp(nodes)
    n = nodesSP[0]
    print(n)
    print("mon node " + n[0].toString())
    if len(n[1]) == 0:
        return False
    else:
        for i in n[1]:
            print("Sp " + i.toString())
            if isPerfectMatch(n[0], i):
                edges.append(n[0], i)
                nodes.remove(n[0])
                solve(nodes, edges)
            else:
                uni = findUnification(n[0], i)
                # remplaceVar(uni, nodes[i[0]], nodes)
                buckup = getNodesByUni(uni, nodes)
                unifier(uni, nodes)
                nodes.remove(n[0])
                nodes.remove(i)
                if solve(nodes, edges):
                    edges.append([n[0], i])
                    return True
                else:
                    undo(uni, buckup)
        return False


def printListNodes(nodes):
    res = []
    for node in nodes:
        res.append(node.toString())
    return res


def grapheAdapter(edges):
    grapheEdge = []
    grapheNode = []
    for edge in edges:
        e0 = edge[0]
        e1 = edge[1]
        if e1 is None:
            if type(e0) == Node:
                e0 = e0.toString()
            grapheNode.append(e0)
        else:
            if type(e0) == Node:
                e0 = e0.toString()
            if type(e1) == Node:
                e1 = e1.toString()
            grapheEdge.append((e0, e1))

    return [grapheEdge, grapheNode]


def UseGraphVisualizer(edges, fileName):
    graphe = grapheAdapter(edges)
    G2 = nx.DiGraph()
    G2.add_edges_from(graphe[0])
    G2.add_nodes_from(graphe[1])
    pos = nx.spring_layout(G2)
    nx.draw_networkx_nodes(G2, pos, node_size=700)
    nx.draw_networkx_edges(G2, pos, edgelist=G2.edges, edge_color="black", width=1)
    nx.draw_networkx_labels(G2, pos)
    plt.savefig(fileName)
    plt.show()


def testGraphe(edges):
    graphe = grapheAdapter(edges)
    G2 = nx.DiGraph()
    G2.add_edges_from(graphe[0])
    G2.add_nodes_from(graphe[1])
    pos = nx.spring_layout(G2)
    nx.draw_networkx_nodes(G2, pos, node_size=700)
    nx.draw_networkx_edges(G2, pos, edgelist=G2.edges, edge_color="black", width=1)
    nx.draw_networkx_labels(G2, pos)
    nx.draw(G2, pos=graphviz_layout(G2), node_size=1200, node_color='lightblue', linewidths=0.25, font_size=10,
            font_weight='bold', with_labels=True)
    plt.show()  # plt.savefig("graph.png")



def cycle(test_list, val, stop=None):
    temp = dict(test_list)
    stop = stop if stop is not None else val
    while True:
        yield (val.toString())
        val = temp.get(val, stop)
        if val == stop: break


phrase = "Le chat mange Lambek hier"
info = getPOS(phrase)
print(info)
# edges = getEdgesFromFormula(verbeTransitifs)
# print(edges)
# nodes = getNodes(edges)
# print(afficher(edges))
grapheEdges = getEdgesFromData(info)
# print(afficher(grapheEdges))
nodes = getNodes(grapheEdges)
UseGraphVisualizer(grapheEdges, "test.png")
print(solve(nodes, grapheEdges))
UseGraphVisualizer(grapheEdges, "testSolve.png")
