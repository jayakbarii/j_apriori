
from flask import Flask, render_template, url_for, request
from csv import reader
import os
import io

app = Flask(__name__)
def getFromCsvFile(fname):
    loopSets = []
    loopSet = set()

    s = io.StringIO(fname.stream.read().decode("UTF8"), newline=None)
    cRead = reader(s)
    for cell in cRead:
            cell = list(filter(None,cell))
            data = set(cell)
            for item in data:
                loopSet.add(frozenset([item]))
            loopSets.append(data)
    return(loopSet, loopSets)
        
    
def createCell1(dataSet):
    Cell1 = []
    for t in dataSet:
        for item in t:
            if not [item] in Cell1:
                Cell1.append([item])

    Cell1.sort()
    return list(map(frozenset, Cell1))

def aprioriGenerate(Ak, A):  # creates Ck
    retriveList = []
    lenAk = len(Ak)
    for i in range(lenAk):
        for j in range(i + 1, lenAk):
            L1 = list(Ak[i])[:A - 2]
            L2 = list(Ak[j])[:A - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  # if first k-2 elements are equal
                    retriveList.append(Ak[i] | Ak[j])  # set union
    return retriveList

def scanningD(D, Ck, minSupport):
    ssdCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssdCnt:
                    ssdCnt[can] = 1
                else:
                    ssdCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportRecord = {}
    for key in ssdCnt:
        support = ssdCnt[key] / numItems * 1000

        # support = ssdCnt[key]
        # print(support)

        if support >= minSupport:
            retList.insert(0, key)
        supportRecord[key] = support
    return (retList, supportRecord)

def aprioriFromCsvFile(fname, minSup):
    (Cell1ItemSet, recordSetList) = getFromCsvFile(fname)

    # print(recordSetList)

    (L1, supportData) = scanningD(recordSetList, Cell1ItemSet, minSup)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = aprioriGenerate(L[k - 2], k)
        (Lk, supK) = scanningD(recordSetList, Ck, minSup)  # scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return (L, supportData)
  



@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.files['myfile']
    f1, rules = aprioriFromCsvFile(output,20)
    for temp in f1:
        for i1 in f1[0]:
            for i2 in f1[1]:
                for i3 in f1[2]:
                    for i4 in f1[3]:
                        if i1.issubset(i2) \
                                or i1.issubset(i3) \
                                or i1.issubset(i4):
                            try:
                                f1[0].remove(i1)
                            except:
                                {}
                        if i2.issubset(i3) \
                                or i2.issubset(i4):
                            try:
                                f1[1].remove(i2)
                            except:
                                {}
                        if i3.issubset(i4):
                            try:
                                f1[2].remove(i3)
                            except:
                                {}

    return render_template('index.html', temp = f1)
    




if __name__ == "__main__":
    app.run(debug=True)