import csv
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import stdev

synDist = None
ranDist = None

minK = 200
maxK = 3400

missRand = []
gotSyn = []
ks = []

homDir = 'tmpDistancesFull'
for k in range(minK,maxK,200):
    with open('{}/randdist_k={}.csv'.format(homDir,k)) as f:
        ranDist = list(csv.reader(f))

    with open('{}/syndist_k={}.csv'.format(homDir,k)) as f:
        synDist = list(csv.reader(f))

    sd = stdev(ranDist)

    ks.append(k)
    missRand.append(sum(1 if abs(float(rd[0])) > stdev else 0 for rd in ranDist)/float(len(ranDist)))
    gotSyn.append(sum(1 if abs(float(rd[0])) > stdev else 0 for rd in synDist)/float(len(synDist)))

    ax = sns.distplot([float(rd[0]) for rd in ranDist],name="Random pairs")
    ax = sns.distplot([float(rd[0]) for rd in synDist],name="Pairs of synonyms")
    ax.set_xlabel("Inner product between vectors")
    ax.set_ylabel("Frequency")
    ax.set_yscale("log")

    ax.axvline(stdev)
    ax.axvline(-stdev)

    plt.show()
