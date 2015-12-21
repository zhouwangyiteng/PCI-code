from math import sqrt

path = r'F:\pycode\PCI\PCI_data\\'


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, ID=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.distance = distance
        self.ID = ID


def readfile(filename):
    lines = [line for line in file(path + filename)]

    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []

    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])

    return rownames, colnames, data


def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))

    if den==0:
        return 0
    return 1.0 - num / den


def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    clust = [bicluster(rows[i], ID=i) for i in range(len(rows))]

    while len(clust)>1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                if (clust[i].ID, clust[j].ID) not in distances:
                    distances[(clust[i].ID, clust[j].ID)] = distance(clust[i].vec, clust[j].vec)
                d = distances[(clust[i].ID, clust[j].ID)]
                if d<closest:
                    closest = d
                    lowestpair = (i, j)

        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0
                    for i in range(len(clust[0].vec))]
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                               right=clust[lowestpair[1]],
                               distance=closest, ID=currentclustid)

        currentclustid -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(newcluster)

    return clust[0]

def printclust(clust, labels=None, n=0):
    for i in range(n):
        print ' ',
    if clust.ID<0:
        print '-'
    else:
        if labels==None:
            print clust.ID
        else:
            print labels[clust.ID]

    if clust.left!=None:
        printclust(clust.left, labels=labels, n=n+1)
    if clust.right!=None:
        printclust(clust.right, labels=labels, n=n+1)
        




























