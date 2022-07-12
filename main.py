import sys
from functions import *
from jeux2Mots import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QPushButton, QLineEdit


widgets = {"logo": [],
           "button": [],
           "question": [],
           "answer1": [],
           "input": [],
           "answer3": []}
neededInformations = {"phrase": "", "np": [], "verbe": "", "transitive": False, "article": [], "nomC": [],"pos":[]}
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Stage LIRMM version beta")
window.setFixedWidth(1000)
window.move(2700, 200)
window.setStyleSheet("background: #161219;")

grid = QGridLayout()


def clear_widgets():
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()


def start():
    clear_widgets()
    phraseFrame()


def phrase():

    neededInformations["phrase"] = widgets["input"][-1].text()
    print(neededInformations)
    clear_widgets()
    info = getPOS(neededInformations["phrase"])
    neededInformations["phrase"] = info
    grapheEdges = getEdgesFromData(info)
    UseGraphVisualizer(grapheEdges, "avant.png")
    print(neededInformations)
    graphFrame()



def afficher():
    clear_widgets()
    grapheEdges = []
    nodes = []
    acceuilFrame()


def unify():
    clear_widgets()
    grapheEdges = getEdgesFromData(neededInformations["phrase"])
    nodes = getNodes(grapheEdges)
    solve(nodes, grapheEdges)
    UseGraphVisualizer(grapheEdges, "apres.png")
    unifiedGraphFrame()


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

def create_buttons(name):
    button = QPushButton(name)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet("*{border: 4px solid '#BC006C';" +
                         "border-radius: 25px;" +
                         "font-family:'shanti';" +
                         "font-size: 35px;" +
                         "color: 'white';" +
                         "padding: 25px 0;" +
                         "margin-top: 30px;}" +
                         "*:hover{background: '#BC006C';}")

    return button


def acceuilFrame():
    # Afficher le logo
    image = QPixmap("lirmm.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)

    # Button widget
    button = QPushButton("Let's start")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet("*{border: 4px solid '#BC006C';" +
                         "border-radius: 45px;" +
                         "font-size: 35px;" +
                         "color: 'white';" +
                         "padding: 25px 0;" +
                         "margin: 100px 200px;}" +
                         "*:hover{background: '#BC006C';}")
    button.clicked.connect(start)
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


def phraseFrame():
    question = QLabel("Entrez votre phrase")
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet("font-family: Shanti;"
                           "font-size: 25px;" +
                           "color: 'white';" +
                           "padding: 75px;")
    widgets["question"].append(question)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)

    sentence = QLineEdit()
    sentence.setStyleSheet("border: 4px solid '#BC006C';" +
                           "border-radius: 45px;" +
                           "font-family: Shanti;" +
                           "color: 'white';" +
                           "padding: 25px;")
    sentence.move(80, 20)
    sentence.resize(200, 32)
    sentence.setAlignment(QtCore.Qt.AlignCenter)
    widgets["input"].append(sentence)
    grid.addWidget(widgets["input"][-1], 2, 0, 2, 0)

    button = create_buttons("Next")
    button.clicked.connect(phrase)
    widgets["answer1"].append(button)
    grid.addWidget(widgets["answer1"][-1], 3, 1)


def npFrame():
    question1 = QLabel("Entrez les noms propres de votre phrase (eg: Lambek,Godel)")
    question1.setAlignment(QtCore.Qt.AlignCenter)
    question1.setWordWrap(True)
    question1.setStyleSheet("font-family: Shanti;"
                            "font-size: 25px;" +
                            "color: 'white';" +
                            "padding: 75px;")
    widgets["question"].append(question1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 0)

    s = QLineEdit()
    s.setStyleSheet("border: 4px solid '#BC006C';" +
                    "border-radius: 45px;" +
                    "font-family: Shanti;"
                    "color: 'white';" +
                    "padding: 25px;")
    s.move(80, 20)
    s.resize(200, 32)
    s.setAlignment(QtCore.Qt.AlignCenter)
    widgets["input"].append(s)
    grid.addWidget(widgets["input"][-1], 2, 0, 1, 2)
    print(widgets["input"][-1].text())

    button = create_buttons("Next")
    button.clicked.connect(np)
    widgets["answer1"].append(button)
    grid.addWidget(widgets["answer1"][-1], 3, 1)


