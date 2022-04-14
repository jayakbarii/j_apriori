
from flask import Flask, render_template, url_for, request
from csv import reader
import io

app = Flask(__name__)
def getData(fname):

    temp1 = []
    temp2 = set()

    s = io.StringIO(fname.stream.read().decode("UTF8"), newline=None)
    cRead = reader(s)
    for cell in cRead:
            cell = list(filter(None,cell))
            data = set(cell)
            for item in data:
                temp2.add(frozenset([item]))
            temp1.append(data)
    return(temp2, temp1)
        
    
def createCell1(dataSet):
    Cell1 = []
    for t in dataSet:
        for item in t:
            if not [item] in Cell1:
                Cell1.append([item])

    Cell1.sort()
    return list(map(frozenset, Cell1))

def generate(Ak, A):  # creates Ck
    tList = []
    lk = len(Ak)
    for i in range(lk):
        for j in range(i + 1, lk):
            L1 = list(Ak[i])[:A - 2]
            L2 = list(Ak[j])[:A - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  # if first k-2 elements are equal
                    tList.append(Ak[i] | Ak[j])  # set union
    return tList

def sD1(D, Ck, supp):
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
    sR = {}
    for key in ssdCnt:
        support = ssdCnt[key] / numItems * 1000

        # support = ssdCnt[key]
        # print(support)

        if support >= supp:
            retList.insert(0, key)
        sR[key] = support
    return (retList, sR)

def readFile(fname, minSup):
    (temp1, tempList) = getData(fname)

    # print(recordSetList)

    (L1, sD) = sD1(tempList, temp1, minSup)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = generate(L[k - 2], k)
        (Lk, supK) = sD1(tempList, Ck, minSup)  # scan DB to get Lk
        sD.update(supK)
        L.append(Lk)
        k += 1
    return (L, sD)

def sorted(list1):
    for temp in list1:
        for i1 in list1[0]:
            for i2 in list1[1]:
                for i3 in list1[2]:
                    for i4 in list1[3]:
                        if i1.issubset(i2) \
                                or i1.issubset(i3) \
                                or i1.issubset(i4):
                            try:
                                list1[0].remove(i1)
                            except:
                                {}
                        if i2.issubset(i3) \
                                or i2.issubset(i4):
                            try:
                                list1[1].remove(i2)
                            except:
                                {}
                        if i3.issubset(i4):
                            try:
                                list1[2].remove(i3)
                            except:
                                {}
    return list1



@app.route('/')
@app.route('/first')
def home():
    return render_template("first.html")

@app.route('/output',methods=['POST', 'GET'])
def result():
    output = request.files['myfile']
    f1, rules = readFile(output,20)
    f1 = sorted(f1)
    return render_template('first.html', temp = f1)
    




if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)