def taille(element):
    return len(element[1])


resultat = [["1", []], ["4", [1, 2, 3]], ["2", [1]], ["3", [1, 2]]]
print(sorted(resultat, key=lambda x: len(x[1]), reverse=False))


def np():
    neededInformations["np"] = widgets["input"][-1].text().split(",")
    print(neededInformations)
    clear_widgets()
    verbeFrame()


def verbe():
    neededInformations["verbe"] = widgets["input"][-1].text()
    print(neededInformations)
    clear_widgets()
    nomCFrame()


def nomC():
    neededInformations["nomC"] = widgets["input"][-1].text().split(",")
    print(neededInformations)
    clear_widgets()
    articleFrame()


def article():
    neededInformations["article"] = widgets["input"][-1].text().split(",")
    print(neededInformations)
    clear_widgets()
    graphFrame()