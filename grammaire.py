from classes import *
import pickle

articles = {"complexe": False, "quantifier": Node("forAll", "y", "", "-"), "left": Node("n", "cj", "y", "+"),
            "right": Node("np", "ci", "y", "-"), "connect": Node("imp", "y", "", "-")}

verbesIntransitifs = {"complexe": False, "quantifier": Node("forAll", "x0", "", "-"),
                      "left": Node("np", "x0", "ci", "+"),
                      "right": Node("s", "x0", "cj", "-"), "connect": Node("imp", "x0", "", "-")}
verbeTransitifsDroite = {"complexe": False, "quantifier": Node("forAll", "x1", "", "-"),
                         "left": Node("np", "x0", "ci", "+"),
                         "right": Node("s", "x0", "x1", "-"), "connect": Node("imp", "x1", "", "-")}
verbesTransitifs = {"complexe": True, "quantifier": Node("forAll", "x1", "", "-"), "left": Node("np", "cj", "x1", "+"),
                    "right": {"complexe": False, "quantifier": Node("forAll", "x0", "", "-"),
                              "left": Node("np", "x0", "ci", "+"),
                              "right": Node("s", "x0", "x1", "-"), "connect": Node("imp", "x0", "", "-")}
    , "connect": Node("imp", "x1", "", "-")}
adverbes = {"complexe": False, "quantifier": Node("forAll", "z", "", "-"), "left": Node("s", "z", "cj", "+"),
            "right": Node("s", "ci", "z", "-"), "connect": Node("imp", "z", "", "-")}

grammaire = {"articles": articles, "verbesIntransitifs": verbesIntransitifs, "verbesTransitifs": verbesTransitifs, "adverbe": adverbes}

with open('formulesGrammaire', 'wb') as f1:
    pickle.dump(grammaire, f1)
with open('formulesGrammaire', 'rb') as f1:
    OD = pickle.load(f1)

print(OD)