def verbeFrame():
    question1 = QLabel("Entrez le verbe de votre phrase ")
    question1.setAlignment(QtCore.Qt.AlignCenter)
    question1.setWordWrap(True)
    question1.setStyleSheet("font-family: Shanti;"
                            "font-size: 25px;" +
                            "color: 'white';" +
                            "padding: 75px;")
    widgets["question"].append(question1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 0)

    input = QLineEdit()
    input.setStyleSheet("border: 4px solid '#BC006C';" +
                        "border-radius: 45px;" +
                        "font-family: Shanti;"
                        "color: 'white';" +
                        "padding: 25px;")
    input.move(80, 20)
    input.resize(200, 32)
    input.setAlignment(QtCore.Qt.AlignCenter)
    widgets["input"].append(input)
    grid.addWidget(widgets["input"][-1], 2, 0, 1, 2)

    button = create_buttons("Next")
    button.clicked.connect(verbe)
    widgets["answer1"].append(button)
    grid.addWidget(widgets["answer1"][-1], 3, 1)


def nomCFrame():
    question1 = QLabel("Entrez les noms communs de votre phrase (eg: étudiant,école) ")
    question1.setAlignment(QtCore.Qt.AlignCenter)
    question1.setWordWrap(True)
    question1.setStyleSheet("font-family: Shanti;"
                            "font-size: 25px;" +
                            "color: 'white';" +
                            "padding: 75px;")
    widgets["question"].append(question1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 0)

    input = QLineEdit()
    input.setStyleSheet("border: 4px solid '#BC006C';" +
                        "border-radius: 45px;" +
                        "font-family: Shanti;"
                        "color: 'white';" +
                        "padding: 25px;")
    input.move(80, 20)
    input.resize(200, 32)
    input.setAlignment(QtCore.Qt.AlignCenter)
    widgets["input"].append(input)
    grid.addWidget(widgets["input"][-1], 2, 0, 1, 2)

    button = create_buttons("Next")
    button.clicked.connect(nomC)
    widgets["answer1"].append(button)
    grid.addWidget(widgets["answer1"][-1], 3, 1)


def articleFrame():
    question1 = QLabel("Entrez les articles de votre phrase (eg: le,la) ")
    question1.setAlignment(QtCore.Qt.AlignCenter)
    question1.setWordWrap(True)
    question1.setStyleSheet("font-family: Shanti;"
                            "font-size: 25px;" +
                            "color: 'white';" +
                            "padding: 75px;")
    widgets["question"].append(question1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 0)

    input = QLineEdit()
    input.setStyleSheet("border: 4px solid '#BC006C';" +
                        "border-radius: 45px;" +
                        "font-family: Shanti;"
                        "color: 'white';" +
                        "padding: 25px;")
    input.move(80, 20)
    input.resize(200, 32)
    input.setAlignment(QtCore.Qt.AlignCenter)
    widgets["input"].append(input)
    grid.addWidget(widgets["input"][-1], 2, 0, 1, 2)

    button = create_buttons("Next")
    button.clicked.connect(article)
    widgets["answer1"].append(button)
    grid.addWidget(widgets["answer1"][-1], 3, 1)


def graphFrame():
    # Afficher le graphe des formules avant unification
    image = QPixmap("avant.png")
    avant = QLabel()
    avant.setPixmap(image)
    avant.setAlignment(QtCore.Qt.AlignCenter)
    avant.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(avant)

    # Button widget
    button = QPushButton("Unify")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet("*{border: 4px solid '#BC006C';" +
                         "border-radius: 45px;" +
                         "font-size: 35px;" +
                         "color: 'white';" +
                         "padding: 25px 0;" +
                         "margin: 100px 200px;}" +
                         "*:hover{background: '#BC006C';}")
    button.clicked.connect(unify)
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


def unifiedGraphFrame():
    # Afficher le graphe des formules avant unification
    image = QPixmap("apres.png")
    avant = QLabel()
    avant.setPixmap(image)
    avant.setAlignment(QtCore.Qt.AlignCenter)
    avant.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(avant)

    # Button widget
    button = QPushButton("Retry")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet("*{border: 4px solid '#BC006C';" +
                         "border-radius: 45px;" +
                         "font-size: 35px;" +
                         "color: 'white';" +
                         "padding: 25px 0;" +
                         "margin: 100px 200px;}" +
                         "*:hover{background: '#BC006C';}")
    button.clicked.connect(start)
    widgets["button"].append(button)

    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


acceuilFrame()

window.setLayout(grid)

window.show()

sys.exit(app.exec())
