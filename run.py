
from flask import Flask, render_template, url_for, request
from csv import reader
import io
import time

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

def has_infrequent_subset(D, Ck, supp):
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

        if support >= supp:
            retList.insert(0, key)
        sR[key] = support
    return (retList, sR)

def apriori_gen(fname, minSup):
    (temp1, tempList) = getData(fname)

    # print(recordSetList)

    (L1, sD) = has_infrequent_subset(tempList, temp1, minSup)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = generate(L[k - 2], k)
        (Lk, supK) = has_infrequent_subset(tempList, Ck, minSup)
        sD.update(supK)
        L.append(Lk)
        k += 1
    return (L, sD)

def find_frequent_1_itemsets (data):
    tempFrequentData = []
    for i in data:
        for j in i:
            tempFrequentData.append(j)
    finalDataSets = []
    for i in tempFrequentData:
        finalDataSets.append(i)

    for i in range(len(tempFrequentData)):
        for j in range(i + 1, len(tempFrequentData)):
            if tempFrequentData[i].issubset(tempFrequentData[j]):
                try:
                    if tempFrequentData[i] in finalDataSets:
                        finalDataSets.remove(tempFrequentData[i])
                except:
                    {}
    dataSet = []
    for item in finalDataSets:
        dataSet.append(list(item))
    return dataSet


@app.route('/')
@app.route('/first')
def home():
    return render_template("first.html")

@app.route('/output',methods=['POST', 'GET'])
def result():
    minSupp = request.form['minSupp']
    output = request.files['myfile']
    print(minSupp)
    start_time = time.time()
    f1, rules = apriori_gen(output,int(minSupp))
    f1 = find_frequent_1_itemsets (f1)
    final = [f1, len(f1), output, minSupp, (time.time() - start_time)]
    return render_template('first.html', temp = final)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)