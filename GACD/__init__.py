# -*- coding: utf-8 -*-
from networkx.readwrite.gml import read_gml
from GACD.util import load_graph
from GACD.population import Population
import os
popSize = 100
crossoverRate = 0.8
mutatePortion = 0.2
generations = 500
def gacd_main(path,f):
    #接受准则Adapted Kernighan-Lin
    if f == 1:
        G = load_graph(path)
    else:
        G = read_gml(path,label='id')
    bestScores = []
    avgScores = []
    p = Population(popSize,G)
    bestScores.append(p.getMax().score)
    for i in range(generations):
        p.updatePop()
        bestScores.append(p.getMax().score)
    return bestScores
#     return p.pop[-1].decode().values()
if __name__ == '__main__':
#     pathList = ['karate2','dolphins','football','polbooks','power','as-22july06']
    pathList = ['karate2']
    pathList2 = ['LFR_s1','LFR_s9','LFR_s2','LFR_s10','LFR_s3','LFR_s11','LFR_s4','LFR_s12',\
                'LFR_s5','LFR_s13','LFR_s6','LFR_s14','LFR_s7','LFR_s15','LFR_s8']
    for i in range(5):
#         for index in range(0,pathList.__len__()):
#             mod = gacd_main(os.path.join('f:\dataset',pathList[index]) + '.gml',0) 
#             print mod
        for index in range(0,pathList2.__len__()):
            membership = gacd_main(os.path.join('f:\dataset',pathList2[index],'network.dat'),1) 
            print membership

    