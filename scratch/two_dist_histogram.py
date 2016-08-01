import csv
import matplotlib.pyplot as plt
import seaborn as sns
from statistics import stdev

synDist = None
ranDist = None

minK = 200
maxK = 2800

missRand = []
gotSyn = []
ks = []

homDir = 'tmpDistancesFull2'
for k in range(minK,maxK,180):
    with open('{}/randdist_k={}.csv'.format(homDir,k)) as f:
        ranDist = list(csv.reader(f))
        ranDist = [float(a[0]) for a in ranDist]

    with open('{}/syndist_k={}.csv'.format(homDir,k)) as f:
        synDist = list(csv.reader(f))
        synDist = [float(a[0]) for a in synDist]

    sd = stdev(ranDist)

    ks.append(k)
    missRand.append(sum(1.0 if abs(rd) > sd else 0.0 for rd in ranDist)/len(ranDist))
    gotSyn.append(sum(1.0 if abs(rd) > sd else 0.0 for rd in synDist)/len(synDist))

    ax = sns.distplot(ranDist,label="Random pairs",kde=False,hist=True)
    ax = sns.distplot(synDist,label="Pairs of synonyms",kde=False,hist=True)
    ax.set_xlabel("Inner product between vectors")
    ax.set_ylabel("Frequency")
    ax.set_yscale("log")
    ax.legend()
    ax.axvline(sd)
    ax.axvline(-sd)

    print("With k={}. Misclassified random pairs: {}. Accurately classified synonyms: {}"
          .format(k,missRand[-1],gotSyn[-1]))

    plt.show()
    #break
