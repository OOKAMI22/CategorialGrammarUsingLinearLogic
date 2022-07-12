import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from bs4 import BeautifulSoup as bs
import requests
import json

# L = {"Lambek": "np", "dort": "ver:In", "chat": "n"}
# fileJSON = open("Grammaraire.json", "w", encoding="utf-8")
# json.dump(L, fileJSON, indent=4)
# fileJSON.close()



def getHtml(mot, entrant, rel):
    print("getHtml:: begins")
    with requests.Session() as s:
        print("getHtml:: connected to JDM")
        url = 'http://www.jeuxdemots.org/rezo-dump.php?'
        if entrant:
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot, 'rel': rel, 'relin': 'norelout'}
        else:
            payload = {'gotermsubmit': 'Chercher', 'gotermrel': mot, 'rel': rel, 'relout': 'norelin'}

        r = s.get(url, params=payload)
        soup = bs(r.text, 'html.parser')
        prod = soup.find_all('code')
        # print("prod : "+str(type(prod)))
        while ("MUTED_PLEASE_RESEND" in str(prod)):
            print("ERREUR")
            r = s.get(url, params=payload)
            soup = bs(r.text, 'html.parser')
            prod = soup.find_all('code')

        print("getHtml:: ends")

    return prod


def mySplit(expression):
    resultat = []
    tmp = ""
    cond = False
    for i in range(len(expression)):
        if i + 1 == len(expression):
            tmp += expression[i]
            resultat.append(tmp)
        else:
            if expression[i] == "\'" and expression[i + 1] != ";":
                cond = True
            elif expression[i] == "\'" and expression[i + 1] == ";":
                cond = False
            if cond == True:
                tmp += expression[i]
            if cond == False and expression[i] != ";":
                tmp += expression[i]
            elif cond == False and expression[i] == ";":
                resultat.append(tmp)
                tmp = ""

    return resultat


def parseData(html):
    fields_nt = ['ntname']
    fields_e = ["name", "type", "w", "formated name"]
    fields_rt = ['trname', 'trgpname', 'rthelp']
    fields_r = ["node1", "node2", "type", "w"]

    # fields_type = ["e", "nt", "rt", "r"]

    dict0 = {}
    dict_e = {}
    dict_rt = {}
    dict_r = {}
    dict_nt = {}

    lines = html.splitlines()

    for i in range(len(lines)):
        description = list(mySplit(lines[i]))
        # print(description)
        if (len(description) > 0):
            if description[0] == "nt":
                dict2 = {}
                id = description[1]
                for i in range(1):
                    dict2[fields_nt[i]] = description[i + 2]

                dict_nt[id] = dict2


            elif description[0] == "e":
                dict2 = {}
                id = description[1]
                for i in range(3):
                    dict2[fields_e[i]] = description[i + 2]

                if len(description) > 5:
                    dict2[fields_e[3]] = description[5]

                dict_e[id] = dict2


            elif description[0] == "rt":
                dict2 = {}
                id = description[1]
                for i in range(2):
                    dict2[fields_rt[i]] = description[i + 2]

                if len(description) > 4:
                    dict2[fields_rt[2]] = description[4]

                dict_rt[id] = dict2

            elif (description[0] == "r"):
                dict2 = {}
                id = description[1]
                for i in range(4):
                    dict2[fields_r[i]] = description[i + 2]
                dict_r[id] = dict2

    dict0["nt"] = dict_nt
    dict0["e"] = dict_e
    dict0["r"] = dict_r
    dict0["rt"] = dict_rt
    return dict0


def updateGrammar(mot, fileName):
    with open("Grammaraire.json", 'r') as f1:
        Grammar = json.load(f1)
    if mot not in Grammar.keys():
        data = parseData(str(getHtml(mot, True, 4)))
        e = data["e"]
        r = sorted(data["r"].items(), key=lambda t: t[1]["w"], reverse=True)
        best = r[0][1]["node2"]
        bestName = e[best]["name"]
        pos = ""
        if "Det" in bestName or "Pro" in bestName:
            pos = "article"
        elif "Ver" in bestName:
            pos = "Ver"
        elif "Nom" in bestName:
            pos = "n"
            data = parseData(str(getHtml(mot, True, 18)))
            e = data["e"]
            r = sorted(data["r"].items(), key=lambda t: t[1]["w"], reverse=True)
            best = r[0][1]["node2"]
            bestName = e[best]["name"]
            if "Propre" in bestName:
                pos = "np"
        elif "Adv" in bestName:
            pos = "Adv"

        print(pos)

        html = str(getHtml(mot, True, "4"))
        mySplit(html)
        print(Grammar.update({mot: pos}))

        fileJSON = open(fileName, "w", encoding="utf-8")
        json.dump(Grammar, fileJSON, indent=4)
        fileJSON.close()
        return Grammar
    else:
        return Grammar


def getPOS(phrase):
    fileName = "Grammaraire.json"
    result = {"phrase": phrase, "np": [], "n": [], "verbe": [], "article": [], "adverbe": []}
    phrase = phrase.split(" ")
    for mot in phrase:
        grammar = updateGrammar(mot, fileName)
    # print(grammar)
    for i in range(len(phrase)):
        if grammar[phrase[i]] == "np":
            result["np"].append(phrase[i])
        elif grammar[phrase[i]] == "article":
            result["article"].append(phrase[i])
        elif grammar[phrase[i]] == "n":
            if grammar[phrase[i - 1]] == "article":
                result["n"].append(phrase[i])
            else:
                result["verbe"].append(phrase[i])
        elif "Ver" in grammar[phrase[i]]:
            result["verbe"].append(phrase[i])
        elif "Adv" in grammar[phrase[i]]:
            result["adverbe"].append(phrase[i])

    print(result)
    return result


#print(getPOS("Lambek dort"))

mot = "dors"
data = parseData(str(getHtml(mot, True, 4)))
print(data)
d = data["r"]
d = sorted(d.items(), key=lambda t: t[1]["w"], reverse=True)
print(d)
best = d[0][1]["node2"]
print(best)
dataE = data["e"]
fileName = "Grammaraire.json"
print(updateGrammar(mot, fileName))
