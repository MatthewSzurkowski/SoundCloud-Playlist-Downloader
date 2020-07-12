import os
def getFiles(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))        
    newFiles = []
    for f in files:
        brokenUpF = f.split("/")
        f = brokenUpF[len(brokenUpF)-1]
        newFiles.append(f)
    return newFiles

def notMatches(a, b):
    a = set(a)
    b = set(b)
    return list(b - a)

def checkDict(myDict):
    checkFiles = []
    for x in myDict.keys():
        checkFiles.append(x[:-4])
    return checkFiles

def printDuds(newList):
    print(newList)

