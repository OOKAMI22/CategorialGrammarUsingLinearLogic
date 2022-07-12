from classes import *
from functions import *
import networkx as nx
import matplotlib.pyplot as plt
print("Entrez votre phrase \n")
phrase = input()
phrase = phrase.split(" ")
print(phrase)

sujet = input("Sélectionnez le sujet de votre phrase ")

verbe = input("Sélectionnez le verbe de votre phrase ")

transitif = input("votre verbe est il transitif (oui ou non) ?")

article = input(" Votre phrase contient-elle un article (oui ou non) ")

if article == "oui":
    article = input("Entrez l'article de votre phrase")



position = {}
for i in range(len(phrase)):
    print(i)
    position.update({phrase[i]: [i, i + 1]})

print(position)
sPos = Node("s", 0, len(phrase), "+")
print(sPos.toString())
# Ici on mettra un nom Propre pour les noms on verra avec la grammaire
npNeg = Node("np", position[sujet][0], position[sujet][1], "-")

print(npNeg.toString())

verbe = {"complexe" : False, "quantifier": Node("forAll", "x0", "_", "-"), "left": Node("np", "x0", position[verbe][0], "+"),
         "right": Node("s", "x0", position[verbe][1], "-"), "connect": "--o -"}
grapheNodes = [sPos, npNeg, verbe.get("left"), verbe.get("right")]
grapheEdges = [[verbe.get("quantifier"), verbe.get("connect")], [verbe.get("connect"), verbe.get("left")],
               [verbe.get("connect"), verbe.get("right")], [sPos, None], [npNeg, None]]
verbeArbre = formePrenexe(verbe)

#print(verbeArbre)
#print(type(verbe.get("left"))==Node)
#nodesbyx0 = findNodeByVariable("x0", grapheEdges)
#print(nodesbyx0)
#print(afficher(remplaceVar("x0", "1", nodesbyx0, grapheEdges)))
#print(grapheEdges)
#print(findPossibleSolutions(Node("s", "x0", 2, "-"), grapheEdges))
#print(findPossibleSolutions(Node("np", "x0", 1, "+"), grapheEdges))
#print(isMatch(Node("np", "x0", 1, "+"), npNeg))
#print(findUnification(Node("np", "x0", 1, "+"), npNeg))
#print(isMatch(Node("s", "x0", 2, "-"), sPos))

#print(findUnification(Node("s", "x0", 2, "-"), sPos))
nodes = getNodes(grapheEdges)
#remplaceVar("x0", 0, nodes)
#print(nodes[0].toString())
#uni = findUnification(Node("np", "x0", 1, "+"), npNeg)
#print(uni)
#unifier(uni, nodes)
UseGraphVisualizer(grapheEdges,"avant.png")
print(solve(nodes, grapheEdges))
UseGraphVisualizer(grapheEdges,"apres.png")
#print(afficher(grapheEdges))
print(hasCycle(grapheEdges,grapheEdges[2]))
#testGraphe(grapheEdges)

#nodesSP = getNodesSp(nodes, grapheEdges)
#print(nodes)
#print(nodesSP)
def getEdgesFromFormula(formule):
    if formule["complexe"]:
        # TODO
        grapheEdges = getEdgesFromFormula(formule.get("left")).append(getEdgesFromFormula(formule.get("right")))
        if not formule.get("right").get("complexe"):
            grapheEdges.append([formule.get("connect"), formule.get("right").get("quantifier")])
    else:
        grapheEdges = [[formule.get("quantifier"), formule.get("connect")],
                       [formule.get("connect"), formule.get("left")],
                       [formule.get("connect"), formule.get("right")]]
    return grapheEdges







