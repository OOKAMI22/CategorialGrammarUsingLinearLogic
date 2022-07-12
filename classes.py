class Node:

    def __init__(self, name, start, end, sign):
        self.name = name
        self.start = start
        self.end = end
        self.sign = sign

    # implement toString methode
    def toString(self):
        if self.name == "forAll":
            res = "∀" + str(self.start) + self.sign
        elif self.name == "imp":
            res = "--o" + str(self.start) + self.sign
        else:
            res = self.name + "(" + str(self.start) + "," + str(self.end) + ")" + self.sign
        return res

    def negation(self):
        if (self.sign == "+"):
            self.sign = "-"
        else:
            self.sign = "+"


class Formula:
    def __init__(self):
        self.left = Node("", "", "", "")
        self.right = Node("", "", "", "")
        self.connect = "--o"
        self.quantifier = Node("", "", "", "")
        self.complexe = False

    def makeArticle(self, n, ci, cj):
        self.quantifier = Node("forAll", "x" + n, "", "-")
        self.left = Node("n", cj, "x" + n, "+")
        self.right = Node("np", ci, "x" + n, "-")
        self.connect = "--o -"
        self.complexe = False

    def makeIntransVerb(self, n, ci, cj):
        self.quantifier = Node("forAll", "x" + n, "", "-")
        self.left = Node("np", "x" + n, ci, "+")
        self.right = Node("s", "x" + n, cj, "-")
        self.connect = "--o -"
        self.complexe = False


class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def getTuple(self):
        return (self.node1.toString(), self.node2.toString())


class Formule:
    def __init__(self, left, right, connect, quantifier):
        self.left = left
        self.right = right
        self.connect = connect
        self.quantifier = quantifier
        self.graphe = []

    def toString(self):
        res = self.quantifier.toString() + " " + " " + self.left.toString() + self.connect + " " + self.right.toString()
        return res

    def makeNodes(self):
        if self.connect == "--o":
            edge = Edge(self.left.negation(), self.right)
        self.graphe.append(edge)
        return self.graphe

    def makeNodesPrint(self):
        if self.connect == "--o":
            edge = Edge(self.left.negation(), self.right)
            tuple = (self.left.negation().name, self.right.name)
        self.graphe.append(tuple)
        return self.graphe
